import sys
sys.path.append('proto-gen')

import argparse
from diag import risingwave, prometheus, await_tree

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
                    prog='risingwave diagnose')
  parser.add_argument('--connection_string', help='https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING')
  parser.add_argument('--prometheus_address', help='host:port')
  parser.add_argument('--promql_filters', default='job!=""')
  args = parser.parse_args()

  risingwave.diag(args.connection_string)
  prometheus.diag(args.prometheus_address, args.promql_filters)
  await_tree.diag(args.connection_string)
