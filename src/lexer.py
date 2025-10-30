from token_types import Token, TokenType, KEYWORDS

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
    
    def error(self):
        raise Exception(f'Invalid character "{self.current_char}" at position {self.pos}')
    
    def advance(self):
        """حرکت به کاراکتر بعدی"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self):
        """نگاه کردن به کاراکتر بعدی بدون حرکت"""
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def skip_whitespace(self):
        """رد شدن از فاصله‌ها و خطوط جدید"""
        while self.current_char and self.current_char in ' \t\n\r':
            self.advance()
    
    def skip_comment(self):
        """رد شدن از کامنت‌ها (# تا آخر خط)"""
        # اگه # برای فراخوانی تابع نیست
        if self.peek() and (self.peek().isalpha() or self.peek() == '_'):
            return False  # این # برای فراخوانی تابع است
        
        while self.current_char and self.current_char != '\n':
            self.advance()
        self.skip_whitespace()
        return True
    
    def number(self):
        """خواندن یک عدد کامل"""
        result = ''
        start_pos = self.pos
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, int(result), start_pos)
    
    def identifier(self):
        """خواندن identifier یا keyword"""
        result = ''
        start_pos = self.pos
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # بررسی اینکه آیا keyword است یا identifier
        token_type = KEYWORDS.get(result, TokenType.IDENTIFIER)
        return Token(token_type, result, start_pos)
    
    def get_next_token(self):
        """گرفتن Token بعدی"""
        while self.current_char:
            
            if self.current_char in ' \t\n\r':
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return self.number()
            
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            if self.current_char == '+':
                pos = self.pos
                self.advance()
                return Token(TokenType.PLUS, '+', pos)
            
            if self.current_char == '-':
                pos = self.pos
                self.advance()
                return Token(TokenType.MINUS, '-', pos)
            
            if self.current_char == '*':
                pos = self.pos
                self.advance()
                return Token(TokenType.MULTIPLY, '*', pos)
            
            if self.current_char == '/':
                pos = self.pos
                self.advance()
                return Token(TokenType.DIVIDE, '/', pos)
            
            if self.current_char == '=':
                pos = self.pos
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQUALS, '==', pos)
                else:
                    return Token(TokenType.ASSIGN, '=', pos)
            
            if self.current_char == '(':
                pos = self.pos
                self.advance()
                return Token(TokenType.LPAREN, '(', pos)
            
            if self.current_char == ')':
                pos = self.pos
                self.advance()
                return Token(TokenType.RPAREN, ')', pos)
            
            if self.current_char == ',':
                pos = self.pos
                self.advance()
                return Token(TokenType.COMMA, ',', pos)
            
            if self.current_char == '#':
                pos = self.pos
                self.advance()
                return Token(TokenType.HASH, '#', pos)
            
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