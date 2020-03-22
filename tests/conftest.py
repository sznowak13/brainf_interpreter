import pytest

from brainf import Interpreter


@pytest.fixture
def interpreter():
    i = Interpreter(100)
    i.set_file_out('tests/resources/brains_out.txt')
    return i


@pytest.fixture
def small_interpreter():
    i = Interpreter(10)
    i.set_file_out('tests/resources/brains_out.txt')
    return i


@pytest.fixture
def file_out():
    with open('tests/resources/brains_out.txt', 'w') as f:
        f.write('')
    yield
    with open('tests/resources/brains_out.txt', 'w') as f:
        f.write('')
