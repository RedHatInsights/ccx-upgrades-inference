# Contributing

## Testing

All changes in the code are checked once they reach the GitHub repo. Make
sure to run `pre-commit run --all` and `pytest` before pushing any commit.

You can also run and create [BDD tests](https://github.com/RedHatInsights/insights-behavioral-spec/tree/main/features/ccx-upgrades-inference)
to make sure that the service works.

It is also important to run some tests in ephemeral to make sure your changes
work. Please, check [deployment.md](docs/deployment.md) and follow the steps
to manually test the endpoints.

## Adding new models

New models are defined in [inference.py](ccx_upgrades_inference/inference.py)
and then used in the [REST API endpoints](ccx_upgrades_inference/main.py).
