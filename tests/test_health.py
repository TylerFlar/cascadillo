import pytest

from httpx import ASGITransport, AsyncClient

from cascadillo.app import create_app


@pytest.mark.asyncio
async def test_health_endpoints() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for ep in ("/healthz", "/livez", "/readyz", "/"):
            r = await ac.get(ep)
            assert r.status_code == 200
            assert r.json()
