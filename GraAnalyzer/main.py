list = ['E->TP',
        'P->XP',
        'P->ε',
        'X->+T',
        'X->-T',
        'T->FQ',
        'Q->YQ',
        'Q->ε',
        'Y->*F',
        'Y->/F',
        'F->(E)',
        'F->n'
        ]

sentence = '(n)*n'


class production:
    def __init__(self, non_terminal, candidate):
        self.non_terminal = non_terminal
        self.candidate = candidate

    def __repr__(self):
        return self.non_terminal + '->' + self.candidate


class Analyzer:
    def __init__(self, stList):
        self.grammar = [production(statement[0], statement[3:])
                        for statement in stList]

        self.Vt = set()
        self.Vn = set()
        self.FIRST = {}
        self.FOLLOW = {}
        self.__generateVtVn()
        self.__generateFIRST()
        self.__generateFOLLOW()
        # self.FIRST['+E'] = self.__FIRST('+E')
        self.__generateTable()

    def print(self):
        # print([(st.non_terminal, st.candidate) for st in self.grammar])
        print('Vt', self.Vt)
        print('Vn', self.Vn)
        print('FIRST', self.FIRST)
        # print('FOLLOW', self.FOLLOW)
        # print(self.grammar)
        # print(self.table)
        pass

    def __generateVtVn(self):
        for N in self.grammar:
            self.Vn.add(N.non_terminal)
        for N in self.grammar:
            for t in N.candidate:
                if t not in self.Vn and t != 'ε':
                    self.Vt.add(t)

    def __generateFIRST(self):
        for N in self.Vn:
            if N not in self.FIRST.keys():
                self.FIRST[N] = self.__FIRST(N)

    def __FIRST(self, beta):  # 有问题(对于句子)
        setF = set()
        for symbol in beta:
            if symbol in self.Vt:
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
                                self.FIRST[candidate[i]] = self.__FIRST(candidate[i])

                            setS.update(self.FIRST[candidate[i]] - set('ε'))

                            if 'ε' not in self.FIRST[candidate[i]]:
                                break
            setF.update(setS-set('ε'))
            if 'ε' not in setS:
                return setF
        setF.add('ε')
        return setF

    def __generateFOLLOW(self):
        for N in self.Vn:
            if N not in self.FOLLOW.keys():
                self.FOLLOW[N] = self.__FOLLOW(N)

    def __FOLLOW(self, non_t):
        setF = set()
        if non_t == 'E':
            setF.add('$')

        for statement in self.grammar:  # 从生成式中找non_t
            candidate = statement.candidate
            index = candidate.find(non_t)
            if index > -1:  # 找到non_t
                flag = True  # 标记需不需要找上一层的FOLLOW
                for i in candidate[index + 1:]:
                    if i in self.Vt:
                        setF.add(i)
                        flag = False
                        break
                    else:
                        setF.update(self.FIRST[i] - {'ε'})
                        if 'ε' not in self.FIRST[i]:
                            flag = False
                            break
                if flag is True:  # 读到了该生成式的最后一个符号,而且全为'ε',就要找上一层的FOLLOW
                    if statement.non_terminal != non_t:
                        if statement.non_terminal not in self.FOLLOW.keys():
                            self.FOLLOW[statement.non_terminal] = self.__FOLLOW(statement.non_terminal)

                        setF.update(self.FOLLOW[statement.non_terminal])

        return setF

    def __generateTable(self):

        table = {}
        for n in self.Vn:
            table[n] = {}
            for t in self.Vt:
                table[n][t] = 0

        for statement in self.grammar:
            for terminal in self.__FIRST(statement.candidate):
                if terminal != 'ε':
                    table[statement.non_terminal][terminal] = statement
            if 'ε' in self.FIRST[statement.non_terminal]:
                for terminal in self.FOLLOW[statement.non_terminal]:
                    table[statement.non_terminal][terminal] = statement
        self.table = table

    def analyze(self, sentence):
        induction = []
        sentence += '$'
        stack = ['$', 'E']
        ip = 0
        while True:
            X = stack.pop()
            a = sentence[ip]
            if X in self.Vt or X == '$':
                if X == a:
                    ip += 1
                else:
                    return False
            else:
                if self.table[X][a] == 0:
                    return False
                rcandidate = self.table[X][a].candidate[::-1]
                for i in rcandidate:
                    if i != 'ε':
                        stack.append(i)
                induction.append(self.table[X][a])
            if X == '$':
                break
        return induction


A = Analyzer(list)
print(A.analyze(sentence))

A.print()
