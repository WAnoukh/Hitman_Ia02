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
w, h = 1, 1
guard_count, civil_count = 1, 1


class Type(Enum):
    GUARD_N = 0
    GUARD_E = 1
    GUARD_S = 2
    GUARD_W = 3
    CIVIL_N = 4
    CIVIL_E = 5
    CIVIL_S = 6
    CIVIL_W = 7
    SEEN_0 = 8
    SEEN_1 = 9
    SOUND_0 = 10
    SOUND_1 = 11
    SOUND_2 = 12
    SOUND_3 = 13
    SOUND_4 = 14
    SOUND_5 = 15


type_nb = 8

# juste pour garde et civil 
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
    return lit + 1


def literal_from_sound(x: int, y: int, sound: int) -> Literal:
    lit = sound # et si plus de 5 personnes ? C'est quoi w? h ?
    lit += x * 6
    lit += y * w * 6 
    lit += h * w * type_nb
    return lit + 1


def literal_from_seen(x: int, y: int, seen: int) -> Literal:
    lit = seen
    lit += x * 2
    lit += y * w * 2
    lit += h * w * (type_nb + 6)
    return lit + 1


def decode_literal(literal: int) -> (int, int, Type):
    x: int
    y: int
    type: Type
    literal -= 1
    if literal >= h * w * (type_nb + 6):
        literal -= h * w * (type_nb + 6)
        y = literal // (w * 2)
        literal %= (w * 2)
        x = literal // (2)
        seen = literal % 2
        return x, y, Type(seen + 8)
    elif literal >= h * w * type_nb:
        literal -= h * w * type_nb
        y = literal // (w * 6)
        literal %= (w * 6)
        x = literal // 6
        sound = literal % 6
        return x, y, Type(sound + 10)
    else:
        y = literal // (w * type_nb)
        literal %= w * type_nb
        x = literal // type_nb
        literal %= type_nb
        return x, y, Type(literal)

# je veux bien des explications
def get_initial_person_count_clauses(i: int,sign: int ,elts: list[int]) -> ClauseBase: 
    if (i == 0):
        return [[]]
    else:
        newCb: ClauseBase = []
        for k in range(0, len(elts)):
            elts2 = elts[k:]
            elts2.remove(elts[k])
            cb: ClauseBase = get_initial_person_count_clauses(i - 1, sign, elts2)

            for c in cb:
                nc = c[:]
                case_already_taken = False
                for literal_to_check in nc:
                    x,y,t = decode_literal(literal_to_check)
                    x2,y2,t2 = decode_literal(elts[k])
                    if x == x2 and y == y2:
                        case_already_taken = True
                        break
                if not case_already_taken:
                    nc.append(sign * elts[k])
                    newCb.append(nc)
        return newCb


def generate_person_literals(type: str) -> list[Literal]:
    l = []
    for x in range(w):
        for y in range(h):
            for t in [HC.N, HC.E, HC.S, HC.W]:
                l.append(literal_from_cell(x, y, type, t))
    return l


def get_initial_guard_count_clauses() -> ClauseBase:
    lts = generate_person_literals("g")
    total = w * h * guard_count
    p = get_initial_person_count_clauses(len(lts) - guard_count+1, 1, lts)
    n = get_initial_person_count_clauses(guard_count+1 , -1, lts)
    return p + n


def init_KB(nw: int, nh: int, new_guard_count: int, new_civil_count: int):
    global w, h, guard_count, civil_count, KB
    w, h = nw, nh
    guard_count = new_guard_count
    civil_count = new_civil_count


if __name__ == '__main__':
    cb: ClauseBase = get_initial_guard_count_clauses()
    for c in cb:
        print("[", end=" ")
        for l in c:
            if l < 0:
                print("non", end=" ")
                l *= -1
            print(decode_literal(l), end=" ")
        print("]")
    print()
