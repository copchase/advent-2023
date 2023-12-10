import functools
import operator

time_limits: list[int] = [47847467]
distances_to_beat: list[int] = [207139412091014]


def get_distance(button_time: int, time_limit: int) -> int:
    """
    Calculates the distance travelled if the button is pushed for button_time milliseconds
    and the race has an overall time limit of time_limit milliseconds.

    Each millisecond of button pushing increases the constant speed by 1 millimetter per millisecond.
    """
    speed: int = button_time
    remainder_time: int = time_limit - button_time
    return speed * remainder_time


def find_min_and_max_button_times(time_limit: int, distance_to_beat: int) -> tuple[int, int]:
    """
    Finds the minimum and maximum button times in order to beat the given distance for the race
    with the given time limit.

    Returns the ints in order of min, then max.
    """

    # we start with the theoretical max button_time which is time_limit
    # from there we can find the middle value between 0 and time_limit
    # and do a binary search because only the min and max values are of
    # importance here
    min_button_time: int = find_min_button_time(time_limit, distance_to_beat)
    max_button_time: int = find_max_button_time(time_limit, distance_to_beat)
    return min_button_time, max_button_time


def find_min_button_time(time_limit: int, distance_to_beat: int) -> int:
    # left side binary search
    # assumed standard ordering (smallest left, biggest right)
    left: int = 0
    right: int = time_limit // 2
    middle: int = 0

    distance: int = -1
    match: int = -1
    searched_numbers: set[int] = set()
    while left <= right:
        middle = (left + right) // 2
        distance = get_distance(middle, time_limit)

        if distance < distance_to_beat:
            # we scored too low, drop the left half of the search zone
            left = middle
        elif distance > distance_to_beat:
            # scored too high, drop the right half
            right = middle
            # in case the desired distance isn't in the array, save the most recent
            # value that did beat the distance
            match = middle
        elif distance == distance_to_beat:
            # we found a match!
            match = middle

        if middle in searched_numbers:
            # the desired distance isn't in the array, break
            break

        searched_numbers.add(middle)

    distance = get_distance(match, time_limit)
    # we found the desired distance, but we want to iterate UP until we beat the distance
    while distance <= distance_to_beat:
        match += 1
        distance = get_distance(match, time_limit)

    return match


def find_max_button_time(time_limit: int, distance_to_beat: int) -> int:
    # right side reversed binary search
    # we assume the array of distances is in reversed order (biggest on left, smallest on right)
    left: int = time_limit // 2
    right: int = time_limit
    middle: int = 0

    distance: int = -1
    match: int = -1
    searched_numbers: set[int] = set()
    while left <= right:
        middle = (left + right) // 2
        distance: int = get_distance(middle, time_limit)

        if distance > distance_to_beat:
            # we scored too high, drop the left half of the search zone

            # remember this is reverse binary search, we are assuming the right side
            # has the value
            left = middle
            # same thing as standard binary search, save this value just in case
            # the desired distance isn't found
            match = middle
        elif distance < distance_to_beat:
            # scored too low, drop the right half
            right = middle
        elif distance == distance_to_beat:
            # we found a match!
            match = middle

        if middle in searched_numbers:
            # the desired distance isn't in the array, break
            break

        searched_numbers.add(middle)

    distance = get_distance(match, time_limit)
    # we found the desired distance, but we want to iterate DOWN until we beat the distance
    # of course if we've already beat the distance, this while loop will finish immediately
    while distance <= distance_to_beat:
        match -= 1
        distance = get_distance(match, time_limit)

    return match


def main() -> None:
    ways_to_beat: list[int] = []

    for idx in range(len(time_limits)):
        time_limit: int = time_limits[idx]
        distance_to_beat: int = distances_to_beat[idx]

        min_button_time: int
        max_button_time: int
        min_button_time, max_button_time = find_min_and_max_button_times(time_limit, distance_to_beat)

        print(f"min button time: {min_button_time} max button time: {max_button_time}")

        ways_to_beat.append(max_button_time - min_button_time + 1)

    # print(functools.reduce(operator.mul, ways_to_beat))
    print(ways_to_beat)



if __name__ == "__main__":
    main()
