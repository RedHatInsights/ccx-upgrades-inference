"""Definition of the REST API for the inference service."""

import os

from fastapi import FastAPI
from contextlib import asynccontextmanager

from ccx_upgrades_inference.models import UpgradeApiResponse, UpgradeRisksPredictors
from ccx_upgrades_inference.inference import StaticPredictor
from ccx_upgrades_inference.sentry import init_sentry

from prometheus_fastapi_instrumentator import Instrumentator

init_sentry(os.environ.get("SENTRY_DSN", None), None, os.environ.get("SENTRY_ENVIRONMENT", None))


def create_lifespan_handler(instrumentator: Instrumentator):
    """Create a FastAPI lifespan handler for the application.

    @param instrumentator: A prometheus instrumentator used to expose metrics
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        instrumentator.expose(app)
        yield

    return lifespan


def create_app():
    """Initialize the app."""
    instrumentator = Instrumentator()
    app = FastAPI(
        lifespan=create_lifespan_handler(instrumentator),
    )
    instrumentator.instrument(app)
    return app


static_predictor = StaticPredictor()
app = create_app()


@app.get("/upgrade-risks-prediction", response_model=UpgradeApiResponse)
async def upgrade_risks_prediction(risk_predictors: UpgradeRisksPredictors):
    """Return the predition of an upgrade failure given a set of alerts and focs."""
    predictors = static_predictor.predict(risk_predictors)
    return UpgradeApiResponse(upgrade_risks_predictors=predictors)
