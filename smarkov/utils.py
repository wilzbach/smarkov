# encoding: utf-8
#
# Simple Markov chain manipulation
# Copyright (C) 2015 Sebastian Wilzbach
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import deque
import random

__author__ = "greenify"
__copyright__ = "Copyright 2016, greenify"


def get_suffixes(arr):
    """ Returns all possible suffixes of an array (lazy evaluated)
    Args:
        arr: input array
    Returns:
        Array of all possible suffixes (as tuples)
    """
    arr = tuple(arr)
    return [arr]
    return (arr[i:] for i in range(len(arr)))


def prefilled_buffer(start_element, length=-1):
    """ Provides an efficient circular buffer with a limited size
    Will fill the entire buffer with the start elements
    Args:
        start_element: element that will be used to fill the buffer
        length: total length of the buffer
    Returns:
        limited size buffer
    """
    assert length > 0
    return deque([start_element] * length, maxlen=length)


def weighted_choice(item_probabilities):
    """ Randomly choses an item according to defined weights
    Args:
        item_probabilities: list of (item, probability)-tuples
    Returns:
        random item according to the given weights
    """
    probability_sum = sum(x[1] for x in item_probabilities)
    assert probability_sum > 0
    random_value = random.random() * probability_sum
    summed_probability = 0
    for item, value in item_probabilities:
        summed_probability += value
        if summed_probability > random_value:
            return item
