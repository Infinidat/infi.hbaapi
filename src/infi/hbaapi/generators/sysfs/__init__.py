__import__("pkg_resources").declare_namespace(__name__)

from contextlib import contextmanager
from bunch import Bunch
import ctypes
from .. import Generator
from ... import Port, PortStatistics, FC_PORT_STATISTICS

from glob import glob
from os.path import exists, join, sep, relpath

ROOT_FS = sep

def translate_stat_value_to_number(stat_value):
    OVERFLOW = '0xffffffffffffffff'
    return stat_value if isinstance(stat_value, int) else -1 if stat_value == OVERFLOW else int(stat_value, 16)

def translate_wwn(source_wwn):
    """ this function translates 0x010203040506070A to 01:02:03:04:05:06:07:0a
    """
    import re
    from ... import WWN_PATTERN
    dest_wwn = ''
    UNKNOWN_WWN = '0xffffffff'
    return re.sub(WWN_PATTERN, r'\1:\2:\3:\4:\5:\6:\7:\8',
                  source_wwn if source_wwn != UNKNOWN_WWN else ':'.join(['ff'] * 8)).lower()

def translate_supported_speeds(source):
    """ this functions traslates ''1 Gbit, 2 Gbit, 4 Gbit, 8 Gbit' to [1,2,4,8]
    """
    return [int(item.replace(' Gbit', '')) for item in source.split(',')]

def translate_port_speed(source):
    if source.lower() == 'unknown':
        return 0
    return int(source.replace(' Gbit', ''))

def translate_port_state(source):
    lower = source.lower()
    return None if lower in ['unknown', ] else lower

def translate_port_type(source):
    lower = source.lower()
    return None if lower in ['unknown' , 'other', 'not present'] else lower

class Sysfs(Generator):
    def __init__(self):
        Generator.__init__(self)

    def _iter_fc_hosts(self):
        FC_HOST_BASEPATH = join(ROOT_FS, 'sys', 'class', 'fc_host')
        for path in glob(join(FC_HOST_BASEPATH, 'host*')):
            yield path, relpath(path, FC_HOST_BASEPATH).replace('host', '')

    def _iter_remote_fc_ports(self, fc_host_path):
        for path in glob(join(fc_host_path, 'device', 'rport*', 'fc_remote_ports*')):
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

    def _populate_port_attributes_from_scsi_host(self, port, base_path):
        port.model = self.get_file_content(join(base_path, 'model_name'))
        port.model_description = self.get_file_content(join(base_path, 'model_desc*'))
        port.driver_version = self.get_file_content(join(base_path, 'driver_version'))
        port.serial_number = self.get_file_content(join(base_path, 'serial_num'))
        port.hardware_version = self.get_file_content(join(base_path, 'fw_version'))
        port.option_rom_version = self.get_file_content(join(base_path, 'optrom_fw_version'))

    def _populate_remote_port_attributes_from_fc_host(self, port, base_path):
        self._populate_port_attributes_from_fc_host(port, base_path)

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
            self._populate_remote_port_attributes_from_fc_host(remote_port, remote_fc_port_path)
            port.discovered_ports.append(remote_port)

    def iter_ports(self):
        SCSI_HOST_BASEPATH = join(ROOT_FS, 'sys', 'class', 'scsi_host')

        for fc_host_path, host_id in self._iter_fc_hosts():
            # fc_host_path is full path
            scsi_host_path = join(SCSI_HOST_BASEPATH, 'host%s' % host_id)
            port = Port()
            self._populate_remote_port_attributes_from_fc_host(port, fc_host_path)
            self._populate_port_attributes_from_fc_host(port, fc_host_path)
            self._populate_port_attributes_from_scsi_host(port, scsi_host_path)
            self._populate_port_statistics_from_fc_host(port, fc_host_path)
            yield port

    @classmethod
    def is_available(cls):
        from os.path import join
        FC_HOST_BASEPATH = join(ROOT_FS, 'sys', 'class', 'fc_host')
        from os.path import exists, join, sep
        return exists(FC_HOST_BASEPATH)
