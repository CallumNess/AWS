# returns the lesser of two given numbers if both are even, but returns the greater if a number is odd
def lesser_of_two_evens(a, b):

    if a % 2 == 0 and b % 2 == 0:
        return min(a, b)
    else:
        return max(a, b)


lesser_of_two_evens(4, 6)

# Given two integers, return True if the sum of the integers is 20 or if one of the integers is 20. If not, return False


def makes_twenty(num1, num2):

    if num1 == 20 or num1 + num2 == 20:
        return True
    else:
        return False
