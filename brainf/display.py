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

    def _normalize_left(self, ptr_on):
        buffer = 0
        _range = ptr_on - 4
        if _range <= 0:
            _range = 1
        if _range > 1:
            buffer = _range - 1
        return _range, buffer

    def _normalize_right(self, ptr_on, table_size):
        buffer = 0
        _range = ptr_on + 4
        if _range >= table_size - 1:
            _range = table_size - 2
        if _range < table_size - 2:
            buffer = _range + 1
        return _range, buffer

    def _get_buffer_cells(self, low, high):
        buffer_index_str = f"{low}-{high}"
        buffer_str = f"{'...'.center(len(buffer_index_str) + 2, ' ')}|"
        buffer_index_str = buffer_index_str.center(len(buffer_str) - 1, ' ')
        return buffer_index_str, buffer_str

    def _get_index_and_pov_strs(self, table, cell_no):
        pov_str = f"{table[cell_no]}"
        index_str = f"{cell_no}".center(len(pov_str), ' ')
        pov_str = pov_str.center(len(index_str) + 2, ' ') + '|'
        index_str = index_str.center(len(pov_str), ' ')
        return pov_str, index_str

    def print_welcome(self):
        print("\n  ** Welcome!")
        print(f"  ** Brainf Interactive Interpreter version {self.version}")
        print("  ** Author: Szymon 'Shaiibon' Nowak")
        print("  ** github: https://github.com/sznowak13/brainf_interpreter\n")

    def print_brainf_table(self, bf_i):
        # TODO refactor xD
        pointer_on = bf_i.index
        left_range, left_buffer = self._normalize_left(pointer_on)
        right_range, right_buffer = self._normalize_right(pointer_on, bf_i.size)
        table_str = f"[ {bf_i.table[0]} |"
        index_str = "0".center(len(table_str), ' ')
        ptr_str = '^'.center(len(table_str), ' ')
        if left_buffer:
            buffer_index_str, buffer_str = self._get_buffer_cells(1, left_range - 1)
            index_str += buffer_index_str
            table_str += buffer_str
        for i in range(left_range, right_range + 1):
            pov_str, curr_index_str = self._get_index_and_pov_strs(bf_i.table, i)
            index_str += curr_index_str
            if pointer_on == i:
                ptr_str = f"{' ' * len(table_str)}{'^'.center(len(pov_str))}"
            table_str += pov_str
        if right_buffer:
            buffer_index_str, buffer_str = self._get_buffer_cells(right_range + 1, bf_i.size - 2)
            index_str += buffer_index_str
            table_str += buffer_str
        end_str = f"{bf_i.table[-1]}"
        end_index_str = f"{bf_i.size - 1}".center(len(end_str), ' ')
        end_str = end_str.center(len(end_index_str), ' ') + "]"
        end_index_str = end_index_str.center(len(end_str) + 1, ' ')
        index_str += end_index_str
        if pointer_on == bf_i.size - 1:
            ptr_str = f"{' ' * len(table_str)}{'^'.center(len(end_str))}"
        table_str += end_str
        print(f"\n\tState: {table_str}")
        print(f"\tIndex: {index_str}")
        print(f"\tPoint: {ptr_str}\n")
