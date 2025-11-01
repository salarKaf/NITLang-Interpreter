from token_types import TokenType
from ast_nodes import (Number, BinaryOp, Identifier, FunctionDef,
                       FunctionCall, IfExpr, Comparison, LetStatement, LetExpression, Block)

class Environment:
    """
    محیط برای نگهداری توابع و متغیرها با پشتیبانی از Scope
    
    در فاز 3، این کلاس static scoping رو پیاده‌سازی می‌کنه:
    - هر Environment می‌تونه یک parent داشته باشه
    - اگر متغیر پیدا نشد، به parent نگاه می‌کنه
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.functions = {}
        self.variables = {}
    
    def define_function(self, name, func_def):
        """تعریف یک تابع"""
        self.functions[name] = func_def
    
    def get_function(self, name):
        """پیدا کردن یک تابع (با جستجو در parent)"""
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise Exception(f"Undefined function: {name}")
    
    def define_variable(self, name, value):
        """
        تعریف یک متغیر در scope فعلی
        ⭐ مهم: متغیر فقط در scope فعلی ذخیره میشه، نه parent
        """
        self.variables[name] = value
    
    def get_variable(self, name):
        """
        پیدا کردن یک متغیر (با جستجو در parent)
        ⭐ این static scoping رو پیاده‌سازی می‌کنه
        """
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_variable(name)
        raise Exception(f"Undefined variable: {name}")
    
    def __repr__(self):
        return f"Env(vars={self.variables}, funcs={list(self.functions.keys())})"


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
        """
        خواندن مقدار یک متغیر
        ⭐ در فاز 3، این با static scoping کار می‌کنه
        """
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
    
    def visit_LetStatement(self, node):
        """
        ⭐⭐⭐ تعریف متغیر: let x = 10
        
        در فاز 3، این عملیات scope-aware هست:
        - متغیر در scope فعلی تعریف میشه
        - اگر توی تابع باشیم، متغیر local هست
        - اگر در global باشیم، متغیر global هست
        """
        value = self.visit(node.value)
        self.current_env.define_variable(node.name, value)
        return f"Variable '{node.name}' = {value}"
    
    def visit_LetExpression(self, node):
        """
        ⭐⭐⭐ Let Expression: let x = 10 in x + 1
        
        این اجازه میده که let رو توی expression ها استفاده کنیم:
        1. مقدار متغیر رو محاسبه می‌کنیم
        2. یک scope جدید می‌سازیم
        3. متغیر رو توی scope جدید تعریف می‌کنیم
        4. body رو با scope جدید اجرا می‌کنیم
        5. scope رو restore می‌کنیم
        """
        # محاسبه مقدار متغیر در scope فعلی
        value = self.visit(node.value)
        
        # ایجاد scope جدید برای let expression
        new_env = Environment(parent=self.current_env)
        new_env.define_variable(node.name, value)
        
        # ذخیره scope قبلی
        previous_env = self.current_env
        self.current_env = new_env
        
        try:
            # اجرای body با scope جدید
            result = self.visit(node.body)
            return result
        finally:
            # بازگرداندن scope قبلی
            self.current_env = previous_env
    
    def visit_FunctionDef(self, node):
        """تعریف یک تابع و ذخیره در global environment"""
        # ⭐ توابع همیشه در global scope تعریف میشن
        self.global_env.define_function(node.name, node)
        return f"Function '{node.name}' defined"
    
    def visit_FunctionCall(self, node):
        """
        فراخوانی یک تابع با static scoping
        
        ⭐⭐⭐ نحوه کار scope در فاز 3:
        1. Environment جدید با parent=global_env ساخته میشه
        2. پارامترها به متغیرهای local تبدیل میشن
        3. بدنه تابع با environment جدید اجرا میشه
        4. متغیرهای local فقط توی تابع قابل دسترسی هستن
        """
        # پیدا کردن تعریف تابع
        func_def = self.global_env.get_function(node.name)
        
        # محاسبه آرگومان‌ها در environment فعلی
        arg_values = [self.visit(arg) for arg in node.arguments]
        
        # بررسی تعداد پارامترها
        if len(arg_values) != len(func_def.params):
            raise Exception(
                f"Function '{node.name}' expects {len(func_def.params)} "
                f"arguments, got {len(arg_values)}"
            )
        
        # ⭐ ایجاد environment جدید با parent=global_env
        # این باعث میشه توابع فقط به global scope و پارامترهای خودشون دسترسی داشته باشن
        func_env = Environment(parent=self.global_env)
        
        # bind کردن پارامترها به آرگومان‌ها در scope جدید
        for param_name, arg_value in zip(func_def.params, arg_values):
            func_env.define_variable(param_name, arg_value)
        
        # ذخیره environment قبلی و تعویض
        previous_env = self.current_env
        self.current_env = func_env
        
        try:
            # اجرای بدنه تابع در environment جدید
            result = self.visit(func_def.body)
            return result
        finally:
            # بازگرداندن environment قبلی
            self.current_env = previous_env

    def visit_Block(self, node):
        last = None
        for stmt in node.statements:
            last = self.visit(stmt)
        return last

    def interpret(self, tree):
        return self.visit(tree)