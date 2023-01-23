"""Models to be used in the REST API."""

from typing import List
from pydantic import BaseModel, validator  # pylint: disable=no-name-in-module

from ccx_upgrades_inference.examples import EXAMPLE_RISKS


class Risks(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Contain a list of alerts and focs.

    The format must be:
        alert|{NAME}|{NAMESPACE}|{SEVERITY}
    or
        foc|{NAME}|{CONDITION}|{REASON}
    """

    risks: List[str]

    @validator("risks", each_item=True)
    def check_is_foc_or_alert(cls, risk):  # pylint: disable=no-self-argument
        """Check the risk is of type 'foc' or 'alert'."""
        kind = risk.split("|")[0]
        assert kind in ["foc", "alert"], f"'{kind}' not in ['foc','alert']"
        return risk

    # TODO @jdiazsua: Add more data validators once we have the real model

    class Config:  # pylint: disable=too-few-public-methods
        """Update the configuration with an example."""

        schema_extra = {"example": {"risks": EXAMPLE_RISKS}}


class UpgradeApiResponse(BaseModel):  # pylint: disable=too-few-public-methods
    """
    UpgradeApiResponse is the response for the upgrade-risks-prediction endpoint.

    Contain the result of the prediction: whether the upgrade will fail or not; and
    the predictors that the model detected as actual risks.
    """

    upgrade_recommended: bool
    upgrade_risks_predictors: List[str]

    class Config:  # pylint: disable=too-few-public-methods
        """Update the configuration with an example."""

        schema_extra = {
            "example": {"upgrade_recommended": False, "upgrade_risks_predictors": EXAMPLE_RISKS}
        }
