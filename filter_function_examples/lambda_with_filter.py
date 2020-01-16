numbers = [n for n in range(1, 51)]

print("Original numbers:")
print(numbers)

# you can also pass lamda function into filter as first argument.
# the lamda function evaluations if x is divisble by 2 to determine if it is even number.
only_even_numbers = filter(lambda x: x % 2 == 0, numbers)
print("Get all even numbers from original numbers:")
print([even_number for even_number in only_even_numbers])