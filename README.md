# Upgrade Risks Predictions Inference Service

This is the main reporsitory of the Upgrade Risks Predictions Inference service.

Related Jira: [CCXDEV-9718](https://issues.redhat.com/browse/CCXDEV-9718)

The idea behind this service is to provide a REST API to interact with the
predictive models that the TDI team will develop for predicting the likelihood
of an upgrade failure.

The service is deployed as part of the external data pipeline and managed via
[app-interface](https://redhat.com/service/app-interface/-/blob/master/data/services/insights/ccx-data-pipeline/deploy.yml).
You can monitor the deployment of this service in [Grafana](https://grafana.app-sre.devshift.net/d/7x_qKqbVz/ccx-upgrade-risks-predictions?orgId=1&var-datasource=crcp01ue1-prometheus&var-namespace=ccx-data-pipeline-prod).

Check the [CONTRIBUTING](CONTRIBUTING.md) for more information about how to
collaborate.

## Run it in containers

Use `docker` or `podman`:

```
docker build -t ccx-upgrades-inference . && docker run --rm -p 8000:8000 ccx-upgrades-inference
```

## Run it locally

Change to the source folder and run the app using `uvicorn`:

```
uvicorn ccx_upgrades_inference.main:app --reload
```

---

Then run some requests against the server:

```
curl -X 'GET' \
  'http://127.0.0.1:8000/upgrade-risks-prediction' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "alerts": [
    {
      "name": "APIRemovedInNextEUSReleaseInUse",
      "namespace": "openshift-kube-apiserver",
      "severity": "info"
    }
  ],
  "operator_conditions": [
    {"name": "authentication", "condition": "Degraded", "reason": "AsExpected"}
  ]
}'
```

Check the API documentation at http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc.
