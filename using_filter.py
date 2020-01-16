# Populate the numbers.
numbers = [x for x in range(1, 51)]


# so far the best and shortest way to check prime number:
# https://www.tutorialgateway.org/python-program-to-find-prime-number/
def is_prime(num):
    count = 0
    for i in range(2, (num // 2 + 1)):
        if num % i == 0:
            count += 1
            break
    if count == 0 and num !=1:
        return True
    else:
        return False


if __name__ == '__main__':
    print("Original list of numbers:")
    print(numbers)
    # filter takes in the function and iterables: tuple, set, list as arguments.
    # the first argument only requires to pass in the function name with the ().
    # the first argument is a function that does the evaluation of True or False.
    # filter(is_prime, numbers) is the same as below:
    # for num in numbers:
    #   if is_prime(num):
    #       prime_only_numbers.append(num)
    prime_only_numbers = filter(is_prime, numbers)
    print("Prime numbers found within the original list:")
    print([prime_number for prime_number in prime_only_numbers])
    '''
The results:
Original list of numbers:
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
Prime numbers found within the original list:
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    '''