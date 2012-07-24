
import unittest
import mock
import logging
logger = logging.getLogger(__name__)

#pylint: disable-all

class MockGenerator(object):
    def __init__(self):
        object.__init__(self)

    def iter_ports(self):
        return []

    @classmethod
    def is_available(cls):
        return True

class TestCase(unittest.TestCase):
    def test_imports(self):
        from .. import get_ports_collection, get_ports_generator
        from ..generators import Generator, CompositeGenerator
        from .. import Port, PortsCollection
    pass

    @mock.patch("infi.hbaapi.generators.get_list_of_generators")
    def test_iterface(self, mock):
        from ..generators.tests import get_list_of_generators
        from .. import get_ports_collection, get_ports_generator
        mock.return_value = get_list_of_generators()
        generator = get_ports_generator()
        self.assertEquals(mock.call_count, 1)
        available_generators = [item for item in generator.iter_generators()]
        self.assertEquals(len(available_generators), 1)
        collection = get_ports_collection()
        self.assertEquals(len(collection.get_ports()), 0)

    def test_real_thing(self):
        from .. import get_ports_collection
        ports = [port for port in get_ports_collection().iter_ports()]

    @mock.patch("infi.hbaapi.generators.get_list_of_generators")
    def test_with_mock_generator(self, mock):
        mock.return_value = [MockGenerator]
        from .. import get_ports_collection
        ports = [port for port in get_ports_collection().iter_ports()]

class PortAssertions(object):
    def __init__(self, test_case):
        self.test_case = test_case

    def _assert_statistics(self, port):
        from infi.hbaapi import FC_PORT_STATISTICS
        for name in FC_PORT_STATISTICS:
            value = getattr(port.statistics, name)
            self.test_case.assertIsInstance(value, int, "%s is not an instance of int" % repr(value))

    def _assert_wwn(self, wwn):
        import re
        from infi.dtypes.wwn import WWN
        from .. import WWN_PATTERN
        logger.debug(wwn)
        self.test_case.assertIsNotNone(wwn)
        self.test_case.assertIsInstance(wwn, WWN)

    def _assert_supported_speeds(self, port):
        self.test_case.assertIsInstance(port.port_supported_speeds, list)
        for item in port.port_supported_speeds:
            self.test_case.assertIsInstance(item, int)

    def _assert_port_speed(self, port_speed):
        self.test_case.assertIn(port_speed, [0, 1, 2, 4, 8])

    def _assert_port_state(self, port_state):
        self.test_case.assertIn(port_state, [None, 'online', 'offline', 'bypassed', 'diagnostics',
                                   'link down', 'error', 'loopback'])

    def _assert_port_type(self, port_type):
        self.test_case.assertIn(port_type, [None, 'N', 'NL', 'FL', 'F', 'E', 'G', 'L', 'PTP'])

    def _assert_discovered_ports(self, discovered_ports):
        self.test_case.assertIsInstance(discovered_ports, list)
        for port in discovered_ports:
            self.assert_port(port, True)

    def assert_port(self, port, remote_port=False):
        self._assert_wwn(port.port_wwn)
        self._assert_wwn(port.node_wwn)
        self._assert_wwn(port.fabric_name)
        self._assert_supported_speeds(port)
        self._assert_port_speed(port.port_speed)
        self._assert_port_state(port.port_state)
        self._assert_port_type(port.port_type)
        if not remote_port:
            self._assert_statistics(port)
