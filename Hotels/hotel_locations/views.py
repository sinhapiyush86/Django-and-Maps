from django.shortcuts import render
from .models import  Details_Table
import json
from .serializers import DataSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

# function for loading maps.

def maps(request):
    #getting all data as objects
    obj = list(Details_Table.objects.all())
    #serialising object fro json conversion
    serialized_data = DataSerializer(obj, many=True)
    t = json.dumps(serialized_data.data)
    return render(request, "index.html", {'data': t})


#API class to insert data
class Data_Upload(APIView):
    def get(self,request):
        data = Details_Table.objects.all()
        serialized_data = DataSerializer(data, many=True)
        return Response(serialized_data.data)


    def post(self,request):
        data = request.data
        serializer = DataSerializer(data=data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response("Failed to get data")
