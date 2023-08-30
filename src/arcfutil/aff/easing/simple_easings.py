# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from math import sin
from math import cos
from math import pi


def linear(percent):
    return percent


def sine(percent):
    return sin(percent * (pi / 2))


def cosine(percent):
    return cos((percent * (pi / 2)) + pi) + 1
