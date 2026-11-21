from ast_nodes import * 

if __name__ == '__main__':
    pass

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        token = self.current()
        self.pos += 1
        return token

    def expect(self, token_type):
        if self.current()[0] == token_type:
            return self.advance()

        raise SyntaxError(f"Expected {token_type}, got {self.current()[0]}")

    def parse_program(self):
        statements = []

        while self.current()[0] != 'EOF':
            statements.append(self.parse_statement())

        self.expect('EOF')

        return Program(statements)


    def parse_statement(self):

        if self.current()[0] == 'VAR':
            return self.parse_assignment()

        elif self.current()[0] == 'IF':
            return self.parse_if_statement()

        else:
            raise SyntaxError(f"Unexpected token: {self.current()}")

    def parse_program(self):
        statements = []

        while self.current()[0] != 'EOF':
            statements.append(self.parse_statement())

        self.expect('EOF')

        return Program(statements)


    def parse_statement(self):

        if self.current()[0] == 'VAR':
            return self.parse_assignment()

        elif self.current()[0] == 'IF':
            return self.parse_if_statement()

        else:
            raise SyntaxError(f"Unexpected token: {self.current()}")

    def parse_assignment(self):

        name = self.expect('VAR')[1]

        self.expect('ASSIGN')

        expression = self.parse_expression()

        self.expect('SEMICOL')

        return Assignment(name, expression)

    def parse_if_statement(self):

        self.expect('IF')

        condition = self.parse_expression()

        self.expect('THEN')

        then_branch = self.parse_block()

        else_branch = []

        if self.current()[0] == 'ELSE':
            self.advance()
            else_branch = self.parse_block()

        self.expect('END')
        self.expect('SEMICOL')

        return IfStatement(condition, then_branch, else_branch)

    def parse_block(self):

        statements = []

        while self.current()[0] not in ('ELSE', 'END', 'EOF'):
            statements.append(self.parse_statement())

        return statements

    def parse_binary(self, subparser, operators):

        left = subparser()

        while self.current()[0] in operators:
            operator = self.advance()[0]
            right = subparser()

            left = BinaryExpression(left, operator, right)

        return left

    def parse_expression(self):
        return self.parse_logical_or()


    def parse_logical_or(self):
        return self.parse_binary(self.parse_logical_and, ('OR',))


    def parse_logical_and(self):
        return self.parse_binary(self.parse_comparison, ('AND',))


    def parse_comparison(self):
        left = self.parse_additive()

        if self.current()[0] in ('GT', 'LT', 'GTE', 'LTE', 'EQ', 'NEQ'):
            operator = self.advance()[0]
            right = self.parse_additive()

            return BinaryExpression(left, operator, right)

        return left


    def parse_additive(self):
        return self.parse_binary(self.parse_multiplicative, ('PLUS', 'MINUS'))


    def parse_multiplicative(self):
        return self.parse_binary(self.parse_unary, ('MULT', 'DIV'))

    def parse_unary(self):

        if self.current()[0] in ('PLUS', 'MINUS', 'NOT'):
            operator = self.advance()[0]
            operand = self.parse_unary()

            return UnaryExpression(operator, operand)

        return self.parse_primary()

    def parse_primary(self):

        token_type, value = self.current()

        if token_type == 'NUM':
            self.advance()
            return Number(float(value))

        elif token_type == 'VAR':

            self.advance()

            if self.current()[0] == 'LPAR':
                return self.parse_function_call(value)

            return Variable(value)

        elif token_type == 'LPAR':
            self.advance()

            expression = self.parse_expression()

            self.expect('RPAR')

            return expression

        else:
            raise SyntaxError(f"Unexpected token: {self.current()}")

    def parse_function_call(self, name):

        self.expect('LPAR')

        arguments = []

        if self.current()[0] != 'RPAR':

            arguments.append(self.parse_expression())

            while self.current()[0] == 'COM':
                self.advance()
                arguments.append(self.parse_expression())

        self.expect('RPAR')

        return FunctionCall(name, arguments)