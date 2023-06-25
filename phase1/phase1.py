from phase1.sat import *
from hitman.hitman import HitmanReferee
from phase1.lien_avec_gophersat import *

hr, status = None, None
sat_kb = []
guessed = 0
map = None
persons_list= [HC.GUARD_W,HC.GUARD_N,HC.GUARD_E,HC.GUARD_S,HC.CIVIL_E,HC.CIVIL_S,HC.CIVIL_W,HC.CIVIL_N]

def add_to_kb(literal):
    sat_kb.append([literal])

def update_kb(status,first=False):
    global guessed
    for (x,y),type in status["vision"] :
        if map[y][x] is None:
            guessed +=1
        map[y][x] = type
        is_guard = False
        is_civil = False
        if 3<=type.value <=6:
            add_to_kb(literal_from_cell(x,y,"g", type.value-3+14))
            is_guard = True
        elif 7 <= type.value <= 10:
            add_to_kb(literal_from_cell(x, y, "g", type.value - 7 + 14))
            is_civil = True
        if not is_guard:
            add_to_kb(-literal_from_cell(x, y, "g", None))
        if not is_civil:
            add_to_kb(-literal_from_cell(x, y, "c", None))
    x,y = status["position"]
    if status["is_in_guard_range"]:
        add_to_kb(literal_from_seen(x,y,0))
    elif not first:
        add_to_kb(-literal_from_seen(x, y, 0))
    add_to_kb(literal_from_sound(x, y, status["hear"]))
    print(guessed*2,"point against ", status["penalties"],"penalities")

def phase1_run(n_hr, n_status):
    global hr, status, map,sat_kb
    hr = n_hr
    status = n_status
    map = [[None] * status['n'] for _ in range(status['m'])]
    sat_kb = init_KB(status)
    update_kb(status,first=True)

def printMat(mat):
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    for i in range(len(mat)-1,-1,-1):
        for j in range(len(mat[i])):
            print(str(mat[i][j]).ljust(10), end=" ")
        print(" ")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")

def main():
    hr = HitmanReferee()
    status = hr.start_phase1()
    phase1_run(hr, status)
    #print(sat_kb)
    #print(len(sat_kb))
    sat_kb.append([literal_from_seen(0, 0, 1)])
    dmac = clauses_to_dimacs(sat_kb, nb_var())
    file_name = "test.cnf"
    write_dimacs_file(dmac, file_name)
    solution = exec_gophersat(file_name)
    print("Solution :", solution)
    s2 = [e2 for e2 in solution[1] if e2 > 0]