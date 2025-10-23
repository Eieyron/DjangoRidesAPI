from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Prefetch, F, Value
from django.db.models.functions import Radians, Sin, Cos, Sqrt, Power, ATan2

from Ride.models import Ride
from User.models import User
from User.serializers import UserSerializer
from RideEvent.models import RideEvent
from RideEvent.serializers import RideEventSerializer

from datetime import timedelta

class RidePagination(PageNumberPagination):
    page_size = 3           # Number of items per page
    page_size_query_param = 'page_size'  # Allow client to set page_size
    max_page_size = 100      # Max items per page

# serializer for User
class RideSerializer(serializers.HyperlinkedModelSerializer):

    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)
    todays_ride_events = RideEventSerializer(many=True, read_only=True, source='ride_events')

    rider_id = serializers.PrimaryKeyRelatedField(
        source='id_rider', queryset=User.objects.all(), write_only=True
    )
    driver_id = serializers.PrimaryKeyRelatedField(
        source='id_driver', queryset=User.objects.all(), write_only=True
    )

    distance = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Ride
        fields = [
            'url', 
            'status',
            'id_rider',
            'rider_id',
            'id_driver', 
            'driver_id', 
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
            'distance',
            'todays_ride_events'
        ]

    
    
# viewset for Ride
class RideViewSet(viewsets.ModelViewSet):
    
    queryset = Ride.objects.none()

    serializer_class = RideSerializer
    pagination_class = RidePagination

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'status', 
        'id_rider__email'
    ]

    sorting_fields = [
        'pickup_time', 
        '-pickup_time'
    ]

    # select related merges the id_rider/id_driver selection in one query
    # prefetches ALL ride events before the main query, so essentially just two (2) total queries per ride
    # creates a filter for last 24hours such that, when prefetched, only the last 24hrs are taken 
    def get_queryset(self):

        last_24h = timezone.now() - timedelta(hours=24)
        recent_events_filter = RideEvent.objects.filter(created_at__gte=last_24h)

        qs = (
            Ride.objects
            .select_related("id_rider", "id_driver")
            .prefetch_related(
                Prefetch("ride_events", queryset=recent_events_filter)
            )
        )

        sort_by_distance = False
        ref_lat = self.request.query_params.get('latitude')
        ref_lon = self.request.query_params.get('longitude')

        if ref_lat and ref_lon:

            try:
                ref_lat, ref_lon = float(ref_lat), float(ref_lon)
            except ValueError:
                return qs
            
            R = 6371.0  # radius of earth in kms
 
            qs = qs.annotate( # annotate DB with given latitude and longitude 
                dlat=Radians(Value(ref_lat) - F('pickup_latitude')),
                dlon=Radians(Value(ref_lon) - F('pickup_longitude')),
            ).annotate( # annotate db with A value
                a=Power(Sin(F('dlat') / 2), 2) +
                  Cos(Radians(F('pickup_latitude'))) *
                  Cos(Radians(Value(ref_lat))) *
                  Power(Sin(F('dlon') / 2), 2)
            ).annotate( # annotate DB with distance value
                distance=Value(2 * R) * ATan2(Sqrt(F('a')), Sqrt(1 - F('a')))
            )

            sort_by_distance = True # enable sorting by distance

        if sort_by_distance:
            temp_sorting_fields = self.sorting_fields + [
                'distance',
                '-distance'
            ]
        else:
            temp_sorting_fields = self.sorting_fields
        
        # dynamic ordering based on temp_sorting_fields
        ordering = self.request.query_params.get("order")
        if ordering:
            sortfields = {sortfield if sortfield in temp_sorting_fields else '' for sortfield in ordering.split(",")}
            sortfields.discard('')
            if sortfields:
                qs = qs.order_by(*sortfields)

        return qs
