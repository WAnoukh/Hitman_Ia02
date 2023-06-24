from hitman.hitman import HC
from pprint import pprint
import subprocess
from typing import Tuple, List

# from sat import *

hr = None
status = None
directions = None
solid_cells =None
vision_KB = None
route_map = None
KB = []

def printMat(mat):
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            print(str(mat[i][j]).ljust(10), end=" ")
        print(" ")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")


def print_vision_KB():
    cpy = [c[:] for c in reversed(vision_KB)]
    printMat(cpy)


def print_vision_RM():
    cpy = [c[:] for c in reversed(route_map)]
    printMat(cpy)


def add_to_KB_clauses_List(clauses_list : List[List[str]]) :
    for c in clauses_list :
        KB.append(c)

def add_to_KB_clause(clause : List[str]) :
    KB.append(clause)

#pas trop compris
def update_KB():
    for (x, y), cell in status["vision"]:
        vision_KB[y][x] = cell # cell = ce que contient la case
        litteral = str()   # a finir
    # print_vision_KB()
    # pprint(status)



def move():
    print("move !")
    global status
    x, y = status["position"]
    route_map[y][x] = status["orientation"]
    status = hr.move()
    update_KB()
    print_vision_RM()

#ok
def turn_anti_clockwise():
    print("turn anti !")
    global status
    status = hr.turn_anti_clockwise()
    update_KB()

#ok
def turn_clockwise():
    print("turn clock !")
    global status
    status = hr.turn_clockwise()
    update_KB()

#ok
def turn_toward(orientation):
    current_orientation = status["orientation"].value
    orientation = orientation.value
    if current_orientation == orientation:
        return
    if abs(current_orientation - orientation) == 2:
        turn_clockwise()
        turn_clockwise()
        return
    if (HC.N.value if current_orientation == HC.W.value else current_orientation + 1) == orientation:
        turn_clockwise()
        return
    if (HC.W.value if current_orientation == HC.N.value else current_orientation - 1) == orientation:
        turn_anti_clockwise()
        return


def cardinal_to_dir(car):
    for x, y, cardinal in directions:
        if cardinal == car:
            return x, y


def opposite_cardinal(car):
    if car == HC.N:
        return HC.S
    if car == HC.S:
        return HC.N
    if car == HC.E:
        return HC.W
    if car == HC.W:
        return HC.E


def get_cell_forward():
    x, y = cardinal_to_dir(status["orientation"])
    return vision_KB[y][x]


def idiot_route(first=False):
    print("----------------------------------------------------")
    global status
    # s'oriente vers le nord
    initial_orientation = status["orientation"]
    print("orientate north")
    while status["orientation"] != HC.N:
        turn_anti_clockwise()
    # tourne jusqu'a trouver un espace libre
    print("searching empty")
    width, height = status['n'], status['m']
    while True:
        fwrd_cell = get_cell_forward()
        rx, ry = cardinal_to_dir(status["orientation"])
        x, y = status["position"]
        x2, y2 = x + rx, y + ry
        cond = len(status["vision"]) > 0
        print("foward cell is out of map ?", cond)
        if cond:
            cond = cond and status["vision"][0][1] not in solid_cells
            print("foward cell is solid block ?", cond)
            if status["vision"][0][1] in solid_cells:
                route_map[y2][x2] = -1
            cond = cond and (route_map[y2][x2] == 0)
            print("foward cell {},{} is already visited ?".format(x2, y2), route_map[y2][x2], )
        if cond:
            print("found !")
            move()
            # input("clic to continue...")
            # time.sleep(0.2)
            idiot_route()
            print("backpropagated")
        else:
            print("not found")
        turn_clockwise()
        if status["orientation"] == HC.N:
            # tour complet -> reviens en arrière
            # se réoriente dans la direction opposée d'arrivée
            if not first:
                turn_toward(opposite_cardinal(initial_orientation))
                move()
                turn_clockwise()
                turn_clockwise()
            return
    # 1/0 # doit aussi verifier que chemin pas empreinté
    # fwrd_cell = get_cell_forward()
    # while fwrd_cell in solid_cells:
    #    rx, ry = cardinal_to_dir(status["orientation"])
    #    x, y = status["position"]
    #    if route_map[x+rx][y+ry] != 0:
    #        continue
    #    turn_clockwise()
    #    fwrd_cell = get_cell_forward()
    #    if status["orientation"] == HC.N:
    #        # tour complet -> reviens en arrière
    #        # se réoriente dans la direction opposée d'arrivée
    #        turn_toward(opposite_cardinal(initial_orientation))
    #        return


def send_soluce():
    sol = {}
    for i in range(len(vision_KB)):
        for j in range(len(vision_KB[i])):
            sol[(j, i)] = vision_KB[i][j]
    pprint(hr.send_content(sol))
    print(status["penalties"])



####### Creer un fichier .cnf a partir de la KB et le solve via gophersat #######

def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(filename: str, cmd: str = "gophersat", encoding: str = "utf8") -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]


# Exemple d'utilisation
# cnf_formula = "p cnf 3 2\n1 2 0\n-2 -3 0\n"
# file_name = "test.cnf"
# write_dimacs_file(cnf_formula, file_name)
# solution = exec_gophersat(file_name)
# print("Solution :", solution)

def phase1_run(n_hr,n_status):
    global hr, status,directions,solid_cells,vision_KB,route_map
    hr = n_hr
    status = n_status

    directions = [(0, 1, HC.N), (1, 0, HC.E), (0, -1, HC.S), (-1, 0, HC.W)]
    solid_cells = [HC.WALL, HC.GUARD_E, HC.GUARD_S, HC.GUARD_W, HC.GUARD_N, HC.GUARD_N, None]
    vision_KB = [[None] * status['n'] for _ in range(status['m'])]
    route_map = [[0] * status['n'] for _ in range(status['m'])]

    update_KB()
    idiot_route(True)
    send_soluce()
    pass