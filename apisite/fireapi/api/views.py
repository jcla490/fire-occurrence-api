# TODO 
# id             DONE, ValueError if not int
# source         DONE, explicit list
# country        DONE, explicit list
# name           DONE, contains
# size_ac        DONE, greater than only, ValidationError if not int or float
# start_date         this should be a greater than 
# cause          DONE, contains
# state              done, but no real error checking
# latitude       DONE
# longitude      DONE
# fire duration  SCOPING
# radius         SCOPING

from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from django.http import JsonResponse
from rest_framework.views import APIView
import time
import datetime

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

        # Filter by bbox
        bbox = request.GET.get('bbox')
        if bbox:
            bbox = [value.strip() for value in bbox.split(',')]
            if len(bbox) == 4:
                try:
                    fires = fires.filter(latitude__lte=bbox[0], latitude__gte=bbox[1]).filter(longitude__gte=bbox[2], longitude__lte=bbox[3])
                except ValidationError:
                    summary = self.api_error(-1, 'BBOX must be a comma separated string of four INT or FLOAT values.')
                    return JsonResponse(summary, safe=False)
            else:
                summary = self.api_error(-1, 'BBOX must be a comma separated string of four INT or FLOAT values.')
                return JsonResponse(summary, safe=False)

        # radius = request.GET.get('bbox')
        # if radius:
        #     r_box = [value.strip() for value in radius.split(',')]
        #     init_lat = r_box[0]
        #     init_lon = r_box[1]
        #     search_dist = r_box[2]
        #     

        query_start_date = request.GET.get('query_start_date')
        query_end_date = request.GET.get('query_end_date')
        if query_start_date or query_end_date: 
            if query_start_date and query_end_date:
                try:
                    if (len(query_start_date) == 8) and (len(query_end_date) == 8):
                        start = datetime.datetime.strptime(query_start_date, '%Y%m%d').date()
                        end = datetime.datetime.strptime(query_end_date, '%Y%m%d').date()
                        print(start, end)
                        if end >= start:
                            fires = fires.filter(start_date__range=(start, end ))
                        else:
                            summary = self.api_error(-1, 'QUERY_END_DATE must be later than QUERY_START_DATE.')
                            return JsonResponse(summary, safe=False)
                    else:
                        summary = self.api_error(-1, 'QUERY_START_DATE and QUERY_END_DATE must be INT and each have format YYYYmmdd.')
                        return JsonResponse(summary, safe=False)
                except ValueError:
                    summary = self.api_error(-1, 'QUERY_START_DATE and QUERY_END_DATE must be INT and each have format YYYYmmdd.')
                    return JsonResponse(summary, safe=False)
            else:
                summary = self.api_error(-1, 'QUERY_START_DATE and QUERY_END_DATE must be used together with each date having format YYYYmmdd.')
                return JsonResponse(summary, safe=False)

        t1 = time.time() - t0

        summary = {
                'RESPONSE_CODE': Response.status_code,
                'RESPONSE_MESSAGE': 'OK',
                'NUMBER_OF_OBJECTS': len(fires),
                'PROCESSING_TIME': str(t1 * 1000) + " ms" 
            }
        
        serializer = FiresSerializer(fires, many=True)
        return JsonResponse({'FIRES': serializer.data, 'SUMMARY': summary}, safe=False)
