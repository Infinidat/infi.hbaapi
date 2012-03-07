__import__("pkg_resources").declare_namespace(__name__)

from contextlib import contextmanager
from bunch import Bunch
import ctypes
from .. import Generator
from ... import Port, PortStatistics, FC_PORT_STATISTICS

from glob import glob
from os.path import exists, join, sep, relpath

ROOT_FS = sep
OVERFLOW = '0xffffffffffffffff'
UNKNOWN_WWN = '0xffffffff'

def translate_stat_value_to_number(stat_value):
    return stat_value if isinstance(stat_value, int) else -1 if stat_value == OVERFLOW else int(stat_value, 16)

def translate_wwn(source_wwn):
    """ this function translates 0x010203040506070A to 01:02:03:04:05:06:07:0a
    """
    import re
    from ... import WWN_PATTERN
    from infi.dtypes.wwn import WWN
    if source_wwn == -1:
        return None
    return WWN(re.sub(WWN_PATTERN, r'\1:\2:\3:\4:\5:\6:\7:\8',
                  source_wwn if source_wwn != UNKNOWN_WWN else ':'.join(['ff'] * 8)).lower())

def translate_supported_speeds(source):
    """ this functions traslates ''1 Gbit, 2 Gbit, 4 Gbit, 8 Gbit' to [1,2,4,8]
    """
    if source == -1:
        return None
    return [int(item.replace(' Gbit', '')) for item in source.split(',')]

def translate_port_speed(source):
    if source == -1:
        return 0
    if source.lower() == 'unknown':
        return 0
    return int(source.replace(' Gbit', ''))

def translate_port_state(source):
    if source == -1:
        return None
    lower = source.lower()
    return None if lower in ['unknown', ] else lower

def translate_port_type(source):
    if source == -1:
        return None
    lower = source.lower().strip()
    return None if lower in ['unknown' , 'other', 'not present'] else lower

class Sysfs(Generator):
    def __init__(self):
        Generator.__init__(self)

    def _iter_fc_hosts(self):
        FC_HOST_BASEPATH = join(ROOT_FS, 'sys', 'class', 'fc_host')
        for path in glob(join(FC_HOST_BASEPATH, 'host*')):
            yield path, relpath(path, FC_HOST_BASEPATH).replace('host', '')

    def _iter_remote_fc_ports(self, fc_host_path):
        for rport in glob(join(fc_host_path, 'device', 'rport*')):
            if exists(join(rport, 'fc_remote_ports')):
                # this is how its on ubuntu
                for path in glob(join(rport, 'fc_remote_ports', '*')):
                    yield path
            else:
                for path in glob(join(rport, 'fc_remote_ports*')):
                    yield path

    def get_file_content(self, filepath):
        # The purpose of this method is to return the file's content with no exceptions.
        # If we fail to collect the information, just return None (that's OK)
        #
        # If a wildcard '*' is in filepath, we will glob for the list of matching files, and choose the first one
        # This is done to pretect ourself from cases such as model_description is just named model_desc
        if '*' in filepath:
            filelist = glob(filepath)
            if not filelist:
                return None
            filepath = filelist[0]
        try:
            with open(filepath) as fd:
                return fd.read().strip('\n').strip()
        except IOError:
            return -1

    def _populate_port_attributes_from_fc_host(self, port, base_path):
        port.port_fcid = self.get_file_content(join(base_path, 'port_id'))
        port.port_wwn = translate_wwn(self.get_file_content(join(base_path, 'port_name')))
        port.node_wwn = translate_wwn(self.get_file_content(join(base_path, 'node_name')))
        port.port_state = translate_port_state(self.get_file_content(join(base_path, 'port_state')))
        port.port_speed = translate_port_speed(self.get_file_content(join(base_path, 'speed')))
        port.port_type = translate_port_type(self.get_file_content(join(base_path, 'port_type')))
        port.port_supported_speeds = translate_supported_speeds(
                                                self.get_file_content(join(base_path, 'supported_speeds')))
        port.fabric_name = translate_wwn(self.get_file_content(join(base_path, 'fabric_name')))
        port.port_symbolic_name = self.get_file_content(join(base_path, 'symbolic_name'))
	self._populate_local_port_hct(port, base_path)

    def _populate_port_attributes_from_scsi_host(self, port, base_path):
        port.model = self.get_file_content(join(base_path, 'model*name'))
        port.model_description = self.get_file_content(join(base_path, 'model*desc*'))
        port.driver_version = self.get_file_content(join(base_path, '*dr*v*_version'))
        port.serial_number = self.get_file_content(join(base_path, 'serial*num'))
        port.hardware_version = self.get_file_content(join(base_path, 'fw*e*'))
        port.option_rom_version = self.get_file_content(join(base_path, 'optrom_*_version'))

    def _populate_remote_port_hct(self, port, base_path, local_port):
        from re import compile
        pattern = compile(r"(?P<host>\d+)[^\d](?P<channel>\d+)[^\d](?P<target>\d)")
        result = pattern.search(base_path).groupdict()
        # TODO get the target number from the scsi_target_id_file inside base_path
        target_path = join(base_path, "scsi_target_id")
        target_id = open(target_path).read().strip("\n").strip() if exists(target_path) else "-1"
        port.hct = (local_port.hct[0], int(result['channel']), int(target_id))

    def _populate_local_port_hct(self, port, base_path):
        from re import compile
        pattern = compile(r"host(?P<host>\d+)")
        result = pattern.search(base_path).groupdict()
        port.hct = (int(result['host']), -1, -1)

    def _populate_remote_port_attributes_from_fc_host(self, port, base_path, local_port):
        self._populate_port_attributes_from_fc_host(port, base_path)
        self._populate_remote_port_hct(port, base_path, local_port)

    def _populate_port_statistics_from_fc_host(self, port, base_path):
        # currently, FC_PORT_STATISTICS match the files in sysfs, so its easy to this
        stats = PortStatistics()
        for stat_name in FC_PORT_STATISTICS:
            stat_value = self.get_file_content(join(base_path, 'statistics', stat_name))
            # only one name is fucked up here
            setattr(stats, stat_name.replace('prim', 'primitive'), translate_stat_value_to_number(stat_value))
        port.statistics = stats

    def _populate_discovered_ports(self, port, fc_host_path):
        port.discovered_ports = []
        for remote_fc_port_path in self._iter_remote_fc_ports(fc_host_path):
            remote_port = Port()
            self._populate_remote_port_attributes_from_fc_host(remote_port, remote_fc_port_path, port)
            if remote_port.hct[2] == -1:
                # this is not a real target, just a switch port
                continue
            if remote_port.port_state == "not present":
                # this port is no longer connected
                continue
            port.discovered_ports.append(remote_port)

    def iter_ports(self):
        SCSI_HOST_BASEPATH = join(ROOT_FS, 'sys', 'class', 'scsi_host')
        for fc_host_path, host_id in self._iter_fc_hosts():
            # fc_host_path is full path
            scsi_host_path = join(SCSI_HOST_BASEPATH, 'host%s' % host_id)
            port = Port()
            self._populate_port_attributes_from_fc_host(port, fc_host_path)
            self._populate_port_attributes_from_scsi_host(port, scsi_host_path)
            self._populate_port_statistics_from_fc_host(port, fc_host_path)
            self._populate_discovered_ports(port, fc_host_path)
            yield port

    @classmethod
    def is_available(cls):
        FC_HOST_BASEPATH = join(ROOT_FS, 'sys', 'class', 'fc_host')
        return exists(FC_HOST_BASEPATH)
