from hitman import HC, HitmanReferee, complete_map_example
from typing import List, Tuple, Dict

from phase1 import *

def main():
    update_KB()
    idiot_route(True)
    send_soluce()
    complete_map_example[(7, 0)] = HC.EMPTY
    pass


if __name__ == '__main__':
    #print_vision_KB()
    main()
