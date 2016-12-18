#pylint: disable-all

import logging
import unittest
import mock
from contextlib import contextmanager
from os.path import exists, join, sep, dirname, pardir, abspath
from infi import hbaapi
from infi.hbaapi.generators.hbaapi import headers, c_api

logger = logging.getLogger(__name__)

def _translate_wwn(source):
    return source

ADAPTER_NAMES = [b'lsiSAS', b'qlogic1', b'qlogic2']
ADAPTER_HANDLES = {b'lsiSAS': 1, b'qlogic1': 2, b'qlogic2': 3}
ADAPTER_ATTRIBUTES_BY_HANDLE = {1: NotImplementedError,
                                2: dict(
    Manufacturer=b'QLogic Corporation',
    SerialNumber=b'I48461',
    Model=b'QLE2562',
    ModelDescription=b'QLogic QLE2562 Fibre Channel Adapter',
    NodeWWN=_translate_wwn([32, 0, 0, 36, 255, 44, 77, 242, ]),
    NodeSymbolicName=b'QLE2562 FW:v4.06.01 DVR:v9.1.8.6',
    HardwareVersion=b'',
    DriverVersion=b'9.1.8.6',
    OptionROMVersion=b'2.16',
    FirmwareVersion=b'4.06.01',
    VendorSpecificID=624038007,
    NumberOfPorts=1,
    DriverName=b'ql2300.sys',),
                                3: dict(
    Manufacturer=b'QLogic Corporation',
    SerialNumber=b'I48717',
    Model=b'QLE2562',
    ModelDescription=b'QLogic QLE2562 Fibre Channel Adapter',
    NodeWWN=_translate_wwn([32, 0, 0, 36, 255, 44, 77, 243, ]),
    NodeSymbolicName=b'QLE2562 FW:v4.06.01 DVR:v9.1.8.6',
    HardwareVersion=b'',
    DriverVersion=b'9.1.8.6',
    OptionROMVersion=b'2.16',
    FirmwareVersion=b'4.06.01',
    VendorSpecificID=624038007,
    NumberOfPorts=1,
    DriverName=b'ql2300.sys',),
                                4: dict(
    Manufacturer=b'Brocade',
    SerialNumber=b'BUL0443G00S',
    Model=b'Brocade-1860-2p',
    ModelDescription=b'Brocade 16G FC HBA',
    NodeWWN=_translate_wwn([32,0,140,124,255,19,11,0]),
    NodeSymbolicName=b'Brocade-1860-2p | 3.2.2.5 | io122 | Windows Server 2012 R2 Standard | ',
    HardwareVersion=b'Rev-B', DriverVersion=b'3.2.2.5', OptionROMVersion=b'3.2.4.0',
    FirmwareVersion=b'3.2.2.5',
    VendorSpecificID=2233943,
    NumberOfPorts=1,
    DriverName=b'bfad')
}

PORT_ATTRIBUTES_BY_ADAPTER_HANDLE = {2:[dict(
    NodeWWN=_translate_wwn([32, 0, 0, 36, 255, 44, 77, 242, ]),
    PortWWN=_translate_wwn([33, 0, 0, 36, 255, 44, 77, 242, ]),
    PortFcId=0,
    PortType=1,
    PortState=6,
    PortSupportedClassofService=8,
    PortSupportedFc4Types=[0] * 32,
    PortActiveFc4Types=[0] * 32,
    PortSymbolicName=b'',
    OSDeviceName=b'\\\\.\\Scsi3:',
    PortSuggestedSpeed=26,
    PortSpeed=0,
    PortMaxFrameSize=2048,
    FabricName=_translate_wwn([0, 0, 0, 0, 0, 0, 0, 0]),
    NumberOfDiscoveredPorts=1,),
                                        ],
                                     3:[dict(
    NodeWWN=_translate_wwn([32, 0, 0, 36, 255, 44, 77, 243, ]),
    PortWWN=_translate_wwn([33, 0, 0, 36, 255, 44, 77, 243, ]),
    PortFcId=0,
    PortType=1,
    PortState=6,
    PortSupportedClassofService=8,
    PortSupportedFc4Types=[0] * 32,
    PortActiveFc4Types=[0] * 32,
    PortSymbolicName=b'',
    OSDeviceName=b'\\\\.\\Scsi3:',
    PortSuggestedSpeed=26,
    PortSpeed=0,
    PortMaxFrameSize=2048,
    FabricName=_translate_wwn([0, 0, 0, 0, 0, 0, 0, 0]),
    NumberOfDiscoveredPorts=1,),
                                        ],
                                      4:[dict(
    NodeWWN=_translate_wwn([32,0,140,124,255,19,11,0]),
    PortWWN=_translate_wwn([16,0,140,124,255,19,11,0]),
    PortFcId=0,
    PortType=5,
    PortState=6,
    PortSupportedClassofService=8,
    PortSupportedFc4Types=[ 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    PortActiveFc4Types=[ 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    PortSymbolicName=b'',
    OSDeviceName=b'\\\\.\\Scsi4:',
    PortSuggestedSpeed=0,
    PortSpeed=0,
    PortMaxFrameSize=2112,
    FabricName=b'',
    NumberOfDiscoveredPorts=0)]}

REMOTE_PORT_ATTRIBUTES = {
    2: [[dict(
    NodeWWN=_translate_wwn([1, 2, 3, 4, 5, 6, 7, 8]),
    PortWWN=_translate_wwn([1, 2, 3, 4, 5, 6, 7, 8]),
    PortFcId=123,
    PortType=0,
    PortState=1,
    PortSupportedClassofService=0,
    PortSupportedFc4Types=[0] * 32,
    PortActiveFc4Types=[0] * 32,
    PortSymbolicName=b'',
    OSDeviceName=b'',
    PortSuggestedSpeed=0,
    PortSpeed=0,
    PortMaxFrameSize=0,
    FabricName=_translate_wwn([0, 0, 0, 0, 0, 0, 0, 0]),
    NumberOfDiscoveredPorts=0,)]],
    3: [[dict(
    NodeWWN=_translate_wwn([1, 2, 3, 4, 5, 6, 7, 8]),
    PortWWN=_translate_wwn([1, 2, 3, 4, 5, 6, 7, 8]),
    PortFcId=123,
    PortType=0,
    PortState=1,
    PortSupportedClassofService=0,
    PortSupportedFc4Types=[0] * 32,
    PortActiveFc4Types=[0] * 32,
    PortSymbolicName=b'',
    OSDeviceName=b'',
    PortSuggestedSpeed=0,
    PortSpeed=0,
    PortMaxFrameSize=0,
    FabricName=_translate_wwn([0, 0, 0, 0, 0, 0, 0, 0]),
    NumberOfDiscoveredPorts=0,)], ]}

PORT_STATISTICS_BY_ADAPTER_HANDLE = {2:[dict(
    SecondsSinceLastReset= -1,
    TxFrames= -1,
    TxWords= -1,
    RxFrames= -1,
    RxWords= -1,
    LIPCount= -1,
    NOSCount= -1,
    ErrorFrames= -1,
    DumpedFrames= -1,
    LinkFailureCount=0,
    LossOfSyncCount=0,
    LossOfSignalCount=0,
    PrimitiveSeqProtocolErrCount=0,
    InvalidTxWordCount=0,
    InvalidCRCCount=0,
)],
                                     3:[dict(
    SecondsSinceLastReset= -1,
    TxFrames= -1,
    TxWords= -1,
    RxFrames= -1,
    RxWords= -1,
    LIPCount= -1,
    NOSCount= -1,
    ErrorFrames= -1,
    DumpedFrames= -1,
    LinkFailureCount=0,
    LossOfSyncCount=0,
    LossOfSignalCount=0,
    PrimitiveSeqProtocolErrCount=0,
    InvalidTxWordCount=0,
    InvalidCRCCount=0,
)]}

BROCADE_WINDOWS_BUFFER = b' \x00\x8c|\xff\x13\x0b\x00\x10\x00\x8c|\xff\x13\x0b\x00\x00\x00\x00\x00\x05\x00\x00\x00\x06\x00\x00\x00\x08\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\\\\.\\Scsi4:\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

class GeneratorTestCase(unittest.TestCase):
    pass

    @mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetVersion")
    def test_get_version(self, api_mock):
        from infi.hbaapi.generators.hbaapi import c_api
        api_mock.return_value = headers.HBA_UINT32(2)
        self.assertEqual(api_mock.return_value, c_api.HBA_GetVersion())

    @contextmanager
    def _mock_open_close_library(self):
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_LoadLibrary") as load, \
             mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_FreeLibrary") as free:
            load.return_value = 0
            free.return_value = 0
            yield (load, free)

    @contextmanager
    def _mock_get_number_of_adapters(self, expected=2):
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetNumberOfAdapters") as api_mock:
            api_mock.return_value = expected
            yield api_mock

    @contextmanager
    def _mock_get_adapter_name(self):
        def side_effect(*args, **kwargs):
            adapter_index = args[0]
            adapter_name_ctypes_object = args[1]
            if adapter_index > len(ADAPTER_NAMES) - 1:
                raise c_api.InconsistencyError
            adapter_name_ctypes_object.value = ADAPTER_NAMES[adapter_index]
            return 0
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetAdapterName") as api_mock:
            api_mock.side_effect = side_effect
            yield api_mock

    @contextmanager
    def _mock_open_close_adapter(self):
        def side_effect(*args, **kwargs):
            adapter_name_ctypes_object = args[0]
            return headers.HBA_HANDLE(ADAPTER_HANDLES.get(adapter_name_ctypes_object.value))
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_OpenAdapter") as open, \
             mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_CloseAdapter") as close:
            open.side_effect = side_effect
            close.return_value = 0
            yield (open, close)

    @contextmanager
    def _mock_get_adapter_attributes(self):
        def side_effect(*args, **kwargs):
            adapter_handle, buffer = args
            attributes = ADAPTER_ATTRIBUTES_BY_HANDLE[adapter_handle.value]
            if attributes is NotImplementedError:
                raise NotImplementedError
            instance = headers.HBA_AdapterAttributes()
            for key, value in attributes.items():
                setattr(instance, key, value)
            buffer.raw = headers.HBA_AdapterAttributes.write_to_string(instance)
            return 0
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetAdapterAttributes") as api_mock:
            api_mock.side_effect = side_effect
            yield api_mock

    @contextmanager
    def _mock_get_port_attributes(self):
        def side_effect(*args, **kwargs):
            adapter_handle, port_index, buffer = args
            attributes = PORT_ATTRIBUTES_BY_ADAPTER_HANDLE[adapter_handle.value][port_index]
            if attributes is NotImplementedError:
                raise NotImplementedError
            instance = headers.HBA_PortAttributes(**attributes)
            buffer.raw = headers.HBA_PortAttributes.write_to_string(instance)
            return 0
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetAdapterPortAttributes") as api_mock:
            api_mock.side_effect = side_effect
            yield api_mock

    @contextmanager
    def _mock_get_remote_port_attributes(self):
        def side_effect(*args, **kwargs):
            adapter_handle, port_index, remote_port_index, buffer = args
            attributes = REMOTE_PORT_ATTRIBUTES[adapter_handle.value][port_index][remote_port_index]
            if attributes is NotImplementedError:
                raise NotImplementedError
            instance = headers.HBA_PortAttributes(**attributes)
            buffer.raw = headers.HBA_PortAttributes.write_to_string(instance)
            return 0
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetDiscoveredPortAttributes") as api_mock:
            api_mock.side_effect = side_effect
            yield api_mock

    @contextmanager
    def _mock_get_port_statistics(self):
        def side_effect(*args, **kwargs):
            adapter_handle, port_index, buffer = args
            attributes = PORT_STATISTICS_BY_ADAPTER_HANDLE[adapter_handle.value][port_index]
            if attributes is NotImplementedError:
                raise NotImplementedError
            instance = headers.HBA_PortStatistics()
            for key, value in attributes.items():
                setattr(instance, key, value)
            buffer.raw = headers.HBA_PortStatistics.write_to_string(instance)
            return 0
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetPortStatistics") as api_mock:
            api_mock.side_effect = side_effect
            yield api_mock

    @contextmanager
    def _mock_get_fcp4_statistics(self):
        def side_effect(*args, **kwargs):
            from infi.hbaapi.generators.hbaapi.headers import HBA_STATUS_ERROR_UNSUPPORTED_FC4
            return HBA_STATUS_ERROR_UNSUPPORTED_FC4
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetFC4Statistics") as api_mock:
            api_mock.side_effect = side_effect
            yield api_mock

    @contextmanager
    def _mock_get_fcp_target_mappings(self):
        def side_effect(*args, **kwargs):
            from infi.hbaapi.generators.hbaapi.headers import HBA_STATUS_ERROR_NOT_SUPPORTED
            return HBA_STATUS_ERROR_NOT_SUPPORTED
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetFcpTargetMappingV2") as api_mock:
            api_mock.side_effect = side_effect
            yield api_mock

    def test_get_number_of_adapters(self):
        from infi.hbaapi.generators.hbaapi import c_api
        with self._mock_open_close_library(), \
             self._mock_get_number_of_adapters() as number_of_adapters:
            self.assertEqual(number_of_adapters.return_value, c_api.HBA_GetNumberOfAdapters())

    def test_get_port_adapter_raises_exception(self):
        with self._mock_open_close_library(), \
             self._mock_get_number_of_adapters(1), \
             self._mock_get_adapter_name(), \
             self._mock_open_close_adapter(), \
             self._mock_get_adapter_attributes() as api_mock:
            from infi.hbaapi.generators.hbaapi import HbaApi
            ports = [port for port in HbaApi().iter_ports()]
            self.assertEqual(1, api_mock.call_count)

    def test_mock(self):
        with self._mock_open_close_library(), \
             self._mock_get_number_of_adapters(3), \
             self._mock_get_adapter_name(), \
             self._mock_open_close_adapter(), \
             self._mock_get_adapter_attributes(), \
             self._mock_get_port_attributes(), \
             self._mock_get_port_statistics(), \
             self._mock_get_fcp4_statistics(), \
             self._mock_get_remote_port_attributes(), \
             self._mock_get_fcp_target_mappings():
            ports = self._get_ports()
            from . import PortAssertions
            port_test_class = PortAssertions(self)
            for port in ports:
                port_test_class.assert_port(port)
                self.assertEqual(port.port_speed, 0)
                self.assertEqual(port.port_supported_speeds, [2, 4, 8])

    def _get_ports(self):
        from infi.hbaapi.generators.hbaapi import HbaApi
        return [port for port in HbaApi().iter_ports()]

    def test_for_inconsistency__adapter_index_invalid_at_adapter_name(self):
        with self._mock_open_close_library(), \
             self._mock_get_number_of_adapters(5), \
             self._mock_get_adapter_name(), \
             self._mock_open_close_adapter(), \
             self._mock_get_adapter_attributes(), \
             self._mock_get_port_attributes(), \
             self._mock_get_port_statistics(), \
             self._mock_get_fcp4_statistics(), \
             self._mock_get_remote_port_attributes(), \
             self._mock_get_fcp_target_mappings():
            self.assertRaises(c_api.InconsistencyError, self._get_ports)

    def test_for_inconsistency__adapter_index_invalid_at_adapter_attributes(self):
        with self._mock_open_close_library(), \
             self._mock_get_number_of_adapters(1), \
             self._mock_get_adapter_name(), \
             self._mock_open_close_adapter(), \
             self._mock_get_adapter_attributes() as mock_api, \
             self._mock_get_port_attributes(), \
             self._mock_get_port_statistics(), \
             self._mock_get_fcp4_statistics():
            mock_api.side_effect = c_api.InconsistencyError
            self.assertRaises(c_api.InconsistencyError, self._get_ports)

    def test_for_inconsistency__remote_port_has_gone_away(self):
        with self._mock_open_close_library(), \
             self._mock_get_number_of_adapters(3), \
             self._mock_get_adapter_name(), \
             self._mock_open_close_adapter(), \
             self._mock_get_adapter_attributes(), \
             self._mock_get_port_attributes(), \
             self._mock_get_port_statistics(), \
             self._mock_get_fcp4_statistics(), \
             self._mock_get_remote_port_attributes() as mock_api:
            mock_api.side_effect = c_api.InconsistencyError
            self.assertRaises(c_api.InconsistencyError, self._get_ports)

    def test_parsing_wwn_that_ends_with_null(self):
        port_attributes = headers.HBA_PortAttributes.create_from_string(BROCADE_WINDOWS_BUFFER)
        assert len(port_attributes.PortWWN) == 8

    def test_HPT_1776(self):
        # all APIs about one of the remote ports retured HBA_STATUS_ERROR_ILLEGAL_WWN, we didn't handle that
        with self._mock_open_close_library(), \
             self._mock_get_number_of_adapters(3), \
             self._mock_get_adapter_name(), \
             self._mock_open_close_adapter(), \
             self._mock_get_adapter_attributes(), \
             self._mock_get_port_attributes(), \
             self._mock_get_port_statistics(), \
             self._mock_get_fcp4_statistics() as stats_mock, \
             self._mock_get_remote_port_attributes(), \
             self._mock_get_fcp_target_mappings() as remote_port_mock:
            stats_mock.side_effect = RuntimeError(headers.HBA_STATUS_ERROR_ILLEGAL_WWN)
            remote_port_mock.side_effect = RuntimeError(headers.HBA_STATUS_ERROR_ILLEGAL_WWN)
            self.assertEqual(len(self._get_ports()), 2)        # 2 - one of the mocked adapters is "weird"
