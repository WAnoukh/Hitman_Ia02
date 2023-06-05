from typing import List, Tuple, Dict
from hitman import HC
from enum import Enum

# aliases de type
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

KB: ClauseBase
w, h = 2, 2
guard_count, civil_count = 1,1


class Type(Enum):
    GUARD_N = 0
    GUARD_E = 1
    GUARD_S = 2
    GUARD_W = 3
    CIVIL_N = 4
    CIVIL_E = 5
    CIVIL_S = 6
    CIVIL_W = 7


type_nb = 8


def literal_from_cell(x: int, y: int, type: str, dir: HC) -> Literal:
    lit = 0
    if type not in ["g", 'c']:
        raise Exception("invalid type")
    if dir == HC.N:
        lit = Type.GUARD_N.value if type == "g" else Type.CIVIL_N.value
    elif dir == HC.E:
        lit = Type.GUARD_E.value if type == "g" else Type.CIVIL_E.value
    elif dir == HC.S:
        lit = Type.GUARD_S.value if type == "g" else Type.CIVIL_S.value
    elif dir == HC.W:
        lit = Type.GUARD_W.value if type == "g" else Type.CIVIL_W.value
    else:
        raise Exception("invalid dir")
    lit += x * type_nb
    lit += y * w * type_nb
    return lit


def literal_from_sound(x: int, y: int, sound: int) -> Literal:
    lit = sound
    lit += x * 6
    lit += y * w * 6
    lit += h * w * type_nb
    return lit


def literal_from_seen(x: int, y: int, seen: int) -> Literal:
    lit = seen
    lit += x * 2
    lit += y * w * 2
    lit += h * w * (type_nb + 6)
    return lit


def get_initial_guard_count_clauses() -> ClauseBase:
    for
    pass


def init_KB(nw: int, nh: int, new_guard_count: int, new_civil_count: int):
    global w, h,guard_count, civil_count, KB
    w, h = nw, nh
    guard_count = new_guard_count
    civil_count = new_civil_count

if __name__ == '__main__':
    print(literal_from_cell(0, 0, "g", HC.N))
    print(literal_from_cell(0, 0, "g", HC.E))
    print(literal_from_cell(0, 0, "g", HC.S))
    print(literal_from_cell(0, 0, "g", HC.W))
    print(literal_from_cell(0, 0, "c", HC.N))
    print(literal_from_cell(0, 0, "c", HC.E))
    print(literal_from_cell(0, 0, "c", HC.S))
    print(literal_from_cell(0, 0, "c", HC.W))

    print("-")

    print(literal_from_cell(1, 0, "g", HC.N))
    print(literal_from_cell(1, 0, "g", HC.E))
    print(literal_from_cell(1, 0, "g", HC.S))
    print(literal_from_cell(1, 0, "g", HC.W))
    print(literal_from_cell(1, 0, "c", HC.N))
    print(literal_from_cell(1, 0, "c", HC.E))
    print(literal_from_cell(1, 0, "c", HC.S))
    print(literal_from_cell(1, 0, "c", HC.W))

    print("-")

    print(literal_from_cell(0, 1, "g", HC.N))
    print(literal_from_cell(0, 1, "g", HC.E))
    print(literal_from_cell(0, 1, "g", HC.S))
    print(literal_from_cell(0, 1, "g", HC.W))
    print(literal_from_cell(0, 1, "c", HC.N))
    print(literal_from_cell(0, 1, "c", HC.E))
    print(literal_from_cell(0, 1, "c", HC.S))
    print(literal_from_cell(0, 1, "c", HC.W))

    print("-")

    print(literal_from_cell(1, 1, "g", HC.N))
    print(literal_from_cell(1, 1, "g", HC.E))
    print(literal_from_cell(1, 1, "g", HC.S))
    print(literal_from_cell(1, 1, "g", HC.W))
    print(literal_from_cell(1, 1, "c", HC.N))
    print(literal_from_cell(1, 1, "c", HC.E))
    print(literal_from_cell(1, 1, "c", HC.S))
    print(literal_from_cell(1, 1, "c", HC.W))

    print("-")

    print(literal_from_sound(0, 0, 0))
    print(literal_from_sound(0, 0, 1))
    print(literal_from_sound(0, 0, 2))
    print(literal_from_sound(0, 0, 3))
    print(literal_from_sound(0, 0, 4))
    print(literal_from_sound(0, 0, 5))

    print("-")

    print(literal_from_sound(1, 0, 0))
    print(literal_from_sound(1, 0, 1))
    print(literal_from_sound(1, 0, 2))
    print(literal_from_sound(1, 0, 3))
    print(literal_from_sound(1, 0, 4))
    print(literal_from_sound(1, 0, 5))

    print("-")

    print(literal_from_sound(0, 1, 0))
    print(literal_from_sound(0, 1, 1))
    print(literal_from_sound(0, 1, 2))
    print(literal_from_sound(0, 1, 3))
    print(literal_from_sound(0, 1, 4))
    print(literal_from_sound(0, 1, 5))

    print("-")

    print(literal_from_sound(1, 1, 0))
    print(literal_from_sound(1, 1, 1))
    print(literal_from_sound(1, 1, 2))
    print(literal_from_sound(1, 1, 3))
    print(literal_from_sound(1, 1, 4))
    print(literal_from_sound(1, 1, 5))

    print("-")

    print(literal_from_seen(0, 0, 0))
    print(literal_from_seen(0, 0, 1))

    print("-")

    print(literal_from_seen(1, 0, 0))
    print(literal_from_seen(1, 0, 1))

    print("-")

    print(literal_from_seen(0, 1, 0))
    print(literal_from_seen(0, 1, 1))

    print("-")

    print(literal_from_seen(1, 1, 0))
    print(literal_from_seen(1, 1, 1))


