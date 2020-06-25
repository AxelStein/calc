from calc import const


class BinOp:
    def __init__(self, op=None, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return '{} ->{} =>{} '.format(self.op, self.left, self.right)

    def __repr__(self):
        return str(self)


class UnOp:
    def __init__(self, op=None, operand=None):
        self.op = op
        self.operand = operand

    def __str__(self):
        return f'{self.op} ->{self.operand} '

    def __repr__(self):
        return str(self)


class Num:
    def __init__(self, val=None):
        self.val = val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self)


class Var:
    def __init__(self, name, negative=False):
        self.name = name
        self.negative = negative

    def __str__(self):
        s = '-' if self.negative else ''
        return s + self.name

    def __repr__(self):
        return str(self)


class Parser:
    def __init__(self, lexer):
        self.bp_map = {
            const.ASN: 1,
            const.ADD: 2,
            const.SUB: 2,
            const.MUL: 3,
            const.DIV: 3,
            const.DIV_INT: 3,
            const.MOD: 3,
            const.EXP: 4,
        }
        self.lexer = lexer
        self.token = None

    # return next token from lexer
    def _next_token(self):
        self.token = self.lexer.next_token()
        return self.token

    def _peek_next_token(self):
        return self.lexer.peek_next_token()

    # return binding power of operator
    def _bp(self, token):
        if token.type in self.bp_map.keys():
            return self.bp_map[token.type]
        return 0

    # return null-denotation operator with no left context
    def _nud(self, token):
        negative = False
        if token.type == const.SUB:
            negative = True
            token = self._next_token()
        if token.type in (const.INT, const.FLOAT):
            sign = -1 if negative else 1
            return Num(token.val * sign)
        if token.type == const.NAME:
            return Var(token.val, negative)
        if token.type == const.L_PAREN:
            r = self._expr(0)
            self._next_token()
            return r
        if token.type == const.SIN:
            sin = UnOp(const.SIN, self._expr(0))
            self._next_token()
            return sin

    # return left-denotation operator with left context
    def _led(self, left, token):
        bp = self._bp(token)
        if token.type == const.EXP:
            bp -= 1
        return BinOp(token.type, left, self._expr(bp))

    # rbp is binding power of the right operator
    def _expr(self, rbp):
        left = self._nud(self._next_token())
        while self._bp(self._peek_next_token()) > rbp:
            left = self._led(left, self._next_token())
        return left

    def _expr_list(self):
        expr_list = []
        expr = self._expr(0)
        while expr:
            expr_list.append(expr)
            self._next_token()
            expr = self._expr(0)
        return expr_list

    def parse(self):
        return self._expr_list()
