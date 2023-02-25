import pytest
from pytest_httpx._httpx_mock import HTTPXMock

from zerotier_prometheus_sd.config import get_settings
from zerotier_prometheus_sd.service.zerotier import ZeroTierAPI


@pytest.mark.asyncio
async def test_zt_api(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        json=[
            {
                "id": "8056c2e21c000001-abcdef0123",
                "clock": 1612993759070,
                "networkId": "8056c2e21c000001",
                "nodeId": "abcdef01234",
                "controllerId": "8056c2e21c",
                "hidden": False,
                "name": "my-cray-supercomputer",
                "description": "My super awesome cray that I got ZeroTier to run on",
                "config": {
                    "activeBridge": False,
                    "authorized": True,
                    "capabilities": [0],
                    "creationTime": 1599853509872,
                    "id": "abcdef01234",
                    "identity": "abcdef0123:0:abcdef0123abcdef0123abcdef0123abcdef0123abcdef0123abcdef0123abcdef0123",
                    "ipAssignments": ["10.0.0.3"],
                    "lastAuthorizedTime": 1599853637989,
                    "lastDeauthorizedTime": 0,
                    "noAutoAssignIps": False,
                    "revision": 123,
                    "tags": [[123, 456]],
                    "vMajor": 1,
                    "vMinor": 6,
                    "vRev": 3,
                    "vProto": 12,
                },
                "lastOnline": 1612993673254,
                "physicalAddress": "8.8.8.8",
                "clientVersion": "1.6.3",
                "protocolVersion": 12,
                "supportsRulesEngine": True,
            }
        ],
        http_version="HTTP/2.0",
    )
    zt_api = ZeroTierAPI()
    faked_response = await zt_api.get_zt_members(
        zt_network_id="abcdefg", port="9300", settings=get_settings()
    )
    assert faked_response == ["10.0.0.3:9300"]
