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

    def find_dst_range(self: Self, current_src: int, max_src: int) -> tuple[range, int]:
        """
        Starting from the number src, return the longest mapped range object possible within the
        boundaries of current_src and max_src. It also returns the int to be used as the next
        current_src value

        In such case where the MapTriplet goes beyond max_src, we will stop before max_src

        It is expected max_src is exclusive, i.e. [current_src, max_src)
        """

        triplet_max: int = self._src_start + self._range_len
        outgoing_max: int = min(triplet_max, max_src)

        # the current_src may be higher than the src_start
        outgoing_min: int = max(self._src_start, current_src) # they are either equal or current_src is bigger
        outgoing_length: int = outgoing_max - outgoing_min
        dst_offset: int = outgoing_min - self._src_start 
        # if so, we must only map starting from that offset and beyond
        return range(self._dst_start + dst_offset, self._dst_start + dst_offset + outgoing_length), outgoing_max
    
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

        # sort the list by starting key so we can iterate in an orderly fashion
        self._triplet_list.sort(key=lambda x: x._src_start)

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
    
    def find_dst_ranges(self: Self, src_ranges: list[range]) -> list[range]:
        out: list[range] = []
        
        for src_range in src_ranges:
            out.extend(self.find_dst_range(src_range))

        return out
    
    def find_dst_range(self: Self, src_range: range) -> list[range]:
        current_src: int = src_range.start
        max_src: int = src_range.stop

        triplet_idx: int = 0
        dst_ranges: list[range] = []

        # find the starting position for mapping
        # if for some reason, the triplet is ahead, generate a catchup range object
        while current_src < max_src and triplet_idx < len(self._triplet_list): # this conditional is used to stop mapping once we're done
            triplet: MapTriplet = self._triplet_list[triplet_idx]
            print(triplet)
            if current_src < triplet._src_start:
                # we are behind, catch up first! 
                # this is UNMAPPED, so we're doing a 1:1 range instead of a DST range
                # make sure we don't catch up beyond what we need!
                max_catch_up: int = min(triplet._src_start, max_src)
                catch_up_range: range = range(current_src, max_catch_up)
                dst_ranges.append(catch_up_range)
                current_src = triplet._src_start
            elif current_src >= (triplet._src_start + triplet._range_len):
                # we can't be mapped by this triplet, move on
                triplet_idx += 1
            elif current_src >= triplet._src_start:
                # we're in the proper position to start mapping, do that
                mapped_range: range
                new_current_src: int
                mapped_range, new_current_src = triplet.find_dst_range(current_src, max_src)
                dst_ranges.append(mapped_range)
                # where does this mapped range stop? that's our new current_src position
                current_src = new_current_src
                # we're done with this triplet, move on
                triplet_idx += 1                

        if triplet_idx == len(self._triplet_list) and current_src < max_src:
            # we don't have any more map triplets to use, fully catch up at this point
            dst_ranges.append(range(current_src, max_src))

        return dst_ranges
    

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
    
    def map_range(self: Self, src_range: range) -> list[range]:
        """For a given range, returns a list of corresponding dst ranges"""
        dst_ranges: list[range] = [src_range]
        for transformer in self._transformers:
            dst_ranges = transformer.find_dst_ranges(dst_ranges)

        return dst_ranges



def main() -> None:
    file: TextIOWrapper = open("5.txt", "rt")
    s: str = file.read()
    parts: list[str] = s.split("\n\n")
    seeds_str: str = parts[0]
    seed_ranges: list[range] = parse_seeds_as_ranges(seeds_str)

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

    location_ranges: list[range] = []
    for seed_range in seed_ranges:
        location_ranges.extend(mapper.map_range(seed_range))

    min_location: int = 2**63
    for location_range in location_ranges:
        min_location = min(location_range.start, min_location)

    print(min_location)

def parse_seeds(seeds_str: str) -> list[int]:
    # part 1
    return [int(x) for x in seeds_str.removeprefix("seeds: ").split()]

def parse_seeds_as_ranges(seeds_str: str) -> list[range]:
    """
    Returns a list of range objects to be used as generators. It is expected the caller
    will aggregate the resulting dst values without collecting all of the values.
    """

    numbers: list[str] = seeds_str.removeprefix("seeds: ").split()

    # dealing with pairs
    # index 0 is the start value
    # index 1 is the range length
    # remember the range start should always be closed, but the ending should be open
    range_list: list[range] = []

    idx: int = 0
    while (idx + 1) < len(numbers):
        start: int = int(numbers[idx])
        length: int = int(numbers[idx + 1])

        r: range = range(start, start + length, 1)
        range_list.append(r)
        idx += 2

    return range_list


def make_range(start: int, length: int) -> range:
    return range(start, start + length)

if __name__ == "__main__":
    main()
