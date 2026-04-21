"""Tests for demo_project.core module."""

from demo_project.core import calculate_sum, say_hello


def test_say_hello_default():
    assert say_hello() == "Hello, World!"


def test_say_hello_with_name():
    assert say_hello("Alice") == "Hello, Alice!"


def test_calculate_sum_integers():
    assert calculate_sum(1, 2) == 3


def test_calculate_sum_floats():
    assert calculate_sum(1.5, 2.5) == 4.0
