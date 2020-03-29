"""
Brainfuck language interpreter in Python 3.7
Brainfuck is a language created in 1993 by Urban Müller.
https://en.wikipedia.org/wiki/Brainfuck
Version: 0.2
Author: Szymon "ShaiiboN" Nowak
Special thanks to: Maciej "DavidGildour" Nowak
"""
import os
from typing import Callable

from brainf.display import InterpreterDisplay
from brainf.utils import get_corresponding_closing_bracket_index, getch


def get_input():
    """
    An input function that can be mocked in tests.
    :return: input string
    """
    return getch()


class BrainFuckInterpreter:
    """
    Core class containing interpreter logic.
    """

    def __init__(self, table_size: int):
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
        """
        Disables printing to standard output. Used by InterpreterWrapper to handle printing output by itself.
        """
        self._print_to_stdout = False

    def enable_stdout(self):
        """
        Enables printing to standard output when it was disabled.
        """
        self._print_to_stdout = True

    def is_stdout_enabled(self) -> bool:
        """
        Check if standard output printing is enabled.
        :return: is printing enabled
        """
        return self._print_to_stdout

    @property
    def current_value(self):
        """
        Property for value on the current pointer position.
        :return: Current cell value
        """
        return self.table[self.index]

    @current_value.setter
    def current_value(self, value: int):
        """
        Setter for current value.
        :param value: Value to set
        """
        self.table[self.index] = value

    def _decrease_pointer_cell(self):
        """
        Decreases pointer to the previous cell. If the pointer is on the first cell, wrap-around to the last cell.
        """
        if self.index == 0:
            self.index = self.size - 1
        else:
            self.index -= 1

    def _increase_pointer_cell(self):
        """
        Increase pointer to the next cell. If the pointer is on the last cell, wrap-around to the first one.
        """
        if self.index == self.size - 1:
            self.index = 0
        else:
            self.index += 1

    def _increase_pointer_value(self):
        """
        Increase value in the cell that the pointer is currently pointing by 1.
        """
        self.current_value += 1

    def _decrease_pointer_value(self):
        """
        Decrease value in the cell that the pointer is currently pointing by 1.
        :return:
        """
        self.current_value -= 1

    def _print_char(self):
        """
        Prints a character based on the ASCII value of the current cell.
        Can print to both file (when file output is set - see `self.set_file_out()` method)
        and standard output (when printing to standard output is enabled - see `self.is_stdout_enabled()` getter).
        :return: Single ASCII char.
        """
        char = chr(self.current_value)
        if self._file_path:
            with open(self._file_path, 'a') as f:
                f.write(char)
        if self._print_to_stdout:
            print(char, end='', flush=True)
        return char

    def _print_value(self):
        """
        Wrapper method for `self._print_char()`. Gathers all outputted characters in `self._output` list.
        """
        self._output.append(self._print_char())

    def _get_value(self):
        """
        Gets a single character from standard input and stores its ASCII value in the current pointer position.
        """
        inpt = get_input()
        try:
            self.current_value = ord(inpt)
        except TypeError:
            print("\nWARNING :: This command accepts only single characters, not strings. Adding only the first character.")
            self.current_value = ord(inpt[0])

    def _start_loop(self):
        """
        If the value on the current cell is not 0, marks the starting of the loop by pushing the `[` symbol index to the loop stack.
        If, however, the value is 0, it skips to the corresponding `]` symbol in the code.
        """
        if self.current_value:
            self._loop_stack.append(self._code_index)
        else:
            self._code_index += get_corresponding_closing_bracket_index(self._code[self._code_index:])

    def _end_loop(self):
        """
        Ends the loop by returning to the corresponding `[` symbol in the code and pops the top value from the
        loop stack.
        """
        self._code_index = self._loop_stack.pop() - 1

    def _execute(self, cmd: Callable):
        """
        Convenience method for executing a brainfuck command.
        :param cmd: a brainfuck interpreter command to be executed
        """
        cmd()

    def interpret(self, bf_text: str):
        """
        Main entry for interpreting brainfuck commands.
        Reads a command character by character and executes corresponding method.
        If a character is not a valid brainfuck symbol it skips over it - so there can be comments in code
        and the program will execute just fine. It also stores every outputted character in `self._output` list
        for the InterpreterWrapper.
        :param bf_text: a brainfuck source code
        :return: All of the characters outputted by the interpreter
        """
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

    def interpret_file(self, file_path: str):
        """
        Interprets a brainfuck source code from file.
        :param file_path: Path to brainfuck program.
        """
        with open(file_path) as f:
            self.interpret(f.read())

    def set_file_out(self, file_path: str):
        """
        Sets an file where the output of the file will be wrote.
        :param file_path: A path to a output file.
        """
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as f:
                f.write('==== Created by Brainfuck interpreter ===\n')
        self._file_path = file_path

    def reset(self):
        """
        Resets the interpreter, setting all the values to 0 and pointer to the first cell.
        It also resets the loop stack and code index - just to be sure.
        """
        self._code_index = 0
        self.index = 0
        self._loop_stack = []
        self.table = [0 for _ in range(self.size)]


class InteractiveWrapper:
    """
    Interactive wrapper for BrainFuckInterpreter. It wraps the functionality of the former for the convenience
    of the interactive iPython like console.
    """
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
