# Upgrade Failure Predictions Inference Service

This is the main reporsitory of the Upgrade Failure Predictions Inference service.

Related Jira: [CCXDEV-9718](https://issues.redhat.com/browse/CCXDEV-9718)

## Run it locally

Change to the source folder and run the app using `uvicorn`:

```
cd src
uvicorn main:app --reload
```

Then run some requests against the server:

```
curl -X 'GET' \
  'http://127.0.0.1:8000/upgrade-failure-prediction' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "risks": [
    "foca|machine-config|Available",
    "foc|version|Failing|ClusterOperatorDegraded",
    "alert|openshift-cluster-version|ClusterOperatorDown",
    "foc|machine-config|Degraded|MachineConfigDaemonFailed",
    "alert|openshift-sdn|TargetDown|sdn",
    "alert|openshift-cluster-version|ClusterOperatorDegraded",
    "alert|kube-system|TargetDown|kubelet"
  ]
}'
```

Check the API documentation at http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc.
