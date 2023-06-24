from phase2 import phase2_run
from pprint import pprint
from hitman import HitmanReferee, complete_map_example

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
    phase2_run(hr, status, true_map)
    _, score, history = hr.end_phase2()
    print(score)
    print(history)
