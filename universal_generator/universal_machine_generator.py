

class Transition():

    def __init__(self, current_state, read, to_state, write, action):
        self.current_state = current_state
        self.read = read
        self.to_state = to_state
        self.write = write
        self.action = action

    def to_dict(self):
        return { 
                    'read':self.read,
                    'to_state': self.to_state,
                    'write': self.write,
                    'action': self.action
                }


def remove_char_from_list(c: chr, lst: list):
    return list(filter(lambda element: element != c, lst))


def main():
    STATES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'W', 'X', 'Y', 'Z']
    FINAL_STATE = 'Z'
    INPUT_ALPHABET = ['1', '.', '+', '=', '-', '0']
    TRANSITIONS_START = '¡'
    TRANSITIONS_END= '!'
    TRANSITIONS_DESCRIPTION_SEPARATOR = '?'
    POINTER = '*'

    all_characters = set() 
    all_characters.update(STATES)
    all_characters.update(FINAL_STATE)
    all_characters.update(INPUT_ALPHABET)
    all_characters.update(TRANSITIONS_START)
    all_characters.update(TRANSITIONS_END)
    all_characters.update(TRANSITIONS_DESCRIPTION_SEPARATOR)
    all_characters.update(['<', '>'])
    all_characters = sorted(all_characters) #to list

    ALPHABET = all_characters

    transition_dict = {}

    transition_dict['find_initial'] = []
    for state in STATES:
        t = Transition('find_initial', state, f'go_read_input_{state}', state, 'RIGHT')
        transition_dict['find_initial'].append(t.to_dict())

    #go_read_input_{state}
    #once machine knows the initial state, leads to read the first character
    #of the input. cursor finds '!' (TRANSITIONS_END) character
    #and reads the character on the right
    for state in STATES:
        current_state = f'go_read_input_{state}'
        transition_dict[current_state] = []
        for c in remove_char_from_list(TRANSITIONS_END, all_characters):
            t = Transition(current_state, c, current_state, c, 'RIGHT')
            transition_dict[current_state].append(t.to_dict())
        t = Transition(current_state, TRANSITIONS_END, f'read_input_{state}', TRANSITIONS_END, 'RIGHT')
        transition_dict[current_state].append(t.to_dict())


    #read_input_{state}
    #machine is in the position ready to read the input character     
    for state in STATES:
        current_state = f'read_input_{state}'
        transition_dict[current_state] = []
        for char in INPUT_ALPHABET:
            t = Transition(current_state, char, f'go_find_transitions_start_{state}_{char}', POINTER, 'LEFT')
            transition_dict[current_state].append(t.to_dict())


    #go_find_transitions_start_{state}_{char}
    #knowing the state and the read char, machine goes to the transitions 
    #beginning (TRANSITIONS_START, '¡')
    for state in STATES:
        for char in INPUT_ALPHABET:
            current_state = f'go_find_transitions_start_{state}_{char}'
            transition_dict[current_state] = []
            for c in remove_char_from_list(TRANSITIONS_START, all_characters):
                t = Transition(current_state, c, current_state, c, 'LEFT')
                transition_dict[current_state].append(t.to_dict())
            t = Transition(current_state, TRANSITIONS_START, f'go_next_transition_start_{state}_{char}', TRANSITIONS_START, 'RIGHT')
            transition_dict[current_state].append(t.to_dict())

    #go_next_transition_start_{state}_{char}
    #as transition descriptions are preceded by the '?' character
    #machine goes to the next '?'
    for state in STATES:
        for char in INPUT_ALPHABET:
            current_state = f'go_next_transition_start_{state}_{char}'
            transition_dict[current_state] = []
            for read in remove_char_from_list(TRANSITIONS_DESCRIPTION_SEPARATOR, all_characters):
                t = Transition(current_state, read, current_state, read, 'RIGHT')
                transition_dict[current_state].append(t.to_dict())
            t = Transition(current_state, TRANSITIONS_DESCRIPTION_SEPARATOR, f'read_transitions_start_{state}_{char}', TRANSITIONS_DESCRIPTION_SEPARATOR, 'RIGHT')
            transition_dict[current_state].append(t.to_dict())


    #read_transitions_start_{state}_{char}
    #here the machine is checking if the state character is the one is
    #looking for (_{state}_)
    #in case it doesn't match, goes to the next '?'
    #otherwise leads to check the 'read' character
    for state in STATES:
        for char in INPUT_ALPHABET:
            current_state = f'read_transitions_start_{state}_{char}'
            transition_dict[current_state] = []
            for read in remove_char_from_list(state, all_characters):
                t = Transition(current_state, read, f'go_next_transition_start_{state}_{char}', read, 'RIGHT')
                transition_dict[current_state].append(t.to_dict())
            t = Transition(current_state, state, f'check_read_character_in_transition_{state}_{char}', state, 'RIGHT')
            transition_dict[current_state].append(t.to_dict())


    #check_read_character_in_transition_{state}_{char}
    #as the state matches, here machine checks if the read matches too
    #otherwise, it will go to the next '?'
    for state in STATES:
        for char in INPUT_ALPHABET:
            current_state = f'check_read_character_in_transition_{state}_{char}'
            transition_dict[current_state] = []
            for read in remove_char_from_list(char, ALPHABET):
                t = Transition(current_state, read, f'go_next_transition_start_{state}_{char}', read, 'RIGHT')
                transition_dict[current_state].append(t.to_dict())
            t = Transition(current_state, char, f'load_action_next_state', char, 'RIGHT')
            transition_dict[current_state].append(t.to_dict())

    #load_action_next_state
    #machine is on the correct transition description.
    #here it reads the next state the machine will have after performing
    #the operation
    current_state = 'load_action_next_state'
    transition_dict[current_state] = []
    for state in STATES:
        t = Transition(current_state, state, f'load_action_write__{state}', state, 'RIGHT')
        transition_dict[current_state].append(t.to_dict())


    #load_action_write__{state}
    #here it reads the character to write on the target place
    for state in STATES:
        current_state = f'load_action_write__{state}'
        transition_dict[current_state] = []
        for char in INPUT_ALPHABET:
            t = Transition(current_state, char, f'load_direction__{state}_{char}', char, 'RIGHT')
            transition_dict[current_state].append(t.to_dict())

    
    #load_direction__{state}_{char}
    #here it reads the direction the machine will have to go after
    #performing the write operation
    for state in STATES:
        for char in INPUT_ALPHABET:
            current_state = f'load_direction__{state}_{char}'
            transition_dict[current_state] = []
            t = Transition(current_state, '<', f'exec_{state}_{char}_LEFT', '<', 'RIGHT')
            transition_dict[current_state].append(t.to_dict())
            t = Transition(current_state, '>', f'exec_{state}_{char}_RIGHT', '>', 'RIGHT')
            transition_dict[current_state].append(t.to_dict())


    #exec_{state}_{char}_{direction}'
    #time to find the pointer
    #the 'HALT' state here is 'W'
    for state in STATES:
        for char in INPUT_ALPHABET:
            for direction in ["LEFT", "RIGHT"]:
                current_state = f'exec_{state}_{char}_{direction}'
                transition_dict[current_state] = []
                for read in remove_char_from_list(POINTER, ALPHABET):
                    t = Transition(current_state, read, current_state, read, 'RIGHT')
                    transition_dict[current_state].append(t.to_dict())
                if state == 'W':
                    t = Transition(current_state, POINTER, 'W', char, direction)
                else:
                    t = Transition(current_state, POINTER, f'read_input_{state}', char, direction)
                transition_dict[current_state].append(t.to_dict())



    ########### auto-cleaning process before HALT ###########
    #added steps before halt, to clean the coded input
    current_state = 'W'
    transition_dict[current_state] = []
    for read in remove_char_from_list(TRANSITIONS_END, ALPHABET):
        t = Transition(current_state, read, current_state, read, 'LEFT')
        transition_dict[current_state].append(t.to_dict())
    t = Transition(current_state, TRANSITIONS_END, 'X', '.', 'LEFT')
    
    transition_dict[current_state].append(t.to_dict())
    current_state = 'X'
    transition_dict[current_state] = []
    for read in remove_char_from_list(TRANSITIONS_START, ALPHABET):
        t = Transition(current_state, read, current_state, '.', 'LEFT')
        transition_dict[current_state].append(t.to_dict())
    t = Transition(current_state, TRANSITIONS_START, 'Y', '.', 'LEFT')
    
    transition_dict[current_state].append(t.to_dict())
    current_state = 'Y'
    transition_dict[current_state] = []
    for read in STATES:
        t = Transition(current_state, read, 'Z', '.', 'RIGHT')
        transition_dict[current_state].append(t.to_dict())

 
                    
    import json
    output_json = {}
    output_json['name'] = 'universal'
    output_json['alphabet'] = ALPHABET
    output_json['blank'] = '.'
    output_json['states'] = STATES + ['find_initial']
    output_json['initial'] = 'find_initial' 
    output_json['finals'] = ['Z']
    output_json['transitions'] = transition_dict

    with open("universal_machine.json", "w") as outfile: 
        json.dump(output_json, outfile)


if __name__ == '__main__':
    main()




