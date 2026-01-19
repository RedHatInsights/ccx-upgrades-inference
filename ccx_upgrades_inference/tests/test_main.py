"""Test main.py."""

from fastapi.testclient import TestClient

from ccx_upgrades_inference.main import app
from ccx_upgrades_inference.examples import EXAMPLE_PREDICTORS

client = TestClient(app)


class TestUpgradeRisksPrediction:  # pylint: disable=too-few-public-methods
    """Check the /upgrade-risks-prediction endpoint."""

    def test_no_body(self):
        """If the request has no body it should return a 422."""
        response = client.get("/upgrade-risks-prediction")
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"

    def test_unexpected_body(self):
        """If the request has an unexpected body it should return a 422."""
        response = client.request("GET", "/upgrade-risks-prediction", json={"foo": "bar"})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"

    def test_valid_body(self):
        """If the request has an invalid risk it should complain."""
        response = client.request(
            "GET",
            "/upgrade-risks-prediction",
            json=EXAMPLE_PREDICTORS,
        )
        assert response.status_code == 200
        assert "upgrade_recommended" not in response.json().keys()
        assert response.json()["upgrade_risks_predictors"] == EXAMPLE_PREDICTORS
