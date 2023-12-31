# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: monitor_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15monitor_service.proto\x12\x0fmonitor_service\"\x13\n\x11StackTraceRequest\"\xaa\x03\n\x12StackTraceResponse\x12J\n\x0c\x61\x63tor_traces\x18\x01 \x03(\x0b\x32\x34.monitor_service.StackTraceResponse.ActorTracesEntry\x12\x46\n\nrpc_traces\x18\x02 \x03(\x0b\x32\x32.monitor_service.StackTraceResponse.RpcTracesEntry\x12]\n\x16\x63ompaction_task_traces\x18\x03 \x03(\x0b\x32=.monitor_service.StackTraceResponse.CompactionTaskTracesEntry\x1a\x32\n\x10\x41\x63torTracesEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x30\n\x0eRpcTracesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a;\n\x19\x43ompactionTaskTracesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"#\n\x10ProfilingRequest\x12\x0f\n\x07sleep_s\x18\x01 \x01(\x04\"#\n\x11ProfilingResponse\x12\x0e\n\x06result\x18\x01 \x01(\x0c\"#\n\x14HeapProfilingRequest\x12\x0b\n\x03\x64ir\x18\x01 \x01(\t\"\x17\n\x15HeapProfilingResponse\"\x1a\n\x18ListHeapProfilingRequest\"R\n\x19ListHeapProfilingResponse\x12\x0b\n\x03\x64ir\x18\x01 \x01(\t\x12\x15\n\rname_manually\x18\x02 \x03(\t\x12\x11\n\tname_auto\x18\x03 \x03(\t\"\"\n\x12\x41nalyzeHeapRequest\x12\x0c\n\x04path\x18\x01 \x01(\t\"%\n\x13\x41nalyzeHeapResponse\x12\x0e\n\x06result\x18\x01 \x01(\x0c\x32\xe1\x03\n\x0eMonitorService\x12U\n\nStackTrace\x12\".monitor_service.StackTraceRequest\x1a#.monitor_service.StackTraceResponse\x12R\n\tProfiling\x12!.monitor_service.ProfilingRequest\x1a\".monitor_service.ProfilingResponse\x12^\n\rHeapProfiling\x12%.monitor_service.HeapProfilingRequest\x1a&.monitor_service.HeapProfilingResponse\x12j\n\x11ListHeapProfiling\x12).monitor_service.ListHeapProfilingRequest\x1a*.monitor_service.ListHeapProfilingResponse\x12X\n\x0b\x41nalyzeHeap\x12#.monitor_service.AnalyzeHeapRequest\x1a$.monitor_service.AnalyzeHeapResponseB\x18\n\x14\x63om.risingwave.protoH\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'monitor_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024com.risingwave.protoH\001'
  _STACKTRACERESPONSE_ACTORTRACESENTRY._options = None
  _STACKTRACERESPONSE_ACTORTRACESENTRY._serialized_options = b'8\001'
  _STACKTRACERESPONSE_RPCTRACESENTRY._options = None
  _STACKTRACERESPONSE_RPCTRACESENTRY._serialized_options = b'8\001'
  _STACKTRACERESPONSE_COMPACTIONTASKTRACESENTRY._options = None
  _STACKTRACERESPONSE_COMPACTIONTASKTRACESENTRY._serialized_options = b'8\001'
  _globals['_STACKTRACEREQUEST']._serialized_start=42
  _globals['_STACKTRACEREQUEST']._serialized_end=61
  _globals['_STACKTRACERESPONSE']._serialized_start=64
  _globals['_STACKTRACERESPONSE']._serialized_end=490
  _globals['_STACKTRACERESPONSE_ACTORTRACESENTRY']._serialized_start=329
  _globals['_STACKTRACERESPONSE_ACTORTRACESENTRY']._serialized_end=379
  _globals['_STACKTRACERESPONSE_RPCTRACESENTRY']._serialized_start=381
  _globals['_STACKTRACERESPONSE_RPCTRACESENTRY']._serialized_end=429
  _globals['_STACKTRACERESPONSE_COMPACTIONTASKTRACESENTRY']._serialized_start=431
  _globals['_STACKTRACERESPONSE_COMPACTIONTASKTRACESENTRY']._serialized_end=490
  _globals['_PROFILINGREQUEST']._serialized_start=492
  _globals['_PROFILINGREQUEST']._serialized_end=527
  _globals['_PROFILINGRESPONSE']._serialized_start=529
  _globals['_PROFILINGRESPONSE']._serialized_end=564
  _globals['_HEAPPROFILINGREQUEST']._serialized_start=566
  _globals['_HEAPPROFILINGREQUEST']._serialized_end=601
  _globals['_HEAPPROFILINGRESPONSE']._serialized_start=603
  _globals['_HEAPPROFILINGRESPONSE']._serialized_end=626
  _globals['_LISTHEAPPROFILINGREQUEST']._serialized_start=628
  _globals['_LISTHEAPPROFILINGREQUEST']._serialized_end=654
  _globals['_LISTHEAPPROFILINGRESPONSE']._serialized_start=656
  _globals['_LISTHEAPPROFILINGRESPONSE']._serialized_end=738
  _globals['_ANALYZEHEAPREQUEST']._serialized_start=740
  _globals['_ANALYZEHEAPREQUEST']._serialized_end=774
  _globals['_ANALYZEHEAPRESPONSE']._serialized_start=776
  _globals['_ANALYZEHEAPRESPONSE']._serialized_end=813
  _globals['_MONITORSERVICE']._serialized_start=816
  _globals['_MONITORSERVICE']._serialized_end=1297
# @@protoc_insertion_point(module_scope)
