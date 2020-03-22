import os

from brainf.utils import get_corresponding_closing_bracket_index


def get_input():
    """
    A function that can be mocked in tests.
    :return: input string
    """
    return input()


class BrainFuckInterpreter:

    def __init__(self, table_size):
        self.size = table_size
        self.table = [0 for _ in range(table_size)]
        self.index = 0
        self._file_path = None
        self._loop_stack = []
        self._code_index = 0

    @property
    def current_value(self):
        return self.table[self.index]

    @current_value.setter
    def current_value(self, value):
        self.table[self.index] = value

    def _decrease_pointer_cell(self):
        if self.index == 0:
            self.index = self.size
        else:
            self.index -= 1

    def _increase_pointer_cell(self):
        if self.index == self.size:
            self.index = 0
        else:
            self.index += 1

    def _increase_pointer_value(self):
        self.current_value += 1

    def _decrease_pointer_value(self):
        self.current_value -= 1

    def _print_char(self):
        char = chr(self.current_value)
        if self._file_path:
            with open(self._file_path, 'a') as f:
                f.write(char)
        print(char, end='', flush=True)

    def _get_value(self):
        inpt = get_input()
        self.current_value = ord(inpt)

    def interpret(self, bf_text: str):
        while self._code_index < len(bf_text):
            ch = bf_text[self._code_index]
            if ch == '>':
                self._increase_pointer_cell()
            elif ch == '<':
                self._decrease_pointer_cell()
            elif ch == '+':
                self._increase_pointer_value()
            elif ch == '-':
                self._decrease_pointer_value()
            elif ch == '.':
                self._print_char()
            elif ch == ',':
                self._get_value()
            elif ch == '[':
                if self.current_value:
                    self._loop_stack.append(self._code_index)
                else:
                    self._code_index += get_corresponding_closing_bracket_index(bf_text[self._code_index:])
            elif ch == ']':
                self._code_index = self._loop_stack.pop() - 1
            self._code_index += 1
        self._code_index = 0

    def interpret_file(self, file_path):
        with open(file_path) as f:
            self.interpret(f.read())

    def set_file_out(self, file_path):
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as f:
                f.write('==== Created by Brainfuck interpreter ===\n')
        self._file_path = file_path

    def reset(self):
        self._code_index = 0
        self.index = 0
        self._loop_stack = []
        self.table = [0 for _ in range(self.size)]
