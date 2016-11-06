import re

reserve = {"auto", "break", "case", "char", "const", "continue",
           "default", "do", "double", "else", "enum", "extern",
           "float", "for", "goto", "if", "int", "long", "register",
           "return", "short", "signed", "sizeof", "static",
           "struct", "switch", "typedef", "union", "unsigned",
           "void", "volatile", "while"}  # 关键字
table = set()  # 标识符
lexmebegin = 0
forward = 0

with open('/home/shantom/Desktop/test1.txt') as file:
    code = file.read()


def iskey(token):
    """judge whether token is a keyword"""
    # token = ''.join(token)
    if token in reserve:
        return True
    else:
        return False


def table_insert(token):
    """insert token to the identifiers table"""
    table.add(token)


def retract():
    """retract 'forward' by 1"""
    global forward
    forward -= 1


def get_nbc(code):
    """push 'forward' to next non-space char"""
    global forward
    if forward > len(code) - 1:
        return 1
    while code[forward].isspace():
        forward += 1
        if forward > len(code) - 1:
            return 1
    return 0


def analyzer(code):
    global forward, lexmebegin
    if 1 == get_nbc(code):
        return
    C = code[forward]
    forward += 1
    while forward <= len(code) - 1:
        if C.isalpha() or C == '_':  # 字母
            while C.isalpha() or C.isdigit() or C == '_':
                C = code[forward]
                forward += 1
            retract()
            token = code[lexmebegin:forward]
            if iskey(token):
                yield 'keyword', token
            else:
                table_insert(token)
                yield 'identifier', token

            if 1 == get_nbc(code):
                return
            lexmebegin = forward
            C = code[forward]
            forward += 1

        elif C.isdigit():  # 数字
            p = re.compile("([0-9])+(\.([0-9])+)?(e(\+|-)?([0-9])+)?")
            token = p.match(code[forward - 1:]).group()
            forward += len(token) - 1
            if '.' in token:
                yield 'float', float(token)
            else:
                yield 'integer', int(token)

            if 1 == get_nbc(code):
                return
            lexmebegin = forward
            C = code[forward]
            forward += 1

        elif C == '#':
            yield '#', '#'

            lexmebegin = forward
            C = code[forward]
            forward += 1

            while C != '\n':
                C = code[forward]
                forward += 1
            token = code[lexmebegin:forward]

            yield 'precompile', token

            if 1 == get_nbc(code):
                return
            lexmebegin = forward
            C = code[forward]
            forward += 1

        elif C in {'(', ')', '[', ']', '{', '}', '~',
                   '*', '%', '?', ':', ';', ',', '.'}:  # 单个字符
            yield 'operator', C
            if 1 == get_nbc(code):
                return
            lexmebegin = forward
            C = code[forward]
            forward += 1

        elif C == '/':
            C = code[forward]
            forward += 1
            if C == '/':
                yield 'comment symbol', '//'
                lexmebegin = forward
                C = code[forward]
                forward += 1

                while C != '\n':
                    C = code[forward]
                    forward += 1
                token = code[lexmebegin:forward]

                yield 'comment', token

                if 1 == get_nbc(code):
                    return
                lexmebegin = forward
                C = code[forward]
                forward += 1

            elif C == '*':
                yield 'comment symbol', '/*'
                lexmebegin = forward
                C = code[forward]
                forward += 1

                while True:
                    while C != '*':
                        C = code[forward]
                        forward += 1
                    if code[forward] == '/':
                        forward += 1
                        token = code[lexmebegin:forward - 2]  # warning!!!
                        yield 'comment', token
                        yield 'comment symbol', '*/'
                        if 1 == get_nbc(code):
                            return
                        lexmebegin = forward
                        C = code[forward]
                        forward += 1
                        break
                    else:
                        C = code[forward]
                        forward += 1


            else:
                yield 'operator', '/'
                if 1 == get_nbc(code):
                    return
                lexmebegin = forward
                C = code[forward]
                forward += 1

        elif C in {'!', '=', '^'}:
            forward += 1
            if code[forward] == '=':
                yield 'operator', C + '='
            else:
                retract()
                yield 'operator', C
            if 1 == get_nbc(code):
                return
            lexmebegin = forward
            C = code[forward]
            forward += 1

        elif C in {'&', '|', '<', '>', '+', '-'}:
            # forward += 1
            if code[forward] == '=':
                yield 'operator', C + '='
            elif code[forward] == C:
                yield 'operator', C + C
            else:
                # retract()
                yield 'operator', C
            forward += 1
            if 1 == get_nbc(code):
                return
            lexmebegin = forward
            C = code[forward]
            forward += 1

        elif C == '"':  # 双引号
            yield 'quote', '"'
            lexmebegin = forward
            C = code[forward]
            # forward += 1
            while True:
                while C != '"':
                    forward += 1
                    if forward >= len(code):
                        yield 'error', 'expect \'"\''
                        return
                    C = code[forward]
                if code[forward - 1] != '\\':
                    token = code[lexmebegin:forward]
                    yield 'string', token
                    yield 'quote', '"'
                    forward += 1
                    if 1 == get_nbc(code):
                        return
                    lexmebegin = forward
                    C = code[forward]
                    forward += 1
                    break
                else:
                    forward += 1
                    C = code[forward]
                    if forward >= len(code):
                        yield 'error', 'expect " '
                        return



        elif C == '\'':  # 单引号
            yield 'quote', '\''
            lexmebegin = forward
            C = code[forward]
            forward += 1
            if C == '\\':
                C = code[forward]   # '\123'
                forward += 1
            token = code[lexmebegin:forward]
            if code[forward] != '\'':
                forward = code.find('\'', forward)
                if forward == -1:
                    yield 'error', "expect a \''\'"
                    return
                token = code[lexmebegin:forward]
                yield 'error', token + ": expect a character"
            else:
                lexmebegin = forward
                yield 'character', token
            yield 'quote', '\''
            forward += 1
            if 1 == get_nbc(code):
                return
            lexmebegin = forward
            C = code[forward]
            forward += 1
        else:
            yield 'error', C + ": unknowm character"
            if 1 == get_nbc(code):
                return
            lexmebegin = forward
            C = code[forward]
            forward += 1


words = {'precompile': 0, 'comment': 0, 'keyword': 0, 'identifier': 0,
         'float': 0, 'string': 0, 'integer': 0, 'character': 0}
counts = 0
for i in analyzer(code):
    if i[0] in {'precompile', 'comment', 'keyword', 'identifier',
                'float', 'string', 'integer', 'character'}:
        words[i[0]] += 1
        counts += 1
    if i[0] == 'error':
        line = code.count('\n', 0, lexmebegin)
        print(i, 'in line ' + str(line + 1))
    else:
        print(i)

lines = code.count('\n') + 1
print('All ' + str(counts) + ' words and ' + str(lines) + ' lines')
print(words)
