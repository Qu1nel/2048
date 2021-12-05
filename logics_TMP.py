def get_index_from_number(num: int) -> tuple[int, int]:
    """Returns a tuple with indices based on the board cell number"""
    num -= 1
    return num // 4, num % 4
