with open('/home/shantom/Desktop/第四章/22.txt') as file:
    bs = file.readline().split()
    matrix = []
    for line in file:
        matrix.append([float(i) if i != '-1' else float('inf') for i in line.split()])

for i in range(len(matrix)):
    matrix[i][i] = 0


def dijkstra(bsid):
    v = bs.index(bsid)
    n = len(matrix)
    dis = [0] * n
    final = [False] * n
    pre = [v] * n
    final[v] = True  # v or 0
    for i in range(n):
        dis[i] = matrix[v][i]

    k = v
    for j in range(n):
        mini = float('inf')
        for i in range(n):
            if dis[i] < mini and not final[i]:
                mini = dis[i]
                k = i
        final[k] = True
        for i in range(n):
            if dis[k] + matrix[k][i] < dis[i]:
                dis[i] = dis[k] + matrix[k][i]
                pre[i] = k
    return dis, pre


def shortest(start, end, D, P):
    s = bs.index(start)
    e = bs.index(end)
    route = []
    i = e
    route.append(i + 1)
    while i != s:
        i = P[i]
        route.append(i + 1)
    route.reverse()
    print(*route, sep='->', end='\t距离为:')
    print(D[e])


# shortest('567443', '33109')
for a in bs:
    D, P = dijkstra('567443')
    shortest('567443', a, D, P)
