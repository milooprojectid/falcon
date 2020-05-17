from __future__ import print_function
import logging
import grpc
import modules.grpc.protobuf.storm_pb2 as storm_pb2
import modules.grpc.protobuf.storm_pb2_grpc as storm_pb2_grpc


class GrpcClient:
    def __init__(self, connectionUrl):
        channel = grpc.insecure_channel(connectionUrl)
        self.stub = storm_pb2_grpc.StormServiceStub(channel)

    def summarize(self, content):
        try:
            response = self.stub.Summarize(
                storm_pb2.SummarizeRequest(text=content))

            if response.summary == "":
                raise ValueError('response is empty')

            return response.summary
        except:
            return 'Gagal memuat konten atau link berita.'
