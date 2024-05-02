import json
import sys

def create_state_equivalences(states):
    num_of_states = len(states) 
    encoded_states = [chr(n) for n in range(ord('A'), ord('A') + num_of_states)]
    equivalences = {}
    for i, state in enumerate(states):
        if (state == 'HALT'):
        #pseudo-halt. in the universal turing machine this drives to the
        #'auto-cleaner' state, inn which the encoded instructions are erased
            equivalences[state] = 'W' 
        else: 
            equivalences[state] = encoded_states[i]
    return equivalences 


def encode_transition(transition_current_state, transition_description, state_equivalences):
    
    encoded_transition = ''
    encoded_transition += state_equivalences[transition_current_state]
    encoded_transition += transition_description['read']
    encoded_transition += state_equivalences[transition_description['to_state']]
    encoded_transition += transition_description['write']
    encoded_transition += '>' if (transition_description['action'] == 'RIGHT') else '<'
    return encoded_transition

def main():

    if (len(sys.argv) != 2):
        print("usage: python3 encode_turing_json.py path/unary_add.json")
        return 1

    file = open(sys.argv[1])
    data = json.load(file)
    state_equivalences = create_state_equivalences(data['states'])


    encoded_turing = ''
    encoded_turing += state_equivalences[data['initial']] + '¡'
    for transition_current_state in data['transitions']:
        for transition_description in data['transitions'][transition_current_state]:
            encoded_turing += '?' + encode_transition(transition_current_state, transition_description, state_equivalences)

    encoded_turing += '!'

    print('####################################')
    print('# Universal turing machine encoder #')
    print('####################################')

    print(f'To run the machine {data["name"]} on the universal turing machine run:')
    print()
    print(encoded_turing + '\x1b[\33[104m' + 'your input here' + '\x1b[0m')
    print()
    return encoded_turing


if __name__ == '__main__':
    main()



