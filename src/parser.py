from token_types import TokenType
from ast_nodes import Number, BinaryOp

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]
    
    def error(self):
        raise Exception(f'Invalid syntax at position {self.pos}')
    
    def advance(self):
        """حرکت به token بعدی"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
    
    def eat(self, token_type):
        """بررسی و مصرف token مورد انتظار"""
        if self.current_token.type == token_type:
            self.advance()
        else:
            self.error()
    
    def factor(self):
        """factor : NUMBER | LPAREN expr RPAREN"""
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        
        self.error()
    
    def term(self):
        """term : factor ((MULTIPLY | DIVIDE) factor)*"""
        node = self.factor()
        
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self.current_token
            if op_token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif op_token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            
            node = BinaryOp(left=node, operator=op_token.type, right=self.factor())
        
        return node
    
    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token
            if op_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif op_token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            
            node = BinaryOp(left=node, operator=op_token.type, right=self.term())
        
        return node
    
    def parse(self):
        """شروع parsing"""
        return self.expr()