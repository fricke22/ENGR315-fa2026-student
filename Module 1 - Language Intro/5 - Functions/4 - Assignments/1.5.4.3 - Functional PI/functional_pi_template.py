import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    a = 1
    b = 1 / math.sqrt(2)
    t = 1 / 4
    p = 1

    approximation = 0

    while abs(math.pi - approximation) >= abs(target_error):
        old = a

        a = (a + b) / 2
        b = math.sqrt(old * b)
        t = t - p * (old -a) ** 2
        p = 2 * p
        approximation = ((a + b) ** 2) / (4 * t)

    # change this so an actual value is returned
    return approximation




desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
