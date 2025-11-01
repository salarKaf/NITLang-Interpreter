from enum import Enum


class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    # Keywords
    FUNC = "FUNC"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    LET = "LET"  # ⭐ اضافه شد برای فاز 3
    IN = "IN"  # ⭐ برای let expression

    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    EQUALS = "EQUALS"  # ==
    ASSIGN = "ASSIGN"  # =

    # Structure
    LPAREN = "LPAREN"  # (
    RPAREN = "RPAREN"  # )
    COMMA = "COMMA"  # ,
    HASH = "HASH"  # # (برای فراخوانی تابع)
    LBRACE = "LBRACE"  # {
    RBRACE = "RBRACE"  # }

    # Special
    EOF = "EOF"


class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {self.value}, pos={self.position})"


# Keywords dictionary
KEYWORDS = {
    'func': TokenType.FUNC,
    'if': TokenType.IF,
    'then': TokenType.THEN,
    'else': TokenType.ELSE,
    'let': TokenType.LET,  # ⭐ اضافه شد
    'in': TokenType.IN,  # ⭐ اضافه شد
}
