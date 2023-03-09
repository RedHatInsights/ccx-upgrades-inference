"""Definition of the REST API for the inference service."""

from fastapi import FastAPI

from ccx_upgrades_inference.models import UpgradeApiResponse, UpgradeRisksPredictors
from ccx_upgrades_inference.inference import StaticPredictor

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
static_predictor = StaticPredictor()


@app.on_event("startup")
async def expose_metrics():
    """Expose the prometheus metrics in the /metrics endpoint."""
    Instrumentator().instrument(app).expose(app)


@app.get("/upgrade-risks-prediction", response_model=UpgradeApiResponse)
async def upgrade_risks_prediction(risk_predictors: UpgradeRisksPredictors):
    """Return the predition of an upgrade failure given a set of alerts and focs."""
    predictors = static_predictor.predict(risk_predictors)
    return UpgradeApiResponse(upgrade_risks_predictors=predictors)
