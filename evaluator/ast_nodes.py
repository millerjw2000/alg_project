from dataclasses import dataclass

@dataclass
class Program:
    statements: list

@dataclass
class Assignment:
    name: str
    expression: object

@dataclass
class IfStatement:
    condition: object
    then_branch: list
    else_branch: list

@dataclass
class BinaryExpression:
    left: object
    operator: str
    right: object

@dataclass
class UnaryExpression:
    operator: str
    operand: object

@dataclass
class Number:
    value: float

@dataclass
class Variable:
    name: str

@dataclass
class FunctionCall:
    name: str
    arguments: list