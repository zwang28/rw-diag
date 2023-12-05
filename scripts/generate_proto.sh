proto_path=${RW_PROTO_PATH:-"./proto"}
find ${proto_path} -name "*.proto"  -type f | xargs -I{} python -m grpc_tools.protoc -I ${proto_path} --python_out=proto-gen --grpc_python_out=proto-gen {}