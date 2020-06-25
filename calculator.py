import math

from calc.lexer import Lexer
from calc.parser import *


class Calculator:
    def __init__(self):
        self.vars = {}

    def get_var_value(self, node):
        if type(node) is Var:
            if node.name in self.vars.keys():
                v = self.vars[node.name]
                s = -1 if node.negative else 1
                v *= s
                return v
            else:
                print(f'Var {node.name} not found')
                return None
        return node

    def calc(self, op, left, right):
        a = self.get_var_value(left)
        b = self.get_var_value(right)

        if op == const.ADD:
            return a + b
        elif op == const.SUB:
            return a - b
        elif op == const.MUL:
            return a * b
        elif op == const.DIV:
            return a / b
        elif op == const.DIV_INT:
            return a // b
        elif op == const.EXP:
            return a ** b
        elif op == const.MOD:
            return a % b

    def calc_expr(self, node):
        if type(node) is Num:
            return node.val
        if type(node) is Var:
            return node
        if type(node) is UnOp:
            if node.op == const.SIN:
                v = self.calc_expr(node.operand)
                return math.sin(v)
        if type(node) is BinOp:
            left = self.calc_expr(node.left)
            right = self.calc_expr(node.right)
            if node.op == const.ASN:
                self.vars[left.name] = self.get_var_value(right)
            else:
                return self.calc(node.op, left, right)

    def compile(self, node_list):
        for node in node_list:
            if type(node) is Var:
                result = self.get_var_value(node)
            else:
                result = self.calc_expr(node)
            if result is not None:
                print(result)


calc = Calculator()

text = input(">>>")
while text != 'break':
    parser = Parser(Lexer(text))
    calc.compile(parser.parse())
    text = input(">>>")
