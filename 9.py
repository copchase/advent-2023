from io import TextIOWrapper


def main() -> None:
    file: TextIOWrapper = open("9.txt", "rt")

    total: int = 0
    for sequence in file:
        seq: list[int] = parse_sequence_str(sequence)

        # part 2
        seq.reverse()
        # end part 2

        total += find_next_value(seq)

    print(total)


def find_next_value(sequence: list[int]) -> int:
    stack: list[int] = []
    new_sequence: list[int] = sequence.copy()

    while any([x != 0 for x in new_sequence]):
        stack.append(new_sequence[-1])
        new_sequence = difference_list(new_sequence)

    # part 1
    # return sum(stack)
    # end part 1

    # part 2
    current_value: int = 0
    while len(stack) > 0:
        next_stack: int = stack.pop()
        current_value -= next_stack
        current_value *= -1

    return current_value
    # end part 2


def difference_list(sequence: list[int]) -> list[int]:
    out: list[int] = []
    for idx in range(len(sequence) - 1):

        # part 1
        # diff: int = sequence[idx + 1] - sequence[idx]
        # end part 1

        # part 2
        diff: int = sequence[idx] - sequence[idx + 1]
        # end part 2

        out.append(diff)

    return out


def parse_sequence_str(seq_str: str) -> list[int]:
    return [int(x) for x in seq_str.strip().split()]


if __name__ == "__main__":
    main()
