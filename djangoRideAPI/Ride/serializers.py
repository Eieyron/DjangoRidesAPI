from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from Ride.models import Ride

class RidePagination(PageNumberPagination):
    page_size = 3           # Number of items per page
    page_size_query_param = 'page_size'  # Allow client to set page_size
    max_page_size = 100      # Max items per page

# serializer for User
class RideSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ride
        fields = [
            'url', 
            'status',
            'id_rider',
            'id_driver', 
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
        ]
    
# viewset for Ride
class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()

    serializer_class = RideSerializer
    pagination_class = RidePagination

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'id_rider__email']
