from io import TextIOWrapper
from  typing import Self
import logging

class MapTriplet:
    def __init__(self: Self, src_start: int, dst_start: int, range_len: int) -> None:
        self._src_start: int = src_start
        self._dst_start: int = dst_start
        self._range_len: int = range_len

    def find_dst(self: Self, src: int) -> tuple[int, bool]:
        """
        Finds the dst value for the given src value, and returns a bool showing whether
        the search was successful.
        """
        # the src_start must be included, use < or >
        open_max_src: int = self._src_start + self._range_len
        if self._src_start <= src and src < open_max_src:
            # we're in the boundary, find the difference
            diff: int = src - self._src_start
            return self._dst_start + diff, True

        return 0, False

    
    def __repr__(self) -> str:
        return f"src_start: {self._src_start} dst_start: {self._dst_start} range_length: {self._range_len}"

class MapTripletList:
    def __init__(self: Self, s: str) -> None:
        self._triplet_list: list[MapTriplet] = []

        # parse the string into the triplets we need
        parts: list[str] = s.split("\n")
        # remove the header, we don't need that
        self._name: str = parts[0]
        logging.info(f"creating map triplet list for {parts[0]}")
        parts = parts[1:]
        # the problem statement has defined the first number as DST
        # the second number as SRC
        # the third number as range length

        for part in parts:
            numbers: list[str] = part.split(" ")
            dst_start: int = int(numbers[0])
            src_start: int = int(numbers[1])
            range_len: int = int(numbers[2])

            triplet: MapTriplet = MapTriplet(src_start, dst_start, range_len)
            self._triplet_list.append(triplet)

    def find_dst(self: Self, src: int) -> int:
        """
        Searches all triplets in the collection for a dst value for the given src value.

        If no value is found, it is assumed that dst is equal to src, so src will be returned.
        """
        for triplet in self._triplet_list:
            dst: int
            found: bool

            dst, found = triplet.find_dst(src)
            if found:
                return dst
            
        return src
    

class Mapper:
    def __init__(self: Self) -> None:
        self._transformers: list[MapTripletList] = []

    def append(self: Self, map_triplet_list: MapTripletList) -> None:
        self._transformers.append(map_triplet_list)

    def fully_map(self: Self, src_values: list[int]) -> list[int]:
        """
        For a list of src values, map them to dst values for each transforming 
        MapTripletList that the Mapper holds
        """
        out: list[int] = src_values.copy()

        for transformer in self._transformers:
            out = [transformer.find_dst(src) for src in out]

        return out
    
    def map(self: Self, src: int) -> int:
        dst: int = src
        for transformer in self._transformers:
            dst = transformer.find_dst(dst)

        return dst
    
    def map_range(self: Self, r: range) -> list[range]:
        """For a given range, returns a list of corresponding dst ranges"""
        return []



def main() -> None:
    file: TextIOWrapper = open("5.txt", "rt")
    s: str = file.read()
    parts: list[str] = s.split("\n\n")
    seeds_str: str = parts[0]
    seeds: list[int] = parse_seeds(seeds_str)

    seed_to_soil_map: MapTripletList = MapTripletList(parts[1])
    seed_to_fertilizer: MapTripletList = MapTripletList(parts[2])
    fertilizer_to_water: MapTripletList = MapTripletList(parts[3])
    water_to_light: MapTripletList = MapTripletList(parts[4])
    light_to_temperature: MapTripletList = MapTripletList(parts[5])
    temperature_to_humidity: MapTripletList = MapTripletList(parts[6])
    humidity_to_location: MapTripletList = MapTripletList(parts[7])

    mapper: Mapper = Mapper()
    mapper.append(seed_to_soil_map)
    mapper.append(seed_to_fertilizer)
    mapper.append(fertilizer_to_water)
    mapper.append(water_to_light)
    mapper.append(light_to_temperature)
    mapper.append(temperature_to_humidity)
    mapper.append(humidity_to_location)

    locations: list[int] = mapper.fully_map(seeds)
    min_location: int = min(locations)

    print(min_location)

def parse_seeds(seeds_str: str) -> list[int]:
    # part 1
    return [int(x) for x in seeds_str.removeprefix("seeds: ").split()]


if __name__ == "__main__":
    main()
