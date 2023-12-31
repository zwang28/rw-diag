import sys
sys.path.append('proto-gen')

import argparse
from diag import risingwave, prometheus, await_tree

def ignore_exception(f):
  try:
    f()
  except:
    pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
                    prog='risingwave diagnose')
  parser.add_argument('--connection_string', help='https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING')
  parser.add_argument('--prometheus_url')
  parser.add_argument('--promql_filters', default='job!=""')
  args = parser.parse_args()

  ignore_exception(risingwave.diag(args.connection_string))
  ignore_exception(await_tree.diag(args.connection_string))
  ignore_exception(prometheus.diag(args.prometheus_url, args.promql_filters))
