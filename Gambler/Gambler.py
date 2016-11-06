import random
import matplotlib.pyplot as plt

N, n = 10, 10000
total = 2000
A = [0] * 21
for j in range(21):
    for times in range(total):
        a, b = j, 2 * N - j
        for i in range(n):
            if a == 2 * N or a == 0:
                A[j] += 1 if a else 0
                break
            coin = random.randint(0, 1)
            if coin:
                a, b = a + 1, b - 1
            else:
                a, b = a - 1, b + 1
A = map(lambda x: x / total, A)
graph = list(zip(*enumerate(A)))
plt.plot(*graph)
plt.scatter(*graph, marker='o')
plt.xlabel('Initial number of A\'s coin(s)')
plt.ylabel('Winning rate of A')
plt.show()
