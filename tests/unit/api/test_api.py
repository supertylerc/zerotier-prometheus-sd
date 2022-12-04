from fastapi import FastAPI
from starlette.testclient import TestClient

from zerotier_prometheus_sd.api import api
from zerotier_prometheus_sd.config import Settings
from zerotier_prometheus_sd.service.zerotier import ZeroTierAPI


class FakeZeroTierAPI:
    async def get_zt_members(
        self,
        zt_network_id: str,
        port: str,
        settings: Settings,
    ) -> list[str]:
        return [f"192.0.2.1:{port}", f"192.0.2.100:{port}"]


app = FastAPI()
app.include_router(api.api)
client = TestClient(app)
app.dependency_overrides[ZeroTierAPI] = FakeZeroTierAPI


def test_zerotier_targets() -> None:
    response = client.get("/zerotier_targets?port=9300&network_id=abcdefg")
    assert response.status_code == 200
    assert response.json() == [
        {"targets": ["192.0.2.1:9300", "192.0.2.100:9300"], "labels": {}}
    ]
