from typing import Protocol

import httpx
from pydantic import BaseModel

from zerotier_prometheus_sd.config import Settings


class MemberConfigSchema(BaseModel):
    activeBridge: bool  # noqa: N815
    authorized: bool
    capabilities: list[int]
    creationTime: int  # noqa: N815
    id: str
    identity: str
    ipAssignments: list[str]  # noqa: N815
    lastAuthorizedTime: int  # noqa: N815
    lastDeauthorizedTime: int  # noqa: N815
    noAutoAssignIps: bool  # noqa: N815
    revision: int
    tags: list[list[int | bool | None]]
    vMajor: int  # noqa: N815
    vMinor: int  # noqa: N815
    vRev: int  # noqa: N815
    vProto: int  # noqa: N815


# noqa: N815
class NetworkMemberSchema(BaseModel):
    id: str | None
    clock: int | None
    networkId: str | None  # noqa: N815
    nodeId: str | None  # noqa: N815
    controllerId: str | None  # noqa: N815
    hidden: bool | None
    name: str | None
    description: str | None
    config: MemberConfigSchema
    lastOnline: int | None  # noqa: N815
    physicalAddress: str | None  # noqa: N815
    clientVersion: str | None  # noqa: N815
    protocolVersion: int | None  # noqa: N815
    supportsRulesEngine: bool | None  # noqa: N815


class ZeroTierAPIProtocol(Protocol):
    zt_api_base_url: str
    zt_api_version: str
    zt_api_url: str
    client: httpx.AsyncClient

    async def _get(self, client: httpx.AsyncClient, path: str) -> httpx.Response:
        ...

    async def _get_members(
        self, client: httpx.AsyncClient, network_id: str
    ) -> list[NetworkMemberSchema]:
        ...

    async def get_zt_members(
        self,
        zt_network_id: str,
        port: str,
        settings: Settings,
    ) -> list[str]:
        ...


class ZeroTierAPI:
    zt_api_base_url: str
    zt_api_version: str
    zt_api_url: str
    client: httpx.AsyncClient

    def __init__(
        self,
        zt_api_base_url: str = "https://api.zerotier.com/api",
        zt_api_version: str = "v1",
    ) -> None:
        self.zt_api_base_url = zt_api_base_url
        self.zt_api_version = zt_api_version
        self.zt_api_url = f"{zt_api_base_url}/{zt_api_version}"

    async def _get(self, client: httpx.AsyncClient, path: str) -> httpx.Response:
        return await client.get(path)

    async def _get_members(
        self, client: httpx.AsyncClient, network_id: str
    ) -> list[NetworkMemberSchema]:
        api_path = f"network/{network_id}/member"
        resource = f"{self.zt_api_url}/{api_path}"
        response = await self._get(client, resource)
        members = response.json()
        network_members = [NetworkMemberSchema.parse_obj(m) for m in members]
        return network_members

    async def get_zt_members(
        self,
        zt_network_id: str,
        port: str,
        settings: Settings,
    ) -> list[str]:
        headers = {"Authorization": f"token {settings.zt_api_key}"}
        async with httpx.AsyncClient(http2=True, headers=headers) as c:
            members = await self._get_members(c, zt_network_id)
            targets: list[str] = [
                f"{m.config.ipAssignments[0]}:{port}" for m in members
            ]
        return targets
