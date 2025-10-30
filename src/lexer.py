from token_types import Token, TokenType

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
    
    def error(self):
        raise Exception(f'Invalid character at position {self.pos}')
    
    def advance(self):
        """حرکت به کاراکتر بعدی"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        """رد شدن از فاصله‌ها"""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def number(self):
        """خواندن یک عدد کامل"""
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def get_next_token(self):
        """گرفتن Token بعدی"""
        while self.current_char:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.number(), self.pos)
            
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', self.pos - 1)
            
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', self.pos - 1)
            
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*', self.pos - 1)
            
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/', self.pos - 1)
            
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.pos - 1)
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.pos - 1)
            
            self.error()
        
        return Token(TokenType.EOF, None, self.pos)
    
    def tokenize(self):
        """تبدیل کل متن به لیست Token"""
        tokens = []
        token = self.get_next_token()
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        tokens.append(token)  # EOF
        return tokens