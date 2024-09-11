from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .serializers import PropertyInquirySerializer
from .models import PropertyInquiry
import json

class PropertyInquiryViewSet(viewsets.ViewSet):
    def list(self, request):
        return render(request, 'property_inquiry_form.html')

    def create(self, request):
        data = request.data
        for key in data.keys():
            if type(data[key]) == list:
                data[key] = ', '.join(data[key])

        serializer = PropertyInquirySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({"success":True,"message": "Inquiry submitted successfully!", "client_id":serializer.data['id']}, status=status.HTTP_201_CREATED)
        return Response({"success":False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

