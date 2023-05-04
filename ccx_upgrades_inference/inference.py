"""
This module contains the definition of the Machine Learning/static predictors.

They are used for calculating the risk of an upgrade failure.
"""

from ccx_upgrades_inference.models import UpgradeRisksPredictors, Alert, FOC


EXCLUDE_NAMESPACES = [
    "openshift-cnv",
    "openshift-compliance",
    "openshift-operators",
    "openshift-storage",
    "openshift-logging",
    "openshift-gitops",
    "openshift-pipelines",
    "openshift-image-registry",
    "openshift-marketplace",
    "openshift-redhat-marketplace",
    "openshift-distributed-tracing",
    "openshift-gitlab-runner",
    "openshift-devspaces",
    "openshift-logs",
]


class StaticPredictor:
    """This predictor uses basic filters to detect risks."""

    def filter_alert(self, alert: Alert) -> bool:
        """Return True if the alert matches any of the conditions."""
        if alert.namespace is None:
            return False

        return (
            (alert.severity == "critical")
            and (alert.namespace not in EXCLUDE_NAMESPACES)
            and (alert.namespace.startswith("openshift-"))
        )

    def filter_foc(self, foc: FOC) -> bool:
        """Return True if the FOC matches any of the conditions."""
        return foc.condition in ["Not Available", "Degraded"]

    def predict(self, risks: UpgradeRisksPredictors) -> UpgradeRisksPredictors:
        """
        Filter the `risks` with the alerts and FOCs queries.

        Return those elements that are likely to make the upgrade fail.
        """
        suspicious_alerts = [alert for alert in risks.alerts if self.filter_alert(alert)]
        suspicious_operators_conditions = [
            foc for foc in risks.operator_conditions if self.filter_foc(foc)
        ]

        if len(suspicious_alerts) < 2:
            suspicious_alerts = list()

        return UpgradeRisksPredictors(
            alerts=suspicious_alerts, operator_conditions=suspicious_operators_conditions
        )
