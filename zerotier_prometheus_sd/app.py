from fastapi import FastAPI

from zerotier_prometheus_sd.api.api import api

app = FastAPI(debug=True)

app.include_router(api)
