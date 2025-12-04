from rest_framework import serializers
from .models import CloudTable

class CloudTableSerializers(serializers.ModelSerializer):
    class Meta:
        model=CloudTable
        fields="__all__"