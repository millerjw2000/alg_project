from ast_nodes import *
import re

# make sure reserved variables are not modifiable
# make sure variable names are valid
# improve documentation

functions = ['avg','max','min','abs','pow','round','floor','ceil','sqrt']

var_values = {}

def evaluate_program(ast):

    for statement in ast.statements:
        
        print(statement)
        evaluate_statement(statement)
        
    print(var_values)

def evaluate_statement(statement):
    
    if isinstance(statement,Assignment):
    
        evaluate_assignment(statement)
    
    elif isinstance(statement,IfStatement):
    
        evaluate_if(statement)

def evaluate_assignment(assignment_statement):

    #print(assignment_statement)

    name = assignment_statement.name
    if name in functions:
        raise f'{name} is a function name!'
    
    expression = assignment_statement.expression

    if isinstance(expression, BinaryExpression):

        var_values[name] = evaluate_binary_expression(expression)

    elif isinstance(expression, UnaryExpression):

        var_values[name] = evaluate_unary_expression(expression)

    elif isinstance(expression, Number):

        var_values[name] = evaluate_number(expression)

    elif isinstance(expression, Variable):

        var_values[name] = evaluate_variable(expression)

    elif isinstance(expression,FunctionCall):

        var_values[name] = evaluate_function_call(expression)

def evaluate_if(if_statement):

    condition = if_statement.condition
    then_branch = if_statement.then_branch
    else_branch = if_statement.else_branch
    
    if isinstance(condition, BinaryExpression):
        condition_val = evaluate_binary_expression(condition)
    elif isinstance(condition, UnaryExpression):
        condition_val = evaluate_unary_expression(condition)
    elif isinstance(condition,Variable):
        condition_val = evaluate_variable(condition)
    elif isinstance(condition,Number):
        condition_val = evaluate_number(condition)
    elif isinstance(condition,FunctionCall):
        condition_val = evaluate_function_call(condition)

    if condition_val != 0: # non-zero = True

        for statement in then_branch:
            evaluate_statement(statement)

    elif condition_val == 0: # zero = False

        for statement in else_branch:
            evaluate_statement(statement)

def evaluate_binary_expression(binary_expression):

    print(binary_expression)
    
    left = binary_expression.left
    right = binary_expression.right
    operator = binary_expression.operator

    if isinstance(left, BinaryExpression):
        left_val = evaluate_binary_expression(left)
    elif isinstance(left, UnaryExpression):
        left_val = evaluate_unary_expression(left)
    elif isinstance(left, Variable):
        left_val = evaluate_variable(left)
    elif isinstance(left, Number):
        left_val = evaluate_number(left)

    if isinstance(right, BinaryExpression):   
        right_val = evaluate_binary_expression(right)  
    elif isinstance(right, UnaryExpression):   
        right_val = evaluate_unary_expression(right)  
    elif isinstance(right, Variable):   
        right_val = evaluate_variable(right)
    elif isinstance(right, Number):
        right_val = evaluate_number(right)

    print('leftval',left_val)
    print('rightval',right_val)

    if operator == 'PLUS':

        return left_val + right_val

    elif operator == 'MINUS':

        return left_val - right_val

    elif operator == 'MULT':

        return left_val * right_val

    elif operator == 'DIV':

        return left_val / right_val

    elif operator == 'GT':

        return 1 if (left_val > right_val) else 0

    elif operator == 'GTE':
    
        return 1 if (left_val >= right_val) else 0

    elif operator == 'LT':
    
        return 1 if (left_val < right_val) else 0

    elif operator == 'LT':
    
        return 1 if (left_val <= right_val) else 0

    elif operator == 'EQ':
    
        return 1 if (left_val == right_val) else 0

    elif operator == 'NEQ':
    
        return 1 if (left_val != right_val) else 0
    

def evaluate_unary_expression(unary_expression):

    print(unary_expression)
    operator = unary_expression.operator
    operand = unary_expression.operand

    if isinstance(operand, BinaryExpression):

        operand_val = evaluate_binary_expression(operand)

    elif isinstance(operand, Variable):

        operand_val = evaluate_variable(operand)

    elif isinstance(operand, Number):

        operand_val = evaluate_number(operand)

    if operator == 'PLUS':

        return operand_val

    elif operator == 'MINUS':

        return operand_val * -1

    elif operator == 'NOT':

        return 0 if operand != 0 else 1

def evaluate_number(number):

    print(number)
    return float(number.value)

def evaluate_variable(variable):

    print(variable)
    return var_values[variable.name]

def evaluate_function_call(function_call):

    name = function_call.name
    arguments = function_call.arguments

    if name not in functions:

        raise SyntaxError(f'{name} is not a valid function!')

    match name:

        case 'avg':
            return calc_avg(arguments)
            

def calc_avg(arguments):

    if len(arguments) < 1:
    
        raise SyntaxError(f'Invalid number of arguments. Expected > 1, got {len(arguments)}')
    
    sum = 0
    for argument in arguments:
    
        if isinstance(argument,BinaryExpression):
    
            sum += evaluate_binary_expression(argument)
    
        elif isinstance(argument,UnaryExpression):
    
            sum += evaluate_unary_expression(argument)

        elif isinstance(argument,Variable):

            sum += evaluate_variable(argument)

        elif isinstance(argument,FunctionCall):

            sum += evaluate_function_call(argument)

        elif isinstance(argument,Number):

            sum += evaluate_number(argument)

    return sum / len(arguments)