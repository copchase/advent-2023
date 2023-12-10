from collections import deque
from io import TextIOWrapper
from typing import Self


class Card:
    def __init__(self: Self, s: str) -> None:
        card_id: int
        winners: set[int]
        possession: set[int]
        card_id, winners, possession = parse_card(s)
        self.id: int = card_id
        self.winners: set[int] = winners
        self.possession: set[int] = possession

    def points(self: Self) -> int:
        quantity: int = len(self.winners.intersection(self.possession))
        if quantity == 0:
            return 0

        return 2 ** (quantity - 1)

    def num_of_matches(self: Self) -> int:
        return len(self.winners.intersection(self.possession))


_CARD_VALUE: dict[int, list[int]] = {}


def main() -> None:
    file: TextIOWrapper = open("4.txt", "rt")
    for line in file:
        if len(line) == 0:
            continue

        c = Card(line)
        _CARD_VALUE[c.id] = list(range(c.id + 1, c.id + c.num_of_matches() + 1))

    total_cards: int = 0
    card_ids: deque[int] = deque(list(_CARD_VALUE.keys()))

    while len(card_ids) > 0:
        total_cards += 1
        next_key: int = card_ids.popleft()
        next_values: list[int] = _CARD_VALUE[next_key]
        card_ids.extend(next_values)


def parse_card(s: str) -> tuple[int, set[int], set[int]]:
    card_id: int = int(s.split(": ")[0].removeprefix("Card").strip())
    numbers: str = s.split(": ")[1].strip()
    winners: list[int] = [int(x.strip()) for x in numbers.split("|")[0].strip().split(" ") if len(x) > 0]
    possession: list[int] = [int(x.strip()) for x in numbers.split("|")[1].strip().split(" ") if len(x) > 0]
    return card_id, set(winners), set(possession)


if __name__ == "__main__":
    main()
