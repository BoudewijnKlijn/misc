"""Zip is consistently slower than looping over single array.
Checking for is None inside loop has variable and less of an impact."""

import random
import timeit

N = 100_000
nums = [random.randint(0, N) for _ in range(N)]


def f1():
    prev = None
    for num in nums:
        if prev is None:
            prev = num
            continue

        # do something with prev and num
        ans = prev + num

        prev = num


def f2():
    prev = nums[0]
    for num in nums[1:]:
        # do something with prev and num
        ans = prev + num

        prev = num


def f3():
    for prev, num in zip(nums, nums[1:]):
        # do something with prev and num
        ans = prev + num


funcs = [f1, f2, f3]
for func in funcs:
    print(timeit.repeat(func, number=100, repeat=3))

# [0.2791113999555819, 0.29807309998432174, 0.28844749997369945]
# [0.28759740001987666, 0.2649204999906942, 0.2628606000216678]
# [0.3614696000004187, 0.35164890001760796, 0.35239329998148605]
