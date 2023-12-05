import psycopg2
import diag.await_tree as await_tree

def diag(connection_string, meta_node_addr):
  print("\n>>diag risingwave")
  # conn = psycopg2.connect(connection_string)
  # cursor = conn.cursor()
  # cursor.execute("select * from rw_tables")
  # rows = cursor.fetchall()
  # for row in rows:
  #     print(row)

  await_tree.diag_await_tree(meta_node_addr)
  
