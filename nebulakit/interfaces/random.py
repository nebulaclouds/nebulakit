import random as _random

random = _random.Random()
"""
An instance of the global random number generator used by nebulakit.  Nebulakit maintains it's own random instance
to ensure that calls to random.seed(...) do not affect the pseudo-random behavior of nebulakit. This random should be
used by nebulakit components in all cases where random.random would have been used. Components who want additional
protections for their random number generator might also maintain their own separate random instance.
"""


def seed_nebula_random(seed):
    """
    If one wants to influence the pseudo-random behavior of nebulakit, this function can be used to seed the nebulakit
    generator. It is not recommended that this be done as lack of entropy between jobs can result in overwriting data
    created at random locations.

    Currently, this is used by nebulakit to create entropy in low entropy situations (such as Array Jobs) where the job
    index can be used as a seed to ensure sibling jobs do not have random collisions.
    :param Union[Text,int,bytes] seed:
    """
    global random
    random = _random.Random(seed)
