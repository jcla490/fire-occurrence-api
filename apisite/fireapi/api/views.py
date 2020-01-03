# TODO 3 January 2020
# fire duration  SCOPING
# radius         SCOPING
# multiple queries in one param??

import time
import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from fireapi.models import Fires
from fireapi.api.serializers import FiresSerializer


class ListFires(APIView):
    def api_error(self, code, message):
        """
        (func) api_error:
            parameters:
                code: A numeric value representing the failure code. -1 for query parameter formatting issues 
                message: A brief error message to display to the user
            returns: 
                A JSON object specifiying the error code and message
        """

        summary = {
            'SUMMARY':{
                'RESPONSE_CODE': code,
                'RESPONSE_MESSAGE': message,
                'NUMBER_OF_OBJECTS': 0,
                'PROCESSING_TIME': 0
            }
        }

        return summary

    def get(self, request, **kwargs):

        t0 = time.time()
        
        # Hold up wait a minute put a little country in it
        q_params = dict(self.request.query_params)
        if any(x in q_params for x in ['country_iso', 'country', 'COUNTRY', 'COUNTRY_ISO']) == False:
            summary = self.api_error(-1, 'Either COUNTRY_ISO or COUNTRY is required for a valid query.')
            return JsonResponse(summary, safe=False)
        
        # Check for blank parameters
        for param in q_params:
            if q_params[param] == ['']:
                summary = self.api_error(-1, '{} cannot be left blank.'.format(param.upper()))
                return JsonResponse(summary, safe=False)    

        # All fire objects
        fires = Fires.objects.all()

        ###############################################################################################################################################################################
        # COUNTRY QUERY PARAM                                                                                                                                                         #
        ###############################################################################################################################################################################      
        country = request.GET.get('country')
        if country:
            country = country.upper()
            if country in ['UNITED-STATES', 'CANADA', 'MEXICO', 'CHILE']:
                fires = fires.filter(country=country)
            else:
                summary = self.api_error(-1, '{} is not a valid COUNTRY.'.format(country))
                return JsonResponse(summary, safe=False)


        ###############################################################################################################################################################################
        # COUNTRY_ISO QUERY PARAM                                                                                                                                                     #
        ###############################################################################################################################################################################      
        country_iso = request.GET.get('country_iso')
        if country_iso:
            country_iso = country_iso.upper()
            if country_iso in ['US', 'CA', 'MX', 'CL']:
                fires = fires.filter(country_iso=country_iso)
            else:
                summary = self.api_error(-1, '{} is not a valid COUNTRY_ISO.'.format(country_iso))
                return JsonResponse(summary, safe=False)
            

        ###############################################################################################################################################################################
        # STATE QUERY PARAM                                                                                                                                                           #
        ###############################################################################################################################################################################      
        state = request.GET.get('state')
        if state:
            state = state.upper()
            fires = fires.filter(state=state)


        ###############################################################################################################################################################################
        # STATE_ISO QUERY PARAM                                                                                                                                                       #
        ###############################################################################################################################################################################      
        state_iso = request.GET.get('state_iso')
        if state_iso:
            state_iso = state_iso.upper()
            fires = fires.filter(state_iso=state_iso)


        ###############################################################################################################################################################################
        # NAME QUERY PARAM                                                                                                                                                            #
        ###############################################################################################################################################################################      
        name = request.GET.get('name')
        if name:
            name = name.upper()
            fires = fires.filter(name__contains=name)


        ###############################################################################################################################################################################
        # CAUSE QUERY PARAM                                                                                                                                                           #
        ###############################################################################################################################################################################      
        cause = request.GET.get('cause')
        if cause:
            cause = cause.upper()
            if cause in ['HUMAN', 'NATURAL', 'UNKNOWN']:
                fires = fires.filter(cause=cause)
            else:
                summary = self.api_error(-1, '{} is not a valid CAUSE (Only HUMAN, NATURAL, or UNKNOWN can be specified. Leave blank for all causes).'.format(cause))
                return JsonResponse(summary, safe=False)


        ###############################################################################################################################################################################
        # SIZE_AC QUERY PARAM                                                                                                                                                         #
        ###############################################################################################################################################################################      
        size_ac = request.GET.get('size_ac')
        # Greater than one value
        if size_ac and len(size_ac.split('|')) <  2: 
            try:
                fires = fires.filter(size_ac__gte=size_ac)
            except ValidationError:
                summary = self.api_error(-1, 'SIZE_AC must be of type INT or FLOAT.')
                return JsonResponse(summary, safe=False)
        # Between two values
        elif size_ac and len(size_ac.split('|')) == 2:
            size_list = [x.strip() for x in size_ac.split('|')]
            try:
                if float(size_list[1]) < float(size_list[0]):
                    summary = self.api_error(-1, 'The second SIZE_AC value must be greater than or equal to the first.')
                    return JsonResponse(summary, safe=False)
            except ValueError:
                summary = self.api_error(-1, 'SIZE_AC must be of type INT or FLOAT.')
                return JsonResponse(summary, safe=False)
            try:
                fires = fires.filter(size_ac__gte=size_list[0], size_ac__lte=size_list[1])
            except ValidationError:
                summary = self.api_error(-1, 'SIZE_AC must be of type INT or FLOAT.')
                return JsonResponse(summary, safe=False)
        # Too many values
        elif size_ac and len(size_ac.split('|')) > 2:
            summary = self.api_error(-1, 'SIZE_AC must either one number (for results greater than SIZE_AC) or a pipe-separated string of two numbers (for results between two sizes).')
            return JsonResponse(summary, safe=False)


        ###############################################################################################################################################################################
        # SIZE_HA QUERY PARAM                                                                                                                                                         #
        ###############################################################################################################################################################################      
        size_ha = request.GET.get('size_ha')
        if size_ac and size_ha:
            summary = self.api_error(-1, 'Specify either SIZE_AC or SIZE_HA in your query, not both.')
            return JsonResponse(summary, safe=False)

        # Greater than one value
        if size_ha and len(size_ha.split('|')) <  2: 
            try:
                fires = fires.filter(size_ha__gte=size_ha)
            except ValidationError:
                summary = self.api_error(-1, 'SIZE_HA must be of type INT or FLOAT.')
                return JsonResponse(summary, safe=False)
        # Between two values
        elif size_ha and len(size_ha.split('|')) == 2:
            size_list = [x.strip() for x in size_ha.split('|')]
            try:
                if float(size_list[1]) < float(size_list[0]):
                    summary = self.api_error(-1, 'The second SIZE_HA value must be greater than or equal to the first.')
                    return JsonResponse(summary, safe=False)
            except ValueError:
                summary = self.api_error(-1, 'SIZE_HA must be of type INT or FLOAT.')
                return JsonResponse(summary, safe=False)
            try:
                fires = fires.filter(size_ha__gte=size_list[0], size_ha__lte=size_list[1])
            except ValidationError:
                summary = self.api_error(-1, 'SIZE_HA must be of type INT or FLOAT.')
                return JsonResponse(summary, safe=False)
        # Too many values
        elif size_ha and len(size_ha.split('|')) > 2:
            summary = self.api_error(-1, 'SIZE_HA must either one number (for results greater than SIZE_HA) or a pipe-separated string of two numbers (for results between two sizes).')
            return JsonResponse(summary, safe=False)

        ###############################################################################################################################################################################
        # DOY QUERY PARAM                                                                                                                                                         #
        ###############################################################################################################################################################################      
        doy = request.GET.get('doy')
        # Greater than one value
        if doy and len(doy.split('|')) <  2: 
            try:
                fires = fires.filter(fire_doy=doy)
            except ValidationError:
                summary = self.api_error(-1, 'DOY must be of type INT.')
                return JsonResponse(summary, safe=False)
        # Between two values
        elif doy and len(doy.split('|')) == 2:
            doy_list = [x.strip() for x in doy.split('|')]
            try:
                if float(doy_list[1]) < float(doy_list[0]):
                    summary = self.api_error(-1, 'The second DOY value must be greater than or equal to the first.')
                    return JsonResponse(summary, safe=False)
            except ValueError:
                summary = self.api_error(-1, 'DOY must be of type INT.')
                return JsonResponse(summary, safe=False)
            try:
                fires = fires.filter(fire_doy__gte=doy_list[0], fire_doy__lte=doy_list[1])
            except ValidationError:
                summary = self.api_error(-1, 'DOY must be of type INT.')
                return JsonResponse(summary, safe=False)
        # Too many values
        elif doy and len(doy.split('|')) > 2:
            summary = self.api_error(-1, 'DOY must either one number (for results equal to DOY) or a pipe-separated string of two numbers (for results between two DOYs).')
            return JsonResponse(summary, safe=False)

        ###############################################################################################################################################################################
        # YEAR QUERY PARAM                                                                                                                                                         #
        ###############################################################################################################################################################################      
        year = request.GET.get('year')
        # Greater than one value
        if year and len(year.split('|')) <  2: 
            try:
                fires = fires.filter(fire_year=year)
            except ValidationError:
                summary = self.api_error(-1, 'YEAR must be of type INT.')
                return JsonResponse(summary, safe=False)
        # Between two values
        elif year and len(year.split('|')) == 2:
            year_list = [x.strip() for x in year.split('|')]
            try:
                if year_list[1] < year_list[0]:
                    summary = self.api_error(-1, 'The second YEAR value must be greater than or equal to the first.')
                    return JsonResponse(summary, safe=False)
            except ValueError:
                summary = self.api_error(-1, 'YEAR must be of type INT.')
                return JsonResponse(summary, safe=False)
            try:
                fires = fires.filter(fire_year__gte=year_list[0], fire_year__lte=year_list[1])
            except ValidationError:
                summary = self.api_error(-1, 'YEAR must be of type INT.')
                return JsonResponse(summary, safe=False)
        # Too many values
        elif year and len(year.split('|')) > 2:
            summary = self.api_error(-1, 'YEAR must either one number (for results equal to YEAR) or a pipe-separated string of two numbers (for results between two YEARS).')
            return JsonResponse(summary, safe=False)


        ###############################################################################################################################################################################
        # MONTH QUERY PARAM                                                                                                                                                         #
        ###############################################################################################################################################################################      
        month = request.GET.get('month')
        # Greater than one value
        if month and len(month.split('|')) <  2: 
            try:
                fires = fires.filter(fire_month=month)
            except ValidationError:
                summary = self.api_error(-1, 'MONTH must be of type INT.')
                return JsonResponse(summary, safe=False)
        # Between two values
        elif month and len(month.split('|')) == 2:
            month_list = [x.strip() for x in month.split('|')]
            try:
                if month_list[1] < month_list[0]:
                    summary = self.api_error(-1, 'The second MONTH value must be greater than or equal to the first.')
                    return JsonResponse(summary, safe=False)
            except ValueError:
                summary = self.api_error(-1, 'MONTH must be of type INT.')
                return JsonResponse(summary, safe=False)
            try:
                fires = fires.filter(fire_month__gte=month_list[0], fire_month__lte=month_list[1])
            except ValidationError:
                summary = self.api_error(-1, 'MONTH must be of type INT.')
                return JsonResponse(summary, safe=False)
        # Too many values
        elif month and len(month.split('|')) > 2:
            summary = self.api_error(-1, 'MONTH must either one number (for results equal to MONTH) or a pipe-separated string of two numbers (for queries between two MONTHS).')
            return JsonResponse(summary, safe=False)


        ###############################################################################################################################################################################
        # ID QUERY PARAM                                                                                                                                                              #
        ###############################################################################################################################################################################      
        id = request.GET.get('id')
        if id:
            try:
                fires = fires.filter(id=id)
            except ValueError:
                summary = self.api_error(-1, 'ID must be of type INT.')
                return JsonResponse(summary, safe=False)



        ###############################################################################################################################################################################
        # BBOX QUERY PARAM                                                                                                                                                            #
        ###############################################################################################################################################################################      
        bbox = request.GET.get('bbox')
        if bbox:
            bbox = [value.strip() for value in bbox.split('|')]
            if len(bbox) == 4:
                try:
                    fires = fires.filter(latitude__lte=bbox[0], latitude__gte=bbox[1]).filter(longitude__gte=bbox[2], longitude__lte=bbox[3])
                except ValidationError:
                    summary = self.api_error(-1, 'BBOX must be a pipe separated string of four INT or FLOAT values.')
                    return JsonResponse(summary, safe=False)
            else:
                summary = self.api_error(-1, 'BBOX must be a pipe separated string of four INT or FLOAT values.')
                return JsonResponse(summary, safe=False)


        # radius = request.GET.get('bbox')
        # if radius:
        #     r_box = [value.strip() for value in radius.split(',')]
        #     init_lat = r_box[0]
        #     init_lon = r_box[1]
        #     search_dist = r_box[2]
        #     

        ###############################################################################################################################################################################
        # QUERY START AND END DATES                                                                                                                                                           #
        ###############################################################################################################################################################################      
        query_start_date = request.GET.get('query_start_date')
        query_end_date = request.GET.get('query_end_date')
        if query_start_date or query_end_date: 
            if query_start_date and query_end_date:
                try:
                    if (len(query_start_date) == 8) and (len(query_end_date) == 8):
                        start = datetime.datetime.strptime(query_start_date, '%Y-%m-%d').date()
                        end = datetime.datetime.strptime(query_end_date, '%Y-%m-%d').date()
                        if end >= start:
                            fires = fires.filter(start_date__range=(start, end ))
                        else:
                            summary = self.api_error(-1, 'QUERY_END_DATE must be later than QUERY_START_DATE.')
                            return JsonResponse(summary, safe=False)
                    else:
                        summary = self.api_error(-1, 'QUERY_START_DATE and QUERY_END_DATE must each have format YYYY-mm-dd.')
                        return JsonResponse(summary, safe=False)
                except ValueError:
                    summary = self.api_error(-1, 'QUERY_START_DATE and QUERY_END_DATE must be INT and each have format YYYY-mm-dd.')
                    return JsonResponse(summary, safe=False)
            else:
                summary = self.api_error(-1, 'QUERY_START_DATE and QUERY_END_DATE must be used together with each date having format YYYY-mm-dd.')
                return JsonResponse(summary, safe=False)

        # Processing time
        t1 = time.time() - t0

        # Build summary dict
        summary = {
                'RESPONSE_CODE': Response.status_code,
                'RESPONSE_MESSAGE': 'OK',
                'NUMBER_OF_OBJECTS': len(fires),
                'PROCESSING_TIME': str(t1 * 1000) + " ms" 
            }
        
        # Serialize the data and return the JSON response
        serializer = FiresSerializer(fires, many=True)
        return JsonResponse({'FIRES': serializer.data, 'SUMMARY': summary}, safe=False)
