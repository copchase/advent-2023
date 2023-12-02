import re
from re import Match


def main():
    file = open("1.txt", "rt")
    sum: int = 0
    for line in file:
        # first_digit: int = find_first_digit(line)
        # last_digit: int = find_last_digit(line)

        first_digit: int = find_first_digit_as_number_or_word(line)
        last_digit: int = find_last_digit_as_number_or_word(line)

        sum += first_digit * 10 + last_digit

    print(sum)

def find_first_digit(s: str) -> int:
    for char in s:
        if char.isdigit():
            return int(char)
        
    raise RuntimeError("no digit in string")

def find_last_digit(s: str) -> int:
    s_frag: list[str] = list(s)
    s_frag.reverse()

    for char in s_frag:
        if char.isdigit():
            return int(char)
        
    raise RuntimeError("no digit in string")

def find_first_digit_as_number_or_word(s: str) -> int:
    match: list[str] = re.findall(r"^.*?(\d|one|two|three|four|five|six|seven|eight|nine)", s)    
    return convert_to_number(match[0])


def find_last_digit_as_number_or_word(s: str) -> int:
    match: list[str] = re.findall(r".*(\d|one|two|three|four|five|six|seven|eight|nine).*$", s)   
    return convert_to_number(match[0])

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
