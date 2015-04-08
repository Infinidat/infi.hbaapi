
import ctypes
import glob
import sys
from . import headers
from infi.cwrap import WrappedFunction, errcheck_zero, errcheck_nonzero, errcheck_nothing
from infi.os_info import get_platform_string
from infi.cwrap import IN, IN_OUT, wrap_library_function
import os

HBAAPI_SHARED_LIBRARY_FILENAMES = {
    'windows': 'hbaapi.dll',
    'linux': (glob.glob('/usr/lib64/libHBAAPI.so*' if sys.maxsize > 2 ** 32 \
                        else '/usr/lib/libHBAAPI.so*') + ['libHBAAPI.so'])[0],
    'sunos': (glob.glob('/usr/lib64/libsun_fc.so*' if sys.maxsize > 2 ** 32 \
                        else '/usr/lib/libsun_fc.so*') + ['libsun_fc.so'])[0],
    'aix': os.path.join(os.path.dirname(__file__), '_hbaapi_aix.so'),
    'solaris': (glob.glob('/usr/lib64/libsun_fc.so*' if sys.maxsize > 2 ** 32 \
                        else '/usr/lib/libsun_fc.so*') + ['libsun_fc.so'])[0]
    }

class InconsistencyError(Exception):
    pass

def errcheck_not_supported(errcheck_func=errcheck_nonzero):
    def errcheck(result, func, args):
        if result in [headers.HBA_STATUS_ERROR_NOT_SUPPORTED, headers.HBA_STATUS_ERROR_UNSUPPORTED_FC4]:
            raise NotImplementedError
        return errcheck_func()(result, func, args)
    return errcheck

def errcheck_inconsistency(errcheck_func=errcheck_nonzero):
    def errcheck(result, func, args):
        if result in [headers.HBA_STATUS_ERROR_STALE_DATA, headers.HBA_STATUS_ERROR_INVALID_HANDLE,
                      headers.HBA_STATUS_ERROR_ILLEGAL_INDEX, headers.HBA_STATUS_ERROR_TRY_AGAIN,
                      headers.HBA_STATUS_ERROR_UNAVAILABLE]:
            raise InconsistencyError("%s raised return an inconsistency error %s, you should retry",
                                     func.__name__, result)
        return errcheck_func()(result, func, args)
    return errcheck

class HbaApiFunction(WrappedFunction):
    @classmethod
    def _get_function_type(cls):
        return 'CFUNCTYPE'

    @classmethod
    def _get_library(cls):
        library_name = HBAAPI_SHARED_LIBRARY_FILENAMES.get(get_platform_string().split("-")[0], None)
        if library_name is None:
            raise OSError
        try:
            return ctypes.cdll.LoadLibrary(library_name)
        except:
            raise OSError

    @classmethod
    def _get_function(cls):
        # Solaris HBA library exported functions have Sun_fc prefix instead of HBA_, so we add this hack
        if 'solaris' in get_platform_string():
            parameters = cls.get_parameters()
            function = wrap_library_function(cls.__name__.replace("HBA_", "Sun_fc"), cls._get_library(), cls._get_function_type(),
                                             cls.return_value, parameters, cls.get_errcheck())
            return function
        elif 'aix' in get_platform_string():
            parameters = cls.get_parameters()
            function = wrap_library_function(cls.__name__.replace("HBA_", "PyHBA_"), cls._get_library(), cls._get_function_type(),
                                             cls.return_value, parameters, cls.get_errcheck())
            return function
        else:
            return super(HbaApiFunction, cls)._get_function()

# Library Control Functions

class HBA_GetVersion(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_UINT32

    @classmethod
    def get_errcheck(cls):
        return errcheck_zero()

    @classmethod
    def get_parameters(cls):
        return ()

class HBA_LoadLibrary(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_STATUS

    @classmethod
    def get_parameters(cls):
        return ()

class HBA_FreeLibrary(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_STATUS

    @classmethod
    def get_errcheck(cls):
        return errcheck_nothing()
    @classmethod
    def get_parameters(cls):
        return ()

class HBA_GetNumberOfAdapters(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_UINT32

    @classmethod
    def get_errcheck(cls):
        return errcheck_nothing()

    @classmethod
    def get_parameters(cls):
        return ()

class HBA_RefreshAdapterConfiguration(HbaApiFunction): #pylint: disable-msg=C0103
    @classmethod
    def get_errcheck(cls):
        return errcheck_nothing()

    @classmethod
    def get_parameters(cls):
        return ()

# Adapter and Port Information Functions

class HBA_GetAdapterName(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_STATUS

    @classmethod
    def get_errcheck(cls):
        return errcheck_nothing()

    @classmethod
    def get_parameters(cls):
        return (headers.UINT32, IN, 'adapterIndex'), \
            (ctypes.POINTER(ctypes.c_char), IN, 'adapterName')

class HBA_OpenAdapter(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_HANDLE

    @classmethod
    def get_errcheck(cls):
        return errcheck_zero()

    @classmethod
    def get_parameters(cls):
        return (ctypes.POINTER(ctypes.c_char), IN, 'adapterName'),

class HBA_CloseAdapter(HbaApiFunction): #pylint: disable-msg=C0103
    @classmethod
    def get_errcheck(cls):
        return errcheck_nothing()

    @classmethod
    def get_parameters(cls):
        return (headers.HBA_HANDLE, IN_OUT, 'handle'),

class HBA_GetAdapterAttributes(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_STATUS

    @classmethod
    def get_errcheck(cls):
        return errcheck_inconsistency(errcheck_not_supported)

    @classmethod
    def get_parameters(cls):
        return ((headers.HBA_HANDLE, IN, 'handle'),
                (ctypes.c_void_p, IN_OUT, 'adapterAttributes'))

class HBA_GetAdapterPortAttributes(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_STATUS

    @classmethod
    def get_errcheck(cls):
        return errcheck_inconsistency(errcheck_not_supported)

    @classmethod
    def get_parameters(cls):
        return ((headers.HBA_HANDLE, IN, 'handle'),
                (headers.HBA_UINT32, IN, 'portIndex'),
                (ctypes.c_void_p, IN_OUT, 'portAttributes'))

class HBA_GetDiscoveredPortAttributes(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_STATUS

    @classmethod
    def get_errcheck(cls):
        return errcheck_inconsistency(errcheck_not_supported)

    @classmethod
    def get_parameters(cls):
        return ((headers.HBA_HANDLE, IN, 'handle'),
                (headers.HBA_UINT32, IN, 'portIndex'),
                (headers.HBA_UINT32, IN, 'discoveredPortIndex'),
                (ctypes.c_void_p, IN_OUT, 'portAttributes'))

class HBA_GetPortStatistics(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_STATUS

    @classmethod
    def get_errcheck(cls):
        return errcheck_inconsistency(errcheck_not_supported)

    @classmethod
    def get_parameters(cls):
        return ((headers.HBA_HANDLE, IN, 'handle'),
                (headers.HBA_UINT32, IN, 'portIndex'),
                (ctypes.c_void_p, IN_OUT, 'portStatistics'))

class HBA_GetFC4Statistics(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_STATUS

    @classmethod
    def get_errcheck(cls):
        return errcheck_inconsistency(errcheck_not_supported)

    @classmethod
    def get_parameters(cls):
        return ((headers.HBA_HANDLE, IN, 'handle'),
                (ctypes.c_uint64, IN, 'portWWN'),
                (ctypes.c_uint8, IN, 'FC4type'),
                (ctypes.c_void_p, IN_OUT, 'fcpStatistics'))

class HBA_GetFcpTargetMappingV2(HbaApiFunction): #pylint: disable-msg=C0103
    return_value = headers.HBA_STATUS

    @classmethod
    def get_errcheck(cls):
        return errcheck_nonzero()

    @classmethod
    def get_parameters(cls):
        return ((headers.HBA_HANDLE, IN, "handle"),
                (ctypes.c_uint64, IN, "hbaPortWWN"),
                (ctypes.c_void_p, IN_OUT, "pMapping"))

