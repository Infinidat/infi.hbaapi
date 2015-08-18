/*! AIX's hbaapi is a static library but we need a shared library to load.
 * This file is a simple wrapper to the static functions that will be compiled into a shared library !*/

#include <sys/hbaapi.h>

/* Phase 1 Function Prototypes */

HBA_API HBA_UINT32 PyHBA_GetVersion(void)
{
    return HBA_GetVersion();
}

HBA_API HBA_STATUS PyHBA_LoadLibrary(void)
{
    return HBA_LoadLibrary();
}

HBA_API HBA_STATUS PyHBA_FreeLibrary(void)
{
    return HBA_FreeLibrary();
}

HBA_API HBA_STATUS PyHBA_RegisterLibrary(PHBA_ENTRYPOINTS entrypoints)
{
    return HBA_RegisterLibrary(entrypoints);
}

HBA_API HBA_UINT32 PyHBA_GetNumberOfAdapters(void)
{
    return HBA_GetNumberOfAdapters();
}

HBA_API HBA_STATUS PyHBA_GetAdapterName(
    HBA_UINT32          adapterindex,
    char                * adaptername
    )
{
    return HBA_GetAdapterName(adapterindex, adaptername);
}

HBA_API HBA_HANDLE PyHBA_OpenAdapter(
    char                * adaptername
    )
{
    return HBA_OpenAdapter(adaptername);
}

HBA_API void PyHBA_CloseAdapter(
    HBA_HANDLE          handle
    )
{
    return HBA_CloseAdapter(handle);
}

HBA_API HBA_STATUS PyHBA_GetAdapterAttributes(
    HBA_HANDLE          handle,
    HBA_ADAPTERATTRIBUTES       * hbaattributes
    )
{
    return HBA_GetAdapterAttributes(handle, hbaattributes);
}

HBA_API HBA_STATUS PyHBA_GetAdapterPortAttributes(
    HBA_HANDLE          handle,
    HBA_UINT32          portindex,
    HBA_PORTATTRIBUTES      * portattributes
    )
{
    return HBA_GetAdapterPortAttributes(handle, portindex, portattributes);
}

HBA_API HBA_STATUS PyHBA_GetPortStatistics(
    HBA_HANDLE          handle,
    HBA_UINT32          portindex,
    HBA_PORTSTATISTICS      * portstatistics
    )
{
    return HBA_GetPortStatistics(handle, portindex, portstatistics);
}

HBA_API HBA_STATUS PyHBA_GetDiscoveredPortAttributes(
    HBA_HANDLE          handle,
    HBA_UINT32          portindex,
    HBA_UINT32          discoveredportindex,
    HBA_PORTATTRIBUTES      * portattributes
    )
{
    return HBA_GetDiscoveredPortAttributes(handle, portindex, discoveredportindex, portattributes);
}

HBA_API HBA_STATUS PyHBA_GetPortAttributesByWWN(
    HBA_HANDLE          handle,
    HBA_WWN             PortWWN,
    HBA_PORTATTRIBUTES      * portattributes
    )
{
    return HBA_GetPortAttributesByWWN(handle, PortWWN, portattributes);
}

HBA_API HBA_STATUS PyHBA_SendCTPassThru(
    HBA_HANDLE          handle,
    void                * pReqBuffer,
    HBA_UINT32          ReqBufferSize,
    void                * pRspBuffer,
    HBA_UINT32          RspBufferSize
    )
{
    return HBA_SendCTPassThru(handle, pReqBuffer, ReqBufferSize, pRspBuffer, RspBufferSize);
}


HBA_API HBA_STATUS PyHBA_GetEventBuffer(
    HBA_HANDLE          handle,
    PHBA_EVENTINFO          EventBuffer,
    HBA_UINT32          * EventBufferCount
    )
{
    return HBA_GetEventBuffer(handle, EventBuffer, EventBufferCount);
}

HBA_API HBA_STATUS PyHBA_SetRNIDMgmtInfo(
    HBA_HANDLE          handle,
    HBA_MGMTINFO            info
    )
{
    return HBA_SetRNIDMgmtInfo(handle, info);
}

HBA_API HBA_STATUS PyHBA_GetRNIDMgmtInfo(
    HBA_HANDLE          handle,
    HBA_MGMTINFO            * pInfo
    )
{
    return HBA_GetRNIDMgmtInfo(handle, pInfo);
}

HBA_API HBA_STATUS PyHBA_SendRNID(
    HBA_HANDLE          handle,
    HBA_WWN             wwn,
    HBA_WWNTYPE             wwntype,
    void                * pRspBuffer,
    HBA_UINT32          * RspBufferSize
    )
{
    return HBA_SendRNID(handle, wwn, wwntype, pRspBuffer, RspBufferSize);
}

HBA_API void PyHBA_RefreshInformation(
    HBA_HANDLE          handle
    )
{
    return HBA_RefreshInformation(handle);
}

HBA_API void PyHBA_ResetStatistics(
    HBA_HANDLE          handle,
    HBA_UINT32          portindex
    )
{
    return HBA_ResetStatistics(handle, portindex);
}

HBA_API HBA_STATUS PyHBA_GetFcpTargetMapping(
    HBA_HANDLE          handle,
    PHBA_FCPTARGETMAPPING       mapping
    )
{
    return HBA_GetFcpTargetMapping(handle, mapping);
}

HBA_API HBA_STATUS PyHBA_GetFcpPersistentBinding(
    HBA_HANDLE          handle,
    PHBA_FCPBINDING         binding
    )
{
    return HBA_GetFcpPersistentBinding(handle, binding);
}

HBA_API HBA_STATUS PyHBA_SendScsiInquiry (
    HBA_HANDLE          handle,
    HBA_WWN             PortWWN,
    HBA_UINT64          fcLUN,
    HBA_UINT8           EVPD,
    HBA_UINT32          PageCode,
    void                * pRspBuffer,
    HBA_UINT32          RspBufferSize,
    void                * pSenseBuffer,
    HBA_UINT32          SenseBufferSize
    )
{
    return HBA_SendScsiInquiry(handle, PortWWN, fcLUN, EVPD, PageCode, pRspBuffer, RspBufferSize, pSenseBuffer, SenseBufferSize);
}

HBA_API HBA_STATUS PyHBA_SendReportLUNs (
    HBA_HANDLE          handle,
    HBA_WWN             portWWN,
    void                * pRspBuffer,
    HBA_UINT32          RspBufferSize,
    void                * pSenseBuffer,
    HBA_UINT32          SenseBufferSize
    )
{
    return HBA_SendReportLUNs(handle, portWWN, pRspBuffer, RspBufferSize, pSenseBuffer, SenseBufferSize);
}

HBA_API HBA_STATUS PyHBA_SendReadCapacity (
    HBA_HANDLE          handle,
    HBA_WWN             portWWN,
    HBA_UINT64          fcLUN,
    void                * pRspBuffer,
    HBA_UINT32          RspBufferSize,
    void                * pSenseBuffer,
    HBA_UINT32          SenseBufferSize
    )
{
    return HBA_SendReadCapacity(handle, portWWN, fcLUN, pRspBuffer, RspBufferSize, pSenseBuffer, SenseBufferSize);
}


/* Phase 2 Function Prototypes */
HBA_API HBA_STATUS PyHBA_RegisterLibraryV2(HBA_ENTRYPOINTSV2 *pHBAInfo)
{
    return HBA_RegisterLibraryV2(pHBAInfo);
}

HBA_API HBA_STATUS PyHBA_OpenAdapterByWWN(
        HBA_HANDLE *pHandle,
        HBA_WWN wwn
    )
{
    return HBA_OpenAdapterByWWN(pHandle, wwn);
}

HBA_API HBA_STATUS PyHBA_GetFcpTargetMappingV2(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_FCPTARGETMAPPINGV2 *pMapping
    )
{
    return HBA_GetFcpTargetMappingV2(handle, hbaPortWWN, pMapping);
}

HBA_API HBA_STATUS PyHBA_SendCTPassThruV2(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        void *pReqBuffer,
        HBA_UINT32 ReqBufferSize,
        void *pRspBuffer,
        HBA_UINT32 *pRspBufferSize
    )
{
    return HBA_SendCTPassThruV2(handle, hbaPortWWN, pReqBuffer, ReqBufferSize, pRspBuffer, pRspBufferSize);
}

HBA_API void PyHBA_RefreshAdapterConfiguration(void)
{
    return HBA_RefreshAdapterConfiguration();
}

HBA_API HBA_STATUS PyHBA_GetBindingCapability(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_BIND_CAPABILITY*pFlags
    )
{
    return HBA_GetBindingCapability(handle, hbaPortWWN, pFlags);
}

HBA_API HBA_STATUS PyHBA_GetBindingSupport(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_BIND_CAPABILITY*pFlags
    )
{
    return HBA_GetBindingSupport(handle, hbaPortWWN, pFlags);
}

HBA_API HBA_STATUS PyHBA_SetBindingSupport(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_BIND_CAPABILITY flags
    )
{
    return HBA_SetBindingSupport(handle, hbaPortWWN, flags);
}

HBA_API HBA_STATUS PyHBA_SetPersistentBindingV2(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        const HBA_FCPBINDING2 *binding
    )
{
    return HBA_SetPersistentBindingV2(handle, hbaPortWWN, binding);
}

HBA_API HBA_STATUS PyHBA_GetPersistentBindingV2(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_FCPBINDING2 *binding
    )
{
    return HBA_GetPersistentBindingV2(handle, hbaPortWWN, binding);
}

HBA_API HBA_STATUS PyHBA_RemovePersistentBinding(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        const HBA_FCPBINDING2 *binding
    )
{
    return HBA_RemovePersistentBinding(handle, hbaPortWWN, binding);
}

HBA_API HBA_STATUS PyHBA_RemoveAllPersistentBindings(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN
    )
{
    return HBA_RemoveAllPersistentBindings(handle, hbaPortWWN);
}

HBA_API HBA_STATUS PyHBA_SendRNIDV2(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_WWN destWWN,
        HBA_UINT32 destFCID,
        HBA_UINT32 NodeIdDataFormat,
        void *pRspBuffer,
        HBA_UINT32 *pRspBufferSize
    )
{
    return HBA_SendRNIDV2(handle, hbaPortWWN, destWWN, destFCID, NodeIdDataFormat, pRspBufferSize, pRspBufferSize);
}

HBA_API HBA_STATUS PyHBA_ScsiInquiryV2 (
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_WWN discoveredPortWWN,
        HBA_UINT64 fcLUN,
        HBA_UINT8 CDB_Byte1,
        HBA_UINT8 CDB_Byte2,
        void *pRspBuffer,
        HBA_UINT32 *pRspBufferSize,
        HBA_UINT8 *pScsiStatus,
        void *pSenseBuffer,
        HBA_UINT32 *pSenseBufferSize
    )
{
    return HBA_ScsiInquiryV2(handle, hbaPortWWN, discoveredPortWWN, fcLUN, CDB_Byte1, CDB_Byte2, pRspBuffer, pRspBufferSize, pScsiStatus, pSenseBuffer, pSenseBufferSize);
}

HBA_API HBA_STATUS PyHBA_ScsiReportLUNsV2(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_WWN discoveredPortWWN,
        void *pRspBuffer,
        HBA_UINT32 *pRspBufferSize,
        HBA_UINT8 *pScsiStatus,
        void *pSenseBuffer,
        HBA_UINT32 *pSenseBufferSize
    )
{
    return HBA_ScsiReportLUNsV2(handle, hbaPortWWN, discoveredPortWWN, pRspBuffer, pRspBufferSize, pScsiStatus, pSenseBuffer, pSenseBufferSize);
}

HBA_API HBA_STATUS PyHBA_ScsiReadCapacityV2(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_WWN discoveredPortWWN,
        HBA_UINT64 fcLUN,
        void *pRspBuffer,
        HBA_UINT32 *pRspBufferSize,
        HBA_UINT8 *pScsiStatus,
        void *pSenseBuffer,
        HBA_UINT32 *pSenseBufferSize
    )
{
    return HBA_ScsiReadCapacityV2(handle, hbaPortWWN, discoveredPortWWN, fcLUN, pRspBuffer, pRspBufferSize, pScsiStatus, pSenseBuffer, pSenseBufferSize);
}

HBA_API HBA_UINT32 PyHBA_GetWrapperLibraryAttributes(
        HBA_LIBRARYATTRIBUTES *attributes
    )
{
    return HBA_GetWrapperLibraryAttributes(attributes);
}

HBA_API HBA_UINT32 PyHBA_GetVendorLibraryAttributes(
        HBA_UINT32 adapter_index,
        HBA_LIBRARYATTRIBUTES *attributes
    )
{
    return HBA_GetVendorLibraryAttributes(adapter_index, attributes);
}

HBA_API HBA_STATUS PyHBA_RemoveCallback(
        HBA_CALLBACKHANDLE callbackHandle
    )
{
    return HBA_RemoveCallback(callbackHandle);
}

HBA_API HBA_STATUS PyHBA_RegisterForAdapterAddEvents(
        void (*pCallback) (
              void *pData,
              HBA_WWN PortWWN,
              HBA_UINT32 eventType
            ),
        void *pUserData,
        HBA_CALLBACKHANDLE *pCallbackHandle
    )
{
    return HBA_RegisterForAdapterAddEvents(pCallback, pUserData, pCallbackHandle);
}

HBA_API HBA_STATUS PyHBA_RegisterForAdapterEvents(
        void (*pCallback) (
              void *pData,
              HBA_WWN PortWWN,
              HBA_UINT32 eventType
            ),
        void *pUserData,
        HBA_HANDLE handle,
        HBA_CALLBACKHANDLE *pCallbackHandle
    )
{
    return HBA_RegisterForAdapterEvents(pCallback, pUserData, handle, pCallbackHandle);
}

HBA_API HBA_STATUS PyHBA_RegisterForAdapterPortEvents(
        void (*pCallback) (
              void *pData,
              HBA_WWN PortWWN,
              HBA_UINT32 eventType,
              HBA_UINT32 fabricPortID
            ),
        void *pUserData,
        HBA_HANDLE handle,
        HBA_WWN PortWWN,
        HBA_CALLBACKHANDLE *pCallbackHandle
    )
{
    return HBA_RegisterForAdapterPortEvents(pCallback, pUserData, handle, PortWWN, pCallbackHandle);
}

HBA_API HBA_STATUS PyHBA_RegisterForAdapterPortStatEvents(
        void (*pCallback) (
              void *pData,
              HBA_WWN PortWWN,
              HBA_UINT32 eventType
              ),
        void *pUserData,
        HBA_HANDLE handle,
        HBA_WWN PortWWN,
        HBA_PORTSTATISTICS stats,
        HBA_UINT32 statType,
        HBA_CALLBACKHANDLE *pCallbackHandle
    )
{
    return HBA_RegisterForAdapterPortStatEvents(pCallback, pUserData, handle, PortWWN, stats, statType, pCallbackHandle);
}

HBA_API HBA_STATUS PyHBA_RegisterForTargetEvents(
        void (*pCallback) (
              void *pData,
              HBA_WWN hbaPortWWN,
              HBA_WWN discoveredPortWWN,
              HBA_UINT32 eventType
              ),
        void *pUserData,
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_WWN discoveredPortWWN,
        HBA_CALLBACKHANDLE *pCallbackHandle,
        HBA_UINT32 allTargets
    )
{
    return HBA_RegisterForTargetEvents(pCallback, pUserData, handle, hbaPortWWN, discoveredPortWWN, pCallbackHandle, allTargets);
}

HBA_API HBA_STATUS PyHBA_RegisterForLinkEvents(
        void (*pCallback) (
              void *pData,
              HBA_WWN adapterWWN,
              HBA_UINT32 eventType,
              void *pRLIRBuffer,
              HBA_UINT32 RLIRBufferSize
              ),
        void *pUserData,
        void *pRLIRBuffer,
        HBA_UINT32 RLIRBufferSize,
        HBA_HANDLE handle,
        HBA_CALLBACKHANDLE *pCallbackHandle
    )
{
    return HBA_RegisterForLinkEvents(pCallback, pUserData, pRLIRBuffer, RLIRBufferSize, handle, pCallbackHandle);
}

HBA_API HBA_STATUS PyHBA_SendRPL (
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_WWN agent_wwn,
        HBA_UINT32 agent_domain,
        HBA_UINT32 portIndex,
        void *pRspBuffer,
        HBA_UINT32 *pRspBufferSize
    )
{
    return HBA_SendRPL(handle, hbaPortWWN, agent_wwn, agent_domain, portIndex, pRspBuffer, pRspBufferSize);
}

HBA_API HBA_STATUS PyHBA_SendRPS (
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_WWN agent_wwn,
        HBA_UINT32 agent_domain,
        HBA_WWN object_wwn,
        HBA_UINT32 object_port_number,
        void *pRspBuffer,
        HBA_UINT32 *pRspBufferSize
    )
{
    return HBA_SendRPS(handle, hbaPortWWN, agent_wwn, agent_domain,object_wwn, object_port_number, pRspBufferSize, pRspBufferSize);
}

HBA_API HBA_STATUS PyHBA_SendSRL (
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_WWN wwn,
        HBA_UINT32 domain,
        void *pRspBuffer,
        HBA_UINT32 *pRspBufferSize
    )
{
    return HBA_SendSRL(handle, hbaPortWWN, wwn, domain, pRspBuffer, pRspBufferSize);
}

HBA_API HBA_STATUS PyHBA_SendLIRR (
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_WWN destWWN,
        HBA_UINT8 function,
        HBA_UINT8 type,
        void *pRspBuffer,
        HBA_UINT32 *pRspBufferSize
    )
{
    return HBA_SendLIRR(handle, hbaPortWWN, destWWN, function, type, pRspBuffer, pRspBufferSize);
}

HBA_API HBA_STATUS PyHBA_GetFC4Statistics(
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_UINT8 FC4type,
        HBA_FC4STATISTICS *statistics
    )
{
    return HBA_GetFC4Statistics(handle, hbaPortWWN, FC4type, statistics);
}

HBA_API HBA_STATUS PyHBA_GetFCPStatistics(
        HBA_HANDLE handle,
        const HBA_SCSIID *lunit,
        HBA_FC4STATISTICS *statistics
    )
{
    return HBA_GetFCPStatistics(handle, lunit, statistics);
}

HBA_API HBA_STATUS PyHBA_SendRLS (
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_WWN destWWN,
        void *pRspBuffer,
        HBA_UINT32 *pRspBufferSize
    )
{
    return HBA_SendRLS(handle, hbaPortWWN, destWWN, pRspBuffer, pRspBufferSize);
}

HBA_API HBA_STATUS PyHBA_GetSBTargetMapping (
        HBA_HANDLE handle,
        HBA_WWN hbaPortWWN,
        HBA_SBTARGETMAPPING *pMapping
    )
{
    return HBA_GetSBTargetMapping(handle, hbaPortWWN, pMapping);
}

HBA_API HBA_STATUS PyHBA_GetSBStatistics (
        HBA_HANDLE handle,
        const HBA_SBDEVID *device,
        HBA_SBSTATISTICS *statistics
    )
{
    return HBA_GetSBStatistics(handle, device, statistics);
}

HBA_API HBA_STATUS PyHBA_SBDskGetCapacity (
        HBA_DEVICESELFDESC DeviceSelfDesc,
        HBA_SBDSKCAPACITY *pSBDskCapacity
    )
{
    return HBA_SBDskGetCapacity(DeviceSelfDesc, pSBDskCapacity);
}

void init_hbaapi_aix(void)
{
}