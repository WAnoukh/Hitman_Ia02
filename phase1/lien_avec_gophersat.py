import subprocess
from typing import Tuple, List

# à décommenter pour tester 

def clauses_to_dimacs(clauses, nb_vars):
    s = "p cnf {} {}\n".format(nb_vars, len(clauses))
    for clause in clauses:
        for literal in clause:
            s += str(literal) + " "
        s += "0\n"
    return s



def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(filename: str, cmd: str = "gophersat", encoding: str = "utf8") -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd,filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]






# Exemple d'utilisation
if __name__ == '__main__':
    cnf_formula = "p cnf 3 2\n1 0\n-1 0\n"
    file_name = "../test.cnf"
    write_dimacs_file(cnf_formula, file_name)
    solution = exec_gophersat(file_name)
    print("Solution :", solution)