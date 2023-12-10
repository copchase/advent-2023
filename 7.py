from typing import Self, Type
from io import TextIOWrapper
from pprint import pprint


def card_strength(card: str) -> int:
    card_strengths: list[str] = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
    return card_strengths.index(card) + 1


def vector_add(lst: list[int], x: int) -> None:
    for idx in range(len(lst)):
        lst[idx] += x


# baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaat i love object oriented programming
class Hand:
    def __init__(self: Self, cards: list[str], bid: int) -> None:
        self.strength: int = 0
        self.bid: int = bid
        self.cards: list[str] = cards

    @classmethod
    def from_cards_and_bid(cls: type["Hand"], cards_str: str, bid: int) -> "Hand":
        card_dict: dict[str, int] = {}
        cards: list[str] = list(cards_str)
        for card in cards:
            old_value: int = card_dict.get(card, 0)
            old_value += 1
            card_dict[card] = old_value

        card_counts: set[int] = set(card_dict.values())
        if len(card_dict) == 1 and 5 in card_counts:
            return FiveOfAKind(cards, bid)
        elif len(card_dict) == 2 and 4 in card_counts:
            return FourOfAKind(cards, bid)
        elif len(card_dict) == 2 and 3 in card_counts and 2 in card_counts:
            return FullHouse(cards, bid)
        elif len(card_dict) == 3 and 3 in card_counts:
            return ThreeOfAKind(cards, bid)
        elif len(card_dict) == 3 and 2 in card_counts and 1 in card_counts:
            return TwoPair(cards, bid)
        elif len(card_dict) == 4 and 2 in card_counts:
            return OnePair(cards, bid)

        return HighCard(cards, bid)

    @classmethod
    def from_cards_and_bid_with_jokers(cls: type["Hand"], cards_str: str, bid: int) -> "Hand":
        if "J" not in cards_str:
            return cls.from_cards_and_bid(cards_str, bid)

        card_dict: dict[str, int] = {}
        cards: list[str] = list(cards_str)
        for card in cards:
            old_value: int = card_dict.get(card, 0)
            old_value += 1
            card_dict[card] = old_value

        joker_count: int = card_dict.pop("J")
        card_counts: list[int] = list(card_dict.values())
        vector_add(card_counts, joker_count)
        card_counts_set: set[int] = set(card_counts)

        if joker_count >= 4:
            # JJJJJ or 1JJJJ
            return FiveOfAKind(cards, bid)
        elif joker_count == 3:
            # ex: 11JJJ or 12JJJ
            if 5 in card_counts:
                return FiveOfAKind(cards, bid)
            else:
                return FourOfAKind(cards, bid)
        elif joker_count == 2:
            # 111JJ
            # 112JJ
            # 123JJ

            if 5 in card_counts_set:
                return FiveOfAKind(cards, bid)
            elif 4 in card_counts_set:
                return FourOfAKind(cards, bid)
            else:
                return ThreeOfAKind(cards, bid)

        # joker count is 1
        if 5 in card_counts_set:
            # 1111J
            return FiveOfAKind(cards, bid)
        elif 4 in card_counts_set:
            # 1112J
            return FourOfAKind(cards, bid)
        elif 3 in card_counts_set:
            if card_counts.count(3) == 2:
                # 1122J
                return FullHouse(cards, bid)
            else:
                # 1123J
                return ThreeOfAKind(cards, bid)

        # 1234J
        return OnePair(cards, bid)

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, Hand):
            return False

        if self.strength != other.strength:
            return False

        if self.cards != other.cards:
            return False

        return True

    def __lt__(self: Self, other: object) -> bool:
        if not isinstance(other, Hand):
            raise TypeError(f"'<' not supported between instances of '{type(self)}' and '{type(other)}'")

        if self.strength < other.strength:
            return True
        elif self.strength > other.strength:
            return False

        for idx in range(len(self.cards)):
            self_card_strength: int = card_strength(self.cards[idx])
            other_card_strength: int = card_strength(other.cards[idx])

            if self_card_strength < other_card_strength:
                return True
            elif self_card_strength > other_card_strength:
                return False

        # if strength is equal and cards are equal, then they are equal
        return False

    def __gt__(self: Self, other: object) -> bool:
        if not isinstance(other, Hand):
            raise TypeError(f"'>' not supported between instances of '{type(self)}' and '{type(other)}'")

        if self.strength > other.strength:
            return True
        elif self.strength < other.strength:
            return False

        for idx in range(len(self.cards)):
            self_card_strength: int = card_strength(self.cards[idx])
            other_card_strength: int = card_strength(other.cards[idx])

            if self_card_strength > other_card_strength:
                return True
            elif self_card_strength < other_card_strength:
                return False

        # if strength is equal and cards are equal, then they are equal
        return False

    def __ne__(self: Self, other: object) -> bool:
        return not self.__eq__(other)

    def __le__(self: Self, other: object) -> bool:
        try:
            return not self.__gt__(object)
        except TypeError:
            raise TypeError(f"'<=' not supported between instances of '{type(self)}' and '{type(other)}'")

    def __ge__(self: Self, other: object) -> bool:
        try:
            return not self.__lt__(object)
        except TypeError:
            raise TypeError(f"'>= not supported between instances of '{type(self)}' and '{type(other)}'")

    def __repr__(self: Self) -> str:
        return f"{type(self)} cards:{self.cards}  bids:{self.bid}"


class FiveOfAKind(Hand):
    def __init__(self: Self, cards: list[str], bid: int) -> None:
        super().__init__(cards, bid)
        self.strength = 7


class FourOfAKind(Hand):
    def __init__(self: Self, cards: list[str], bid: int) -> None:
        super().__init__(cards, bid)
        self.strength = 6


class FullHouse(Hand):
    def __init__(self: Self, cards: list[str], bid: int) -> None:
        super().__init__(cards, bid)
        self.strength = 5


class ThreeOfAKind(Hand):
    def __init__(self: Self, cards: list[str], bid: int) -> None:
        super().__init__(cards, bid)
        self.strength = 4


class TwoPair(Hand):
    def __init__(self: Self, cards: list[str], bid: int) -> None:
        super().__init__(cards, bid)
        self.strength = 3


class OnePair(Hand):
    def __init__(self: Self, cards: list[str], bid: int) -> None:
        super().__init__(cards, bid)
        self.strength = 2


class HighCard(Hand):
    def __init__(self: Self, cards: list[str], bid: int) -> None:
        super().__init__(cards, bid)
        self.strength = 1


def main() -> None:
    file: TextIOWrapper = open("7.txt", "rt")

    hands: list[Hand] = []

    for line in file:
        if len(line) == 0:
            continue

        s: str = line.strip()
        ls: list[str] = s.split()
        cards: str = ls[0].strip()
        bid: int = int(ls[1].strip())

        hand: Hand = Hand.from_cards_and_bid_with_jokers(cards, bid)
        hands.append(hand)

    hands.sort()
    pprint(hands, indent=2, width=150)

    total: int = 0
    for idx in range(len(hands)):
        rank: int = idx + 1
        hand_bid: int = hands[idx].bid
        total += rank * hand_bid

    print(total)


if __name__ == "__main__":
    main()
