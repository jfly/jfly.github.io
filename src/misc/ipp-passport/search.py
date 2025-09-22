#!/usr/bin/env python3

import argparse
from collections import namedtuple

from board import Board
from piece import Piece

BoardAndPieces = namedtuple("BoardAndPieces", ["board", "pieces"])


def search(starting_board, starting_pieces):
    fringe = [BoardAndPieces(starting_board, starting_pieces)]
    while len(fringe) > 0:
        board_and_pieces = fringe.pop(0)
        board = board_and_pieces.board
        pieces = board_and_pieces.pieces
        if board.is_unsolvable():
            continue

        # Print out a little bit of progress.
        print(len(fringe), len(pieces))

        if board.is_full():
            print("Found a solution!!!")
            print(board)

        # Sanity check that the board is still solvable.
        can_fill_count = sum(piece.get_pixel_count() for piece in pieces)
        need_to_fill_count = len(board.get_unfilled_locations())
        assert can_fill_count == need_to_fill_count

        for i, piece in enumerate(pieces):
            remaining_pieces = pieces[:i] + pieces[i + 1 :]
            next_boards = board.get_all_boards_with_piece_placed(piece)
            for next_board in next_boards:
                fringe.append(BoardAndPieces(board=next_board, pieces=remaining_pieces))

    print("Done searching")


def main():
    parser = argparse.ArgumentParser(description="Solve jigsaws")
    parser.add_argument("jigsaw", choices=Board.empty_board_by_name.keys())
    args = parser.parse_args()

    search(Board.empty_board_by_name[args.jigsaw], Piece.all_pieces)


if __name__ == "__main__":
    main()
