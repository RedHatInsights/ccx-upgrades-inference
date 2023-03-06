"""A set of static examples for the rest of the files."""

EXAMPLE_PREDICTORS = {
    "alerts": [
        {
            "name": "APIRemovedInNextEUSReleaseInUse",
            "namespace": "openshift-kube-apiserver",
            "severity": "critical",
        },
        {
            "name": "Other",
            "namespace": "openshift-other",
            "severity": "critical",
        },
    ],
    "operator_conditions": [
        {"name": "authentication", "condition": "Degraded", "reason": "AsExpected"}
    ],
}

EXAMPLE_ALERT = {
    "name": "APIRemovedInNextEUSReleaseInUse",
    "namespace": "openshift-kube-apiserver",
    "severity": "critical",
}

EXAMPLE_FOC = {"name": "authentication", "condition": "Degraded", "reason": "AsExpected"}
