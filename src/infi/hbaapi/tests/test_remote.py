
import unittest

class RemoteHCTLTestCase(unittest.TestCase):
    def test_remote_port_hctl(self):
        from infi.hbaapi import get_ports_collection
        local_ports = get_ports_collection().get_ports()
        for local_port in local_ports:
            remote_ports = local_port.discovered_ports
            for remote_port in remote_ports:
                self.assertFalse(remote_port.hct is None)

