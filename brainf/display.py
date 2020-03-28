def get_version():
    with open("version") as f:
        v = f.read()
    return v


class InterpreterDisplay:

    def __init__(self):
        self.version = get_version()

    def get_input(self, exec_line):
        cmd = input(f'[In {exec_line}]: ')
        return cmd

    def _print(self, text, line_break=False):
        print(text, end='' if not line_break else '\n')

    def print_welcome(self):
        print("\n  ** Welcome!")
        print(f"  ** Brainf Interactive Interpreter version {self.version}")
        print("  ** Author: Szymon 'Shaiibon' Nowak")
        print("  ** github: https://github.com/sznowak13/brainf_interpreter\n")

    def print_brainf_table(self, bf_i):
        # TODO refactor xD
        left_buffer = 0
        right_buffer = 0
        pointer_on = bf_i.index
        left_range = pointer_on - 4
        if left_range <= 0:
            left_range = 1
        if left_range > 1:
            left_buffer = left_range - 1
        right_range = pointer_on + 4
        if right_range >= bf_i.size - 1:
            right_range = bf_i.size - 2
        if right_range < bf_i.size - 2:
            right_buffer = right_range + 1
        table_str = f"[ {bf_i.table[0]} |"
        index_str = "0".center(len(table_str), ' ')
        ptr_str = '^'.center(len(table_str), ' ')
        if left_buffer:
            buffer_index_str = f"1-{left_range - 1}"
            buffer_str = f"{'...'.center(len(buffer_index_str) + 2, ' ')}|"
            buffer_index_str = f"1-{left_range - 1}".center(len(buffer_str), ' ')
            index_str += buffer_index_str
            table_str += buffer_str
        for i in range(left_range, right_range + 1):
            pov_str = f" {bf_i.table[i]} |"
            index_str += f"{i}".center(len(pov_str), ' ')
            if pointer_on == i:
                ptr_str = f"{' ' * len(table_str)}{'^'.center(len(pov_str))}"
            table_str += pov_str
        if right_buffer:
            buffer_index_str = f"{right_range + 1}-{bf_i.size - 2}"
            buffer_str = f"{'...'.center(len(buffer_index_str) + 2, ' ')}|"
            buffer_index_str = f"{right_range + 1}-{bf_i.size - 2}".center(len(buffer_str), ' ')
            index_str += buffer_index_str
            table_str += buffer_str
        end_str = f" {bf_i.table[-1]} ]"
        index_str += f"{bf_i.size - 1}".center(len(end_str), ' ')
        if pointer_on == bf_i.size - 1:
            ptr_str = f"{' ' * len(table_str)}{'^'.center(len(end_str))}"
        table_str += end_str
        print()
        print(f"\tState: {table_str}")
        print(f"\tIndex: {index_str}")
        print(f"\tPoint: {ptr_str}")
        print()
