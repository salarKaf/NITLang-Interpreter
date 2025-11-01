class ASTNode:
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

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"


class FunctionDef(ASTNode):

    def __init__(self, name, params, body):
        self.name = name  
        self.params = params 
        self.body = body  

    def __repr__(self):
        params_str = ', '.join(self.params)
        return f"FunctionDef({self.name}({params_str}) = {self.body})"


class FunctionCall(ASTNode):

    def __init__(self, name, arguments):
        self.name = name  
        self.arguments = arguments  

    def __repr__(self):
        args_str = ', '.join(str(arg) for arg in self.arguments)
        return f"FunctionCall({self.name}({args_str}))"


class IfExpr(ASTNode):

    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        return f"IfExpr(if {self.condition} then {self.true_branch} else {self.false_branch})"


class Comparison(ASTNode):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Comparison({self.left} {self.operator.name} {self.right})"


class LetStatement(ASTNode):

    def __init__(self, name, value):
        self.name = name  
        self.value = value  

    def __repr__(self):
        return f"LetStatement({self.name} = {self.value})"


class LetExpression(ASTNode):

    def __init__(self, name, value, body):
        self.name = name  
        self.value = value  
        self.body = body  

    def __repr__(self):
        return f"LetExpression(let {self.name} = {self.value} in {self.body})"


class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements  

    def __repr__(self):
        return f"Block({self.statements})"
