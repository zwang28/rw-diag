from prometheus_api_client import PrometheusConnect

def diag(prometheus_address):
  if prometheus_address is None:
    print("\n>>skip diag prometheus because prometheus_address is not specified")
    return
  print("\n>>diag prometheus")
  prometheus = PrometheusConnect(url=f'http://{prometheus_address}')
  metric_data = prometheus.custom_query(query='all_barrier_nums')
  print(metric_data)

