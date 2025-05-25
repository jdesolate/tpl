from enum import Enum
from typing import Any

class TokenType(Enum):
    # Data types
    INT = 'INT'
    CHAR = 'CHAR'
    BOOL = 'BOOL'
    FLOAT = 'FLOAT'
    
    # Keywords
    VAR = 'VAR'
    AS = 'AS'
    START = 'START'
    STOP = 'STOP'
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    
    # Operators
    ASSIGN = '='
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    MODULO = '%'
    GT = '>'
    LT = '<'
    GTE = '>='
    LTE = '<='
    EQ = '=='
    NEQ = '<>'
    
    # Delimiters
    LPAREN = '('
    RPAREN = ')'
    LSQUARE = '['
    RSQUARE = ']'
    COMMA = ','
    AMPERSAND = '&'
    COLON = ':'
    HASH = '#'
    
    # Literals
    INTEGER = 'INTEGER'
    FLOAT_NUM = 'FLOAT_NUM'
    STRING = 'STRING'
    CHARACTER = 'CHARACTER'
    BOOLEAN = 'BOOLEAN'
    
    # Identifiers
    IDENTIFIER = 'IDENTIFIER'
    
    # Special
    NEWLINE = 'NEWLINE'
    EOF = 'EOF'
    COMMENT = 'COMMENT'

class Token:
    def __init__(self, type_: TokenType, value: Any, line: int = 0):
        self.type = type_
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f'Token({self.type}, {self.value})'
      