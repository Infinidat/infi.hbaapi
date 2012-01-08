
import ctypes
from infi.instruct import Struct, VarSizeArray, ReadPointer, Field, Padding
from infi.instruct import FixedSizeArray as Array
from infi.instruct import FixedSizeString as String
from infi.instruct import UNInt32, UNInt8, SNInt64, UNInt64

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

BitsArray = Array('bits', 32, UNInt8)

def HBA_WWN(name):
    return String(name, 8)

PortSupportedFc4Types = Array("PortSupportedFc4Types", 32, UNInt8)
PortActiveFc4Types = Array("PortActiveFc4Types", 32, UNInt8)

def is_64bit():
    from sys import maxsize
    return maxsize > 2 ** 32

class HBA_AdapterAttributes(Struct): #pylint: disable-msg=C0103
    _fields_ = [
               String("Manufacturer", 64),
               String("SerialNumber", 64),
               String("Model", 256),
               String("ModelDescription", 256),
               HBA_WWN("NodeWWN"),
               String("NodeSymbolicName", 256),
               String("HardwareVersion", 256),
               String("DriverVersion", 256),
               String("OptionROMVersion", 256),
               String("FirmwareVersion", 256),
               UNInt32("VendorSpecificID"),
               UNInt32("NumberOfPorts"),
               String("DriverName", 256)
               ]

class HBA_PortAttributes(Struct): #pylint: disable-msg=C0103
    _fields_ = [
                HBA_WWN("NodeWWN"),
                HBA_WWN("PortWWN"),
                UNInt32("PortFcId"),
                UNInt32("PortType"),
                UNInt32("PortState"),
                UNInt32("PortSupportedClassofService"),
                PortSupportedFc4Types,
                PortActiveFc4Types,
                String("PortSymbolicName", 256),
                String("OSDeviceName", 256),
                UNInt32("PortSuggestedSpeed"),
                UNInt32("PortSpeed"),
                UNInt32("PortMaxFrameSize"),
                HBA_WWN("FabricName"),
                UNInt32("NumberOfDiscoveredPorts")
                ]

class HBA_PortStatistics(Struct): #pylint: disable-msg=C0103
    _fields_ = [
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
                SNInt64("InvalidCRCCount")
                ]

class HBA_FC4Statistics(Struct): #pylint: disable-msg=C0103
    _fields_ = [
               SNInt64("InputRequests"),
               SNInt64("OutputRequests"),
               SNInt64("ControlRequests"),
               SNInt64("InputMegabytes"),
               SNInt64("OutputMegabytes")
               ]

class HBA_SCSIID(Struct): #pylint: disablemsg=C0103
    _fields_ = [
                String("OSDeviceName", 256),
                UNInt32("ScsiBusNumber"),
                UNInt32("ScsiTargetNumber"),
                UNInt32("ScsiOSLun"),
                Padding(4), ]

class HBA_FcpId(Struct): #pylint: disablemsg=C0103
    _fields_ = [
                UNInt32("Fcid"),
                HBA_WWN("NodeWWN"),
                HBA_WWN("PortWWN"),
                UNInt64("FcpLun"),
                ]

class HBA_LUID(Struct): #pylint: disablemsg=C0103
    _fields_ = [
                String("buffer", 256),
                ]

class HBA_FcpScsiEntryV2(Struct): #pylint: disablemsg=C0103
    _fields_ = [Field("ScsiId", HBA_SCSIID),
                Field("FcId", HBA_FcpId),
                Field("LUID", HBA_LUID),
                Padding(4),
                ]

class HBA_FCPTargetMappingV2(Struct): #pylint: disablemsg=C0103
    _fields_ = [
                UNInt32("NumberOfEntries"),
                Padding(4),
                VarSizeArray("entry", ReadPointer("NumberOfEntries"), HBA_FcpScsiEntryV2)
                ]

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

HBA_PORTTYPE = {'0':None,
                '1':None,
                '2':None,
                '3':None,
                '5':'N',
                '6':'NL',
                '7':'FL',
                '8':'F',
                '9':'E',
                '10':'G',
                '20':'L',
                '21':'PTP'}

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
