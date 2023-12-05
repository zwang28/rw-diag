import argparse
from diag import risingwave, prometheus

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
                    prog='risingwave diagnose')
  parser.add_argument('--connection_string')
  parser.add_argument('--meta_node_addr')
  args = parser.parse_args()

  risingwave.diag(args.connection_string, args.meta_node_addr)
  prometheus.diag()
