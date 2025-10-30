class ASTNode:
    """کلاس پایه برای همه node های AST"""
    pass


class Number(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"


class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.operator.name} {self.right})"


class Identifier(ASTNode):
    """نام متغیر یا پارامتر"""
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Identifier({self.name})"


class FunctionDef(ASTNode):
    """تعریف تابع: func fact(n) = body"""
    def __init__(self, name, params, body):
        self.name = name        # نام تابع
        self.params = params    # لیست پارامترها
        self.body = body        # بدنه تابع (یک AST node)
    
    def __repr__(self):
        params_str = ', '.join(self.params)
        return f"FunctionDef({self.name}({params_str}) = {self.body})"


class FunctionCall(ASTNode):
    """فراخوانی تابع: #fact(5)"""
    def __init__(self, name, arguments):
        self.name = name           # نام تابع
        self.arguments = arguments # لیست آرگومان‌ها
    
    def __repr__(self):
        args_str = ', '.join(str(arg) for arg in self.arguments)
        return f"FunctionCall({self.name}({args_str}))"


class IfExpr(ASTNode):
    """عبارت شرطی: if condition then true_branch else false_branch"""
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
    
    def __repr__(self):
        return f"IfExpr(if {self.condition} then {self.true_branch} else {self.false_branch})"


class Comparison(ASTNode):
    """مقایسه: a == b"""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"Comparison({self.left} {self.operator.name} {self.right})"