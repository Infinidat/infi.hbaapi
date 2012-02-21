__import__("pkg_resources").declare_namespace(__name__)

"""
This module fetch HBAAPI information from several sources, depending which ones are availble for the operating system.
Such sources are the actual hbaapi shared library, sysfs, etc...

The only entry points you should use are the PortsCollection class and the function get_port_collection.
Under the exmaples module, you can find some real-life examples of the outputs of this module.

The specific attirbutes available for each port are listed in FC_PORT_ATTRIBUTES
Their format or expected values are not documented here at this point. However, you can find this out by reading
the PortAssertions class in the tests modules
""" #pylint: disable-msg=W0105


from bunch import Bunch

WWN_OCTECT = '[0-9a-fA-F]{2}'
WWN_PATTERN = r'.*' + r'(?:0x)?' + r'[:-]?'.join(['(%s)' % WWN_OCTECT] * 8) + r'.*'

FC_PORT_ATTRIBUTES = ['node_wwn', 'port_wwn', 'port_fcid', 'port_state', 'port_type',
                      'port_symbolic_name', 'os_device_name', 'port_supported_speeds',
                      'port_speed', 'port_max_frame_size', 'fabric_name',
                      'driver_name', 'driver_version', 'manufacturer', 'serial_number',
                      'model', 'model_description', 'hardware_version', 'firmware_version',
                      'option_rom_version', 'discovered_ports', 'statistics', 'hct']
# TODO add tests for both sysfs and hbaapi implementations

FC_PORT_STATISTICS = ['dumped_frames', 'error_frames', 'fcp_control_requests', 'fcp_input_megabytes',
                      'fcp_input_requests', 'fcp_output_megabytes', 'fcp_output_requests', 'invalid_crc_count',
                      'invalid_tx_word_count', 'link_failure_count', 'lip_count', 'loss_of_signal_count',
                      'loss_of_sync_count', 'nos_count', 'primitive_seq_protocol_err_count',
                      'rx_frames', 'rx_words', 'seconds_since_last_reset', 'tx_frames', 'tx_words']

class Port(Bunch):
    """ Representation of a HBA port.
    For the list of available attributes, see the FC_PORT_ATTRIBUTES list
    """
    def __init__(self):
        Bunch.__init__(self)
        self._set_defaults()

    def _set_defaults(self):
        for attribute in FC_PORT_ATTRIBUTES:
            self.__setitem__(attribute, None) #pylint: disable-msg=E1101
        self.__setitem__('discovered_ports', list()) #pylint: disable-msg=E1101
        self.__setitem__('statistics', PortStatistics()) #pylint: disable-msg=E1101

    def update_not_none_values(self, other_port):
        for key, value in other_port.iteritems():
            our_value = self.get(key, None) #pylint: disable-msg=E1101
            if key == 'statistics':
                continue
            if our_value not in [-1, 0, None, '', [], ]:
                continue
            if value in [-1, 0, None, '', []]:
                continue
            self.__setitem__(key, value) #pylint: disable-msg=E1101
        if not other_port.get('statistics'): #pylint: disable-msg=E1101
            return self
        _ = self.statistics.update_not_none_values(other_port.get('statistics', dict())) #pylint: disable-msg=E1101
        return self

class PortStatistics(Port):
    def _set_defaults(self):
        for attribute in FC_PORT_STATISTICS:
            self.__setitem__(attribute, -1) #pylint: disable-msg=E1101

class PortsCollection(object):
    """ The entry point for this module. It provides a generator object trough iter_ports method, which yields Port
    objects, and the get_ports methods, which returns a list of all methods
    """
    def __init__(self):
        object.__init__(self)
        self._ports = {}

    def get_ports(self):
        return [port for port in self._ports.values()]

    def iter_ports(self):
        for port in self._ports.values():
            yield port

    def get_port_by_wwn(self, wwn):
        return self._ports[wwn]

    def add_port(self, port):
        if not self._ports.has_key(port.port_wwn):
            self._ports[port.port_wwn] = port
        else:
            self._ports[port.port_wwn].update_not_none_values(port)

    def remove_port_by_wwn(self, wwn):
        del(self._ports[wwn])

def get_ports_generator():
    """ Returns a composite component of Fiber Channel Ports generators that are available on this operating system
    """
    from .generators import get_list_of_generators, CompositeGenerator
    composite = CompositeGenerator()
    for leaf in get_list_of_generators():
        if not leaf.is_available():
            continue
        composite.add_generator(leaf)
    return composite

def get_ports_collection():
    """ Returns a unique collection of Fiber Channel Ports
    This is a simple wrapping usage of the PortsCollection case
    """
    collection = PortsCollection()
    generator = get_ports_generator()
    for port in generator.iter_ports():
        collection.add_port(port)
    return collection

__all__ = ['get_ports_collection', ]
