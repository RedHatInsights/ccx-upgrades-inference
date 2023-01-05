"""Test main.py."""

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


class TestUpgradeFailurePrediction:  # pylint: disable=too-few-public-methods
    """Check the /upgrade-failure-prediction endpoint."""

    def test_no_body(self):
        """If the request has no body it should return a 422."""
        response = client.get("/upgrade-failure-prediction")
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "field required"

    def test_unexpected_body(self):
        """If the request has an unexpected body it should return a 422."""
        response = client.request("GET", "/upgrade-failure-prediction", json={"foo": "bar"})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "field required"

    def test_invalid_risk(self):
        """If the request has an invalid risk it should complain."""
        response = client.request(
            "GET", "/upgrade-failure-prediction", json={"risks": ["test|others"]}
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "'test' not in ['foc','alert']"

    def test_empty_risks(self):
        """If the request has no risks it shouldn't complain."""
        response = client.request("GET", "/upgrade-failure-prediction", json={"risks": []})
        assert response.status_code == 200
        assert not response.json()["upgrade_recommended"]
        assert response.json()["upgrade_failure_predictors"] == []

    def test_valid_body(self):
        """If the request has an invalid risk it should complain."""
        response = client.request(
            "GET", "/upgrade-failure-prediction", json={"risks": ["alert|test"]}
        )
        assert response.status_code == 200
        assert not response.json()["upgrade_recommended"]
        assert response.json()["upgrade_failure_predictors"] == ["alert|test"]
