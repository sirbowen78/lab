import functools

'''
Another example on decorator.
On many websites the decorator tutorials use functions that do not return values.
Hence I am experimenting myself on how to use decorators with functions that return values.
The decorator portion was inspired by flask_jwt's jwt_required decorator.
'''


# so far the best and shortest way to check prime number:
# https://www.tutorialgateway.org/python-program-to-find-prime-number/
def is_prime(num):
    count = 0
    for i in range(2, (num // 2 + 1)):
        if num % i == 0:
            count += 1
            break
    if count == 0 and num != 1:
        return True
    else:
        return False


# evaluate prime numbers
# to be decorated on functions that require this function.
def confirm_prime(fn):
    # functools.wraps preserve the original function reference which it was called.
    @functools.wraps(fn)
    # Evaluate the return value of the function to test if it is a prime number.
    # I was inspired by the jwt_required decorator which uses _jwt_required within the decorator.
    def wrapper(num):
        test_num = fn(num)
        if is_prime(test_num):
            return test_num
    return wrapper


@confirm_prime
def find_prime(num):
    return num


if __name__ == '__main__':
    found = False
    from random import randrange
    while not found:
        # randomly test each number between 1 and 99.
        p = randrange(1, 100)
        test = find_prime(p)
        if test:
            found = True
    print(test)
