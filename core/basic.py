class Token(object):
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"

    def __repr__(self):
        return self.__str__()

class TOKENS(object):
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    EOF = 'EOF'
    INT = 'INT'
    FLOAT = 'FLOAT'
    POWER = 'POWER'

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(TOKENS.FLOAT, float(result))
        return Token(TOKENS.INT, int(result))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.integer()
            if self.current_char == '+':
                self.advance()
                return Token(TOKENS.PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(TOKENS.MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(TOKENS.MUL, '*')
            if self.current_char == '^':
                self.advance()
                return Token(TOKENS.POWER, '^')
            if self.current_char == '/':
                self.advance()
                return Token(TOKENS.DIV, '/')
            if self.current_char == '(':
                self.advance()
                return Token(TOKENS.LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(TOKENS.RPAREN, ')')
            if self.current_char == '[':
                self.advance()
                return Token(TOKENS.LBRACKET, '[')
            if self.current_char == ']':
                self.advance()
                return Token(TOKENS.RBRACKET, ']')
            self.error()
        return Token(TOKENS.EOF, None)

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == TOKENS.PLUS:
            self.eat(TOKENS.PLUS)
            return self.factor()
        if token.type == TOKENS.MINUS:
            self.eat(TOKENS.MINUS)
            return -self.factor()
        if token.type == TOKENS.INT:
            self.eat(TOKENS.INT)
            return token.value
        if token.type == TOKENS.FLOAT:
            self.eat(TOKENS.FLOAT)
            return token.value
        if token.type == TOKENS.LPAREN:
            self.eat(TOKENS.LPAREN)
            result = self.expr()
            self.eat(TOKENS.RPAREN)
            return result
        if token.type == TOKENS.LBRACKET:
            self.eat(TOKENS.LBRACKET)
            result = self.expr()
            self.eat(TOKENS.RBRACKET)
            return result

    def power(self):
        result = self.factor()
        while self.current_token.type == TOKENS.POWER:
            token = self.current_token
            if token.type == TOKENS.POWER:
                self.eat(TOKENS.POWER)
                result = result ** self.factor()
        return result

    def term(self):
        result = self.power()
        while self.current_token.type in (TOKENS.MUL, TOKENS.DIV):
            token = self.current_token
            if token.type == TOKENS.MUL:
                self.eat(TOKENS.MUL)
                result = result * self.power()
            elif token.type == TOKENS.DIV:
                self.eat(TOKENS.DIV)
                result = result / self.power()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (TOKENS.PLUS, TOKENS.MINUS):
            token = self.current_token
            if token.type == TOKENS.PLUS:
                self.eat(TOKENS.PLUS)
                result = result + self.term()
            elif token.type == TOKENS.MINUS:
                self.eat(TOKENS.MINUS)
                result = result - self.term()
        return result

    def interpret(self):
        return self.expr()