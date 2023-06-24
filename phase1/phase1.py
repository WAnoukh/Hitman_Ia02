from phase1.sat import *
from hitman.hitman import HitmanReferee
from phase1.lien_avec_gophersat import *

hr, status = None, None
sat_kb = []


def phase1_run(n_hr, n_status):
    global hr, status
    hr = n_hr
    status = n_status


def main():
    hr = HitmanReferee()
    status = hr.start_phase1()
    phase1_run(hr, status)
    global sat_kb
    sat_kb = init_KB(status)
    print(sat_kb)
    print_kb(sat_kb)
    print(len(sat_kb))
    sat_kb.append([literal_from_seen(0, 0, 1)])
    dmac = clauses_to_dimacs(sat_kb, nb_var())
    file_name = "test.cnf"
    write_dimacs_file(dmac, file_name)
    solution = exec_gophersat(file_name)
    print("Solution :", solution)
    s2 = [e2 for e2 in solution[1] if e2 > 0]
    print_kb([s2])
