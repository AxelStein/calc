from calc import const


class Token:
    def __init__(self, t, v=None):
        self.type = t
        self.val = v

    def __str__(self):
        s = 'Token {}'
        if self.val is not None:
            s += ' {}'
        s += ' '
        return s.format(self.type, self.val)


class Lexer:
    def __init__(self, txt):
        self.txt = txt.strip()
        self.pos = 0

    def _forward(self):
        self.pos += 1

    def _pop_next_char(self):
        self._forward()
        if self.pos < len(self.txt):
            return self.txt[self.pos]

    def _peek_char(self):
        if self.pos < len(self.txt):
            return self.txt[self.pos]

    def _peek_next_char(self):
        p = self.pos + 1
        if p < len(self.txt):
            return self.txt[p]

    def _get_digit(self, ch):
        is_float = False
        buf = []
        while ch.isdigit():
            buf.append(ch)
            ch = self._pop_next_char()
            if not ch:
                break
            if ch == '.' or ch == ',':
                is_float = True
                buf.append('.')
                ch = self._pop_next_char()
        s = ''.join(buf)
        if is_float:
            return Token(const.FLOAT, float(s))
        return Token(const.INT, int(s))

    def _get_name(self, ch):
        buf = []
        while ch.isalpha() or ch.isdigit() or ch == '_':
            buf.append(ch)
            ch = self._pop_next_char()
            if not ch:
                break
        s = ''.join(buf)
        if s == 'sin':
            return Token(const.SIN)
        return Token(const.NAME, s)

    def _get_op(self, ch):
        self._forward()
        if ch == '+':
            return Token(const.ADD)
        elif ch == '-':
            return Token(const.SUB)
        elif ch == '^':
            return Token(const.EXP)
        elif ch == '*':
            return Token(const.MUL)
        elif ch == '/':
            c = self._peek_char()
            if c == '/':
                self._forward()
                return Token(const.DIV_INT)
            return Token(const.DIV)
        elif ch == '(':
            return Token(const.L_PAREN)
        elif ch == ')':
            return Token(const.R_PAREN)
        elif ch == '%':
            return Token(const.MOD)
        elif ch == '=':
            return Token(const.ASN)

    def next_token(self):
        if self.pos >= len(self.txt):
            return Token(const.EOF)

        ch = self._peek_char()
        while ch in (' ', '\t'):
            ch = self._pop_next_char()
        if ch == '\n':
            self._forward()
            return Token(const.EOL)
        elif ch.isdigit():
            return self._get_digit(ch)
        elif ch.isalpha():
            return self._get_name(ch)
        else:
            return self._get_op(ch)

    def peek_next_token(self):
        p = self.pos
        nt = self.next_token()
        self.pos = p
        return nt
