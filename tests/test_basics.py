from unittest.mock import patch
import pytest

from brainf import Interpreter


def assert_file_is(string):
    with open('tests/resources/brains_out.txt') as f:
        assert f.read() == string


@pytest.mark.parametrize('table_size', [100, 10_000, 666, 456789])
def test_interpreter_inits_with_a_proper_table(table_size):
    i = Interpreter(table_size)
    assert len(i.table) == table_size
    assert isinstance(i.table, list)
    assert all(e == 0 for e in i.table)


def test_interpreter_increments_pointer(interpreter):
    assert interpreter.index == 0
    interpreter.interpret('>')
    assert interpreter.index == 1
    interpreter.interpret('>>>')
    assert interpreter.index == 4


def test_interpreter_decrements_pointer(interpreter):
    interpreter.index = 10
    interpreter.interpret('<')
    assert interpreter.index == 9
    interpreter.interpret('<<<')
    assert interpreter.index == 6


def test_interpreter_increments_pointer_correctly_on_border_cases(interpreter):
    # Interpreter from fixture has 100 cells in table.
    assert interpreter.index == 0
    interpreter.interpret('<')
    assert interpreter.index == 100
    interpreter.interpret('>')
    assert interpreter.index == 0


def test_interpreter_increments_pointer_value(interpreter):
    assert interpreter.current_value == 0
    interpreter.interpret('+')
    assert interpreter.current_value == 1
    interpreter.interpret('+++')
    assert interpreter.current_value == 4


def test_interpreter_decrements_pointer_value(interpreter):
    assert interpreter.current_value == 0
    interpreter.interpret('-')
    assert interpreter.current_value == -1
    interpreter.interpret('---')
    assert interpreter.current_value == -4


def test_interpreter_can_increment_multiple_cells(interpreter):
    assert interpreter.current_value == 0
    interpreter.interpret('+++++')
    assert interpreter.current_value == 5
    interpreter.interpret('>+++++')
    assert interpreter.current_value == 5
    interpreter.interpret('<++')
    assert interpreter.current_value == 7
    interpreter.interpret('>+++')
    assert interpreter.current_value == 8
    assert interpreter.table[:2] == [7, 8]  # First to elements of the table


def test_interpreter_can_decrement_multiple_cells(interpreter):
    assert interpreter.current_value == 0
    interpreter.interpret('---')
    assert interpreter.current_value == -3
    interpreter.interpret('>--')
    assert interpreter.current_value == -2
    interpreter.interpret('<--')
    assert interpreter.current_value == -5
    interpreter.interpret('>-')
    assert interpreter.current_value == -3
    assert interpreter.table[:2] == [-5, -3]  # First to elements of the table


def test_changing_values(interpreter):
    interpreter.interpret('+++>--->+-+-')
    assert interpreter.table[:3] == [3, -3, 0]
    interpreter.interpret('<<+>+++++')
    assert interpreter.table[:3] == [4, 2, 0]  # 420 BLAZE IT


def test_printing_ascii_value(small_interpreter, file_out):
    small_interpreter.interpret('+' * 65)  # ASCII 'A' == 65
    small_interpreter.interpret('.')
    assert_file_is('A')
    small_interpreter.interpret('.')
    assert_file_is('AA')
    small_interpreter.interpret('+.+.+.+.')
    assert_file_is('AABCDE')


@pytest.mark.parametrize('input_char, char_value', [('A', 65), ('B', 66), ('C', 67), ('+', 43), ('a', 97), ('\\', 92)])
def test_ascii_input(small_interpreter, input_char, char_value):
    with patch('brainf.interpreter.get_input', return_value=input_char):
        small_interpreter.interpret(',')
        assert small_interpreter.current_value == char_value


def test_loop_adding(small_interpreter):
    small_interpreter.interpret('+++[>++<-]')  # Adding 3 to first cell, then lopping until first cell is 0 and second is 6
    assert small_interpreter.table[:2] == [0, 6]
    small_interpreter.reset()
    small_interpreter.interpret('+++[>++<-]>[>++<-]')
    assert small_interpreter.table[:3] == [0, 0, 12]


def test_interpreter_reset(small_interpreter):
    small_interpreter.interpret('+++>+++>+++')
    assert small_interpreter.table[:3] == [3, 3, 3]
    small_interpreter.reset()
    assert small_interpreter.table[:3] == [0, 0, 0]
    small_interpreter.interpret('++>++>++')
    assert small_interpreter.table[:3] == [2, 2, 2]


def test_interpreting_from_file(small_interpreter):
    small_interpreter.interpret_file('tests/resources/to_interpret.bf')
    assert small_interpreter.table[:3] == [3, 3, 3]
