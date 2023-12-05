from prometheus_api_client import PrometheusConnect

def diag(prometheus_url, promql_filters):
  """
  Query prometheus and (TODO)raise alarm.
  """

  # TODO handle auth

  if prometheus_url is None:
    print("\n>>skip diag prometheus because prometheus_url is not specified")
    return
  print("\n>>diag prometheus")
  prometheus = PrometheusConnect(url=prometheus_url)

  metric_data = prometheus.custom_query(query=f'topk(3, rate(stream_source_output_rows_counts{{{promql_filters}}}[10m]))')
  print(f"\nSource Throughput(rows/s)\n{metric_data}")

  metric_data = prometheus.custom_query(query=f'topk(3, sum(rate(stream_mview_input_row_count{{{promql_filters}}}[10m])) by (table_id) * on(table_id) group_left(table_name) group(table_info) by (table_id, table_name))')
  print(f"\nMaterialized View Throughput(rows/s)\n{metric_data}")

  metric_data = prometheus.custom_query(query=f'topk(3, histogram_quantile(0.9, sum(rate(stream_join_matched_join_keys_bucket{{{promql_filters}}}[10m])) by (le, fragment_id, table_id)))')
  print(f"\nJoin Executor Matched Rows\n{metric_data}")

  metric_data = prometheus.custom_query(query=f'topk(3, histogram_quantile(0.5, sum(rate(state_store_get_duration_bucket{{{promql_filters}}}[10m])) by (le, table_id)))')
  print(f"\nHummock Read Duration - Get\n{metric_data}")

  metric_data = prometheus.custom_query(query=f'topk(3, histogram_quantile(0.5, sum(rate(state_store_iter_init_duration_bucket{{{promql_filters}}}[10m])) by (le, table_id)))')
  print(f"\nHummock Read Duration - Iter\n{metric_data}")

  metric_data = prometheus.custom_query(query=f'topk(3, sum(rate(storage_commit_write_throughput{{{promql_filters}}}[10m])) by (table_id))')
  print(f"\nCommit Flush Bytes\n{metric_data}")

  metric_data = prometheus.custom_query(query=f'sum(rate(object_store_read_bytes{{{promql_filters},job=~"compute|compactor"}}[10m]))by(job, instance)')
  print(f"\nObject Store Read Throughput Bytes\n{metric_data}")

  metric_data = prometheus.custom_query(query=f'sum(rate(object_store_write_bytes{{{promql_filters},job=~"compute|compactor"}}[10m]))by(job, instance)')
  print(f"\nObject Store Write Throughput Bytes\n{metric_data}")

  metric_data = prometheus.custom_query(query=f'sum(rate(object_store_operation_latency_count{{{promql_filters},job=~"compute|compactor", type!~"streaming_upload_write_bytes|streaming_read_read_bytes|streaming_read"}}[10m])) by (le, type, job, instance)')
  print(f"\nObject Store Operation Rate\n{metric_data}")

  metric_data = prometheus.custom_query(query=f'histogram_quantile(0.5, sum(rate(object_store_operation_latency_bucket{{{promql_filters},job=~"compute|compactor", type!~"streaming_upload_write_bytes|streaming_read"}}[10m])) by (le, type, job, instance))')
  print(f"\nObject Store Operation Duration\n{metric_data}")