from django.shortcuts import render
from confluent_kafka import Producer
import json
from rest_framework.views import APIView
from .serializers import UserDataSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

producer = Producer({'bootstrap.servers': 'localhost:9092'})


def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Message produced: {msg.value()}")


class UserDataView(APIView):
    def post(self, request:Request, *args, **kwargs):
        serializer = UserDataSerializer(request.data)
        producer.produce('userData', value=json.dumps(serializer.data), callback=acked)
        producer.poll(1)
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
    
