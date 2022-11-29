from rest_framework import viewsets, status
from .models import Alarm, ScadaPoint
from .serializers import AlarmSerializer, ScadaPointSerializer
from rest_framework.decorators import action 
##from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .services import str2bool
import datetime as dt


class ScadaPointViewSet(viewsets.ModelViewSet):
    queryset = ScadaPoint.objects.all()
    serializer_class = ScadaPointSerializer
    http_method_names = ['get']


class AlarmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    http_method_names = ['get']

    def get_queryset(self):
        query_set = self.queryset
        if 'status' in  self.request.query_params:
            val = str2bool(self.request.query_params.get('status'))
            if val in (0, 1):
                query_set = query_set.filter(status=val)
            else:
                raise ValidationError('Invalid parameter "status"')
        
        if 'date_time' in  self.request.query_params:
            val = self.request.query_params.get('date_time')
            is_date=False
            try: 
                date_t = dt.datetime.fromisoformat(val)
                is_date=True
            except ValueError:
                is_date=False

            if is_date:
                query_set = query_set.filter(date_time__gte=date_t)
            else:
                raise ValidationError('Invalid parameter "date_time"')

        return query_set[:50]