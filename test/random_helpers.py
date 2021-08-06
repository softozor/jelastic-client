import random
import string


def random_env_name():
    return "test-" + "".join(random.choice(string.digits) for i in range(7))
