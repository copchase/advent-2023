def main():
    file = open("1.txt", "rt")
    sum: int = 0
    for line in file:
        first_digit: int
        last_digit: int
        first_digit, last_digit = find_first_and_last_digits_in_string(line)

        sum += first_digit * 10 + last_digit

    print(sum)


def find_first_and_last_digits_in_string(s: str) -> tuple[int, int]:
    key_words: list[str] = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]

    # track starting index and length, like C pointers to char arrays

    idxMap: dict[int, int] = {}

    for word in key_words:
        idx: int = -1
        while True:  # words can repeat, search for all of them
            idx = s.find(word, idx + 1)

            if idx == -1:
                break

            length: int = len(word)

            idxMap[idx] = length

    min_idx: int = min(idxMap.keys())
    max_idx: int = max(idxMap.keys())

    first_digit: int = convert_to_number(s[min_idx : min_idx + idxMap[min_idx]])
    last_digit: int = convert_to_number(s[max_idx : max_idx + idxMap[max_idx]])
    return first_digit, last_digit


def convert_to_number(x: str) -> int:
    if len(x) == 1:
        return int(x)

    mapper: dict[str, int] = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    return mapper[x]


if __name__ == "__main__":
    main()
