from io import TextIOWrapper
    

def main() -> None:
    file: TextIOWrapper = open("3.txt", "rt")
    s: str = file.read()
    symbol_neighbors: set[str] = parse_by_symbol(s)
    numbers_by_symbol: dict[str, list[int]] = {}

    for symbol in symbol_neighbors:
        numbers_by_symbol[symbol] = []

    # total: int = sum_the_numbers(symbol_neighbors, s)
    total: int = 0
    add_numbers_to_symbol_list(numbers_by_symbol, s)
    for number_list in list(numbers_by_symbol.values()):
        if len(number_list) != 2:
            continue

        product: int = number_list[0] * number_list[1]
        total += product

    print(total)

 # Returns a set of coordinates that neighbor symbols
def parse_by_symbol(s: str) -> set[str]:
    neighbor_set: set[str] = set()
    row_idx: int = 1
    column_idx: int = 1

    for char in s:
        if char == ".":
            # do nothing
            pass
        elif char == "\n":
            row_idx += 1
            column_idx = 1
            continue
        elif char.isdigit():
            # do nothing
            pass
        elif char == "*":
            neighbor: str = f"{row_idx}, {column_idx}"
            neighbor_set.add(neighbor)

        column_idx += 1


    return neighbor_set

def sum_the_numbers(ns: set[str], s: str) -> int:
    total: int = 0
    row_idx: int = 1
    column_idx: int = 1

    column_start_idx: int = -1
    num: int = 0
    num_length: int = 0

    for char in s:
        if char == "\n":
            row_idx += 1
            column_idx = 1
            continue
        elif char.isdigit():
            if column_start_idx == -1:
                column_start_idx = column_idx
            num = num * 10 + int(char)
            num_length += 1

            column_idx += 1
            continue

        # if the char is a period (.), either add the number or move on
        if num == 0:
            # nothing to add, move on
            column_idx += 1
            continue
        else:
            # add num to the total if it is a neighbor to a symbol
            rows: list[int] = [row_idx - 1, row_idx, row_idx + 1]
            columns: list[int] = list(range(column_start_idx - 1, column_start_idx + num_length + 1))

            add: bool = False
            for r in rows:
                for c in columns:
                    neighbor: str = f"{r}, {c}"
                    if neighbor in ns:
                        add = True

            if add:
                if num == 586:
                    breakpoint()
                total += num

            column_start_idx = -1
            num = 0
            num_length = 0

        column_idx += 1

            

    return total

def add_numbers_to_symbol_list(nbs: dict[str, list[int]], s: str) -> None:
    row_idx: int = 1
    column_idx: int = 1

    column_start_idx: int = -1
    num: int = 0
    num_length: int = 0

    for char in s:
        if char == "\n":
            row_idx += 1
            column_idx = 1
            continue
        elif char.isdigit():
            if column_start_idx == -1:
                column_start_idx = column_idx
            num = num * 10 + int(char)
            num_length += 1

            column_idx += 1
            continue

        # if the char is a period (.), either add the number or move on
        if num == 0:
            # nothing to add, move on
            column_idx += 1
            continue
        else:
            # add num to the total if it is a neighbor to a symbol
            rows: list[int] = [row_idx - 1, row_idx, row_idx + 1]
            columns: list[int] = list(range(column_start_idx - 1, column_start_idx + num_length + 1))

            for r in rows:
                for c in columns:
                    neighbor: str = f"{r}, {c}"
                    if neighbor in nbs:
                        nbs[neighbor].append(num)

            column_start_idx = -1
            num = 0
            num_length = 0

        column_idx += 1



if __name__ == "__main__":
    main()
