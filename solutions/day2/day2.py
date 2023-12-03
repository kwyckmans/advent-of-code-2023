from dataclasses import dataclass
from pathlib import Path
from aoc_utils import loader


@dataclass
class GameData:
    id: int
    red: int = 1
    green: int = 1
    blue: int = 1


def get_game_data(raw_input: str) -> GameData:
    game_id = int(raw_input.split(":")[0].split(" ")[1])
    # print(f"{raw_input} has id: {game_id}")

    red = 0
    blue = 0
    green = 0

    plays = raw_input.split(":")[1].split(";")
    for play in plays:
        for draw in play.split(","):
            count = int(draw.lstrip().split(" ")[0])
            # print(f"draw {draw} has count {count}")
            if "red" in draw:
                red = max(red, count)
            elif "blue" in draw:
                blue = max(blue, count)
            elif "green" in draw:
                green = max(green, count)

    return GameData(game_id, red=red, blue=blue, green=green)


if __name__ == "__main__":
    p = Path(__file__).parent / "input.txt"

    RED = 12
    GREEN = 13
    BLUE = 14

    id_sum, power = 0, 0

    for game in loader.load_per_line(p):
        game_data = get_game_data(game)
        if game_data.red <= RED and game_data.green <= GREEN and game_data.blue <= BLUE:
            id_sum += game_data.id
        power += game_data.red * game_data.blue * game_data.green

    print(id_sum)
    print(power)
