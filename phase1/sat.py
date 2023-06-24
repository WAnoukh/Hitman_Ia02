from typing import List
from hitman.hitman import HC
from enum import Enum

# aliases de type
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

KB: ClauseBase
w, h = 1, 1
guard_count, civil_count = 0, 1


class Type(Enum):
    GUARD_N = 0
    GUARD_E = 1
    GUARD_S = 2
    GUARD_W = 3
    GUARD = 4
    CIVIL_N = 4 + 1
    CIVIL_E = 5 + 1
    CIVIL_S = 6 + 1
    CIVIL_W = 7 + 1
    CIVIL = 8 + 1
    SEEN_G = 8 + 2
    SEEN_C = 9 + 2
    SOUND_0 = 10 + 2
    SOUND_1 = 11 + 2
    SOUND_2 = 12 + 2
    SOUND_3 = 13 + 2
    SOUND_4 = 14 + 2
    SOUND_5 = 15 + 2


person_type_nb = 10

def nb_var():
    return (Type.SOUND_5.value+1) * w*h

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
    elif dir == None:
        lit = Type.GUARD.value if type == "g" else Type.CIVIL.value
    else:
        raise Exception("invalid dir")
    lit += x * person_type_nb
    lit += y * w * person_type_nb
    return lit + 1


def literal_from_sound(x: int, y: int, sound: int) -> Literal:
    lit = sound  # et si plus de 5 personnes ? C'est quoi w? h ?
    lit += x * 6
    lit += y * w * 6
    lit += h * w * person_type_nb
    return lit + 1


def literal_from_seen(x: int, y: int, seen: int) -> Literal:
    # seen = 0 -> guard , 1 -> civil
    lit = seen
    lit += x * 2
    lit += y * w * 2
    lit += h * w * (person_type_nb + 6)
    return lit + 1


def decode_literal(literal: int) -> (int, int, Type):
    x: int
    y: int
    type: Type
    literal -= 1
    if literal >= h * w * (person_type_nb + 6):
        literal -= h * w * (person_type_nb + 6)
        y = literal // (w * 2)
        literal %= (w * 2)
        x = literal // (2)
        seen = literal % 2
        return x, y, Type(seen + Type.SEEN_G.value)
    elif literal >= h * w * person_type_nb:
        literal -= h * w * person_type_nb
        y = literal // (w * 6)
        literal %= (w * 6)
        x = literal // 6
        sound = literal % 6
        return x, y, Type(sound + Type.SOUND_0.value)
    else:
        y = literal // (w * person_type_nb)
        literal %= w * person_type_nb
        x = literal // person_type_nb
        literal %= person_type_nb
        return x, y, Type(literal)


# je veux bien des explications
def get_initial_person_count_clauses(i: int, sign: int, elts: list[int]) -> ClauseBase:
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
                    x, y, t = decode_literal(literal_to_check)
                    x2, y2, t2 = decode_literal(elts[k])
                    if x == x2 and y == y2:
                        case_already_taken = True
                        break
                if not case_already_taken:
                    nc.append(sign * elts[k])
                    newCb.append(nc)

    return get_initial_person_count_clauses(2, 1, elts)


def k_parmis_n(n: int, k: int):
    if k > n or k == 0:
        return [[]]
    l = k_parmis_n(n, k - 1)
    nl = []
    for e in l:
        for j in range(n):
            if j not in e:
                if len(e) > 0:
                    if e[-1] >= j:
                        continue
                ne = e[:]
                ne.append(j)
                nl.append(ne)
    return nl


def count(n, k):
    if k <= 0:
        return [[]]
    l = count(n, k - 1)
    nl = []
    for e in l:
        for i in range(n):
            ne = e[:]
            ne.append(i)
            nl.append(ne)
    return nl


def at_lm_person_aux(s, e, l, elts, ):
    if l <= 0:
        return [[]]
    cb = []
    for j in range(s, e + 1 - l):
        cb2 = at_lm_person_aux(j + 1, e, l - 1, elts)
        for c in cb2:
            c2 = c[:]
            cb.append([elts[j]] + c2)
    return cb


def at_least_person(i, elts):
    if (i == 0):
        return [[]]
    else:
        print(0, len(elts), len(elts) - i, elts)
        return at_lm_person_aux(0, len(elts), len(elts) - i + 1, elts)


'''def at_most_person(i: int, elts: list[list[int]]) -> ClauseBase:
    cb = []
    li = k_parmis_n(len(elts), i + 1)
    li2 = count(len(elts[0]), len(li[0]))
    for c in range(len(li)):
        for l2 in li2:
            nc = []
            c2 = 0
            for l in li[c]:
                nc.append(-elts[l][l2[c2]])
                c2 += 1
            cb.append(nc)
    return cb'''


def at_most_person(i, elts):
    if i >= len(elts):
        return [[]]
    nelts = [-e for e in elts]
    return at_lm_person_aux(0, len(nelts), i + 1, nelts)


def clause_person_direction(elts, elts2):
    cb = []
    for i in range(len(elts)):
        cb2 = [-elts[i]] + elts2[i]
        cb.append(cb2)
        for e in elts2[i]:
            cb.append([-e, elts[i]])
    return cb


def generate_person_literals(type: str) -> list[list[Literal]]:
    l = []
    l2 = []
    for x in range(w):
        for y in range(h):
            l.append(literal_from_cell(x, y, type, None))
            l3 = []
            for t in [HC.N, HC.E, HC.S, HC.W]:
                l3.append(literal_from_cell(x, y, type, t))
            l2.append(l3)
    return l, l2


def vision(type):
    cb = []
    for x in range(w):
        for y in range(h):
            seen_lit = literal_from_seen(x, y, 0 if type == 'g' else 1)
            c1 = [-seen_lit]
            civil_lit = None
            if type=='g':
                civil_lit = literal_from_cell(x,y,"c",None)
                cb.append( [-seen_lit,-civil_lit])
            ls = [(1, 0), (2, 0), (-1, 0), (-2, 0), (0, 1), (0, 2), (0, -1), (0, -2)] if type == 'g' else [(1, 0), (-1, 0),  (0, 1),  (0, -1)]
            for rx, ry in ls:
                x2 = rx + x
                y2 = y + ry
                if not (0 <= x2 < w and 0 <= y2 < h):
                    continue
                dir = None
                if ry > 0:
                    dir = HC.S
                elif ry < 0:
                    dir = HC.N
                elif rx > 0:
                    dir = HC.W
                elif rx < 0:
                    dir = HC.E
                person_lit = literal_from_cell(x2, y2, type, dir)
                c1.append(person_lit)
                c2 = [seen_lit,-person_lit]
                if type == 'g':
                    c2.append(civil_lit)
                cb.append(c2)
            cb.append(c1)
    return cb


def get_initial_person_count_clauses() -> ClauseBase:
    cb = []
    for type, count in [('g', guard_count), ('c', civil_count)]:
        glts, glts2 = generate_person_literals(type)
        print(glts, glts2)
        cb += at_least_person(count, glts)
        cb += at_most_person(count, glts)
        cb += clause_person_direction(glts, glts2)
        go = []  # qu'une seule direction par case
        n_pos = []
        for position in glts2:
            n_pos = [e for e in position]
            go += at_most_person(1, n_pos)
        cb += go
        cb += vision(type)
    # clts = generate_person_literals("c")
    # cl = at_least_person(civil_count, clts)
    # cm = at_most_person(civil_count, clts)
    # co = []  # qu'une seule direction par case
    # n_pos = []
    # for position in clts:
    #    n_pos = [[e] for e in position]
    #    co += at_most_person(1, n_pos)

    # n_pos = []
    # for i in range(len(clts)):
    #    n_pos = [[e] for e in clts[i] + glts[i]]
    #    co += at_most_person(1, n_pos)

    return cb


def init_KB(status):
    global w, h, guard_count, civil_count
    w, h = status["n"], status["m"]
    print("w :", w, "h:", h)
    w, h = 1, 3
    guard_count = status["guard_count"]
    civil_count = status["civil_count"]
    guard_count = 1
    civil_count = 1
    print("g :", guard_count, "c:", civil_count)
    return get_initial_person_count_clauses()


def print_kb(kb):
    for c in kb:
        print("[")
        for l in c:
            if l < 0:
                print("non", end=" ")
                l *= -1
            print(decode_literal(l))
        print("]")


if __name__ == '__main__':
    w = 2
    for i in range(50):
        print(literal_from_seen(1,0,1))
        print( i,decode_literal(i))