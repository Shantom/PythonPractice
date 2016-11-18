# -*- coding: UTF-8 -*-
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

sentence = '(n*n)+(n/(n-n)'  # 假设前提在词法分析之后,所有无符号数已经被分析为代号n


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
        self.table = {}
        self.process = False
        self.__generateVtVn()
        self.__generateFIRST()
        self.__generateFOLLOW()
        self.__generateTable()

    def printSelf(self):
        print('sentence: ', sentence)
        print('Vt: ', self.Vt)
        print('Vn: ', self.Vn)
        print('FIRST: ')
        for key, value in self.FIRST.items():
            print(key, value)
        print('FOLLOW: ')
        for key, value in self.FOLLOW.items():
            print(key, value)
        self.printTable()
        self.printResult()
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

    def __FIRST(self, beta):
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
                                self.FIRST[candidate[i]] = self.__FIRST(
                                    candidate[i])

                            setS.update(self.FIRST[candidate[i]] - set('ε'))

                            if 'ε' not in self.FIRST[candidate[i]]:
                                break
            setF.update(setS - set('ε'))
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
                            self.FOLLOW[statement.non_terminal] = self.__FOLLOW(
                                statement.non_terminal)

                        setF.update(self.FOLLOW[statement.non_terminal])

        return setF

    def __generateTable(self):

        table = {}
        for n in self.Vn:
            table[n] = {}
            for t in self.Vt | {'$'}:
                table[n][t] = '-'

        for statement in self.grammar:
            for terminal in self.__FIRST(statement.candidate):
                if terminal != 'ε':
                    table[statement.non_terminal][terminal] = statement
            if 'ε' in self.FIRST[statement.non_terminal]:
                for terminal in self.FOLLOW[statement.non_terminal]:
                    table[statement.non_terminal][terminal] = statement
        self.table = table

    def analyze(self, sentence):
        process = []
        sentence += '$'
        stack = ['$', 'E']
        ip = 0
        while True:
            X = stack[-1]
            a = sentence[ip]
            if X in self.Vt or X == '$':
                if X == a:
                    process.append([''.join(stack), sentence[ip:], '-'])
                    ip += 1
                    X = stack.pop()
                else:
                    self.process = False
                    return
            else:
                if self.table[X][a] == '-':
                    self.process = False
                    return
                rcandidate = self.table[X][a].candidate[::-1]
                process.append(
                    [''.join(stack), sentence[ip:], self.table[X][a]])
                X = stack.pop()
                for i in rcandidate:
                    if i != 'ε':
                        stack.append(i)
            if X == '$':
                break
        self.process = process

    def printTable(self):
        values = sorted(self.table['E'].keys())
        print("%-8s" % "table", end='')
        for terminal in values:
            print("%-8s" % terminal, end='')
        print('')
        for key, value in self.table.items():
            print("%-8s" % key, end='')
            for non_t in sorted(value.keys()):
                print("%-8s" % value[non_t], end='')
            print('')

    def printResult(self):

        if self.process is False:
            print("this sentence is not acceptable")
        else:
            print("\nprocess table")
            print("%-20s%-20s%-20s" % ("stack", "input", "output"))
            for step in self.process:
                print("%-20s%-20s%-20s" % (step[0], step[1], step[2]))

A = Analyzer(list)
A.analyze(sentence)
A.printSelf()
