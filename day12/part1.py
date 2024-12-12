#!/bin/env python
import collections
import pathlib


class Region:
    def __init__(self, upper_left_plot):
        x, y = upper_left_plot.pos
        if upper_left_plot.region is not None:
            raise ValueError(f"plot ({x},{y}) already has a region")
        self.upper_left_plot = upper_left_plot
        self.plant = upper_left_plot.plant
        self.plots = {upper_left_plot.pos: upper_left_plot}
        self.perimeter = 4
        upper_left_plot.region = self

    def __repr__(self):
        return f"{self.plant} ({self.size()})"

    def add_plot(self, plot):
        x, y = plot.pos
        if plot.region is not None:
            raise ValueError(f"plot ({x},{y}) already has a region")
        if plot.pos in self.plots:
            raise ValueError(f"plot ({x},{y}) already in region")
        self.plots[plot.pos] = plot
        self.perimeter += 4 - 2 * len(
            {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} & self.plots.keys()
        )
        plot.region = self

    def remove_plot(self, plot):
        x, y = plot.pos
        if plot.region is None:
            raise ValueError(f"plot ({x},{y}) has no region")
        if plot.pos not in self.plots:
            raise ValueError(f"plot ({x},{y}) is not in region")
        del self.plots[plot.pos]
        plot.region = None
        # RH: TODO: perimeter

    # Merges the smaller region into the bigger one, updating all plots in the smaller one
    # Returns the smaller (now empty) region
    def merge(self, region):
        if self.plant != region.plant:
            raise ValueError("cannot merge regions with different plants")
        big_region, small_region = (
            (self, region) if self.size() >= region.size() else (region, self)
        )
        for plot in [plot for plot in small_region.plots.values()]:
            small_region.remove_plot(plot)
            big_region.add_plot(plot)
        return small_region

    def size(self):
        return len(self.plots)


class Plot:
    def __init__(self, plant, pos):
        self.plant = plant
        self.pos = pos
        self.region = None

    def __repr__(self):
        return self.plant


class Map:
    def __init__(self, lines):
        self.map = []
        self.regions_by_plant = collections.defaultdict(set)
        for y, line in enumerate(lines):
            self.map.append([])
            for x, plant in enumerate(line.strip()):
                plot = Plot(plant, (x, y))
                self.map[y].append(plot)
                self.add_plot_to_region(plot)

    def __repr__(self):
        return f"{self.map}:\n{self.regions_by_plant}"

    # this assumes plots are read left-to-right, then top-to-bottom, and only once.
    def add_plot_to_region(self, plot):
        x, y = plot.pos
        if plot.region is not None:
            raise ValueError(f"plot ({x},{y}) already has a region")
        if x > 0:
            left_plot = self.map[y][x - 1]
            if left_plot.plant == plot.plant:
                # plot is part of the same region its left neighbour
                left_plot.region.add_plot(plot)
        if y > 0:
            top_plot = self.map[y - 1][x]
            if top_plot.plant == plot.plant:
                # plot is part of the same region its top neighbour
                if plot.region is not None:
                    # plot already has a region from its left neighbour
                    if plot.region != top_plot.region:
                        # regions must be merged
                        removed_region = top_plot.region.merge(plot.region)
                        self.regions_by_plant[removed_region.plant].remove(
                            removed_region
                        )
                else:
                    top_plot.region.add_plot(plot)
        if plot.region is None:
            # no matching plants left or right, create a new region
            region = Region(plot)
            self.regions_by_plant[plot.plant].add(region)

    def regions(self):
        return set.union(*self.regions_by_plant.values())

    def price(self):
        return sum(r.size() * r.perimeter for r in self.regions())


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        map = Map(file.readlines())
    print(map)
    print(len(map.regions()))
    print(map.price())


if __name__ == "__main__":
    main()
