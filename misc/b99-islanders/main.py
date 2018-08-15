#!/usr/bin/env python3

"""
There are 12 people living on an island. 11 of them weigh the exact same
amount, and 1 of them weighs either more or less than the others. There is also
a scale you can use to compare N islands to N islanders. How many times do you
need to use the scale to figure out which islander weighs a different amount
than the rest?
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Set, FrozenSet

######### Types + Helpers ######################

class Weight(Enum):
    """What we know about an islander's weight."""
    POSSIBLY_HEAVIER = 1
    POSSIBLY_LIGHTER = 2
    NORMAL = 3
    CLUELESS = 4

@dataclass
class Islanders:
    """Represents a collection of islanders."""
    possibly_heavier_count: int = 0
    possibly_lighter_count: int = 0
    normal_count: int = 0
    clueless_count: int = 0

    def __post_init__(self):
        assert self.possibly_heavier_count >= 0
        assert self.possibly_lighter_count >= 0
        assert self.normal_count >= 0
        assert self.clueless_count >= 0

    def total_count(self):
        """Returns the total number of islanders this object represents."""
        return sum(self.to_count_by_weight().values())

    def to_count_by_weight(self) -> Dict[Weight, int]:
        """Returns a mapping of Weight to the number of islanders with that Weight."""
        return {
            Weight.POSSIBLY_HEAVIER: self.possibly_heavier_count,
            Weight.POSSIBLY_LIGHTER: self.possibly_lighter_count,
            Weight.NORMAL: self.normal_count,
            Weight.CLUELESS: self.clueless_count,
        }

    def __add__(self, other):
        return Islanders(
            possibly_heavier_count=self.possibly_heavier_count + other.possibly_heavier_count,
            possibly_lighter_count=self.possibly_lighter_count + other.possibly_lighter_count,
            normal_count=self.normal_count + other.normal_count,
            clueless_count=self.clueless_count + other.clueless_count,
        )

    def __sub__(self, other):
        return Islanders(
            possibly_heavier_count=self.possibly_heavier_count - other.possibly_heavier_count,
            possibly_lighter_count=self.possibly_lighter_count - other.possibly_lighter_count,
            normal_count=self.normal_count - other.normal_count,
            clueless_count=self.clueless_count - other.clueless_count,
        )

    def __repr__(self) -> str:
        strs = []
        for weight, count in self.to_count_by_weight().items():
            if count > 0:
                strs.append(f'{count} {weight.name}')

        return "{" + ("Nobody" if len(strs) == 0 else ", ".join(strs)) + "}"

@dataclass
class ScaleOperation:
    """Represents a usage of the scale. On each side of the scale, we place
    some number islanders of each KnownWeight."""
    left_side: Islanders
    right_side: Islanders
    all_islanders: Islanders

    def get_not_on_scale(self) -> Islanders:
        """Get Islanders that were not on the scale."""
        return self.all_islanders - self.left_side - self.right_side

    def __post_init__(self):
        assert self.left_side.total_count() == self.right_side.total_count()
        for weight, count in (self.left_side + self.right_side).to_count_by_weight().items():
            assert count <= self.all_islanders.to_count_by_weight()[weight]

    def __repr__(self) -> str:
        return f'{self.left_side} vs. {self.right_side}'

class ScaleResult(Enum):
    """Which side of the scale tipped down?"""
    LEFT_SIDE = 1
    RIGHT_SIDE = 2
    SAME = 3

class WhereOnScale(Enum):
    """Where an islander can be on a scale."""
    LEFT_SIDE = 1
    RIGHT_SIDE = 2
    NOT_ON_SCALE = 3

#<<< class ScaleObservation(NamedTuple):
#<<<     operation: ScaleOperation
#<<<     result: ScaleResult
#<<<
#<<<     def __repr__(self) -> str:
#<<<         return f'{self.operation} leaned {self.result}'

######################################

def operate_scale(operation: ScaleOperation) -> Dict[ScaleResult, Islanders]:
    """Perform the given ScaleOperation on the given Islanders and return new
    Islanders for each possible result."""

    islanders = operation.all_islanders
    left_side = operation.left_side
    right_side = operation.right_side
    not_on_scale: Islanders = operation.get_not_on_scale()

    return {
        ScaleResult.LEFT_SIDE: Islanders(
            normal_count=islanders.normal_count + left_side.possibly_lighter_count + right_side.possibly_heavier_count + not_on_scale.possibly_lighter_count + not_on_scale.possibly_heavier_count + not_on_scale.clueless_count,
            clueless_count=islanders.clueless_count - left_side.clueless_count - right_side.clueless_count - not_on_scale.clueless_count,
            possibly_heavier_count=islanders.possibly_heavier_count + left_side.clueless_count +  right_side.possibly_heavier_count - not_on_scale.possibly_heavier_count,
            possibly_lighter_count=islanders.possibly_lighter_count + right_side.clueless_count + left_side.possibly_lighter_count - not_on_scale.possibly_lighter_count,
        ),
        ScaleResult.RIGHT_SIDE: Islanders(
            normal_count=islanders.normal_count + right_side.possibly_lighter_count + left_side.possibly_heavier_count + not_on_scale.possibly_lighter_count + not_on_scale.possibly_heavier_count + not_on_scale.clueless_count,
            clueless_count=islanders.clueless_count - right_side.clueless_count - left_side.clueless_count - not_on_scale.clueless_count,
            possibly_heavier_count=islanders.possibly_heavier_count + right_side.clueless_count + left_side.possibly_heavier_count - not_on_scale.possibly_heavier_count,
            possibly_lighter_count=islanders.possibly_lighter_count + left_side.clueless_count + right_side.possibly_lighter_count - not_on_scale.possibly_lighter_count,
        ),
        ScaleResult.SAME: Islanders(
            normal_count=islanders.normal_count + right_side.possibly_heavier_count + right_side.possibly_lighter_count + right_side.clueless_count + left_side.possibly_heavier_count + left_side.possibly_lighter_count + left_side.clueless_count,
            clueless_count=islanders.clueless_count - right_side.clueless_count - left_side.clueless_count,
            possibly_heavier_count=islanders.possibly_heavier_count - right_side.possibly_heavier_count - left_side.possibly_heavier_count,
            possibly_lighter_count=islanders.possibly_heavier_count - right_side.possibly_lighter_count - left_side.possibly_lighter_count,
        ),
    }

def get_operations(islanders: Islanders) -> FrozenSet[ScaleOperation]:
    """
    There are 4 things we can know about an islander:
        1. normal weight
        2. clueless about their weight
        3. possibly heavier
        4. possibly lighter

    We want to generate all scale operations between these
    islanders. It does not matter if these operations are "interesting" (it's
    ok if the act of actually performing that operation gives us no new
    information).

    The set of all possible scale operations is:
        { N normal, C clueless,  H heavier,  L lighter } vs
        { 0 normal, C2 clueless, H2 heavier, L2 lighter }
    where N + C + H + L = C2 + H2 + L2
    (note that there's never any value in putting normals on both sides of the scale)
    """
    operations: Set[ScaleOperation] = set()
    for left_normal_count in range(islanders.normal_count + 1):
        for clueless_count in range(islanders.clueless_count + 1):
            for left_heavier_count in range(islanders.possibly_heavier_count + 1):
                for left_lighter_count in range(islanders.possibly_lighter_count + 1):
                    left_count = (left_normal_count + clueless_count + left_heavier_count + left_lighter_count)
                    if left_count == 0:
                        continue
                    for right_clueless_count in range(islanders.clueless_count + 1 - clueless_count):
                        for right_heavier_count in range(islanders.possibly_heavier_count + 1 - left_heavier_count):
                            right_lighter_count = left_count - (right_clueless_count + right_heavier_count)
                            if 0 <= right_lighter_count <= islanders.possibly_lighter_count - left_lighter_count:
                                operations.add(ScaleOperation(
                                    all_islanders=islanders,
                                    left_side=Islanders(
                                        normal_count=left_normal_count,
                                        clueless_count=clueless_count,
                                        possibly_heavier_count=left_heavier_count,
                                        possibly_lighter_count=left_lighter_count,
                                    ),
                                    right_side=Islanders(
                                        normal_count=0,
                                        clueless_count=right_clueless_count,
                                        possibly_heavier_count=right_heavier_count,
                                        possibly_lighter_count=right_lighter_count,
                                    ),
                                ))
    return frozenset(operations)

#<<< class ScoredOperation(NamedTuple):
#<<<     score: int
#<<<     operation: Optional[ScaleOperation]
#<<<
#<<< def dump_args(func):
#<<<     depth = 0
#<<<     def wrapper(universes):
#<<<         nonlocal depth
#<<<
#<<<         indent = "\t"*depth
#<<<         invocation_str = f'{func.__qualname__}({pretty_print_universes(universes)})'
#<<<         print(f'{indent}{invocation_str}')
#<<<
#<<<         depth += 1
#<<<         ret_val = func(universes)
#<<<         depth -= 1
#<<<
#<<<         print(f'{indent}{invocation_str} = {ret_val}')
#<<<         return ret_val
#<<<     return wrapper
#<<<
#<<< def get_worst_result_score(universes: Universes, operation: ScaleOperation) -> Optional[int]:
#<<<     # Consider all the possible results of this operation, and figure out the worst cost.
#<<<     worst_result_score = None
#<<<     for result, next_universes in operate_scale(universes, operation).items():
#<<<         if next_universes == universes:
#<<<             # This operation gave us no new information, totally ignore it.
#<<<             return None
#<<<         score = search(next_universes).score + 1
#<<<         if worst_result_score is None or score > worst_result_score:
#<<<             worst_result_score = score
#<<<
#<<<     return worst_result_score
#<<<
#<<< memoed: Dict[Tuple, ScoredOperation] = {} #<<<
#<<< #<<< @dump_args
#<<< def search(universes: Universes) -> ScoredOperation:
#<<<
#<<<     if len(universes) == 1:
#<<<         return ScoredOperation(0, None)
#<<<     elif len(universes) == 2:
#<<<         universe_1, universe_2 = list(universes)
#<<<         if universe_1.islander == universe_2.islander:
#<<<             return ScoredOperation(0, None)
#<<<
#<<<     analyzed_universes = analyze_universes(universes)
#<<<     global memoed
#<<<     result = memoed.get(analyzed_universes.key(), None)
#<<<     if result is not None:
#<<<         return result
#<<<
#<<<     best_scored_operation = None
#<<<     for operation in get_operations(analyzed_universes):
#<<<         worst_result_score = get_worst_result_score(universes, operation)
#<<<         if worst_result_score is None:
#<<<             continue
#<<<         if best_scored_operation is None or worst_result_score < best_scored_operation.score:
#<<<             best_scored_operation = ScoredOperation(worst_result_score, operation)
#<<<
#<<<     assert best_scored_operation is not None
#<<<     memoed[analyzed_universes.key()] = best_scored_operation #<<<
#<<<     return best_scored_operation

ISLANDERS = Islanders(clueless_count=12)

def test():
    """Playing around with some of our utilities."""

    operation = ScaleOperation(
        all_islanders=ISLANDERS,
        left_side=Islanders(clueless_count=3),
        right_side=Islanders(clueless_count=3),
    )

    islanders_by_result = operate_scale(operation)

    print(f"Initial knowledge: {ISLANDERS}")
    print(f"After comparing {operation}")
    for result, islanders in islanders_by_result.items():
        print(f"\t{result}:\t{islanders}")

def main():
    """Go go go!"""

    test()
    #<<< scored_operation = search(UNIVERSES)
    #<<< print(scored_operation)

if __name__ == "__main__":
    main()
