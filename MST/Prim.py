import itertools
import tkinter as tk

root = 22
with open('/home/shantom/Desktop/第四章/{}.txt'.format(str(root))) as file:
    bs = file.readline().split()
    matrix = []
    for line in file:
        matrix.append([float(i) if i != '-1' else float('inf') for i in line.split()])

for i in range(len(matrix)):
    matrix[i][i] = 0

with open('/home/shantom/Desktop/第四章/1033pos.txt') as bs1033:
    pos = {}
    # tmp = zip(*[line.split() for line in bs1033])
    # print(len(list(tmp)))
    # pos = dict([(ID, (float(la), float(lo))) for ID, la, lo in zip(*[line.split() for line in bs1033]) if ID in bs])
    for line in bs1033:
        l = line.split()
        if l[0] in bs:
            pos[l[0]] = (float(l[1]), float(l[2]))


# print(min(pos.items(), key=lambda x: x[1][0])[1][0])
# print(min(pos.items(), key=lambda x: x[1][1])[1][1])
# print(max(pos.items(), key=lambda x: x[1][0])[1][0])
# print(max(pos.items(), key=lambda x: x[1][1])[1][1])


def prim():
    T = set()
    S = {0}
    V = set(range(len(bs)))
    while S != V:
        w = float('inf')
        i, j = 0, 0
        for x, y in itertools.product(S, V - S):
            if matrix[x][y] < w:
                i, j, w = x, y, matrix[x][y]
        T.add((i, j, w))
        S.add(j)
    suma = sum(map(lambda x: x[2], T))
    return T, suma


if __name__ == '__main__':
    tree, cost = prim()

    top = tk.Tk()
    top.title("MST")

    cvs = tk.Canvas(top, width=1000, height=1000)
    cvs.pack()

    if root == 42:
        minLa = 102.711
        minLo = 24.98292
    else:
        minLa = 102.746
        minLo = 25.039062

    for i, j in itertools.product(range(len(matrix)), range(len(matrix))):
        if matrix[i][j] != -1 and matrix[i][j] != float('inf'):
            a, b = pos[bs[i]]
            a, b = (a - minLa) * 40000 + 20, (b - minLo) * 40000 + 5
            c, d = pos[bs[j]]
            c, d = (c - minLa) * 40000 + 20, (d - minLo) * 40000 + 5
            cvs.create_line(a, b, c, d)

    for edge in tree:
        a, b = pos[bs[edge[0]]]
        a, b = (a - minLa) * 40000 + 20, (b - minLo) * 40000 + 5
        c, d = pos[bs[edge[1]]]
        c, d = (c - minLa) * 40000 + 20, (d - minLo) * 40000 + 5
        cvs.create_line(a, b, c, d, fill='red', width='3')

    top.mainloop()
    print(cost)
