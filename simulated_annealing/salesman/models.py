from __future__ import unicode_literals

import copy
import math
import random

from collections import OrderedDict
from django.db import models
from geopy.distance import great_circle
from random import randint


class City(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, default='')
    lat = models.FloatField(blank=False, default=0.0)
    long = models.FloatField(blank=False, default=0.0)

    REQUIRED_FIELDS = ['name', 'lat', 'long']

    @property
    def coords(self):
        return self.lat, self.long

    @classmethod
    def build_distance_map(cls):
        """
        Returns: A list of Cities with all the distance between cities calculated
        """

        cities = cls.objects.all()

        for city in cities:
            city.distances = OrderedDict()
            for c in cities:
                if city.id == c.id:
                    distance = 0
                else:
                    distance = great_circle(city.coords, c.coords).miles
                city.distances[c.name] = distance

        return cities

    @classmethod
    def calculate_tour_distance(cls, tour, distance_map):
        """
        Args:
            tour: The tour
            distance_map: a map of city to city distances
        Returns: The total distance in the given tour, using the distance_map
        """

        distance = 0.00
        for city in tour:
            if tour.index(city) == len(tour) - 1:
                # Last city in tour, next city is the first city in the tour
                next_city = tour[0]
            else:
                next_city = tour[tour.index(city) + 1]
            distance += distance_map[city][next_city]

        # # Calculate distance from last city to first city
        # first_city = tour[0]
        # last_city = tour[-1]
        # distance += distance_map[last_city][first_city]

        return distance

    @classmethod
    def randomize_tour(cls, tour):
        """
        Args:
            tour: The tour

        Returns: A the tour by randomly changing the positions of two cities
        """

        index_of_first_city = 0
        index_of_second_city = 0
        # We need to make sure that the cities to be swapped in the tour have different indexes
        while index_of_first_city == index_of_second_city:
            index_of_first_city = randint(0, len(tour) - 1)
            index_of_second_city = randint(0, len(tour) - 1)

        # Swap the cities using tour[index_of_city]
        tour[index_of_first_city], tour[index_of_second_city] = tour[index_of_second_city], tour[index_of_first_city]

        return tour

    @classmethod
    def acceptance_probability(cls, current_distance, new_distance, temperature):
        """

        Args:
            current_distance (): The distance of the current tour
            new_distance (): The distance of the new tour
            temperature (): The current temperature

        Returns:
            True: If the new tour is acceptable

        """
        if new_distance < current_distance:
            return 1.0
        else:
            return math.exp((current_distance - new_distance)/temperature)

    @classmethod
    def simulate_annealing(cls):
        """

        Returns: The Best Tour

        """
        print 'annealing data'
        cities = cls.build_distance_map()
        distance_map = OrderedDict()
        current_tour = []
        temperature = 40000
        cooling_rate = 0.001

        for city in cities:
            distance_map[city.name] = city.distances
            current_tour.append(city.name)  # Create the first tour

        random.shuffle(current_tour)  # We need to shuffle the initial tour
        current_distance = cls.calculate_tour_distance(current_tour, distance_map)
        print 'current_distance : ', current_distance
        best_tour = copy.deepcopy(current_tour)  # Initialize the best tour
        best_distance = current_distance
        print 'best_distance : ', best_distance
        while temperature > 1:

            new_tour = cls.randomize_tour(current_tour)
            new_distance = cls.calculate_tour_distance(new_tour, distance_map)

            # If the new distance < old distance, use this new tour
            # If the Acceptance Probability is greater than the random number we use the new tour as the current tour
            if cls.acceptance_probability(current_distance, new_distance, temperature) > random.random():
                current_tour = copy.deepcopy(new_tour)
                current_distance = new_distance

                # If the current tour has a shorter distance than the best distance, the current tour is the best tour
                if current_distance < best_distance:
                    best_tour = copy.deepcopy(current_tour)
                    best_distance = current_distance

            # Apply the cooling rate to the temperature
            temperature *= (1 - cooling_rate)

        return best_tour, best_distance

    class Meta:
        ordering = ('created',)
