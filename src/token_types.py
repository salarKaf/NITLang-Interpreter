from enum import Enum

class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    
    # Structure
    LPAREN = "LPAREN"  # (
    RPAREN = "RPAREN"  # )
    
    # Special
    EOF = "EOF"

class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.position})"