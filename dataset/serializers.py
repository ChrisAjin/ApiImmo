from rest_framework import serializers
from .models import DataSet

class DataSetSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = '__all__'