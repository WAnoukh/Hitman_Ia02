from hitman.hitman import HC
from copy import deepcopy
from enum import Enum
from oracle import set_world_exemple, Oracle

target_x, target_y = (0, 1)
start_x, start_y = (0, 0)
wire_x, wire_y = (2, 2)


class State:
    def __init__(self, hr, status, euristic, pred, method, clt=0, crt=0, prevPos=None):
        self.hr = hr
        self.status = status
        self.euristic = euristic
        self.pred = pred
        self.method = method
        self.consecutive_l_turn = clt
        self.consecutive_r_turn = crt
        if prevPos is None:
            prevPos = []
        self.previousPos = prevPos


class Action(Enum):
    move = 0
    kill_target = 1
    neutralize_guard = 2
    neutralize_civil = 3
    take_suit = 4
    take_weapon = 5
    put_on_suit = 6
    turn_clockwise = 7
    turn_anti_clockwise = 8
    CIVIL_W = 9
    TARGET = 10


states = []


def euristic(hr, status):
    eur = 0
    pos_x, pos_y = status["position"]
    if (not status["has_weapon"]):
        eur = abs(pos_x - wire_x) + abs(pos_y - wire_y)
        # plus dist bet wire and target
        eur += abs(wire_x - target_x) + abs(wire_y - target_y) * 2
        # plus dist bet target exit
        eur += abs(start_x - target_x) + abs(start_y - target_y) * 2
        eur += 4
    elif (not status["is_target_down"]):
        eur = abs(pos_x - target_x) + abs(pos_y - target_y)
        # plus dist bet target exit
        eur += abs(start_x - target_x) + abs(start_y - target_y) * 2
        eur += 2
    else:
        eur = abs(start_x - pos_x) + abs(start_y * pos_y)
    eur += status["penalties"]
    return eur


def pop_state():
    return states.pop(0)


def push_state(state):
    i = 0
    while i < len(states):
        if states[i].euristic < state.euristic:
            i += 1
        else:
            break
    states.insert(i, state)


def is_goal(state):
    return state.status["is_target_down"] and state.status["position"] == (start_x, start_y)


def execute_action(hr, old_status, i):
    status = None
    if i is None:
        return
    if i == Action.move:
        status = hr.move()
    elif i == Action.kill_target:
        status = hr.kill_target()
    elif i == Action.neutralize_guard:
        status = hr.neutralize_guard()
    elif i == Action.neutralize_civil:
        status = hr.neutralize_civil()
    elif i == Action.take_suit:
        status = hr.take_suit()
    elif i == Action.take_weapon:
        status = hr.take_weapon()
    elif i == Action.put_on_suit:
        status = hr.put_on_suit()
    elif i == Action.turn_clockwise:
        status = hr.turn_clockwise()
    elif i == Action.turn_anti_clockwise:
        status = hr.turn_anti_clockwise()
    return status


def action_name_from_state(state):
    i = state.method
    if i is not None:
        return i.name
    return "Start"


def succ(state):
    list = []
    for index in range(9):
        action = Action(index)
        if action == Action.turn_clockwise:
            if state.method == Action.turn_anti_clockwise or state.consecutive_r_turn >= 2:
                continue
        elif action == Action.turn_anti_clockwise:
            if state.method == Action.turn_clockwise or state.consecutive_l_turn >= 2:
                continue
        elif action == Action.kill_target and state.method == Action.kill_target:
            continue
        elif action == Action.put_on_suit and state.status["is_suit_on"]:
            continue
        n_hr, n_status, n_eur = deepcopy(state.hr), None, None

        try:
            n_status = execute_action(n_hr, state.status, action)
        except:
            continue

        if n_status["status"] == 'OK':
            n_previousPos = state.previousPos[:]
            if action == Action.move:
                position = n_status["position"]
                oldpos = state.status["position"]
                pass
                if position in state.previousPos:
                    continue
                else:
                    n_previousPos.append(oldpos)
            elif action not in [Action.turn_clockwise, Action.turn_anti_clockwise, Action.put_on_suit]:
                n_previousPos = []
            clt = 0
            crt = 0
            if action == Action.turn_clockwise:
                crt = state.consecutive_r_turn
                crt += 1
            elif action == Action.turn_anti_clockwise:
                clt = state.consecutive_l_turn
                clt += 1

            list.append(State(n_hr, n_status, euristic(n_hr, n_status), state, action, clt, crt, n_previousPos))
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
            print(action_name_from_state(st), st.euristic, st.status["penalties"], st.status["position"], end="")
        print("]")
    else:
        print("start State")


def A_star(hr, status):
    initial_state = State(hr, status, euristic(hr, status), None, None)
    #push_state(initial_state)
    save = [initial_state.status]
    state = initial_state
    i = 0
    while not is_goal(state):
        for suc in succ(state):
            edited_status = suc.status.copy()
            edited_status["penalties"] = 0
            # we are doing this because we want to not being in the same place with everything else the same, because it's
            # mean that we are doing the same thing but with more penalties
            # so we are saving status with 0 penalties to only check if something else is different
            if edited_status not in save:
                save.append(edited_status)
                push_state(suc)
        if len(states) == 0:
            break

        # print(i,end=" ")

        print_path(state)
        for s in succ(state):
            print("|->",end=" ")
            print_path(s)
        print("------------")
        for s in states:
            print("         |",end=" ")
            print_path(s)
        print("------------")
        state = pop_state()
        i += 1
        # prin
    print("finished in", i, "iterations !")
    print("with", state.status["penalties"], "penalties !")
    print("Score :", state.status["penalties"] / i)
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

from pprint import pprint

def phase2_run(hr, status, map):
    search_map(map, status)
    set_world_exemple( [[map[(x, y)] for x in range(status['n'])] for y in range(status['m'])])
    print([[map[(x, y)] for x in range(status['n'])] for y in range(status['m'])])
    oracle = Oracle()
    o_status = oracle.start_phase2()
    state = A_star(oracle, o_status)
    print("\n\n\n\nFINAL :")
    print_path(state)

    for st in get_state_path(state):
        status = execute_action(hr, status, st.method)
        # print(action_name_from_state(st))
        # pprint(status)
    return
