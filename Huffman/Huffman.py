import heapq

# with open('/home/shantom/Desktop/附件2.哈夫曼编码输入文本.txt') as file:
#     str_1 = file.readline()


str_1='iroutqwemvdcibwgemhxzxvcmbakjlrthoiuerfobskdnv'
freq = {}  # 频率字典

for ch in range(26):
    freq[chr(ch + ord('a'))] = str_1.count(chr(ch + ord('a')))
for ch in range(26):
    freq[chr(ch + ord('A'))] = str_1.count(chr(ch + ord('A')))
freq['#'] = str_1.count('#')
freq['/'] = str_1.count('/')

tree = list(freq.items())
for k, v in tree:
    if v == 0:
        del freq[k]
freqDic = freq.copy()

tree = sorted(freq.items(), key=lambda x: x[1])  # 哈夫曼树的频率列表

originFreq = tree

originCh = []
for x in tree:
    originCh.append(x[0])

parents = {}  # 父节点
for ch in tree:
    parents[ch[0]] = 0


def allZero():
    for i in range(len(tree) - 1):
        if parents[tree[i][0]] == 0:
            return True
    return False


j = len(tree)
while allZero():
    twoMins = heapq.nsmallest(2, tree, key=lambda x: (x[1] if parents[x[0]] == 0 else 0x3f3f3f3f))
    # print(twoMins)
    parents[twoMins[0][0]] = -j
    parents[twoMins[1][0]] = +j
    newChs = twoMins[0][0] + twoMins[1][0]
    newFreq = freq[twoMins[0][0]] + freq[twoMins[1][0]]
    freq[newChs] = newFreq
    parents[newChs] = 0
    tree.append((newChs, newFreq))
    j += 1


def encode(ch):
    code = ''
    while parents[ch]:
        code += ('1' if parents[ch] > 0 else '0')
        # print(tree[abs(parents[ch])])
        ch = tree[abs(parents[ch])][0]
    return code[::-1]


codeDic = {}
for ch in originCh:
    codeDic[ch] = encode(ch)

# 1. {a, b, c,..,x, y, z, #}中各成员在文本中的出现频率和哈夫曼编码
print('出现频率:')
print(freqDic)
print('哈夫曼编码')
print(codeDic)
# 2. 采用哈夫曼编码、定长编码，输入文本需要的存储比特数
huffNum = 0
for ch in freqDic.keys():
    huffNum += freqDic[ch] * len(codeDic[ch])
print('哈夫曼编码:' + str(huffNum))
print('定长编码' + str(len(str_1) * 5))
