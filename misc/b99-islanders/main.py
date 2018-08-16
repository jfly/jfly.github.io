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
from typing import Dict, FrozenSet, List, Optional, Set
import functools

import pptree

######### Types + Helpers ######################

class Weight(Enum):
    """What we know about an islander's weight."""
    HEAVIER_OR_NORMAL = 1
    LIGHTER_OR_NORMAL = 2
    NORMAL = 3
    CLUELESS = 4

    def to_unicode(self) -> str:
        """TODO"""
        if self == Weight.HEAVIER_OR_NORMAL:
            return "+"
        elif self == Weight.LIGHTER_OR_NORMAL:
            return "-"
        elif self == Weight.NORMAL:
            return "✔"
        elif self == Weight.CLUELESS:
            return "±"
        else:
            assert False

@dataclass(frozen=True)
class Islanders:
    """Represents a collection of islanders."""
    heavier_or_normal_count: int = 0
    lighter_or_normal_count: int = 0
    normal_count: int = 0
    clueless_count: int = 0

    def __post_init__(self):
        assert self.heavier_or_normal_count >= 0
        assert self.lighter_or_normal_count >= 0
        assert self.normal_count >= 0
        assert self.clueless_count >= 0

    def is_solved(self):
        """Returns True if we know which islander weighs a different amount
        than everyone else."""
        unknown_count = self.heavier_or_normal_count + self.lighter_or_normal_count + self.clueless_count
        return unknown_count == 1

    def total_count(self):
        """Returns the total number of islanders this object represents."""
        return sum(self.to_count_by_weight().values())

    def to_count_by_weight(self) -> Dict[Weight, int]:
        """Returns a mapping of Weight to the number of islanders with that Weight."""
        return {
            Weight.HEAVIER_OR_NORMAL: self.heavier_or_normal_count,
            Weight.LIGHTER_OR_NORMAL: self.lighter_or_normal_count,
            Weight.NORMAL: self.normal_count,
            Weight.CLUELESS: self.clueless_count,
        }

    def __add__(self, other):
        return Islanders(
            heavier_or_normal_count=self.heavier_or_normal_count + other.heavier_or_normal_count,
            lighter_or_normal_count=self.lighter_or_normal_count + other.lighter_or_normal_count,
            normal_count=self.normal_count + other.normal_count,
            clueless_count=self.clueless_count + other.clueless_count,
        )

    def __sub__(self, other):
        return Islanders(
            heavier_or_normal_count=self.heavier_or_normal_count - other.heavier_or_normal_count,
            lighter_or_normal_count=self.lighter_or_normal_count - other.lighter_or_normal_count,
            normal_count=self.normal_count - other.normal_count,
            clueless_count=self.clueless_count - other.clueless_count,
        )

    def __repr__(self) -> str:
        strs = []
        for weight, count in self.to_count_by_weight().items():
            if count > 0:
                strs.append(f'{count}{weight.to_unicode()}')

        return "{" + ("Nobody" if len(strs) == 0 else ", ".join(strs)) + "}"

@dataclass(frozen=True)
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
    BALANCED = 3

class WhereOnScale(Enum):
    """Where an islander can be on a scale."""
    LEFT_SIDE = 1
    RIGHT_SIDE = 2
    NOT_ON_SCALE = 3

######################################

def operate_scale(operation: ScaleOperation) -> Dict[ScaleResult, Islanders]:
    """Perform the given ScaleOperation on the given Islanders and return new
    Islanders for each possible result."""

    islanders = operation.all_islanders
    left_side = operation.left_side
    right_side = operation.right_side
    not_on_scale: Islanders = operation.get_not_on_scale()

    islanders_by_result = {}

    # Could the scale tip left?
    heavier_or_normal_count = left_side.heavier_or_normal_count + left_side.clueless_count
    lighter_or_normal_count = right_side.lighter_or_normal_count + right_side.clueless_count
    if heavier_or_normal_count + lighter_or_normal_count > 0:
        islanders_by_result[ScaleResult.LEFT_SIDE] = Islanders(
            normal_count=islanders.total_count() - heavier_or_normal_count - lighter_or_normal_count,
            clueless_count=0,
            heavier_or_normal_count=heavier_or_normal_count,
            lighter_or_normal_count=lighter_or_normal_count,
        )

    # Could the scale tip right?
    heavier_or_normal_count = right_side.heavier_or_normal_count + right_side.clueless_count
    lighter_or_normal_count = left_side.lighter_or_normal_count + left_side.clueless_count
    if heavier_or_normal_count + lighter_or_normal_count > 0:
        islanders_by_result[ScaleResult.RIGHT_SIDE] = Islanders(
            normal_count=islanders.total_count() - heavier_or_normal_count - lighter_or_normal_count,
            clueless_count=0,
            heavier_or_normal_count=heavier_or_normal_count,
            lighter_or_normal_count=lighter_or_normal_count,
        )

    # Could the scale balance out?
    normal_count = not_on_scale.normal_count + left_side.total_count() + right_side.total_count()
    heavier_or_normal_count = not_on_scale.heavier_or_normal_count
    lighter_or_normal_count = not_on_scale.lighter_or_normal_count
    clueless_count = not_on_scale.clueless_count
    if heavier_or_normal_count + lighter_or_normal_count + clueless_count > 0:
        islanders_by_result[ScaleResult.BALANCED] = Islanders(
            normal_count=normal_count,
            clueless_count=clueless_count,
            heavier_or_normal_count=heavier_or_normal_count,
            lighter_or_normal_count=lighter_or_normal_count,
        )

    return islanders_by_result

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
            for left_heavier_count in range(islanders.heavier_or_normal_count + 1):
                for left_lighter_count in range(islanders.lighter_or_normal_count + 1):
                    left_count = (left_normal_count + clueless_count + left_heavier_count + left_lighter_count)
                    if left_count == 0:
                        continue
                    for right_clueless_count in range(islanders.clueless_count + 1 - clueless_count):
                        for right_heavier_count in range(islanders.heavier_or_normal_count + 1 - left_heavier_count):
                            right_lighter_count = left_count - (right_clueless_count + right_heavier_count)
                            if 0 <= right_lighter_count <= islanders.lighter_or_normal_count - left_lighter_count:
                                operations.add(ScaleOperation(
                                    all_islanders=islanders,
                                    left_side=Islanders(
                                        normal_count=left_normal_count,
                                        clueless_count=clueless_count,
                                        heavier_or_normal_count=left_heavier_count,
                                        lighter_or_normal_count=left_lighter_count,
                                    ),
                                    right_side=Islanders(
                                        normal_count=0,
                                        clueless_count=right_clueless_count,
                                        heavier_or_normal_count=right_heavier_count,
                                        lighter_or_normal_count=right_lighter_count,
                                    ),
                                ))
    return frozenset(operations)

@dataclass(frozen=True)
class ScoredOperation:
    """An operation with a score associated."""
    score: int
    operation: Optional[ScaleOperation]

def get_worst_result_score(islanders: Islanders, operation: ScaleOperation) -> Optional[int]:
    """Consider all the possible results of this operation, and figure out the worst cost."""
    worst_result_score = None
    for _result, next_islanders in operate_scale(operation).items():
        if next_islanders == islanders:
            # This operation gave us no new information, totally ignore it.
            return None
        score = search(next_islanders).score + 1
        if worst_result_score is None or score > worst_result_score:
            worst_result_score = score

    return worst_result_score

@functools.lru_cache(maxsize=None)
def search(islanders: Islanders) -> ScoredOperation:
    """Return the optimal operation to take given Islanders."""
    if islanders.is_solved():
        return ScoredOperation(0, None)

    best_scored_operation = None
    for operation in get_operations(islanders):
        worst_result_score = get_worst_result_score(islanders, operation)
        if worst_result_score is None:
            continue
        if best_scored_operation is None or worst_result_score < best_scored_operation.score:
            best_scored_operation = ScoredOperation(worst_result_score, operation)

    assert best_scored_operation is not None
    return best_scored_operation

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

class Node:
    """TODO"""

    def __init__(self, islanders: Islanders, parent: Optional['Node'] = None) -> None:
        self.islanders = islanders
        self.operation: Optional[ScaleOperation] = None
        self.children: List['Node'] = []
        if parent:
            parent.children.append(self)

    def __str__(self) -> str:
        s = ""
        s += str(self.islanders)
        if self.operation is not None:
            s += " now do " + str(self.operation)
        return s

def build_tree(original_islanders: Islanders) -> Node:
    """TODO"""
    root_node = Node(original_islanders)
    fringe = [root_node]
    next_fringe: List[Node] = []
    while True:
        if not fringe:
            if not next_fringe:
                break
            fringe, next_fringe = next_fringe, fringe

        node = fringe.pop()
        operation = search(node.islanders).operation
        if operation is not None:
            node.operation = operation
            for next_islanders in operate_scale(operation).values():
                next_fringe.append(Node(next_islanders, parent=node))

    return root_node

def main():
    """Go go go!"""

    #<<< test()

    tree = build_tree(ISLANDERS)
    pptree.print_tree(tree)

if __name__ == "__main__":
    main()
