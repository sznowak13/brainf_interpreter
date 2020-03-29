import os

from brainf.display import InterpreterDisplay
from brainf.utils import get_corresponding_closing_bracket_index, getch


def get_input():
    """
    A function that can be mocked in tests.
    :return: input string
    """
    return getch()


class BrainFuckInterpreter:

    def __init__(self, table_size):
        self.size = table_size
        self.table = [0 for _ in range(table_size)]
        self.index = 0
        self._code = None
        self._output = []
        self._file_path = None
        self._loop_stack = []
        self._code_index = 0
        self._print_to_stdout = True
        self._cmd_map = {
            ">": self._increase_pointer_cell,
            "<": self._decrease_pointer_cell,
            "+": self._increase_pointer_value,
            "-": self._decrease_pointer_value,
            ",": self._get_value,
            ".": self._print_value,
            "[": self._start_loop,
            "]": self._end_loop,
        }

    def disable_stdout(self):
        self._print_to_stdout = False

    def enable_stdout(self):
        self._print_to_stdout = True

    def is_stdout_enabled(self):
        return self._print_to_stdout

    @property
    def current_value(self):
        return self.table[self.index]

    @current_value.setter
    def current_value(self, value):
        self.table[self.index] = value

    def _decrease_pointer_cell(self):
        if self.index == 0:
            self.index = self.size - 1
        else:
            self.index -= 1

    def _increase_pointer_cell(self):
        if self.index == self.size - 1:
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
        if self._print_to_stdout:
            print(char, end='', flush=True)
        return char

    def _print_value(self):
        self._output.append(self._print_char())

    def _get_value(self):
        inpt = get_input()
        try:
            self.current_value = ord(inpt)
        except TypeError:
            print("\nWARNING :: This command accepts only single characters, not strings. Adding only the first character.")
            self.current_value = ord(inpt[0])

    def _start_loop(self):
        if self.current_value:
            self._loop_stack.append(self._code_index)
        else:
            self._code_index += get_corresponding_closing_bracket_index(self._code[self._code_index:])

    def _end_loop(self):
        self._code_index = self._loop_stack.pop() - 1

    def _execute(self, cmd):
        cmd()

    def interpret(self, bf_text: str):
        self._code = bf_text
        while self._code_index < len(self._code):
            ch = self._code[self._code_index]
            if ch in self._cmd_map:
                self._execute(self._cmd_map[ch])
            self._code_index += 1
        self._code_index = 0
        self._code = None
        printed_chars = [*self._output]
        self._output = []
        return ''.join(printed_chars)

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


class InteractiveWrapper:
    def __init__(self, size: int):
        self._interpreter = BrainFuckInterpreter(size)
        self._display = InterpreterDisplay()
        self._special_cmd_map = {
            "reset": self.reset_interpreter,
            "quit": self.stop_interactive,
            "undo": self.undo
        }
        self.exec_line = 0
        self.interactive_mode = False
        self.prev_state = self._interpreter.table.copy(), self._interpreter.index

    def print_output(self, output):
        print(f"[Out {self.exec_line}]: {output}")

    def reset_interpreter(self):
        print("INFO :: Resetting interpreter...")
        self._interpreter.reset()

    def stop_interactive(self):
        print("\nINFO :: Quitting...")
        self.interactive_mode = False

    def undo(self):
        print("INFO :: Undoing previous command")
        self._interpreter.table, self._interpreter.index = self.prev_state

    def start_interactive(self):
        self.interactive_mode = True
        self._interpreter.disable_stdout()
        self._display.print_welcome()
        while self.interactive_mode:
            out = ''
            self._display.print_brainf_table(self._interpreter)
            try:
                bf_cmd = self._display.get_input(self.exec_line)
                if bf_cmd in self._special_cmd_map:
                    self._special_cmd_map[bf_cmd]()
                else:
                    self.prev_state = self._interpreter.table.copy(), self._interpreter.index
                    out = self._interpreter.interpret(bf_cmd)
                if out:
                    self.print_output(out)
            except KeyboardInterrupt:
                self.stop_interactive()
            self.exec_line += 1

    def interpret_file(self, file_path):
        self._interpreter.interpret_file(file_path)

    def set_file_out(self, file_path):
        self._interpreter.set_file_out(file_path)
