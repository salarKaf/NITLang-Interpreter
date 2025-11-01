from token_types import TokenType
from ast_nodes import (Number, BinaryOp, Identifier, FunctionDef,
                       FunctionCall, IfExpr, Comparison, LetStatement, LetExpression, Block)

class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.functions = {}
        self.variables = {}
    
    def define_function(self, name, func_def):
        self.functions[name] = func_def
    
    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise Exception(f"Undefined function: {name}")
    
    def define_variable(self, name, value):
        self.variables[name] = value
    
    def get_variable(self, name):
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
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')
    
    def visit_Number(self, node):
        return node.value
    
    def visit_Identifier(self, node):
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
        condition_val = self.visit(node.condition)
        if condition_val != 0:
            return self.visit(node.true_branch)
        else:
            return self.visit(node.false_branch)
    
    def visit_LetStatement(self, node):
        value = self.visit(node.value)
        self.current_env.define_variable(node.name, value)
        return f"Variable '{node.name}' = {value}"
    
    def visit_LetExpression(self, node):
        value = self.visit(node.value)
        new_env = Environment(parent=self.current_env)
        new_env.define_variable(node.name, value)
        previous_env = self.current_env
        self.current_env = new_env
        try:
            result = self.visit(node.body)
            return result
        finally:
            self.current_env = previous_env
    
    def visit_FunctionDef(self, node):
        self.global_env.define_function(node.name, node)
        return f"Function '{node.name}' defined"
    
    def visit_FunctionCall(self, node):
        func_def = self.global_env.get_function(node.name)
        arg_values = [self.visit(arg) for arg in node.arguments]
        if len(arg_values) != len(func_def.params):
            raise Exception(
                f"Function '{node.name}' expects {len(func_def.params)} "
                f"arguments, got {len(arg_values)}"
            )
        func_env = Environment(parent=self.global_env)
        for param_name, arg_value in zip(func_def.params, arg_values):
            func_env.define_variable(param_name, arg_value)
        previous_env = self.current_env
        self.current_env = func_env
        try:
            result = self.visit(func_def.body)
            return result
        finally:
            self.current_env = previous_env

    def visit_Block(self, node):
        last = None
        for stmt in node.statements:
            last = self.visit(stmt)
        return last

    def interpret(self, tree):
        return self.visit(tree)
