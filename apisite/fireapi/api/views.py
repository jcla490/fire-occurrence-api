from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from django.http import JsonResponse
from rest_framework.views import APIView
import time

from fireapi.models import Fires
from fireapi.api.serializers import FiresSerializer


class ListFires(APIView):
    def api_error(self, code, message):
        summary = {
            'SUMMARY':{
                'RESPONSE_CODE': code,
                'RESPONSE_MESSAGE': message,
                'NUMBER_OF_OBJECTS': 0,
                'PROCESSING_TIME': 0
            }
        }
        return summary

    def get(self, request):
        t0 = time.time()

        # All fire objects
        fires = Fires.objects.all()

        # Filter by country
        country = request.GET.get('country')
        if country:
            country = country.upper()
            if country in ['USA', 'CANADA']:
                fires = fires.filter(country=country)
            else:
                summary = self.api_error(-1, '{} is not a valid country'.format(country))
                return JsonResponse(summary, safe=False)

        # Filter by state
        state = request.GET.get('state')
        if state:
            state = state.upper()
            fires = fires.filter(state=state)

        # Filter by name
        name = request.GET.get('name')
        if name:
            name = name.upper()
            fires = fires.filter(name__contains=name)

        # Filter by cause
        cause = request.GET.get('cause')
        if cause:
            cause = cause.upper()
            fires = fires.filter(cause__contains=cause)

        # Filter by size
        size_ac = request.GET.get('size_ac')
        if size_ac:
            try:
                fires = fires.filter(size_ac__gte=size_ac)
            except ValidationError:
                summary = self.api_error(-1, 'SIZE must be of type INT or FLOAT.')
                return JsonResponse(summary, safe=False)

        # Filter by source
        source = request.GET.get('source')
        if source:
            source = source.upper()
            if source in ['FPA-FOD']:
                fires = fires.filter(source=source)
            else:
                summary = self.api_error(-1, '{} is not a valid source system.'.format(source))
                return JsonResponse(summary, safe=False)

        # Filter by id
        id = request.GET.get('id')
        if id:
            try:
                fires = fires.filter(id=id)
            except ValueError:
                summary = self.api_error(-1, 'ID must be of type INT.')
                return JsonResponse(summary, safe=False)


       # TODO 
       # id             done, ValueError if not int
       # source         done, explicit list
       # country        DONE, explicit list
       # name           DONE, contains
       # size_ac        DONE, greater than only, ValidationError if not int or float
       # start_date     this should be a greater than 
       # end_date       should this exist?
       # cause          DONE, contains
       # state          done, but no real error checking
       # latitude       should be a bounding box
       # longitude      should be a bounding box

        t1 = time.time() - t0

        summary = {
                'RESPONSE_CODE': Response.status_code,
                'RESPONSE_MESSAGE': 'OK',
                'NUMBER_OF_OBJECTS': len(fires),
                'PROCESSING_TIME': str(t1 * 1000) + " ms" 
            }
        
        serializer = FiresSerializer(fires, many=True)
        return JsonResponse({'FIRES': serializer.data, 'SUMMARY': summary}, safe=False)
