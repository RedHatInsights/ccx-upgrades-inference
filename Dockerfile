FROM registry.access.redhat.com/ubi8/python-39:1-97.1675807508

WORKDIR /ccx-upgrades-inference

COPY . /ccx-upgrades-inference

USER 0

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install .

USER 1001

EXPOSE 8000

CMD ["uvicorn", "ccx_upgrades_inference.main:app", "--host=0.0.0.0", "--port=8000"]
