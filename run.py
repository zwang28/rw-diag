import sys
sys.path.append('proto-gen')

import argparse
from diag import risingwave, prometheus, await_tree

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
                    prog='risingwave diagnose')
  parser.add_argument('--connection_string', help='https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING')
  parser.add_argument('--meta_node_address', help='host:port')
  parser.add_argument('--compute_node_address', help='host:port. The argument can be used multiple times. If none is specified, diag will try to list compute node from meta node.', action='append')
  parser.add_argument('--prometheus_address', help='host:port')
  args = parser.parse_args()

  risingwave.diag(args.connection_string)
  prometheus.diag(args.prometheus_address)
  await_tree.diag(args.meta_node_address, args.compute_node_address)
