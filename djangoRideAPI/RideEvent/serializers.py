from rest_framework import serializers, viewsets
from RideEvent.models import RideEvent

# serializer for User
class RideEventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RideEvent
        fields = [
            'url', 
            'id_ride',
            'description',
            'created_at'
        ]

# viewset for RideEvent
class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
