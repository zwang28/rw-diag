test_name=${TEST_NAME:-"t0.txt"}
python3 -c '''
import sys
sys.path.append('proto-gen')
from diag.await_tree import parse_trace_file, report
actor_traces = parse_trace_file("tests/data/{}".format(sys.argv[1]))
report(actor_traces)
# for actor_id, trace in actor_traces.items():
#   print(actor_id, trace)
''' ${test_name}