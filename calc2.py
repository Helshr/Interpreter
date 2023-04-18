INTEGER, PLUS, MINUS, EOF, MULTIPLY, DIVISION = "INTEGER", "PLUS", "MINUS", "EOF", "MULTIPLY", "DIVISION"


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token {self.type}, {self.value}"

    def __repr__(self):
        return self.__str__()


class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) -1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == "+":
                self.advance()
                return Token(PLUS, self.current_char)
            if self.current_char == "-":
                self.advance()
                return Token(MINUS, self.current_char)
            if self.current_char == "*":
                self.advance()
                return Token(MULTIPLY, self.current_char)
            if self.current_char == "/":
                self.advance()
                return Token(DIVISION, self.current_char)
            self.error()
        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def operator_function(self, op_type, number_list):
        if op_type == PLUS:
            result = number_list[0] + number_list[1]
        elif op_type == MINUS:
            result = number_list[0] - number_list[1]
        elif op_type == MULTIPLY:
            result = number_list[0] * number_list[1]
        else:
            result = number_list[0] / float(number_list[1])
        return result

    def expr(self):
        result = 0
        number_and_list = []
        op_type = None
        while self.pos < len(self.text):
            self.current_token = self.get_next_token()
            if self.current_token.type is INTEGER:
                number_and_list.append(self.current_token.value)
            else:
                op_type = self.current_token.type
            if op_type is not None and len(number_and_list) == 2:
                result = self.operator_function(op_type, number_and_list)
                number_and_list = [result]
        return result


def main():
    while True:
        try:
            raw_text = input('calc> ')
        except EOFError:
            break
        if not raw_text:
            continue
        text = raw_text.rstrip()

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
