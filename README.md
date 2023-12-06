## Description
This repository contains scripts to collect diagnostic data for RisingWave, from various sources, including RisingWave and Prometheus.

The diagnostic data includes:
- Potential slow actors, inferred from the await-tree of compute nodes.
- Basic cluster info queried from rw_catalog.
- Noteworthy metrics queried from Prometheus.

## Usage
```shell
python run.py --connection_string "host=localhost port=4566 dbname=dev user=root" --prometheus_url "http://127.0.0.1:9500" --promql_filters "namespace='cluster_namespace'"
```
The output should be like:
[report.txt](https://github.com/zwang28/rw-diag/files/13575427/report.txt)

**Note that if RisingWave is deployed on Kubernetes, the script above should be run in the same cluster**. Otherwise, it may fail due to the inability to resolve the domain names of worker nodes.

Both `connection_string` and `prometheus_address` are optional. Corresponding diagnostic data won't be collected if it is not specified.

`promql_filters` should be correctly set to filter out metrics that don't belong to this cluster in the same Prometheus server.
