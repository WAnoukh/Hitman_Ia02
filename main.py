from hitman import HC, HitmanReferee, complete_map_example
from pprint import pprint
import heapq
from copy import deepcopy

target_x, target_y = (0, 1)
start_x, start_y = (0, 0)
wire_x, wire_y = (2, 2)


class State:
    def __init__(self, hr, status, euristic, pred, method):
        self.hr = hr
        self.status = status
        self.euristic = euristic
        self.pred = pred
        self.method = method


states = []


def euristic(hr, status):
    eur = 0
    pos_x, pos_y = status["position"]
    if (not status["has_weapon"]):
        eur = abs(pos_x - wire_x) + abs(pos_y - wire_y)
        # plus dist bet wire and target
        eur += abs(wire_x - target_x) + abs(wire_y - target_y)*2
        # plus dist bet target exit
        eur += abs(start_x - target_x) + abs(start_y - target_y)*2
    elif (not status["is_target_down"]):
        eur = abs(pos_x - target_x) + abs(pos_y - target_y)
        # plus dist bet target exit
        eur += abs(start_x - target_x) + abs(start_y - target_y)*2
    else:
        eur = abs(start_x - pos_x) + abs(start_y * pos_y)
    eur += status["penalties"]
    return eur


def pop_state():
    return states.pop(0)


def push_state(state):
    i = 0
    while i < len(states):
        if (states[i].euristic < state.euristic):
            i += 1
        else:
            break
    states.insert(i, state)


def is_goal(state):
    return state.status["is_target_down"] and state.status["position"] == (start_x, start_y)


def execute_action(hr, old_status, i):
    status = None
    if i == 0:
        status = hr.move()
    elif i == 2:
        status = hr.kill_target()
    elif i == 3:
        status = hr.neutralize_guard()
    elif i == 4:
        status = hr.neutralize_civil()
    elif i == 5:
        status = hr.take_suit()
    elif i == 6:
        status = hr.take_weapon()
    elif i == 7:
        status = hr.put_on_suit()
    elif i == 8:
        status = hr.turn_clockwise()
    elif i == 1:
        status = hr.turn_anti_clockwise()
    return status


def action_name_from_state(state):
    i = state.method
    if i == 0:
        return "move()"
    elif i == 2:
        return "kill_target()"
    elif i == 3:
        return "neutralize_guard()"
    elif i == 4:
        return "neutralize_civil()"
    elif i == 5:
        return "take_suit()"
    elif i == 6:
        return "take_weapon()"
    elif i == 7:
        return "put_on_suit()"
    elif i == 8:
        return "turn_clockwise()"
    elif i == 1:
        return "turn_anti_clockwise()"
    return "Start"


def succ(state):
    list = []
    for i in range(9):
        n_hr, n_status, n_eur = deepcopy(state.hr), None, None
        try:
            n_status = execute_action(n_hr, state.status, i)
        except:
            continue
        if n_status["status"] == 'OK':
            list.append(State(n_hr, n_status, euristic(n_hr, n_status), state, i))
    '''for el in map(action_name_from_state,list[:]):
        print(el)'''
    return list


def get_state_path(state):
    actions = [state]
    while state.pred is not None:
        actions.insert(0, state.pred)
        state = state.pred
    return actions

def print_path(state):
    print("[", end='')
    started = False
    path = get_state_path(state)
    if path is not None:
        for st in path:
            if started:
                print(", ", end="")
            else:
                started = True
            print(action_name_from_state(st), st.euristic,st.status["penalties"],st.status["position"], end="")
        print("]")
    else:
        print("start State")

def A_star(hr, status):
    initial_state = State(hr, status, euristic(hr, status), None, None)
    push_state(initial_state)
    save = [initial_state.status]
    state = initial_state
    while not is_goal(state):
        for suc in succ(state):
            if suc.status not in save:
                save.append(suc.status)
                push_state(suc)
        state = pop_state()
        #print_path(state)
    return state


def search_map(map, status):
    global wire_x, wire_y, target_x, target_y
    m, n = status['m'], status['n']
    for x in range(n):
        for y in range(m):
            if map[(x, y)] == HC.PIANO_WIRE:
                wire_x, wire_y = x, y
            elif map[(x, y)] == HC.TARGET:
                target_x, target_y = x, y


def phase2_run(hr, status, map):
    search_map(map, status)
    state = A_star(hr, status)
    print("\n\n\n\nFINAL :")
    print_path(state)
    return


if __name__ == '__main__':
    hr = HitmanReferee()
    status = hr.start_phase1()
    pprint(status)
    hr.send_content(complete_map_example)
    _, score, history, true_map = hr.end_phase1()
    pprint(score)
    pprint(true_map)
    pprint(history)
    status = hr.start_phase2()
    pprint(status)
    phase2_run(hr, status, true_map)
    _, score, history = hr.end_phase2()
    # pprint(score)
    # pprint(history)
