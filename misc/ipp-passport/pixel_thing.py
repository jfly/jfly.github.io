from collections import namedtuple

class Location(namedtuple('Location', ['row', 'column'])):
    def __add__(self, other):
        return Location(self.row + other.row, self.column + other.column)

    def __sub__(self, other):
        return Location(self.row - other.row, self.column - other.column)

class PixelThing:
    def __init__(self, pixel_str):
        self.grid = []
        max_row_length = max(len(line) for line in pixel_str.splitlines())
        for line in pixel_str.splitlines():
            if line:
                padding_count = max_row_length - len(line)
                self.grid.append(tuple([True if ch == "1" else False for ch in line] + [0]*padding_count))
        self.grid = tuple(self.grid)

    def get_pixel_count(self):
        return len(self.get_pixel_locations())

    def get_pixel_locations(self):
        locations = []
        for nthRow, row in enumerate(self.grid):
            for nthCol, pixel in enumerate(row):
                if pixel:
                    locations.append(Location(row=nthRow, column=nthCol))
        return locations

    def width(self):
        return len(self.grid[0])

    def height(self):
        return len(self.grid)

    def mirror(self):
        mirrored_grid = map(reversed, self.grid)
        return PixelThing(grid_to_pixel_str(mirrored_grid))

    def rotate_clockwise_90(self):
        rotated_grid = map(reversed, zip(*self.grid))
        return PixelThing(grid_to_pixel_str(rotated_grid))

    def __hash__(self):
        return hash(self.grid)

    def __eq__(self, other):
        return self.grid == other.grid

    def to_pixel_str(self):
        return grid_to_pixel_str(self.grid)

def grid_to_pixel_str(grid):
    return "\n".join("".join("1" if pixel else " " for pixel in row) for row in grid)
