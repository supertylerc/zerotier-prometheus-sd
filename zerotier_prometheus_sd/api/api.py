from fastapi import APIRouter, Depends

from zerotier_prometheus_sd.api.schemas import PromSDItemSchema
from zerotier_prometheus_sd.config import Settings, get_settings
from zerotier_prometheus_sd.service.zerotier import ZeroTierAPI, ZeroTierAPIProtocol

api = APIRouter()


@api.get("/zerotier_targets", response_model=list[PromSDItemSchema])
async def get_zerotier_targets(
    network_id: str,
    port: str,
    settings: Settings = Depends(get_settings),
    zt_api: ZeroTierAPIProtocol = Depends(ZeroTierAPI),
) -> list[PromSDItemSchema]:
    members = await zt_api.get_zt_members(network_id, port, settings)
    return [PromSDItemSchema(targets=members, labels={})]
