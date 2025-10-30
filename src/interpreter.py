from token_types import TokenType
from ast_nodes import Number, BinaryOp

class Interpreter:
    def visit(self, node):
        """روش بازگشتی برای پیمایش AST"""
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')
    
    def visit_Number(self, node):
        return node.value
    
    def visit_BinaryOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        
        if node.operator == TokenType.PLUS:
            return left_val + right_val
        elif node.operator == TokenType.MINUS:
            return left_val - right_val
        elif node.operator == TokenType.MULTIPLY:
            return left_val * right_val
        elif node.operator == TokenType.DIVIDE:
            if right_val == 0:
                raise Exception("Division by zero")
            return left_val // right_val  # تقسیم صحیح
    
    def interpret(self, tree):
        return self.visit(tree)