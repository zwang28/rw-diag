from prometheus_api_client import PrometheusConnect

def diag(prometheus_address):
  if prometheus_address is None:
    print("\n>>skip diag prometheus because prometheus_address is not specified")
    return
  print("\n>>diag prometheus")
  prometheus = PrometheusConnect(url=f'http://{prometheus_address}')

  metric_data = prometheus.custom_query(query='topk(3, rate(stream_source_output_rows_counts[10m]))')
  print(f"\nSource Throughput(rows/s)\n{metric_data}")

  metric_data = prometheus.custom_query(query='topk(3, sum(rate(stream_mview_input_row_count[10m])) by (table_id) * on(table_id) group_left(table_name) group(table_info) by (table_id, table_name))')
  print(f"\nMaterialized View Throughput(rows/s)\n{metric_data}")

  metric_data = prometheus.custom_query(query='topk(3, histogram_quantile(0.9, sum(rate(stream_join_matched_join_keys_bucket[10m])) by (le, fragment_id, table_id)))')
  print(f"\nJoin Executor Matched Rows\n{metric_data}")

  metric_data = prometheus.custom_query(query='topk(3, histogram_quantile(0.5, sum(rate(state_store_get_duration_bucket[10m])) by (le, table_id)))')
  print(f"\nRead Duration - Get\n{metric_data}")

  metric_data = prometheus.custom_query(query='topk(3, histogram_quantile(0.5, sum(rate(state_store_iter_init_duration_bucket[10m])) by (le, table_id)))')
  print(f"\nRead Duration - Iter\n{metric_data}")