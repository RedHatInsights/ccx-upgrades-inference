"""Definition of the REST API for the inference service."""

from fastapi import FastAPI

from ccx_inference_service.models import Risks, UpgradeApiResponse

app = FastAPI()


@app.get("/upgrade-risks-prediction", response_model=UpgradeApiResponse)
async def upgrade_risks_prediction(risks: Risks):
    """Return the predition of an upgrade failure given a set of alerts and focs."""
    # TODO @jdiazsua (CCXDEV-9842): use a real model instead of a mocked response
    return UpgradeApiResponse(upgrade_recommended=False, upgrade_risks_predictors=risks.risks)
