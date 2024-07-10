# file: fuzzy_logic_language.py

import re
import math

# Define token types
TOKEN_TYPES = {
    'NUMBER': r'\d+(\.\d+)?',
    'IDENTIFIER': r'[a-zA-Z_]\w*',
    'OPERATOR': r'[+\-*/]',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'COMMA': r',',
    'ASSIGN': r'=',
    'KEYWORDS': r'(if|else|end|and|or|not)',
    'WHITESPACE': r'\s+'
}

# Lexer: Tokenize the input code
def lexer(code):
    tokens = []
    while code:
        for token_type, pattern in TOKEN_TYPES.items():
            match = re.match(pattern, code)
            if match:
                if token_type != 'WHITESPACE':  # Ignore whitespace
                    tokens.append((token_type, match.group(0)))
                code = code[len(match.group(0)):]
                break
        else:
            raise SyntaxError(f"Unexpected character: {code[0]}")
    return tokens

# Parser: Define AST nodes
class Number:
    def __init__(self, value):
        self.value = float(value)

class Identifier:
    def __init__(self, name):
        self.name = name

class BinaryOp:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOp:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

# Parse tokens into an AST
def parse(tokens):
    def parse_expression(index):
        token = tokens[index]
        if token[0] == 'NUMBER':
            return Number(token[1]), index + 1
        elif token[0] == 'IDENTIFIER':
            return Identifier(token[1]), index + 1
        elif token[0] == 'OPERATOR' and token[1] in ['+', '-', '*', '/']:
            left, next_index = parse_expression(index + 1)
            right, next_index = parse_expression(next_index)
            return BinaryOp(left, token[1], right), next_index
        elif token[0] == 'KEYWORDS' and token[1] in ['not']:
            operand, next_index = parse_expression(index + 1)
            return UnaryOp(token[1], operand), next_index
        else:
            raise SyntaxError(f"Unexpected token: {token}")
    ast, next_index = parse_expression(0)
    if next_index != len(tokens):
        raise SyntaxError("Unexpected tokens at the end of input")
    return ast

# Evaluator: Fuzzy logic operations
def fuzzy_and(a, b):
    return min(a, b)

def fuzzy_or(a, b):
    return max(a, b)

def fuzzy_not(a):
    return 1.0 - a

# Evaluate the AST
def evaluate(node, context):
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, Identifier):
        return context.get(node.name, 0.0)
    elif isinstance(node, BinaryOp):
        left = evaluate(node.left, context)
        right = evaluate(node.right, context)
        if node.operator == '+':
            return fuzzy_or(left, right)
        elif node.operator == '*':
            return fuzzy_and(left, right)
        else:
            raise ValueError(f"Unknown operator: {node.operator}")
    elif isinstance(node, UnaryOp):
        operand = evaluate(node.operand, context)
        if node.operator == 'not':
            return fuzzy_not(operand)
        else:
            raise ValueError(f"Unknown operator: {node.operator}")
    else:
        raise TypeError(f"Unknown AST node: {type(node)}")

# Main Interpreter: REPL
def repl():
    context = {}
    while True:
        try:
            code = input("fuzzy> ")
            tokens = lexer(code)
            ast = parse(tokens)
            result = evaluate(ast, context)
            print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()
