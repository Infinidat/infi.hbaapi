__import__("pkg_resources").declare_namespace(__name__)

import logging
import unittest
import mock
from contextlib import contextmanager, nested
from construct import Container
from os.path import exists, join, sep, dirname, pardir, abspath
from ... import hbaapi
from .. import headers, c_api

ADAPTER_NAMES = ['lsiSAS', 'qlogic1', 'qlogic2']
ADAPTER_HANDLES = {'lsiSAS': 1, 'qlogic1': 2, 'qlogic2': 3}
ADAPTER_ATTRIBUTES_BY_HANDLE = {1: NotImplementedError,
                                2: Container(
    Manufacturer='QLogic Corporation',
    SerialNumber='I48461',
    Model='QLE2562',
    ModelDescription='QLogic QLE2562 Fibre Channel Adapter',
    NodeWWN=Container(wwn=[32, 0, 0, 36, 255, 44, 77, 242, ]),
    NodeSymbolicName='QLE2562 FW:v4.06.01 DVR:v9.1.8.6',
    HardwareVersion='',
    DriverVersion='9.1.8.6',
    OptionROMVersion='2.16',
    FirmwareVersion='4.06.01',
    VendorSpecificID=624038007,
    NumberOfPorts=1,
    DriverName='ql2300.sys',),
                                3: Container(
    Manufacturer='QLogic Corporation',
    SerialNumber='I48717',
    Model='QLE2562',
    ModelDescription='QLogic QLE2562 Fibre Channel Adapter',
    NodeWWN=Container(wwn=[32, 0, 0, 36, 255, 44, 77, 243, ]),
    NodeSymbolicName='QLE2562 FW:v4.06.01 DVR:v9.1.8.6',
    HardwareVersion='',
    DriverVersion='9.1.8.6',
    OptionROMVersion='2.16',
    FirmwareVersion='4.06.01',
    VendorSpecificID=624038007,
    NumberOfPorts=1,
    DriverName='ql2300.sys',
)}

PORT_ATTRIBUTES_BY_ADAPTER_HANDLE = {2:[Container(
    NodeWWN=Container(wwn=[32, 0, 0, 36, 255, 44, 77, 242, ]),
    PortWWN=Container(wwn=[33, 0, 0, 36, 255, 44, 77, 242, ]),
    PortFcId=0,
    PortType=1,
    PortState=6,
    PortSupportedClassofService=8,
    PortSupportedFc4Types=Container(bits=[0] * 32),
    PortActiveFc4Types=Container(bits=[0] * 32),
    PortSymbolicName='',
    OSDeviceName='\\\\.\\Scsi3:',
    PortSuggestedSpeed=26,
    PortSpeed=0,
    PortMaxFrameSize=2048,
    FabricName=Container(wwn=[0, 0, 0, 0, 0, 0, 0, 0]),
    NumberOfDiscoveredPorts=1,),
                                        ],
                                     3:[Container(
    NodeWWN=Container(wwn=[32, 0, 0, 36, 255, 44, 77, 243, ]),
    PortWWN=Container(wwn=[33, 0, 0, 36, 255, 44, 77, 243, ]),
    PortFcId=0,
    PortType=1,
    PortState=6,
    PortSupportedClassofService=8,
    PortSupportedFc4Types=Container(bits=[0] * 32),
    PortActiveFc4Types=Container(bits=[0] * 32),
    PortSymbolicName='',
    OSDeviceName='\\\\.\\Scsi3:',
    PortSuggestedSpeed=26,
    PortSpeed=0,
    PortMaxFrameSize=2048,
    FabricName=Container(wwn=[0, 0, 0, 0, 0, 0, 0, 0]),
    NumberOfDiscoveredPorts=1,),
                                        ]}

REMOTE_PORT_ATTRIBUTES = {
    2: [[Container(
    NodeWWN=Container(wwn=[1, 2, 3, 4, 5, 6, 7, 8]),
    PortWWN=Container(wwn=[1, 2, 3, 4, 5, 6, 7, 8]),
    PortFcId=123,
    PortType=0,
    PortState=1,
    PortSupportedClassofService=0,
    PortSupportedFc4Types=Container(bits=[0] * 32),
    PortActiveFc4Types=Container(bits=[0] * 32),
    PortSymbolicName='',
    OSDeviceName='',
    PortSuggestedSpeed=0,
    PortSpeed=0,
    PortMaxFrameSize=0,
    FabricName=Container(wwn=[0] * 8),
    NumberOfDiscoveredPorts=0,)]],
    3: [[Container(
    NodeWWN=Container(wwn=[1, 2, 3, 4, 5, 6, 7, 8]),
    PortWWN=Container(wwn=[1, 2, 3, 4, 5, 6, 7, 8]),
    PortFcId=123,
    PortType=0,
    PortState=1,
    PortSupportedClassofService=0,
    PortSupportedFc4Types=Container(bits=[0] * 32),
    PortActiveFc4Types=Container(bits=[0] * 32),
    PortSymbolicName='',
    OSDeviceName='',
    PortSuggestedSpeed=0,
    PortSpeed=0,
    PortMaxFrameSize=0,
    FabricName=Container(wwn=[0] * 8),
    NumberOfDiscoveredPorts=0,)], ]}

PORT_STATISTICS_BY_ADAPTER_HANDLE = {2:[Container(
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
                                     3:[Container(
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

FCP4_STATISTICS_BY_ADAPTER_HANDLE = {2:[NotImplementedError],
                                     3:[NotImplementedError]}

class GeneratorTestCase(unittest.TestCase):
    pass

    @mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetVersion")
    def test_get_version(self, api_mock):
        from .. import c_api
        api_mock.return_value = headers.HBA_UINT32(2)
        self.assertEquals(api_mock.return_value, c_api.HBA_GetVersion())

    @contextmanager
    def _mock_open_close_library(self):
        with nested(mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_LoadLibrary"),
                               mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_FreeLibrary")
                               ) as (load, free):
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
        with nested(mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_OpenAdapter"),
                    mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_CloseAdapter"),
                    ) as (open, close):
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
            buffer.raw = headers.HBA_AdapterAttributes.build(attributes)
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
            buffer.raw = headers.HBA_PortAttributes.build(attributes)
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
            buffer.raw = headers.HBA_PortAttributes.build(attributes)
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
            buffer.raw = headers.HBA_PortStatistics.build(attributes)
            return 0
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetPortStatistics") as api_mock:
            api_mock.side_effect = side_effect
            yield api_mock

    @contextmanager
    def _mock_get_fcp4_statistics(self):
        def side_effect(*args, **kwargs):
            adapter_handle, port_index, buffer = args
            attributes = FCP4_STATISTICS_BY_ADAPTER_HANDLE[adapter_handle.value][port_index]
            if attributes is NotImplementedError:
                raise NotImplementedError
            buffer.raw = headers.HBA_GetFC4Statistics.build(attributes)
            return 0
        with mock.patch("infi.hbaapi.generators.hbaapi.c_api.HBA_GetFC4Statistics") as api_mock:
            api_mock.side_effect = side_effect
            yield api_mock

    def test_get_number_of_adapters(self):
        from .. import c_api
        with nested(
                    self._mock_open_close_library(),
                    self._mock_get_number_of_adapters()
                    ) as (_, number_of_adapters):
            self.assertEquals(number_of_adapters.return_value, c_api.HBA_GetNumberOfAdapters())

    def test_get_port_adapter_raises_exception(self):
        with nested(
                    self._mock_open_close_library(),
                    self._mock_get_number_of_adapters(1),
                    self._mock_get_adapter_name(),
                    self._mock_open_close_adapter(),
                    self._mock_get_adapter_attributes(),
                    mock.patch("logging.debug"),
                    ) as (_, _, _, _, api_mock, debug):
            from .. import HbaApi
            ports = [port for port in HbaApi().iter_ports()]
            self.assertEquals(1, api_mock.call_count)
            self.assertEquals(1, debug.call_count)

    def test_mock(self):
        with nested(
                    self._mock_open_close_library(),
                    self._mock_get_number_of_adapters(3),
                    self._mock_get_adapter_name(),
                    self._mock_open_close_adapter(),
                    self._mock_get_adapter_attributes(),
                    self._mock_get_port_attributes(),
                    self._mock_get_port_statistics(),
                    self._mock_get_fcp4_statistics(),
                    self._mock_get_remote_port_attributes(),
                    ):
            ports = self._get_ports()
            from infi.hbaapi.tests import PortAssertions
            port_test_class = PortAssertions(self)
            for port in ports:
                port_test_class.assert_port(port)
                self.assertEquals(port.port_speed, 0)
                self.assertEquals(port.port_supported_speeds, [2, 4, 8])

    def _get_ports(self):
        from .. import HbaApi
        return [port for port in HbaApi().iter_ports()]

    def test_for_inconsistency__adapter_index_invalid_at_adapter_name(self):
        with nested(
                    self._mock_open_close_library(),
                    self._mock_get_number_of_adapters(5),
                    self._mock_get_adapter_name(),
                    self._mock_open_close_adapter(),
                    self._mock_get_adapter_attributes(),
                    self._mock_get_port_attributes(),
                    self._mock_get_port_statistics(),
                    self._mock_get_fcp4_statistics(),
                    self._mock_get_remote_port_attributes()
                    ):
            self.assertRaises(c_api.InconsistencyError, self._get_ports)

    def test_for_inconsistency__adapter_index_invalid_at_adapter_attributes(self):
        with nested(
                    self._mock_open_close_library(),
                    self._mock_get_number_of_adapters(1),
                    self._mock_get_adapter_name(),
                    self._mock_open_close_adapter(),
                    self._mock_get_adapter_attributes(),
                    self._mock_get_port_attributes(),
                    self._mock_get_port_statistics(),
                    self._mock_get_fcp4_statistics(),
                    ) as (_, _, _, _, mock_api, _, _, _):
            mock_api.side_effect = c_api.InconsistencyError
            self.assertRaises(c_api.InconsistencyError, self._get_ports)

    def test_for_inconsistency__remote_port_has_gone_away(self):
        with nested(
                    self._mock_open_close_library(),
                    self._mock_get_number_of_adapters(3),
                    self._mock_get_adapter_name(),
                    self._mock_open_close_adapter(),
                    self._mock_get_adapter_attributes(),
                    self._mock_get_port_attributes(),
                    self._mock_get_port_statistics(),
                    self._mock_get_fcp4_statistics(),
                    self._mock_get_remote_port_attributes()
                    ) as (_, _, _, _, _, _, _, _, mock_api):
            mock_api.side_effect = c_api.InconsistencyError
            self.assertRaises(c_api.InconsistencyError, self._get_ports)
