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
        DEFAULT_DAYS = 1
        days = DEFAULT_DAYS
        status_ok = False
        date_time_ok = False
        days_ok = False

        if 'status' in  self.request.query_params:
            try:
                val = str2bool(self.request.query_params.get('status'))
                status_ok = True
            except:
                raise ValidationError('Parametro "status" invalido')
            
            if status_ok and val in (0, 1):
                query_set = query_set.filter(status=val)
            else:
                raise ValidationError('Parametro "status" no es 0, 1, True, False')

        if 'days' in  self.request.query_params:
            val = self.request.query_params.get('days')
            try:
                val = int(val)
                days_ok = True
            except:
                val = DEFAULT_DAYS
                days_ok = False
                

            if days_ok and val>0 and val < 31:
                days = val
            else:
                days = DEFAULT_DAYS
                ValidationError('Parametro "days" invalido')


        if 'date_time' in  self.request.query_params:
            val = self.request.query_params.get('date_time')
            try: 
                date_t = dt.datetime.fromisoformat(val)
                date_time_ok=True
            except ValueError:
                date_time_ok=False

            if date_time_ok:
                final_date = date_t + dt.timedelta(days = days)
                query_set = query_set.filter(date_time__gte=date_t, date_time__lte=final_date)
            else:
                raise ValidationError('Invalid parameter "date_time"')

        return query_set.order_by('-date_time')[:1000]