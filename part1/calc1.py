INTEGER, PLUS, MINUS, EOF, MULTIPLY = "INTEGER", "PLUS", "MINUS", "EOF", "MULTIPLY"


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

    def error(self):
        raise Exception('Error parsing input')

    def character_is_symbol(self, character):
        symbols = ["+", "-"]
        return character in symbols

    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1:
            return Token(EOF, None)
        final_result = ""
        for i in range(self.pos, len(text)):
            current_char = text[i]
            if self.character_is_symbol(current_char) and len(final_result) != 0:
                token = Token(INTEGER, int(final_result))
                return token
            if i == len(text) - 1 and current_char.isdigit():
                final_result += current_char
                token = Token(INTEGER, int(final_result))
                return token
            elif current_char.isdigit():
                final_result += current_char
                self.pos += 1
            elif current_char == "+":
                self.pos += 1
                token = Token(PLUS, current_char)
                return token
            elif current_char == "-":
                self.pos += 1
                token = Token(MINUS, current_char)
                return token
            elif current_char.isspace():
                self.pos += 1
                continue
            else:
                self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        self.eat(op.type)

        right = self.current_token
        self.eat(INTEGER)
        result = eval(f"{left.value}{op.value}{right.value}")
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
