"""Definition of the REST API for the inference service."""

from fastapi import FastAPI

from ccx_upgrades_inference.models import UpgradeApiResponse, UpgradeRisksPredictors

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()


@app.on_event("startup")
async def expose_metrics():
    """Expose the prometheus metrics in the /metrics endpoint."""
    Instrumentator().instrument(app).expose(app)


@app.get("/upgrade-risks-prediction", response_model=UpgradeApiResponse)
async def upgrade_risks_prediction(risk_predictors: UpgradeRisksPredictors):
    """Return the predition of an upgrade failure given a set of alerts and focs."""
    print(risk_predictors)
    # TODO @jdiazsua (CCXDEV-9842): use a real model instead of a mocked response
    return UpgradeApiResponse(upgrade_recommended=False, upgrade_risks_predictors=risk_predictors)
