"""Definition of the REST API for the inference service."""

import os

from fastapi import FastAPI

from ccx_upgrades_inference.models import UpgradeApiResponse, UpgradeRisksPredictors
from ccx_upgrades_inference.inference import StaticPredictor
from ccx_upgrades_inference.sentry import init_sentry

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
static_predictor = StaticPredictor()
init_sentry(os.environ.get("SENTRY_DSN", None), None, os.environ.get("SENTRY_ENVIRONMENT", None))


@app.on_event("startup")
async def expose_metrics():
    """Expose the prometheus metrics in the /metrics endpoint."""
    Instrumentator().instrument(app).expose(app)


@app.get("/upgrade-risks-prediction", response_model=UpgradeApiResponse)
async def upgrade_risks_prediction(risk_predictors: UpgradeRisksPredictors):
    """Return the predition of an upgrade failure given a set of alerts and focs."""
    predictors = static_predictor.predict(risk_predictors)
    return UpgradeApiResponse(upgrade_risks_predictors=predictors)
