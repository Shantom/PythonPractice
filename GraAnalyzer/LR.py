import copy  # 用于深拷贝

testList = [
    # 'E->CC',
    # 'C->cC',
    # 'C->d',
    # 'E->L=R',
    # 'E->R',
    # 'L->*R',
    # 'L->i',
    # 'R->L'
    'E->E+T',
    'E->T',
    'T->T*F',
    'T->F',
    'F->(E)',
    'F->i'
]

graList = [
    'E->E+T',
    'E->E-T',
    'E->T',
    'T->T*F',
    'T->T/F',
    'T->F',
    'F->(E)',
    'F->n',
]


class Production:
    def __init__(self, non_terminal, candidate):
        self.non_terminal = non_terminal
        self.candidate = candidate

    def __repr__(self):
        return self.non_terminal + '->' + self.candidate


class Item:
    def __init__(self, non_t, left, right, tail):
        self.non_t = non_t
        self.left = 'ε' if len(left) == 0 else left
        self.right = 'ε' if len(right) == 0 else right

        self.tail = tail

    def __repr__(self):
        left = '' if self.left == 'ε' else self.left
        right = '' if self.right == 'ε' else self.right

        return '[' + self.non_t + '->' + left + '·' + right + ', ' + self.tail + ']'

    def __eq__(self, other):
        n = self.non_t == other.non_t
        l = self.left == other.left
        r = self.right == other.right
        t = self.tail == other.tail
        return n and l and r and t

    def __hash__(self):
        return hash((self.non_t, self.left, self.right, self.tail))


class Analyzer:
    def __init__(self, stList):
        self.grammar = [Production(statement[0], statement[3:])
                        for statement in stList]
        self.Vt = set()
        self.Vn = set()
        self.FIRST = {}
        self.process = False
        self.triTuple = {}
        self.CanCol = []
        self.__generateVtVn()
        self.__generateFIRST()
        self.__generateCanonicalCollection()
        self.action = [{key: '-' for key in self.Vt | {'$'}} for n in range(len(self.CanCol))]
        self.goto = [{key: '-' for key in self.Vn} for n in range(len(self.CanCol))]
        self.__generateTable()

    def printSelf(self):
        print('sentence: ', sentence)
        print(self.grammar)
        print('Vt: ', self.Vt)
        print('Vn: ', self.Vn)
        print('FIRST: ')
        for key, value in self.FIRST.items():
            print(key, value)
        self.printDFA()
        self.printTable()
        self.printResult()
        pass

    def __getCandidates(self, non_t):
        S = set()
        for production in self.grammar:
            if production.non_terminal == non_t:
                S.add(production.candidate)
        return S

    def __generateVtVn(self):
        for N in self.grammar:
            self.Vn.add(N.non_terminal)
        for N in self.grammar:
            for t in N.candidate:
                if t not in self.Vn and t != 'ε':
                    self.Vt.add(t)

    def __generateFIRST(self):
        while True:
            F_new = copy.deepcopy(self.FIRST)
            for N in sorted(list(self.Vn)):
                if N not in self.FIRST.keys():
                    self.FIRST[N] = set()
                self.FIRST[N].update(self.__FIRST(N))
            if F_new == self.FIRST:
                break

    def __FIRST(self, beta):
        setF = set()
        for symbol in beta:
            if symbol in self.Vt | {'$'}:
                setF.add(symbol)
                return setF
            setS = set()
            for statement in self.grammar:
                if statement.non_terminal == symbol:
                    candidate = statement.candidate

                    if candidate[0] == 'ε':
                        setS.add('ε')
                        continue

                    for i in range(len(candidate)):
                        if candidate[i] in self.Vt:  # 终结符 则返回
                            setS.add(candidate[i])
                            break

                        else:
                            if candidate[i] not in self.FIRST.keys():
                                self.FIRST[candidate[i]] = set()

                            setS.update(self.FIRST[candidate[i]] - set('ε'))

                            if 'ε' not in self.FIRST[candidate[i]]:
                                break
            setF.update(setS - set('ε'))
            if 'ε' not in setS:
                return setF
        setF.add('ε')
        return setF

    def __closure(self, I):
        J = copy.deepcopy(I)
        while True:
            J_new = copy.deepcopy(J)
            for item in J_new:
                if item.right[0] in self.Vn:
                    non_t = item.right[0]
                    candidates = self.__getCandidates(non_t)
                    for terminal in self.__FIRST(item.right[1:] + item.tail):
                        if terminal in self.Vt | {'$'}:
                            for candidate in candidates:
                                J.add(Item(non_t, '', candidate, terminal))
            if J == J_new:
                return J

    def __go(self, I, X):
        J = set()
        for item in I:
            if item.right[0] == X:
                newLeft = X if item.left == 'ε' else item.left + X
                J.add(Item(item.non_t, newLeft, item.right[1:], item.tail))
        return self.__closure(J)

    def __generateCanonicalCollection(self):
        I_all = [self.__closure({Item('Z', '', 'E', '$')})]  # Z supersedes E'
        while True:
            C = copy.deepcopy(I_all)
            index_I = 0  # I0? I1?...I5?...
            for I in C:
                for X in self.Vn | self.Vt:
                    J = self.__go(I, X)
                    if len(J) != 0:
                        try:
                            index_J = I_all.index(J)
                            self.triTuple[(index_I, X)] = index_J
                        except:
                            I_all.append(J)
                            self.triTuple[index_I, X] = len(I_all) - 1

                index_I += 1

            if C == I_all:
                self.CanCol = C
                break

    def __generateTable(self):
        C = self.CanCol
        for i in range(len(C)):
            for item in C[i]:
                if Item('Z', 'E', '', '$') == item:  # 接收
                    self.action[i]['$'] = 'acc'
                elif item.right == 'ε':  # 归约
                    candidate = item.left + item.right
                    if candidate != 'ε':
                        candidate = candidate.replace('ε', '')
                    prod = Production(item.non_t, candidate)
                    self.action[i][item.tail] = ('r', prod)
                elif item.right[0] in self.Vt:
                    j = self.triTuple[(i, item.right[0])]
                    self.action[i][item.right[0]] = ('s', j)

            for key, value in self.triTuple.items():
                if key[0] == i and key[1] in self.Vn:
                    self.goto[i][key[1]] = value

    def printTable(self):
        values = sorted(self.action[0].keys())
        print("%-15s" % "action", end='')
        for terminal in values:
            print("%-15s" % terminal, end='')
        print('')
        for n in range(len(self.CanCol)):
            print("%-15s" % n, end='')
            for value in values:
                print("%-15s" % str(self.action[n][value]), end='')
            print('')

        values = sorted(self.goto[0].keys())
        print("%-15s" % "goto", end='')
        for terminal in values:
            print("%-15s" % terminal, end='')
        print('')
        for n in range(len(self.CanCol)):
            print("%-15s" % n, end='')
            for value in values:
                print("%-15s" % str(self.goto[n][value]), end='')
            print('')

    def analyze(self, sentence):
        stack = ['0']
        buffer = list(sentence) + ['$']
        ip = 0
        process = []
        while True:
            S = int(stack[-1])
            a = buffer[ip]
            act = self.action[S][a]
            if act == '-':
                self.process = False
                return
            elif act == 'acc':
                process.append((''.join(stack), ''.join(buffer[ip:]), 'acc'))
                self.process = process
                return
            elif act[0] == 's':
                process.append((''.join(stack), ''.join(buffer[ip:]), 'Shift %s' % act[1]))
                stack.append(a)
                stack.append(str(act[1]))
                ip += 1
            elif act[0] == 'r':
                process.append((''.join(stack), ''.join(buffer[ip:]), 'Reduced by %s' % act[1]))
                length = len(act[1].candidate) if act[1].candidate != 'ε' else 0
                for i in range(2 * length):
                    stack.pop()
                Z = int(stack[-1])
                A = act[1].non_terminal
                stack.append(A)
                stack.append(str(self.triTuple[(Z, A)]))

    def printResult(self):

        if self.process is False:
            print("this sentence is not acceptable")
        else:
            print("\nprocess table")
            print("%-30s%-30s%-30s" % ("stack", "input", "output"))
            for step in self.process:
                print("%-30s%-30s%-30s" % (step[0], step[1], step[2]))

    def printDFA(self):
        print('\nDFA:')

        print('Edges: ')
        keys = sorted(list(self.triTuple.keys()))
        new_index = 0
        for key in keys:
            index = new_index
            new_index = key[0]
            if index != new_index:
                print('')
            print('%-17s' % (str(key) + ':' + str(self.triTuple[key])), end='')
        print('')

        print('CanCol: ')
        for i in range(len(self.CanCol)):
            print('I_%d: ' % i, self.CanCol[i])
        print('')



sentence = '(n)+((n-n)+n*n)'
# A = Analyzer(testList)
A = Analyzer(graList)
A.analyze(sentence)
A.printSelf()
