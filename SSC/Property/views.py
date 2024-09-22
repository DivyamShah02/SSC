from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import json
import time


class PropertyDetailFormViewSet(viewsets.ViewSet):
    def list(self, request):
        return render(request, 'property_detail_form.html')


