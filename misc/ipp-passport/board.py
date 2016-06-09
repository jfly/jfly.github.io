from collections import namedtuple

from pixel_thing import PixelThing, Location
from piece import Piece
from colors import to_black_bg

def northwestmost_location(locations):
    return min(locations, key=lambda location: (location.row, location.column))

class PlacedPiece(namedtuple('PlacedPiece', ['piece', 'location'])):
    def board_locations(self):
        locations = []

        piece_pixel_locations = self.piece.get_pixel_locations()
        northwestmost_piece_location = northwestmost_location(piece_pixel_locations)
        for location_in_piece in piece_pixel_locations:
            # Note: we position this piece such that it's northwestmost piece
            # is exactly at self.location.
            location_in_board = self.location + (location_in_piece - northwestmost_piece_location)
            locations.append(location_in_board)

        return locations

class Board(PixelThing):
    empty_board_by_name = {}

    def __init__(self, pixel_str, name, placed_pieces=tuple()):
        super().__init__(pixel_str)

        self.location_to_piece = {}
        self.placed_pieces = placed_pieces
        self.name = name
        for placed_piece in self.placed_pieces:
            assert self.can_place_piece(placed_piece)
            for location in placed_piece.board_locations():
                assert self.can_place_pixel_at(location)
                self.location_to_piece[location] = placed_piece.piece

        if len(placed_pieces) == 0:
            Board.empty_board_by_name[self.name] = self

    def can_place_pixel_at(self, location):
        return location not in self.location_to_piece and location in self.get_pixel_locations()

    def can_place_piece(self, placed_piece):
        return all(self.can_place_pixel_at(location) for location in placed_piece.board_locations())

    def is_full(self):
        return len(self.get_unfilled_locations()) == 0

    def get_unfilled_locations(self):
        return set(filter(lambda location: self.can_place_pixel_at(location), self.get_pixel_locations()))

    def get_board_with_piece_placed(self, placed_piece):
        assert self.can_place_piece(placed_piece)
        new_placed_pieces = self.placed_pieces + tuple([placed_piece])
        return Board(self.to_pixel_str(), name=self.name, placed_pieces=new_placed_pieces)

    def get_unfilled_region_at(self, location):
        region = set()
        potential_region_members = { location }
        while len(potential_region_members) > 0:
            location = potential_region_members.pop()
            if location in region:
                continue
            if self.can_place_pixel_at(location):
                region.add(location)
                potential_region_members.add(location + Location(1, 0))
                potential_region_members.add(location + Location(-1, 0))
                potential_region_members.add(location + Location(0, 1))
                potential_region_members.add(location + Location(0, -1))
        return region

    def is_unsolvable(self):
        unfilled_locations = self.get_unfilled_locations()
        while len(unfilled_locations) > 0:
            location = unfilled_locations.pop()
            region = self.get_unfilled_region_at(location)
            if len(region) < Piece.MIN_PIECE_SIZE:
                return True
            for connected_location in region:
                if connected_location != location:
                    unfilled_locations.remove(connected_location)

        return False

    def get_all_boards_with_piece_placed(self, piece):
        boards = []
        northwestmost_open_location = northwestmost_location(self.get_unfilled_locations())
        for variant in piece.get_variants():
            placed_piece = PlacedPiece(variant, northwestmost_open_location)
            if self.can_place_piece(placed_piece):
                boards.append(self.get_board_with_piece_placed(placed_piece))
        return boards

    def __str__(self):
        s = ""
        for nthRow, row in enumerate(self.grid):
            for nthCol, part_of_board in enumerate(row):
                location = Location(row=nthRow, column=nthCol)
                piece = self.location_to_piece.get(location)
                if piece:
                    s += piece.getPrintablePixel()
                elif part_of_board:
                    s += " "
                else:
                    s += to_black_bg(" ")
            s += "\n"
        return s

b = Board("""
     1
    111
   11111
 1  111  1
111 111 111
11111111111
 111111111
  1111111
   11111
     1
     1
""", name="maple")

b2 = Board(b.rotate_clockwise_90().rotate_clockwise_90().to_pixel_str(), name="elpam")

Board("""
    111
   11111
  1111111
 111111111
 111111111
 111111111
  1111111
   11111
    111
""", "sun")
