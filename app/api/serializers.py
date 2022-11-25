from rest_framework import serializers
from .models import Alarm, ScadaPoint

class ScadaPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScadaPoint
        fields = ('id', 'scada_pid', 'name', 'description')

class AlarmSerializer(serializers.ModelSerializer):
    plant = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    prior = serializers.SerializerMethodField()
    def get_plant(self, instance):
        return(str(instance.scada_point.generator.plant))
    def get_unit(self, instance):
        return(str(instance.scada_point.generator))
    def get_prior(self, instance):
        return(str(instance.priority))    
    class Meta:
        model = Alarm
        fields = ('plant', 'unit', 'date_time', 'status', 'prior')
        #fields = ('scada_point', 'priority', 'date_time', 'status')

