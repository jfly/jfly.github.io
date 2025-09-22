from memoize import memoize
from pixel_thing import PixelThing


class Piece(PixelThing):
    all_pieces = tuple()

    def __init__(self, pixel_str, char):
        super().__init__(pixel_str)

        self.char = char
        Piece.all_pieces = tuple(Piece.all_pieces + tuple([self]))

    def getPrintablePixel(self):
        return self.char

    @memoize
    def get_variants(self):
        variants = set()
        for mirror in [self, Piece(self.mirror().to_pixel_str(), self.char)]:
            rotation = mirror

            variants.add(rotation)
            for rotations in range(1, 4):
                rotation = rotation.rotate_clockwise_90()
                variants.add(Piece(rotation.to_pixel_str(), self.char))

        return variants


Piece(
    """
  1
 11
11
 1
""",
    "0",
)

Piece(
    """
 1
 11
11
""",
    "1",
)

Piece(
    """
 1
11
11
""",
    "2",
)

Piece(
    """
111
11
 1
 1
""",
    "3",
)

Piece(
    """
  11
111
1
""",
    "4",
)

Piece(
    """
 1
111
 11
""",
    "5",
)

Piece(
    """
11 11
 111
""",
    "6",
)

Piece(
    """
 1
111
 1
""",
    "7",
)

Piece(
    """
11
 1
 1
""",
    "8",
)

Piece(
    """
11
 11
11
""",
    "9",
)

Piece.MIN_PIECE_SIZE = min(map(lambda piece: piece.get_pixel_count(), Piece.all_pieces))
