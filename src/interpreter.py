from token_types import TokenType
from ast_nodes import (Number, BinaryOp, Identifier, FunctionDef, 
                       FunctionCall, IfExpr, Comparison)

class Environment:
    """محیط برای نگهداری توابع و متغیرها"""
    def __init__(self, parent=None):
        self.parent = parent
        self.functions = {}
        self.variables = {}
    
    def define_function(self, name, func_def):
        """تعریف یک تابع"""
        self.functions[name] = func_def
    
    def get_function(self, name):
        """پیدا کردن یک تابع"""
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise Exception(f"Undefined function: {name}")
    
    def define_variable(self, name, value):
        """تعریف یک متغیر (پارامتر)"""
        self.variables[name] = value
    
    def get_variable(self, name):
        """پیدا کردن یک متغیر"""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_variable(name)
        raise Exception(f"Undefined variable: {name}")


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
    
    def visit(self, node):
        """روش بازگشتی برای پیمایش AST"""
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')
    
    def visit_Number(self, node):
        return node.value
    
    def visit_Identifier(self, node):
        """خواندن مقدار یک متغیر (پارامتر)"""
        return self.current_env.get_variable(node.name)
    
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
            return left_val // right_val
    
    def visit_Comparison(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        
        if node.operator == TokenType.EQUALS:
            return 1 if left_val == right_val else 0
        
        raise Exception(f"Unknown comparison operator: {node.operator}")
    
    def visit_IfExpr(self, node):
        """اجرای عبارت شرطی"""
        condition_val = self.visit(node.condition)
        
        # در NITLang، 0 = false، غیر از 0 = true
        if condition_val != 0:
            return self.visit(node.true_branch)
        else:
            return self.visit(node.false_branch)
    
    def visit_FunctionDef(self, node):
        """تعریف یک تابع و ذخیره در environment"""
        self.global_env.define_function(node.name, node)
        return f"Function '{node.name}' defined"
    
    def visit_FunctionCall(self, node):
        """فراخوانی یک تابع"""
        # پیدا کردن تعریف تابع
        func_def = self.global_env.get_function(node.name)
        
        # محاسبه آرگومان‌ها
        arg_values = [self.visit(arg) for arg in node.arguments]
        
        # بررسی تعداد پارامترها
        if len(arg_values) != len(func_def.params):
            raise Exception(
                f"Function '{node.name}' expects {len(func_def.params)} "
                f"arguments, got {len(arg_values)}"
            )
        
        # ایجاد environment جدید برای اجرای تابع
        func_env = Environment(parent=self.global_env)
        
        # bind کردن پارامترها به آرگومان‌ها
        for param_name, arg_value in zip(func_def.params, arg_values):
            func_env.define_variable(param_name, arg_value)
        
        # ذخیره environment قبلی و تعویض
        previous_env = self.current_env
        self.current_env = func_env
        
        try:
            # اجرای بدنه تابع
            result = self.visit(func_def.body)
            return result
        finally:
            # بازگرداندن environment قبلی
            self.current_env = previous_env
    
    def interpret(self, tree):
        return self.visit(tree)