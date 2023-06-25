from phase1.sat import *
from hitman.hitman import HitmanReferee
from phase1.lien_avec_gophersat import *
from Astar import A_star, print_path, get_state_path, execute_action
from pprint import pprint
from copy import deepcopy

hr, status = None, None
sat_kb = []
guessed = 0
map = None
persons_list = [HC.GUARD_W, HC.GUARD_N, HC.GUARD_E, HC.GUARD_S, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W, HC.CIVIL_N]


def add_to_kb(literal):
    sat_kb.append([literal])


def update_kb(status, first=False):
    global guessed
    for (x, y), type in status["vision"]:
        if map[y][x] is None:
            guessed += 1
        map[y][x] = type

#add to kb what Hitman sees
    # if hitman watch toward north or south
    if hitman->HC.N or hitman->HC.S : 
        ry = 1
        # while there is nothing to stop the view, hitman watch further (until 3 tiles)
        while (ry <= 3) and (case(x, y+ry) == type) and (type in [HC.EMPTY, HC.SUIT, HC.PIANO_WIRE]) : # pas sûre que ça marche
            if hitman->HC.N :
                add_to_kb(literal_from_cell_and_type(x, y+ry, type ))
            if hitman->HC.S :
                add_to_kb(literal_from_cell_and_type(x, y-ry, type ))
            ry += 1

    # if hitman watch toward West or East
    if hitman->HC.E or hitman->HC.W : 
        rx = 1
        # while there is nothing to stop the view, hitman watch further (until 3 tiles)
        while (rx <= 3) and (case(x + rx, y) == type) and (type in [HC.EMPTY, HC.SUIT, HC.PIANO_WIRE]) : 
            if hitman->HC.E :
                add_to_kb(literal_from_cell_and_type(x + rx, y, type ))
            if hitman->HC.W :
                add_to_kb(literal_from_cell_and_type(x - rx, y, type ))
            rx += 1



    x, y = status["position"]
    add_to_kb(-literal_from_cell(x, y, "g", None))

    add_to_kb(literal_from_sound(x, y, status["hear"]))


    #Use SAT solver to know if we can deduct that an unknown tile hosts a guard
    for x,y in unknown_tiles :
        
        sat_test = deepcopy(sat_kb)
        sat_test.append(f"-{literal_from_cell(x, y, 'g', None)}") 

        dimacs_string = clauses_to_dimacs(sat_test, h*w*len(Type))
        file_name = "../test.cnf"
        write_dimacs_file(dimacs_string, file_name)

        directions = [None, HC.N, HC.S, HC.W, HC.E]
        j = 0
        
        # KB + not guard on an unknown tile   -->  if it is unsat, we know that there is a guard on this tile 
        # if we know there is a guard on this tile, we have to know its direction so we test with HC.N, HC.S, HC.W, HC.E
        # when we have     KB + not guard with a direction --> unsat    we know the direction of the guard
        while (j == 0 and exec_gophersat(file_name) == False ) or (0 < j and j < 5 and exec_gophersat(file_name) != False) :
            sat_test = deepcopy(sat_kb)
            dimacs_string = clauses_to_dimacs(sat_test, h*w*len(Type))
            sat_test.append(f"-{literal_from_cell(x, y, 'g', directions[j])}") 
            write_dimacs_file(dimacs_string, file_name)
            j += 1
        
        if j < 1 and 4 < j :
            add_to_kb(literal_from_cell(x, y, "g", directions[j]))
            





    print(guessed * 2, "point against ", status["penalties"], "penalities ! Score",guessed * 2- status["penalties"] )


def nearest_unknown(x, y, w, h, visited=None):
    if map[y][x] in [HC.WALL,HC.GUARD_W,HC.GUARD_N,HC.GUARD_E,HC.GUARD_S]:
        return
    if visited is None:
        visited = []
    visited.append((x, y))
    for rx, ry in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if (0 <= x + rx < w and 0 <= y + ry < h):
            if map[y + ry][x + rx] is None:
                if (x + rx, y + ry) not in visited:
                    return x + rx, y + ry
    for rx, ry in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if 0 <= x + rx < w and 0 <= y + ry < h:
            if (x + rx, y + ry) not in visited:
                ans = nearest_unknown(x + rx, y + ry, w, h, visited)
                if ans is not None:
                    return ans
    return None


def send_soluce(hr):
    sol = {}
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] is not None:
                sol[(j, i)] = map[i][j]
            else:
                sol[(j, i)] = HC.EMPTY
    print("solution ",sol)
    pprint(hr.send_content(sol))


def phase1_run(n_hr, n_status):
    global hr, status, map, sat_kb
    hr = n_hr
    status = n_status
    map = [[None] * status['n'] for _ in range(status['m'])]
    sat_kb = init_KB(status)
    update_kb(status, first=True)
    print(map)
    x, y = status["position"]
    w, h = status["n"], status["m"]
    nu = nearest_unknown(x, y, w, h)
    while nu != None:
        nux, nuy = nu
        custom_map = {}
        for i in range(h):
            for j in range(w):
                custom_map[(j, i)] = map[i][j] if map[i][j] is not None else HC.EMPTY
        #print("gaol :", nux, nuy)
        #printMat(map)
        #print(custom_map)
        state = A_star(n_hr, n_status, custom_map, nux, nuy, phase=1)
        #print("doing   ", end="")
        #print_path(state)
        #print_path(get_state_path(state)[1])
        n_status = execute_action(n_hr, n_status, get_state_path(state)[1].method)
        update_kb(n_status)
        #pprint(n_status)
        #printMat(map)
        x, y = n_status["position"]
        w, h = n_status["n"], n_status["m"]
        if map[nuy][nux] is not None:
            nu = nearest_unknown(x, y, w, h)
        #print("next nearest", nu)
        #input()
        #if guessed > h*w/2:
        #    break
    send_soluce(n_hr)
    pass


def printMat(mat):
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    for i in range(len(mat) - 1, -1, -1):
        for j in range(len(mat[i])):
            print(str(mat[i][j]).ljust(10), end=" ")
        print(" ")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")


def main():
    hr = HitmanReferee()
    status = hr.start_phase1()
    phase1_run(hr, status)
    # print(sat_kb)
    # print(len(sat_kb))
    '''sat_kb.append([literal_from_seen(0, 0, 1)])
    dmac = clauses_to_dimacs(sat_kb, nb_var())
    file_name = "test.cnf"
    write_dimacs_file(dmac, file_name)
    solution = exec_gophersat(file_name)
    print("Solution :", solution)
    s2 = [e2 for e2 in solution[1] if e2 > 0]'''
