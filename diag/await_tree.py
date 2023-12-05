import re
import io
import monitor_service_pb2_grpc
import monitor_service_pb2
import grpc
import psycopg2

def diag(connection_string):
  """
  Collect trace files from all compute nodes and find the suspicious actors if any.
  """
  if connection_string is None:
    print("\n>>skip diag await tree because connection_string is not specified")
    return
  print("\n>>diag await tree")
  conn = psycopg2.connect(connection_string)
  cursor = conn.cursor()

  cursor.execute("select concat(host::varchar,':',port::varchar) from rw_worker_nodes where type='WORKER_TYPE_COMPUTE_NODE';")
  compute_node_addresses = list(map(lambda r: r[0], cursor.fetchall()))

  actor_traces = {}
  for compute_node_addr in compute_node_addresses:
    with grpc.insecure_channel(compute_node_addr) as channel:
      stub = monitor_service_pb2_grpc.MonitorServiceStub(channel)
      response = stub.StackTrace(monitor_service_pb2.StackTraceRequest())
      for actor_id, trace_text in response.actor_traces.items():
        actor_traces[actor_id] = ActorTrace(actor_id, trace_text)
  report(actor_traces)

trace_line_pattern = re.compile(r"^(?P<span_name>.*) \[!*(?P<duration>\s?[\d\.]*)(?P<unit>s|ms)\](  <== current)?$")
epoch_node_pattern = re.compile(r"^Epoch (?P<epoch>\d+)$")
output_node_pattern = re.compile(r"^(LocalOutput|RemoteOutput) \(actor (?P<actor_id>\d+)\)$")

class ActorTrace:
  def __init__(self, actor_id, trace_text):
    self.actor_id = actor_id
    self.nodes = []
    self.epoch = None
    self.epoch_duration_sec = None
    self.downstream_actor_id = None
    for trace_line in io.StringIO(trace_text):
      if len(trace_line) == 0:
        continue
      node = ActorTraceNode(trace_line.strip())
      self.add_node(node)

  def add_node(self, node):
    self.nodes.append(node)
    epoch = node.as_epoch()
    if epoch is not None:
      self.epoch = epoch
      self.epoch_duration_sec = node.duration_sec
    downstream_actor_id = node.as_output()
    if downstream_actor_id is not None:
      self.downstream_actor_id = downstream_actor_id

  def __str__(self) -> str:
    s = "ActorTrace: Actor {}, Epoch {}, Downstream Actor {}".format(self.actor_id, self.epoch, self.downstream_actor_id)
    for node in self.nodes:
      s += "\n{}".format(node)
    return s

def report(actor_traces):
  # Find the actor with earliest epoch.
  root_actor_id = None
  for actor_trace in actor_traces.values():
    if root_actor_id is None or actor_trace.epoch_duration_sec > actor_traces[root_actor_id].epoch_duration_sec:
      root_actor_id = actor_trace.actor_id
  if root_actor_id is None:
    return
  
  # Find the bottomest several trace nodes.
  bottomest_two_actor_ids = [root_actor_id]
  while actor_traces[bottomest_two_actor_ids[-1]].downstream_actor_id is not None:
    next_actor_id = actor_traces[bottomest_two_actor_ids[-1]].downstream_actor_id
    bottomest_two_actor_ids.append(next_actor_id)
    bottomest_two_actor_ids = bottomest_two_actor_ids[-2:]

  # Print
  print("\nEarliest Epoch {}, Duration {}sec".format(actor_traces[root_actor_id].epoch, actor_traces[root_actor_id].epoch_duration_sec))
  for actor_id in bottomest_two_actor_ids:
    print("\n{}".format(actor_traces[actor_id]))

class ActorTraceNode:
  def __init__(self, trace_line):
    m = re.match(trace_line_pattern, trace_line)
    self.span_name = m.group("span_name")
    self.duration = m.group("duration")
    self.unit = m.group("unit")
    if self.unit == 'ms':
      self.duration_sec = float(self.duration)/1000
    elif self.unit == 's':
      self.duration_sec = float(self.duration)
    else:
      raise Exception("unexpected unit {}".format(self.unit))

  def __str__(self) -> str:
    return "{} [{}{}]".format(self.span_name, self.duration, self.unit)
  
  def as_epoch(self):
    m = re.match(epoch_node_pattern, self.span_name)
    if m is None:
      return None
    return m.group("epoch")
  
  def as_output(self):
    m = re.match(output_node_pattern, self.span_name)
    if m is None:
      return None
    return m.group("actor_id")
  
def parse_trace_file(file_path):
  """
  Parse trace file generated by risectl trace.
  """
  header_pattern = re.compile(r"^>> Actor (?P<actor_id>\d+)$")
  from enum import Enum
  class State(Enum):
    INIT = 1,
    START = 2,
    PROCESSING = 3,
    DETACH = 4,
    END = 5,
  state = State.INIT
  actor_traces = {}
  actor_id = None
  trace_text = ""
  with open(file_path, 'r') as f:
    for line in f.readlines():
      line = line.strip()
      if state == State.INIT:
        if line == '--- Actor Traces ---':
          state = State.START
      elif state == State.START:
        m = re.match(header_pattern, line)
        if m is None:
          state = State.END
          continue
        actor_id = m.group("actor_id")
        state = State.PROCESSING
      elif state == State.PROCESSING:
        if len(line) == 0:
          actor_traces[actor_id] = ActorTrace(actor_id, trace_text)
          actor_id = None
          trace_text = ""
          state = State.START
          continue
        if line.startswith("[Detached"):
          state = State.DETACH
          continue
        trace_text += line + "\n"
      elif state == State.DETACH:
        state = State.PROCESSING
      else:
        break
  return actor_traces