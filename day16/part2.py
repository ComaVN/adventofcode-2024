#!/bin/env python
import pathlib
import heapq


class Cell:
    def __init__(self, *, accessible=True):
        self.accessible = accessible
        self.scores_by_direction = {}
        self.best_seat = False


class Map:
    def __init__(self, lines):
        self.start = None
        self.direction = ">"
        self.end = None
        self.map = []
        for y, line in enumerate(lines):
            map_line = []
            for x, ch in enumerate(line.strip()):
                match ch:
                    case "#":
                        map_line.append(Cell(accessible=False))
                    case ".":
                        map_line.append(Cell())
                    case "S":
                        map_line.append(Cell())
                        if self.start is not None:
                            raise ValueError(
                                "more than one start position not supported"
                            )
                        self.start = (x, y)
                    case "E":
                        map_line.append(Cell(accessible=True))
                        if self.end is not None:
                            raise ValueError("more than one end position not supported")
                        self.end = (x, y)
                    case _:
                        raise ValueError(f"character '{ch}' in map not supported")
            self.map.append(map_line)
        if self.start is None:
            raise ValueError("map must have a start position")
        if self.end is None:
            raise ValueError("map must have an end position")
        self.height = len(self.map)
        self.width = len(self.map[0])

    def __str__(self):
        result = ""
        for y, line in enumerate(self.map):
            for x, ch in enumerate(line):
                if self.start == (x, y):
                    ch = "S"
                elif self.end == (x, y):
                    ch = "E"
                elif len(self.map[y][x].scores_by_direction) > 0:
                    ch = "O" if self.map[y][x].best_seat else "-"
                elif self.map[y][x].accessible:
                    ch = "."
                else:
                    ch = "#"
                result += ch
            result += "\n"
        return result

    def solve(self):
        def estimate_heap_item(score, direction, pos, path):
            # x, y = pos
            # end_x, end_y = self.end
            # match direction:
            #     case "^":
            #         if x == end_x:
            #             est_score = score + abs(y - end_y)
            #         else:
            #             est_score = score + abs(y - end_y) + 1000 + abs(x - end_x)
            #     case ">":
            #         if y == end_y:
            #             est_score = score + abs(x - end_x)
            #         else:
            #             est_score = score + abs(y - end_y) + 1000 + abs(x - end_x)
            #     case "v" | "<":
            #         est_score = score + abs(y - end_y) + 2000 + abs(x - end_x)
            #     case _:
            #         raise ValueError(f"direction '{direction}' not supported")
            return (score, score, direction, pos, path)

        to_do_heap = [
            estimate_heap_item(
                0,
                self.direction,
                self.start,
                [],
            )
        ]
        heapq.heapify(to_do_heap)
        best_score = None
        best_paths = []
        prev_score = -1
        while len(to_do_heap) > 0:
            est_score, score, direction, (x, y), path = heapq.heappop(to_do_heap)
            assert score >= prev_score
            # if score > prev_score:
            #     print(f"New score: {score}")
            prev_score = score
            if (x, y) == self.end:
                path.append(("E", (x, y)))
                if best_score is None or score < best_score:
                    print(f"New best score: {score}")
                    best_score = score
                    best_paths = [path]
                elif score == best_score:
                    # print(f"same best score: {score}")
                    best_paths.append(path)
                continue
            cell = self.map[y][x]
            if cell.accessible:
                if (best_score is None or score < best_score) and (
                    direction not in cell.scores_by_direction
                    or score <= cell.scores_by_direction[direction]
                ):
                    cell.scores_by_direction[direction] = score
                    if x > 0 and direction != ">":
                        # try going left
                        heapq.heappush(
                            to_do_heap,
                            estimate_heap_item(
                                score + (1 if direction == "<" else 1001),
                                "<",
                                (x - 1, y),
                                path + [("<", (x, y))],
                            ),
                        )
                    if x < self.width - 1 and direction != "<":
                        # try going right
                        heapq.heappush(
                            to_do_heap,
                            estimate_heap_item(
                                score + (1 if direction == ">" else 1001),
                                ">",
                                (x + 1, y),
                                path + [(">", (x, y))],
                            ),
                        )
                    if y > 0 and direction != "v":
                        # try going up
                        heapq.heappush(
                            to_do_heap,
                            estimate_heap_item(
                                score + (1 if direction == "^" else 1001),
                                "^",
                                (x, y - 1),
                                path + [("^", (x, y))],
                            ),
                        )
                    if y < self.height - 1 and direction != "^":
                        # try going down
                        heapq.heappush(
                            to_do_heap,
                            estimate_heap_item(
                                score + (1 if direction == "v" else 1001),
                                "v",
                                (x, y + 1),
                                path + [("v", (x, y))],
                            ),
                        )
            else:
                assert len(cell.scores_by_direction) == 0
        assert best_score is not None
        assert len(best_paths) > 0
        best_seats = {pos for path in best_paths for _, pos in path}
        for x, y in best_seats:
            self.map[y][x].best_seat = True
        return len(best_seats)


def main():
    for filename in (
        "input.small.example.txt",
        "input.large.example.txt",
        "input.txt",
    ):
        filepath = pathlib.Path(__file__).parent / filename
        print(filepath)
        with open(filepath, "r") as file:
            m = Map(file)
        print(m)
        score = m.solve()
        print(m)
        print(score)


if __name__ == "__main__":
    main()
