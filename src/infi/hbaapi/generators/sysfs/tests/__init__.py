__import__("pkg_resources").declare_namespace(__name__)

#pylint: disable-all

import logging
import unittest
import mock
from os.path import exists, join, sep, dirname, pardir, abspath
from ... import sysfs

logger = logging.getLogger(__name__)

MOCK_ROOT_FS = abspath(join(dirname(__file__), pardir, pardir, pardir, pardir, pardir, pardir, 'mock_fs', 'redhat_no_remote_ports'))
REMOTE_PORTS_MOCK_ROOT_FS = abspath(join(dirname(__file__), pardir, pardir, pardir, pardir, pardir, pardir, 'mock_fs', 'mock_fs_hbaapi-5'))

class GeneratorTestCase(unittest.TestCase):
    def test_stat_conversion__zero(self):
        self.assertEquals(0, sysfs.translate_stat_value_to_number('0x0'))

    def test_stat_conversion__ff(self):
        self.assertEquals(255, sysfs.translate_stat_value_to_number('0xff'))

    def test_stat_conversion__overflow(self):
        self.assertEquals(-1, sysfs.translate_stat_value_to_number('0xffffffffffffffff'))

    @mock.patch.object(sysfs, 'ROOT_FS' , MOCK_ROOT_FS)
    def test_mock_fs(self):
        from infi.hbaapi.tests import PortAssertions
        logger.debug("mock_fs = %s", MOCK_ROOT_FS)
        self.assertIs(sysfs.ROOT_FS, MOCK_ROOT_FS)
        self.assertTrue(sysfs.Sysfs.is_available())
        ports = [port for port in sysfs.Sysfs().iter_ports()]
        port_test_class = PortAssertions(self)
        for port in ports:
            port_test_class.assert_port(port)

    def _assert_wwn_translation(self, expected, actual):
        self.assertEquals(sysfs.translate_wwn(actual), expected)

    def test_wwn_translation(self):
        for expected, actual in [('01:02:03:04:05:06:07:08', '01:02:03:04:05:06:07:08'),
                                 ('01:02:03:04:05:06:07:08', '0x0102030405060708'),
                                 ('ab:cd:ab:cd:ab:cd:ab:cd', 'ab:cd:ab:cd:ab:cd:ab:cd'.upper())]:
            self._assert_wwn_translation(expected, actual)

class RemotePortsTestCase(unittest.TestCase):
    @mock.patch.object(sysfs, 'ROOT_FS' , REMOTE_PORTS_MOCK_ROOT_FS)
    def test_mock_fs(self):
        raise unittest.SkipTest("the mocked filesystem was removed because windows filesystem")
        logger.debug("mock_fs = %s", REMOTE_PORTS_MOCK_ROOT_FS)
        self.assertIs(sysfs.ROOT_FS, REMOTE_PORTS_MOCK_ROOT_FS)
        self.assertTrue(sysfs.Sysfs.is_available())
        self._assert_remote_ports()

    def _assert_remote_ports(self):
        from infi.dtypes.wwn import WWN
        ports = [port for port in sysfs.Sysfs().iter_ports()]
        remote_ports = ports[0].discovered_ports
        self.assertEqual(len(remote_ports), 2)
        self.assertEqual(remote_ports[0].port_wwn, WWN("5000402001f45eb5"))
        self.assertEqual(remote_ports[1].port_wwn, WWN("21000024ff2c4df3"))
        self.assertEqual(remote_ports[0].hct, (2,0,0))
        self.assertEqual(remote_ports[1].hct, (2,0,1))

