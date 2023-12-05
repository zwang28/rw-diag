## Description
This repository contains scripts to collect diagnostic data for RisingWave, from various sources, including RisingWave and Prometheus.

The diagnostic data includes:
- Potential slow actors, inferred from the await-tree of compute nodes.
- Basic cluster info queried from rw_catalog.
- Noteworthy metrics queried from Prometheus.

## Example
```shell
python run.py --connection_string "host=localhost port=4566 dbname=dev user=root" --prometheus_address "127.0.0.1:9500"
```

**Note that if RisingWave is deployed on Kubernetes, the script above should be run in the same cluster**. Otherwise, it may fail due to the inability to resolve the domain names of worker nodes.

Both `connection_string` and `prometheus_address` are optional. Corresponding diagnostic data won't be collected if it is not specified.