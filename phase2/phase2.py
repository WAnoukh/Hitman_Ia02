from Astar import A_star,print_path,get_state_path,execute_action
from pprint import pprint

def phase2_run(hr, status, map):
    state = A_star(hr, status,map)
    print("\n\n\n\nFINAL :")
    print_path(state)

    for st in get_state_path(state):
        status = execute_action(hr, status, st.method)
        # print(action_name_from_state(st))
        # pprint(status)
    return
