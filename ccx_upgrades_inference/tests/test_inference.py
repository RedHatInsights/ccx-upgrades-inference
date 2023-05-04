"""Test the inference.py functions."""

import pytest

from ccx_upgrades_inference.inference import StaticPredictor, EXCLUDE_NAMESPACES
from ccx_upgrades_inference.models import Alert, FOC, UpgradeRisksPredictors


static_predictor = StaticPredictor()


class TestStaticPredictor:  # pylint: disable=too-few-public-methods
    """Test the StaticPredictor."""

    class TestFilterAlert:  # pylint: disable=too-few-public-methods
        """Test the StaticPredictor.filter_alert function."""

        def test_openshift_namespace_no_critical_severity(self):
            """Check that the static predictor doesn't fire if the alert is not critical."""
            alert = Alert(name="test", namespace="openshift-test", severity="not critical")

            assert not static_predictor.filter_alert(alert), "a non critical alert should not fire"

        def test_openshift_namespace_critical_severity(self):
            """Check that the static predictor fires if the alert is critical."""
            alert = Alert(name="test", namespace="openshift-test", severity="critical")

            assert static_predictor.filter_alert(alert), "a critical alert should fire"

        def test_no_namespace_critical_severity(self):
            """Check that the it doesn't fire if the alert is critical but the namespace is not defined."""
            alert = Alert(name="test", severity="critical")

            assert not static_predictor.filter_alert(
                alert
            ), "a critical alert shouldn't fire if namespace is not defined"

        def test_other_namespace_critical_severity(self):
            """Check that the it doesn't fire if the alert is critical but the namespace is not an openshift namespace."""
            alert = Alert(name="test", severity="critical", namespace="not-openshift")

            assert not static_predictor.filter_alert(
                alert
            ), "a critical alert shouldn't fire if namespace isn't openshift-*"

        @pytest.mark.parametrize("namespace", EXCLUDE_NAMESPACES)
        def test_excluded_namespace_critical_severity(self, namespace):
            """Check that it doesn't fire if alert is critical but no namespace."""
            alert = Alert(name="test", severity="critical", namespace=namespace)

            assert not static_predictor.filter_alert(
                alert
            ), "a critical alert shouldn't fire if namespace is excluded"

    class TestFilterFOC:  # pylint: disable=too-few-public-methods
        """Test the StaticPredictor.filter_foc function."""

        def test_no_available_or_degraded(self):
            """Check that it doesn't fire if foc is not 'Not Available' or 'Degraded'."""
            foc = FOC(name="test", condition="test")

            assert not static_predictor.filter_foc(
                foc
            ), "a non 'Not Available' or 'Degraded' foc shouldn't fire"

        @pytest.mark.parametrize("condition", ["Not Available", "Degraded"])
        def test_available_or_degraded(self, condition):
            """Check that it fires if the foc is one of 'Not Available' or 'Degraded'."""
            foc = FOC(name="test", condition=condition)

            assert static_predictor.filter_foc(
                foc
            ), "an 'Not Available' or 'Degraded' foc should fire"

    class TestPredict:  # pylint: disable=too-few-public-methods
        """Test the StaticPredictor.predict function."""

        def test_predict_both_fire(self):
            """
            Check that predict filters the alerts and focs if both fire.

            If firing alerts are < 2, they are not included.
            """
            alert = Alert(name="test", severity="critical", namespace="openshift-test")
            foc = FOC(name="test", condition="Not Available")
            risks = UpgradeRisksPredictors(alerts=[alert], operator_conditions=[foc])
            got = static_predictor.predict(risks)
            assert got == UpgradeRisksPredictors(alerts=[], operator_conditions=[foc])

        def test_predict_1_alert_fire(self):
            """
            Check that predict filters the alerts and focs if the alert fires.

            If firing alerts are < 2, they are not included.
            """
            alert = Alert(name="test", severity="critical", namespace="openshift-test")
            foc = FOC(name="test", condition="this doesn't fire")
            risks = UpgradeRisksPredictors(alerts=[alert], operator_conditions=[foc])
            got = static_predictor.predict(risks)
            assert got == UpgradeRisksPredictors(alerts=[], operator_conditions=[])

        def test_predict_2_alerts_fire(self):
            """
            Check that predict filters the alerts and focs if the alert fires.

            If firing alerts are >= 2, they are included.
            """
            alert = Alert(name="test", severity="critical", namespace="openshift-test")
            foc = FOC(name="test", condition="this doesn't fire")
            risks = UpgradeRisksPredictors(alerts=[alert, alert], operator_conditions=[foc])
            got = static_predictor.predict(risks)
            assert got == UpgradeRisksPredictors(alerts=[alert, alert], operator_conditions=[])

        def test_predict_foc_fire(self):
            """Check that predict filters the alerts and focs if the foc fires."""
            alert = Alert(name="test", severity="non critical", namespace="openshift-test")
            foc = FOC(name="test", condition="Not Available")
            risks = UpgradeRisksPredictors(alerts=[alert], operator_conditions=[foc])
            got = static_predictor.predict(risks)
            assert got == UpgradeRisksPredictors(alerts=[], operator_conditions=[foc])

        def test_predict_no_alert_or_foc_fire(self):
            """Check that predict filters the alerts and focs if the no one fires."""
            alert = Alert(name="test", severity="non critical", namespace="openshift-test")
            foc = FOC(name="test", condition="this doesn't fire")
            risks = UpgradeRisksPredictors(alerts=[alert], operator_conditions=[foc])
            got = static_predictor.predict(risks)
            assert got == UpgradeRisksPredictors(alerts=[], operator_conditions=[])
