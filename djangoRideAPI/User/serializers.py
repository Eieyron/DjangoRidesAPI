from rest_framework import serializers, viewsets
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
User = get_user_model()

# serializer for User
class UserSerializer(serializers.HyperlinkedModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = [
            'url', 
            'username',
            'first_name',
            'last_name', 
            'email',
            'role',
            'phone',
            'password'
        ]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

# viewset for User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
