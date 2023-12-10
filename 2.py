from typing import Self


class Game:
    def __init__(self: Self, s: str) -> None:
        s = s.removesuffix("\n")
        game_metadata: list[str] = s.split(": ")
        self.game_id: int = int(game_metadata[0].split(" ")[1])
        pulls: str = game_metadata[1]
        rounds: list[str] = pulls.split(";")
        self.max_red: int = 0
        self.max_green: int = 0
        self.max_blue: int = 0

        for r in rounds:
            red: int
            green: int
            blue: int
            red, green, blue = get_count_of_colors(r)

            self.max_red = max(self.max_red, red)
            self.max_green = max(self.max_green, green)
            self.max_blue = max(self.max_blue, blue)

    def __repr__(self: Self) -> str:
        return f"Game {self.game_id}: {self.max_red} red, {self.max_green} green, {self.max_blue} blue"

    def power(self: Self) -> int:
        return self.max_red * self.max_green * self.max_blue


def main():
    file = open("2.txt", "rt")
    games: list[Game] = []
    for line in file:
        new_game = Game(line)
        games.append(new_game)
        print(new_game)

    # filtered_games: list[Game] = filter_games_matching_max_colors(games)

    sum: int = 0
    # for fg in filtered_games:
    #     sum += fg.game_id

    for game in games:
        sum += game.power()

    print(sum)


def filter_games_matching_max_colors(games: list[Game]) -> list[Game]:
    allowed_max_red: int = 12
    allowed_max_green: int = 13
    allowed_max_blue: int = 14

    filtered_games: list[Game] = []
    for game in games:
        if game.max_red > allowed_max_red or game.max_green > allowed_max_green or game.max_blue > allowed_max_blue:
            continue

        filtered_games.append(game)

    return filtered_games


# always returns in R G B
def get_count_of_colors(s: str) -> tuple[int, int, int]:
    red: int = 0
    green: int = 0
    blue: int = 0

    by_color: list[str] = s.split(", ")
    for color in by_color:
        color: str = color.strip()
        print(color)
        if color.endswith("red"):
            red = int(color.removesuffix(" red"))
        elif color.endswith("green"):
            green = int(color.removesuffix(" green"))
        elif color.endswith("blue"):
            blue = int(color.removesuffix(" blue"))

        print(red, green, blue)

    return red, green, blue


if __name__ == "__main__":
    main()
