#!/usr/bin/env python3

"""
There are 12 people living on an island. 11 of them weigh the exact same
amount, and 1 of them weighs either more or less than the others. There is also
a scale you can use to compare N islands to N islanders. How many times do you
need to use the scale to figure out which islander weighs a different amount
than the rest?
"""

from enum import Enum
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Optional, Set, FrozenSet, Tuple
import itertools
import math
import sys

######### Types + Helpers ######################

class Islander(Enum):
    JOHN = 1
    GARY = 2
    JOE = 3
    RACHEL = 4
    DAN = 5
    AARON = 6
    JAMES = 7
    MARY = 8
    MARTIN = 9
    BENJAMIN = 10
    JEREMY = 11
    FELIKS = 12

class Weight(Enum):
    HEAVIER = 1
    LIGHTER = 2

class Universe(NamedTuple):
    islander: Islander
    weight: Weight

class ScaleOperation(NamedTuple):
    left_side: FrozenSet[Islander]
    right_side: FrozenSet[Islander]

    def __repr__(self) -> str:
        return f'{[ i.value for i in self.left_side]} vs. {[ i.value for i in self.right_side]}'

class ScaleResult(Enum):
    """Which side of the scale tipped down?"""
    LEFT_SIDE = 1
    RIGHT_SIDE = 2
    SAME = 3

class ScaleObservation(NamedTuple):
    operation: ScaleOperation
    result: ScaleResult

    def __repr__(self) -> str:
        return f'{self.operation} leaned {self.result}'

Universes = FrozenSet[Universe]

class AnalyzedUniverses(NamedTuple):
    normal_islanders: FrozenSet[Islander]
    totally_unknown_islanders: FrozenSet[Islander]
    possibly_heavier_islanders: FrozenSet[Islander]
    possibly_lighter_islanders: FrozenSet[Islander]

    def unknown_islanders(self):
        return self.totally_unknown_islanders | self.possibly_heavier_islanders | self.possibly_lighter_islanders

    def key(self):
        return (
            len(self.normal_islanders),
            len(self.totally_unknown_islanders),
            len(self.possibly_heavier_islanders),
            len(self.possibly_lighter_islanders),
        )

def analyze_universes(universes: Universes) -> AnalyzedUniverses:
    normal_islanders: Set = set()
    totally_unknown_islanders: Set = set()
    possibly_heavier_islanders: Set = set()
    possibly_lighter_islanders: Set = set()

    universes_by_islander: Dict[Islander, Set[Universe]] = defaultdict(set)
    for universe in universes:
        universes_by_islander[universe.islander].add(universe)

    for islander in Islander:
        weights = [ universe.weight for universe in universes_by_islander[islander] ]
        if Weight.HEAVIER in weights and Weight.LIGHTER in weights:
            totally_unknown_islanders.add(islander)
        elif Weight.HEAVIER in weights:
            possibly_heavier_islanders.add(islander)
        elif Weight.LIGHTER in weights:
            possibly_lighter_islanders.add(islander)
        else:
            normal_islanders.add(islander)

    return AnalyzedUniverses(
        normal_islanders=frozenset(normal_islanders),
        totally_unknown_islanders=frozenset(totally_unknown_islanders),
        possibly_heavier_islanders=frozenset(possibly_heavier_islanders),
        possibly_lighter_islanders=frozenset(possibly_lighter_islanders),
    )


def pretty_print_universes(universes: Universes) -> str:
    analyzed_universes = analyze_universes(universes)

    strs: List[str] = []

    for islander in sorted(analyzed_universes.possibly_lighter_islanders, key=lambda i: i.value):
        strs.append(f'{islander.value}-')

    for islander in sorted(analyzed_universes.possibly_heavier_islanders, key=lambda i: i.value):
        strs.append(f'{islander.value}+')

    for islander in sorted(analyzed_universes.totally_unknown_islanders, key=lambda i: i.value):
        strs.append(f'{islander.value}±')

    return ", ".join(strs)

######################################

def operate_scale(universes: Universes, operation: ScaleOperation) -> Dict[ScaleResult, Universes]:
    universes_by_result: Dict[ScaleResult, Set[Universe]] = defaultdict(set)

    assert operation.left_side.isdisjoint(operation.right_side)
    assert len(operation.left_side) == len(operation.right_side)
    for universe in universes:
        if universe.islander in operation.left_side:
            if universe.weight == Weight.HEAVIER:
                universes_by_result[ScaleResult.LEFT_SIDE].add(universe)
            else:
                universes_by_result[ScaleResult.RIGHT_SIDE].add(universe)
        elif universe.islander in operation.right_side:
            if universe.weight == Weight.HEAVIER:
                universes_by_result[ScaleResult.RIGHT_SIDE].add(universe)
            else:
                universes_by_result[ScaleResult.LEFT_SIDE].add(universe)
        else:
            universes_by_result[ScaleResult.SAME].add(universe)

    return { result: frozenset(universes) for result, universes in universes_by_result.items() }

def split_set(s: FrozenSet, x: int, y: int):
    """Extract x and y distinct elements from the given set."""
    elements = list(itertools.islice(s, x + y))
    return (elements[:x], elements[x:x+y])

def get_operations(analyzed_universes: AnalyzedUniverses) -> FrozenSet[ScaleOperation]:
    """
    There are 4 things we can know about an islander:
        1. normal weight
        2. totally unknown weight
        3. possibly heavier
        4. possibly lighter

    We want to generate all scale operations between these
    islanders. It does not matter if these operations are "interesting" (it's
    ok if the act of actually performing that operation gives us no new
    information).

    The set of all possible scale operations is:
        { N normal, U unknown, H heavier, L lighter } vs
        { 0 normal, U' unknown, H' heavier, L' lighter }
    where N + U + H + L = U' + H' + L'
    (note that there's never any value in putting normals on both sides of the scale)
    """
    operations: Set[ScaleOperation] = set()
    for n in range(len(analyzed_universes.normal_islanders) + 1):
        for u in range(len(analyzed_universes.totally_unknown_islanders) + 1):
            for h in range(len(analyzed_universes.possibly_heavier_islanders) + 1):
                for l in range(len(analyzed_universes.possibly_lighter_islanders) + 1):
                    left_count = (n + u + h + l)
                    if left_count == 0:
                        continue
                    for u2 in range(len(analyzed_universes.totally_unknown_islanders) + 1 - u):
                        for h2 in range(len(analyzed_universes.possibly_heavier_islanders) + 1 - h):
                            l2 = left_count - (u2 + h2)
                            if 0 <= l2 <= len(analyzed_universes.possibly_lighter_islanders) - l:
                                left_normal, _ = split_set(analyzed_universes.normal_islanders, n, 0)
                                left_unknown, right_unknown = split_set(analyzed_universes.totally_unknown_islanders, u, u2)
                                left_heavier, right_heavier = split_set(analyzed_universes.possibly_heavier_islanders, h, h2)
                                left_lighter, right_lighter = split_set(analyzed_universes.possibly_lighter_islanders, l, l2)
                                left_side = frozenset(
                                    left_normal + left_unknown + left_heavier + left_lighter
                                )
                                right_side = frozenset(
                                    right_unknown + right_heavier + right_lighter
                                )
                                operations.add(ScaleOperation(left_side, right_side))
    return frozenset(operations)

class ScoredOperation(NamedTuple):
    score: int
    operation: Optional[ScaleOperation]

def dump_args(func):
    depth = 0
    def wrapper(universes):
        nonlocal depth

        indent = "\t"*depth
        invocation_str = f'{func.__qualname__}({pretty_print_universes(universes)})'
        print(f'{indent}{invocation_str}')

        depth += 1
        ret_val = func(universes)
        depth -= 1

        print(f'{indent}{invocation_str} = {ret_val}')
        return ret_val
    return wrapper

def get_worst_result_score(universes: Universes, operation: ScaleOperation) -> Optional[int]:
    # Consider all the possible results of this operation, and figure out the worst cost.
    worst_result_score = None
    for result, next_universes in operate_scale(universes, operation).items():
        if next_universes == universes:
            # This operation gave us no new information, totally ignore it.
            return None
        score = search(next_universes).score + 1
        if worst_result_score is None or score > worst_result_score:
            worst_result_score = score

    return worst_result_score

memoed: Dict[Tuple, ScoredOperation] = {} #<<<
#<<< @dump_args
def search(universes: Universes) -> ScoredOperation:

    if len(universes) == 1:
        return ScoredOperation(0, None)
    elif len(universes) == 2:
        universe_1, universe_2 = list(universes)
        if universe_1.islander == universe_2.islander:
            return ScoredOperation(0, None)

    analyzed_universes = analyze_universes(universes)
    global memoed
    result = memoed.get(analyzed_universes.key(), None)
    if result is not None:
        return result

    best_scored_operation = None
    for operation in get_operations(analyzed_universes):
        worst_result_score = get_worst_result_score(universes, operation)
        if worst_result_score is None:
            continue
        if best_scored_operation is None or worst_result_score < best_scored_operation.score:
            best_scored_operation = ScoredOperation(worst_result_score, operation)

    assert best_scored_operation is not None
    memoed[analyzed_universes.key()] = best_scored_operation #<<<
    return best_scored_operation

UNIVERSES = [ Universe(islander, weight) for islander in Islander for weight in Weight ]

def test():
    operation = ScaleOperation(
        left_side={Islander(1), Islander(2), Islander(3)},
        right_side={Islander(4), Islander(5), Islander(6)},
    )

    universes_by_observation = operate_scale(UNIVERSES, operation)

    print(f"Possible universes: {pretty_print_universes(UNIVERSES)}")
    print(f"After comparing {operation}")
    for observation, universes in universes_by_observation.items():
        print(f"\t{observation}:\t{pretty_print_universes(universes)}")

def main():
    #<<< test()
    scored_operation = search(UNIVERSES)
    print(scored_operation)

if __name__ == "__main__":
    main()
