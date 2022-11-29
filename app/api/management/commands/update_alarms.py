from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from api.models import Alarm, ScadaPoint, Priority
import datetime as dt

import datetime as dt

class Command(BaseCommand):
    help = "Updates the alarm table"

    def handle(self, *args, **kwargs):
        self.stdout.write("\nUpdate starting.......\n")
        sps = ScadaPoint.objects.values_list('scada_pid', flat=True)
        scada_connected = False
        try:
            scada_cursor = connections['scada'].cursor()
            scada_connected = True
        except OperationalError as e:
            self.stdout.write(e)
            scada_connected = False
            self.stdout.write("NO HAY CONEXION CON LA BASE DE DATOS!!")

        if scada_connected:
            query = f"exec GetAlarms"
            scada_cursor.execute(query)
            filtered_data = [row for row in scada_cursor.fetchall() if row[0] in sps]
            alrm_datalist = []
            for row in filtered_data:
                sp = ScadaPoint.objects.get(scada_pid=row[0])
                dtime = row[1] - dt.timedelta(hours=6)
                dtime = dtime.replace(microsecond=0)    # to avoid rounding errors
                val = 0 if row[2] == sp.out_value else 1
                prior = Priority.objects.get(level=row[3])
                
                if not Alarm.objects.filter(scada_point=sp, date_time=dtime):
                    alrm = Alarm(scada_point=sp, priority=prior, date_time=dtime, status=val)
                    alrm_datalist.append(alrm)
            Alarm.objects.bulk_create(alrm_datalist)
            self.stdout.write(f'{dt.datetime.now()} - {len(alrm_datalist)} elements added...')
            #Alarm.objects.all().delete()

