def get_corresponding_closing_bracket_index(bf_str: str):
    """
    Get a ] bracket index that is closing the corresponding [ bracket.
    Param bf_str must start with a [ bracket
    :param bf_str: Brainf code string that STARTS with [
    :return: index of ] bracket in the bf_str
    """
    if not bf_str.startswith('['):
        raise Exception("Should start with '[' symbol.")
    level = 0
    for i, ch in enumerate(bf_str):
        if ch == '[':
            level += 1
        elif ch == ']':
            if level == 1:
                return i
            else:
                level -= 1
