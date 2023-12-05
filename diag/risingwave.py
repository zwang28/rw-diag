import psycopg2
import json
import sys

def diag(connection_string):
  """
  Query rw_catalog and (TODO)raise alarm..
  """
  if connection_string is None:
    print("\n>>skip diag risingwave because connection_string is not specified")
    return

  print("\n>>diag risingwave")
  conn = psycopg2.connect(connection_string)
  cursor = conn.cursor()

  num_tables = query_count(cursor, "select count(*) from rw_tables;")
  num_mvs = query_count(cursor, "select count(*) from rw_materialized_views;")
  num_sources = query_count(cursor, "select count(*) from rw_sources;")
  num_sinks = query_count(cursor, "select count(*) from rw_sinks;")
  num_frags = query_count(cursor, "select count(*) from rw_fragments;")
  num_actors = query_count(cursor, "select count(*) from rw_actors;")
  print("\nbasic info")
  print("number of actors: {}".format(num_actors))
  print("number of tables: {}".format(num_tables))
  print("number of materialized views: {}".format(num_mvs))
  print("number of sources: {}".format(num_sources))
  print("number of sinks: {}".format(num_sinks))
  print("number of fragments: {}".format(num_frags))

  print("\nworker nodes")
  query_and_print_all_rows(cursor, "select * from rw_worker_nodes;")

  print("\nactor distribution on worker")
  query_and_print_all_rows(cursor, '''
SELECT worker_id, 
       count(*)
FROM   rw_actors t1
       JOIN rw_parallel_units t2
         ON t1.parallel_unit_id = t2.id
GROUP  BY t2.worker_id;
                           ''')

  print("\nlatest barriers completions")
  query_and_print_all_rows(cursor, "select * except (unique_id,event_type) from rw_event_logs where event_type='BARRIER_COMPLETE' limit 10;")

  print("\nlatest barrier failures")
  query_and_print_all_rows(cursor, "select * except (unique_id,event_type) from rw_event_logs where event_type in ('INJECT_BARRIER_FAIL', 'COLLECT_BARRIER_FAIL') limit 3;")

  print("\nlatest panics")
  query_and_print_all_rows(cursor, "select * except (unique_id,event_type) from rw_event_logs where event_type='WORKER_NODE_PANIC' limit 3;")

  print("\nstorage backpressure")
  query_and_print_all_rows(cursor, "select id, compaction_config from rw_hummock_compaction_group_configs where active_write_limit is not null order by id;")

  print("\nSSTable highest delete ratio")
  query_and_print_all_rows(cursor, '''
WITH sst_delete_ratio AS
(
   SELECT sstable_id,
          compaction_group_id,
          level_id,
          sub_level_id,
          range_tombstone_count * 1.0 / total_key_count AS range_delete_ratio,
    stale_key_count * 1.0 / total_key_count AS delete_ratio
   FROM   rw_catalog.rw_hummock_sstables
)
SELECT   *
FROM     sst_delete_ratio
ORDER BY delete_ratio DESC
LIMIT 10;
                           ''')

def query_and_print_all_rows(cursor, sql):
  try:
    query_and_print_all_rows_impl(cursor, sql)
  except Exception as e:
    print(f"failed: {sql}. {e}", file=sys.stderr)
    pass

def query_and_print_all_rows_impl(cursor, sql):
  from datetime import datetime
  from decimal import Decimal
  class SimpleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)
  cursor.execute(sql)
  rows = cursor.fetchall()
  if len(rows) == 0:
     print("N/A")
     return
  column_names = [desc[0] for desc in cursor.description]
  column_widths = [max(len(str(row[i])) for row in rows + [column_names]) for i in range(len(column_names))]
  header = "  ".join(f"{name:{width}}" for name, width in zip(column_names, column_widths))
  print(header)
  for row in rows:
    row_values = "  ".join(f"{json.dumps(value, cls=SimpleEncoder):{width}}" if value is not None else "" for value, width in zip(row, column_widths))
    print(row_values)

def query_count(cursor, sql):
  try:
     query_count_impl(cursor, sql)
  except Exception as e:
    print(f"failed: {sql}. {e}", file=sys.stderr)
    pass

def query_count_impl(cursor, sql):
  cursor.execute(sql)
  count = cursor.fetchone()[0]
  return int(count)
