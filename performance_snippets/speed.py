import timeit
from collections import deque
from queue import Queue

q1 = Queue()
q2 = deque()

N = 100_000


def f1():
    for i in range(N):
        q1.put((i, i))
        out = q1.get()


def f2():
    for i in range(N):
        q2.append((i, i))
        out = q2.pop()


print(timeit.repeat(f1, number=10, repeat=3))
print(timeit.repeat(f2, number=10, repeat=3))

# result
# [1.2680216000007931, 1.308478200022364, 1.2586785000166856]
# [0.06609149998985231, 0.06513079997966997, 0.06527149997418746]
