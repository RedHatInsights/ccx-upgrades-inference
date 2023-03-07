# Deployment

## Testing the local version of the service in an ephemeral cluster

**VPN needed!**

1. Install `bonfire`
```
pip install crc-bonfire
```

2. Log into ephemeral cluster

```
oc login --token=${TOKEN} --server=<ephemeral cluster>
```

3. Reserve a namespace
```
export NAMESPACE=$(bonfire namespace reserve)
```

4. Deploy the inference service
```
bonfire deploy -c deploy/test.yaml -n $NAMESPACE ccx-data-pipeline
```

5. Check the pod is deployed

```
POD=`oc --namespace $NAMESPACE get pods | grep ccx-upgrades-inference | awk '{print $1}'`
oc --namespace $NAMESPACE logs $POD
```

6. Make a request to the inference service

Launch a debugging pod with curl installed:
```
oc --namespace $NAMESPACE run curl -i --tty --rm \
    --image=docker.io/curlimages/curl:latest -- sh
```

Wait for the command prompt. Then run some requests:

```
curl -s -X 'GET' \
    'ccx-upgrades-inference-svc:8000/upgrade-risks-prediction' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d @- << EOF 
{"alerts":[
        {"name": "APIRemovedInNextEUSReleaseInUse","namespace": "openshift-kube-apiserver","severity": "critical"},
        {"name": "Other","namespace": "openshift-other","severity": "critical"}
    ],
    "operator_conditions": [
        {"name": "authentication", "condition": "Degraded", "reason": "AsExpected"}
    ]
}
EOF
```

You should see the response. Exit the container using `CTRL+D` or `exit`. The 
pod is automatically deleted.

6. Delete the namespace

```
bonfire namespace release $NAMESPACE 
```