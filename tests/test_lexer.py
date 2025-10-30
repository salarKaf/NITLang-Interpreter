import sys
sys.path.insert(0, '../src')

from lexer import Lexer
from token_types import TokenType

def test_simple_expression():
    lexer = Lexer("2 + 3")
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == 2
    assert tokens[1].type == TokenType.PLUS
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == 3
    
    print("✅ Lexer test passed!")

if __name__ == '__main__':
    test_simple_expression()
    