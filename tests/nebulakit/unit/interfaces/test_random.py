import random as global_random

from nebulakit.interfaces import random


def test_isolated_random_state():
    random.seed_nebula_random("abc")
    r = random.random.random()
    global_random.seed("abc")
    assert random.random.random() != r


def test_seed():
    random.seed_nebula_random("abc")
    r = random.random.random()
    random.seed_nebula_random("abc")
    assert r == random.random.random()
