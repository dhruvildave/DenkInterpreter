from base import ErrorCode, ParserError
from lex import TokenType


class AST:
    pass


# Classes that extend ast

# Different Types of node classes act differently


class BinOp(AST):
    def __init__(self, left, op: TokenType, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, right):
        self.token = self.op = op
        self.right = right


class Compound(AST):
    """Represents a 'BEGIN ... END' block"""

    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    """The Var node is constructed out of ID token."""

    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Param(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class ProcedureDecl(AST):
    def __init__(self, procName, params, blockNode, token):
        self.procName = procName
        self.params = params  # a list of Param nodes
        self.blockNode = blockNode
        self.token = token


class FunctionDecl(AST):
    def __init__(self, funcName, params, returnType, blockNode, token):
        self.funcName = funcName
        self.params = params
        self.returnType = returnType
        self.blockNode = blockNode
        self.token = token


class Readint(AST):
    def __init__(self, token):
        self.token = token


class Readfloat(AST):
    def __init__(self, token):
        self.token = token


class Readstring(AST):
    def __init__(self, token):
        self.token = token


class ProcedureCall(AST):
    def __init__(self, proc_name, actual_params, token):
        self.proc_name = proc_name
        self.actual_params = actual_params  # a list of AST nodes
        self.token = token


class WritelnCall(AST):
    def __init__(self, proc_name, actual_params, token):
        self.proc_name = proc_name
        self.actual_params = actual_params
        self.token = token


class Call(AST):
    def __init__(self, name, actualParams, token):
        self.name = name
        self.actualParams = actualParams
        self.token = token

        # super().__init__()


class Condition(AST):
    def __init__(self, token, condition, then, myElse=None):
        self.token = token
        self.condition = condition
        self.then = then
        self.myElse = myElse


class While(AST):
    def __init__(self, token, condition, MyDo):
        self.token = token
        self.condition = condition
        self.myDo = MyDo

        # super().__init__()


class MyDo(AST):
    def __init__(self, token, child):
        self.token = token
        self.child = child
        # super().__init__()


class Continue(AST):
    def __init__(self, token):
        self.token = token
        # super().__init__()


class Break(AST):
    def __init__(self, token):
        self.token = token
        # super().__init__()


class Then(AST):
    def __init__(self, token, child):
        self.token = token
        self.child = child
        # super().__init__()


class MyElse(AST):
    def __init__(self, token, child):
        self.token = token
        self.child = child


class MyBoolean(AST):
    def __init__(self, token):
        self.value = bool(token.value)


class Parser:
    """Parse Class Which Generates AST"""

    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

    def peek(self):
        peekChar = self.lexer.current_char
        return peekChar

    def get_next_token(self):
        return self.lexer.get_next_token()

    def error(self, error_code, token):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f"{error_code.value} -> {token}",
        )

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type and self.current_token is not None:
            self.current_token = self.get_next_token()
            # print(self.current_token)
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN, token=self.current_token,
            )

    # """Functions that create the tree by calling each other"""

    def program(self):
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(TokenType.PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(TokenType.SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(TokenType.DOT)
        return program_node

    # Recurssive precedence hierarchy

    def precedence1(self):
        currentToken = self.current_token
        if currentToken.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            return UnaryOp(currentToken, self.precedence1())
        elif currentToken.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnaryOp(currentToken, self.precedence1())
        elif currentToken.type == TokenType.BWISENOT:
            self.eat(TokenType.BWISENOT)
            return UnaryOp(currentToken, self.precedence1())
        elif currentToken.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            return UnaryOp(currentToken, self.precedence1())
        elif currentToken.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Num(currentToken)
        elif currentToken.type == TokenType.REAL_CONST:
            self.eat(TokenType.REAL_CONST)
            return Num(currentToken)
        elif currentToken.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(currentToken)
        elif currentToken.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return MyBoolean(currentToken)
        elif currentToken.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return MyBoolean(currentToken)
        elif currentToken.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expr()
            self.eat(TokenType.RPAREN)
            return result
        elif self.current_token.type == TokenType.ID and self.peek() == "(":
            return self.callStatement()
        elif self.current_token.type == TokenType.READINT:
            return self.readintStatement()
        elif self.current_token.type == TokenType.READFLOAT:
            return self.readfloatStatement()
        elif self.current_token.type == TokenType.READSTRING:
            return self.readstringStatement()
        else:
            return self.variable()

    def precedence2(self):
        left = self.precedence1()
        result = left
        while (
            self.current_token.type == TokenType.MUL
            or self.current_token.type == TokenType.INTEGER_DIV
            or self.current_token.type == TokenType.FLOAT_DIV
            or self.current_token.type == TokenType.AND
        ):
            op = self.current_token
            self.eat(op.type)
            result = BinOp(result, op, self.precedence1())
        return result

    def precedence3(self):
        left = self.precedence2()
        result = left
        while (
            self.current_token.type == TokenType.PLUS
            or self.current_token.type == TokenType.MINUS
            or self.current_token.type == TokenType.OR
        ):
            op = self.current_token
            self.eat(op.type)
            result = BinOp(result, op, self.precedence2())
        return result

    def precedence4(self):
        left = self.precedence3()
        result = left
        while (
            self.current_token.type == TokenType.BWISESHIFTRIGHT
            or self.current_token.type == TokenType.BWISESHIFTLEFT
        ):
            op = self.current_token
            self.eat(op.type)
            result = BinOp(result, op, self.precedence3())
        return result

    def precedence5(self):
        left = self.precedence4()
        result = left
        while (
            self.current_token.type == TokenType.EQUALS
            or self.current_token.type == TokenType.GREATER_THAN
            or self.current_token.type == TokenType.GREATER_OR_EQUALS_THAN
            or self.current_token.type == TokenType.LESS_THAN
            or self.current_token.type == TokenType.LESS_OR_EQUALS_THAN
            or self.current_token.type == TokenType.NOT_EQUALS
        ):
            op = self.current_token
            self.eat(op.type)
            result = BinOp(result, op, self.precedence4())
        return result

    def precedence6(self):
        left = self.precedence5()
        result = left
        while (
            self.current_token.type == TokenType.BWISEAND
            or self.current_token.type == TokenType.BWISEOR
            or self.current_token.type == TokenType.BWISEXOR
        ):
            op = self.current_token
            self.eat(op.type)
            result = BinOp(result, op, self.precedence5())
        return result

    def block(self):

        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):

        declarations = []

        while True:
            if self.current_token.type == TokenType.VAR:
                self.eat(TokenType.VAR)
                while self.current_token.type == TokenType.ID:
                    var_decl = self.variable_declaration()
                    declarations.extend(var_decl)
                    self.eat(TokenType.SEMI)
            elif self.current_token.type == TokenType.PROCEDURE:
                proc_decl = self.procedure_declaration()
                declarations.append(proc_decl)
            elif self.current_token.type == TokenType.FUNCTION:
                func_decl = self.function_declaration()
                declarations.append(func_decl)
            else:
                break

        # while self.current_token.type == TokenType.PROCEDURE:
        #     proc_decl = self.procedure_declaration()
        #     declarations.append(proc_decl)

        return declarations

    def variable_declaration(self):

        var_nodes = [Var(self.current_token)]  # first ID
        self.eat(TokenType.ID)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)

        type_node = self.type_spec()
        var_declarations = [VarDecl(var_node, type_node) for var_node in var_nodes]
        return var_declarations

    def procedure_declaration(self):

        self.eat(TokenType.PROCEDURE)
        proc_name = self.current_token.value
        self.eat(TokenType.ID)
        params = []

        params = self.formal_parameter_list()

        self.eat(TokenType.SEMI)
        block_node = self.block()
        proc_decl = ProcedureDecl(proc_name, params, block_node, self.current_token)
        self.eat(TokenType.SEMI)
        return proc_decl

    def function_declaration(self):
        self.eat(TokenType.FUNCTION)
        funcName = self.current_token.value
        token = self.current_token
        self.eat(TokenType.ID)
        # params = []
        params = self.formal_parameter_list()
        self.eat(TokenType.COLON)
        typ = self.type_spec()
        self.eat(TokenType.SEMI)
        block_node = self.block()
        self.eat(TokenType.SEMI)
        funcDecl = FunctionDecl(funcName, params, typ, block_node, token)
        return funcDecl

    def formal_parameters(self):

        param_nodes = []

        param_tokens = [self.current_token]
        self.eat(TokenType.ID)
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            param_tokens.append(self.current_token)
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)
        type_node = self.type_spec()

        for param_token in param_tokens:
            param_node = Param(Var(param_token), type_node)
            param_nodes.append(param_node)

        return param_nodes

    def formal_parameter_list(self):

        declarations = []
        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            while self.current_token.type == TokenType.ID:
                vardec = self.formal_parameters()
                declarations.extend(vardec)
                if self.current_token.type == TokenType.RPAREN:
                    break
                elif self.current_token.type == TokenType.SEMI:
                    self.eat(TokenType.SEMI)
            self.eat(TokenType.RPAREN)
        return declarations

    def type_spec(self):

        token = self.current_token
        if self.current_token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
        elif self.current_token.type == TokenType.REAL:
            self.eat(TokenType.REAL)
        elif self.current_token.type == TokenType.BOOLEAN:
            self.eat(TokenType.BOOLEAN)
        elif self.current_token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
        node = Type(token)
        return node

    def compound_statement(self):

        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):

        node = self.statement()

        results = [node]

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.statement())

        return results

    def statement(self):

        if self.current_token.type == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.WHILE:
            node = self.whileStatement()
        elif self.current_token.type == TokenType.BREAK:
            node = self.breakStatement()
        elif self.current_token.type == TokenType.CONTINUE:
            node = self.continueStatement()
        elif self.current_token.type == TokenType.WRITELN:
            node = self.writelnStatement()
        elif self.current_token.type == TokenType.IF:
            node = self.conditionStatement()
        elif self.current_token.type == TokenType.ID and self.lexer.current_char == "(":
            node = self.callStatement()
        elif self.current_token.type == TokenType.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def proccall_statement(self):

        token = self.current_token

        proc_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)
        actual_params = []
        if self.current_token.type != TokenType.RPAREN:
            node = self.expr()
            actual_params.append(node)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node = self.expr()
            actual_params.append(node)

        self.eat(TokenType.RPAREN)

        node = Call(name=proc_name, actualParams=actual_params, token=token,)
        return node

    def assignment_statement(self):

        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def conditionStatement(self):
        token = self.current_token
        self.eat(TokenType.IF)
        condition = self.expr()
        tokenThen = self.current_token
        self.eat(TokenType.THEN)
        thenStatementList = self.statement()
        then = Then(tokenThen, thenStatementList)
        node = None
        if self.current_token.type == TokenType.ELSE:
            myElseToken = self.current_token
            self.eat(TokenType.ELSE)
            myElseStatementList = self.statement()
            myElse = MyElse(myElseToken, myElseStatementList)
            node = Condition(token, condition, then, myElse)
        else:
            node = Condition(token, condition, then)
        return node

    def readintStatement(self):
        self.eat(TokenType.READINT)
        self.eat(TokenType.LPAREN)
        self.eat(TokenType.RPAREN)
        return Readint(self.current_token)

    def readfloatStatement(self):
        self.eat(TokenType.READFLOAT)
        self.eat(TokenType.LPAREN)
        self.eat(TokenType.RPAREN)
        return Readfloat(self.current_token)

    def readstringStatement(self):
        self.eat(TokenType.READSTRING)
        self.eat(TokenType.LPAREN)
        self.eat(TokenType.RPAREN)
        return Readstring(self.current_token)

    def whileStatement(self):
        token = self.current_token
        self.eat(TokenType.WHILE)
        condition = self.expr()
        tokenMyDo = self.current_token
        self.eat(TokenType.DO)
        myDoStatementList = self.statement()
        then = MyDo(tokenMyDo, myDoStatementList)

        node = While(token, condition, then)
        return node

    def breakStatement(self):
        token = self.current_token
        self.eat(TokenType.BREAK)
        node = Break(token)
        return node

    def continueStatement(self):
        token = self.current_token
        self.eat(TokenType.CONTINUE)
        node = Continue(token)
        return node

    def writelnStatement(self):
        token = self.current_token
        self.eat(TokenType.WRITELN)
        self.eat(TokenType.LPAREN)
        actual_params = []

        while self.current_token.type != TokenType.RPAREN:
            node = self.expr()
            actual_params.append(node)

            if self.current_token.type == TokenType.RPAREN:
                break
            elif self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)

        self.eat(TokenType.RPAREN)

        return WritelnCall("writeln", actual_params, token)

    def callStatement(self):
        token = self.current_token

        proc_name = self.current_token.value
        # print(f"call on {token} and {proc_name}")
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)

        actual_params = []

        while self.current_token.type != TokenType.RPAREN:
            node = self.expr()
            actual_params.append(node)

            if self.current_token.type == TokenType.RPAREN:
                break
            elif self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)

        self.eat(TokenType.RPAREN)

        node = Call(name=proc_name, actualParams=actual_params, token=token,)
        return node

    def variable(self):

        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    def empty(self):

        return NoOp()

    def expr(self):
        return self.precedence6()

    def parseError(self, errorCode, token):
        return ParserError(errorCode, token, "{}->{}".format(errorCode, token))

    def parse(self):
        """Main Function That starts parsing"""

        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN, token=self.current_token,
            )

        return node
