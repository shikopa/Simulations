import collections

from django.contrib.auth.models import Group, User
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response


from simulated_annealing.salesman.models import City
from simulated_annealing.salesman.serializers import CitySerializer, GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """
    queryset = City.objects.all().order_by('-name')
    serializer_class = CitySerializer


@api_view(['GET', 'POST'])
def city_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # clear the DB of Cities
        City.objects.all().delete()
        updated_data = []  # List of cities
        for city, coords in request.data[0].items():
            updated_data.append({'name': city, 'lat': coords[0], 'long': coords[1]})
        serializer = CitySerializer(data=updated_data, many=True)
        if serializer.is_valid():
            serializer.save()

            # Anneal the data, and get the best tour
            tour, distance = City.simulate_annealing()
            # Rotate the tour to New York City
            index = -1 * tour.index('New York City')
            tour = collections.deque(tour)
            tour.rotate(index)


            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'items': list(tour)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def city_detail(request, pk, format=None):
    """
    Retrieve, update or delete a City.
    """
    try:
        city = City.objects.get(pk=pk)
    except City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CitySerializer(city)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CitySerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)