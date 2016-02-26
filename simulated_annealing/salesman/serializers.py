from django.contrib.auth.models import User, Group
from rest_framework import serializers
from simulated_annealing.salesman.models import City


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CityListSerializer(serializers.Serializer):
    def create(self, validated_data):
        print 'bulk creation.....'
        cities = [City(**city) for city in validated_data]
        return City.objects.bulk_create(cities)


class CitySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    lat = serializers.FloatField(required=True)
    long = serializers.FloatField(required=True)
    coords = serializers.ListField(required=False, child=serializers.FloatField(default=0.0))


    def create(self, validated_data):
        """
        Create and return a new `City` instance, given the validated data.
        """
        return City.objects.create(**validated_data)

    def update(self, city, validated_data):
        """
        Update and return an existing `City` instance, given the validated data.
        """
        city.name = validated_data.get('name', city.name)
        city.lat = validated_data.get('lat', city.lat)
        city.long = validated_data.get('long', city.long)
        city.save()

        return city

    def to_representation(self, obj):
        # get the parameter from request
        data = super(CitySerializer, self).to_representation(obj)
        # data = self.to_representation(obj)
        data['coords'] = [data['lat'], data['long']]
        del data['lat']
        del data['long']
        return data

    def to_internal_value(self, data):

        obj = super(CitySerializer, self).to_internal_value(data)

        return obj