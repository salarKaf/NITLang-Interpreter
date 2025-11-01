from token_types import TokenType
from ast_nodes import (Number, BinaryOp, Identifier, FunctionDef, 
                       FunctionCall, IfExpr, Comparison, LetStatement, LetExpression)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, msg="Invalid syntax"):
        raise Exception(f'{msg} at position {self.pos}, token: {self.current_token}')
    
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
            self.error(f"Expected {token_type}, got {self.current_token.type}")
    
    def factor(self):
        """
        factor : NUMBER 
               | IDENTIFIER
               | LPAREN expr RPAREN
               | HASH IDENTIFIER LPAREN arguments RPAREN  (function call)
        """
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Identifier(token.value)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        
        elif token.type == TokenType.HASH:
            # Function call: #fact(5)
            self.eat(TokenType.HASH)
            func_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.LPAREN)
            arguments = self.arguments()
            self.eat(TokenType.RPAREN)
            return FunctionCall(func_name, arguments)
        
        self.error("Expected number, identifier, or expression")
    
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
    
    def arith_expr(self):
        """arith_expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token
            if op_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif op_token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            
            node = BinaryOp(left=node, operator=op_token.type, right=self.term())
        
        return node
    
    def comparison(self):
        """comparison : arith_expr (EQUALS arith_expr)?"""
        node = self.arith_expr()
        
        if self.current_token.type == TokenType.EQUALS:
            op_token = self.current_token
            self.eat(TokenType.EQUALS)
            node = Comparison(left=node, operator=op_token.type, right=self.arith_expr())
        
        return node
    
    def expr(self):
        """
        expr : IF expr THEN expr ELSE expr
             | LET IDENTIFIER ASSIGN expr IN expr  (let expression)
             | comparison
        """
        if self.current_token.type == TokenType.IF:
            self.eat(TokenType.IF)
            condition = self.expr()
            self.eat(TokenType.THEN)
            true_branch = self.expr()
            self.eat(TokenType.ELSE)
            false_branch = self.expr()
            return IfExpr(condition, true_branch, false_branch)
        
        # ⭐⭐⭐ Let Expression: let x = 10 in x + 1
        elif self.current_token.type == TokenType.LET:
            self.eat(TokenType.LET)
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.ASSIGN)
            value_expr = self.expr()
            
            # بررسی می‌کنیم که آیا IN داریم؟
            if self.current_token.type == TokenType.IN:
                self.eat(TokenType.IN)
                body_expr = self.expr()
                return LetExpression(var_name, value_expr, body_expr)
            else:
                # این یه statement هست، نه expression
                raise Exception("let without 'in' is not allowed in expression context. Use 'let x = ... in ...'")
        
        return self.comparison()
    
    def arguments(self):
        """arguments : expr (COMMA expr)* | empty"""
        args = []
        
        if self.current_token.type == TokenType.RPAREN:
            return args
        
        args.append(self.expr())
        
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            args.append(self.expr())
        
        return args
    
    def parameters(self):
        """parameters : IDENTIFIER (COMMA IDENTIFIER)* | empty"""
        params = []
        
        if self.current_token.type == TokenType.RPAREN:
            return params
        
        params.append(self.current_token.value)
        self.eat(TokenType.IDENTIFIER)
        
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
        
        return params
    
    def statement(self):
        """
        statement : LET IDENTIFIER ASSIGN expr           (let statement)
                  | FUNC IDENTIFIER LPAREN parameters RPAREN ASSIGN expr
                  | expr
        """
        # ⭐⭐⭐ پشتیبانی از let statement برای فاز 3
        if self.current_token.type == TokenType.LET:
            self.eat(TokenType.LET)
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.ASSIGN)
            value_expr = self.expr()
            return LetStatement(var_name, value_expr)
        
        elif self.current_token.type == TokenType.FUNC:
            self.eat(TokenType.FUNC)
            func_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.LPAREN)
            params = self.parameters()
            self.eat(TokenType.RPAREN)
            self.eat(TokenType.ASSIGN)
            body = self.expr()
            return FunctionDef(func_name, params, body)
        
        return self.expr()
    
    def parse(self):
        """شروع parsing"""
        node = self.statement()
        if self.current_token.type != TokenType.EOF:
            self.error("Expected end of input")
        return node