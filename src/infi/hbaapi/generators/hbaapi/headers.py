'''
Created on Jun 20, 2011

@author: guy
'''

import ctypes
from construct import Struct, String, UNInt32, UNInt8, Array, SNInt64
##############
# Data Types #
##############
UINT32 = ctypes.c_uint32

HBA_UINT8 = ctypes.c_uint8
HBA_UINT32 = ctypes.c_uint32
HBA_HANDLE = HBA_UINT32
HBA_BOOLEAN = HBA_UINT8
HBA_UINT8 = HBA_BOOLEAN
HBA_STATUS = HBA_UINT32
HBA_PORTTYPE = HBA_UINT32
HBA_PORTSTATE = HBA_UINT32
HBA_PORTSPEED = HBA_UINT32
HBA_COS = HBA_UINT32

##############
# Structures #
##############

NodeWWN = Struct("NodeWWN",
                 Array(8, UNInt8("wwn")))

PortWWN = Struct("PortWWN",
                 Array(8, UNInt8("wwn")))

FabricName = Struct("FabricName",
                 Array(8, UNInt8("wwn")))

PortSupportedFc4Types = Struct("PortSupportedFc4Types",
                               Array(32, UNInt8("bits")))

PortActiveFc4Types = Struct("PortActiveFc4Types",
                               Array(32, UNInt8("bits")))

HBA_AdapterAttributes = Struct("HBA_AdapterAttributes",
                               String("Manufacturer", length=64, padchar='\x00'),
                               String("SerialNumber", length=64, padchar='\x00'),
                               String("Model", length=256, padchar='\x00'),
                               String("ModelDescription", length=256, padchar='\x00'),
                               NodeWWN,
                               String("NodeSymbolicName", length=256, padchar='\x00'),
                               String("HardwareVersion", length=256, padchar='\x00'),
                               String("DriverVersion", length=256, padchar='\x00'),
                               String("OptionROMVersion", length=256, padchar='\x00'),
                               String("FirmwareVersion", length=256, padchar='\x00'),
                               UNInt32("VendorSpecificID"),
                               UNInt32("NumberOfPorts"),
                               String("DriverName", length=256, padchar='\x00'))

HBA_PortAttributes = Struct("HBA_PortAttributes",
                            NodeWWN,
                            PortWWN,
                            UNInt32("PortFcId"),
                            UNInt32("PortType"),
                            UNInt32("PortState"),
                            UNInt32("PortSupportedClassofService"),
                            PortSupportedFc4Types,
                            PortActiveFc4Types,
                            String("PortSymbolicName", length=256, padchar='\x00'),
                            String("OSDeviceName", length=256, padchar='\x00'),
                            UNInt32("PortSuggestedSpeed"),
                            UNInt32("PortSpeed"),
                            UNInt32("PortMaxFrameSize"),
                            FabricName,
                            UNInt32("NumberOfDiscoveredPorts"))

HBA_PortStatistics = Struct("HBA_PortStatistics",
                            SNInt64("SecondsSinceLastReset"),
                            SNInt64("TxFrames"),
                            SNInt64("TxWords"),
                            SNInt64("RxFrames"),
                            SNInt64("RxWords"),
                            SNInt64("LIPCount"),
                            SNInt64("NOSCount"),
                            SNInt64("ErrorFrames"),
                            SNInt64("DumpedFrames"),
                            SNInt64("LinkFailureCount"),
                            SNInt64("LossOfSyncCount"),
                            SNInt64("LossOfSignalCount"),
                            SNInt64("PrimitiveSeqProtocolErrCount"),
                            SNInt64("InvalidTxWordCount"),
                            SNInt64("InvalidCRCCount"))

HBA_FC4Statistics = Struct("HBA_FC4Statistics",
                           SNInt64("InputRequests"),
                           SNInt64("OutputRequests"),
                           SNInt64("ControlRequests"),
                           SNInt64("InputMegabytes"),
                           SNInt64("OutputMegabytes"))

#############
# Constants #
#############

HBA_STATUS_OK = 0
HBA_STATUS_ERROR = 1
HBA_STATUS_ERROR_NOT_SUPPORTED = 2
HBA_STATUS_ERROR_INVALID_HANDLE = 3
HBA_STATUS_ERROR_ARG = 4
HBA_STATUS_ERROR_ILLEGAL_WWN = 5
HBA_STATUS_ERROR_ILLEGAL_INDEX = 6
HBA_STATUS_ERROR_MORE_DATA = 7
HBA_STATUS_ERROR_STALE_DATA = 8
HBA_STATUS_SCSI_CHECK_CONDITION = 9
HBA_STATUS_ERROR_BUSY = 10
HBA_STATUS_ERROR_TRY_AGAIN = 11
HBA_STATUS_ERROR_UNAVAILABLE = 12
HBA_STATUS_ERROR_ELS_REJECT = 13
HBA_STATUS_ERROR_INVALID_LUN = 14
HBA_STATUS_ERROR_INCOMPATIBLE = 15
HBA_STATUS_ERROR_AMBIGUOUS_WWN = 16
HBA_STATUS_ERROR_LOCAL_BUS = 17
HBA_STATUS_ERROR_LOCAL_TARGET = 18
HBA_STATUS_ERROR_LOCAL_LUN = 19
HBA_STATUS_ERROR_LOCAL_SCSIID_BOUND = 20
HBA_STATUS_ERROR_TARGET_FCID = 21
HBA_STATUS_ERROR_TARGET_NODE_WWN = 22
HBA_STATUS_ERROR_TARGET_PORT_WWN = 23
HBA_STATUS_ERROR_TARGET_LUN = 24
HBA_STATUS_ERROR_TARGET_LUID = 25
HBA_STATUS_ERROR_NO_SUCH_BINDING = 26
HBA_STATUS_ERROR_NOT_A_TARGET = 27
HBA_STATUS_ERROR_UNSUPPORTED_FC4 = 28
HBA_STATUS_ERROR_INCAPABLE = 29

HBA_PORTTYPE_UNKNOWN = 1
HBA_PORTTYPE_OTHER = 2
HBA_PORTTYPE_NOTPRESENT = 3
HBA_PORTTYPE_NPORT = 5
HBA_PORTTYPE_NLPORT = 6
HBA_PORTTYPE_FLPORT = 7
HBA_PORTTYPE_FPORT = 8
HBA_PORTTYPE_EPORT = 9
HBA_PORTTYPE_GPORT = 10
HBA_PORTTYPE_LPORT = 20
HBA_PORTTYPE_PTP = 21

HBA_PORTSTATE_UNKNOWN = 1
HBA_PORTSTATE_ONLINE = 2
HBA_PORTSTATE_OFFLINE = 3
HBA_PORTSTATE_BYPASSED = 4
HBA_PORTSTATE_DIAGNOSTICS = 5
HBA_PORTSTATE_LINKDOWN = 6
HBA_PORTSTATE_ERROR = 7
HBA_PORTSTATE_LOOPBACK = 8

HBA_PORTSPEED_UNKNOWN = 0
HBA_PORTSPEED_1GBIT = 1
HBA_PORTSPEED_2GBIT = 2
HBA_PORTSPEED_10GBIT = 4
HBA_PORTSPEED_4GBIT = 8
HBA_PORTSPEED_8GBIT = 16
HBA_PORTSPEED_NOT_NEGOTIATED = 1 << 15

MAX_ADAPTERNAME_LENGTH = 256
