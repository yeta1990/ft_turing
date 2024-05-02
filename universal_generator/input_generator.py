

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
    STATES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Z']
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
    print(all_characters)

    #print(list(filter(lambda a: a != '1', all_characters)))
    print(remove_char_from_list('!', all_characters))

    instruction = 'A¡?A1A1>?A+A1>!11+1='
    t = Transition('A', '1', 'A', '1', '>').to_dict()
    transition_list = []
    transition_dict = {}
    
    transition_dict['find_initial'] = []
    for state in STATES:
        t = Transition('find_initial', state, f'go_read_input_{state}', state, 'RIGHT')
        transition_list.append(t)
        transition_dict['find_initial'].append(t.to_dict())

    #go_read_input_{state}
    for state in STATES:
        current_state = f'go_read_input_{state}'
        transition_dict[current_state] = []
        for c in remove_char_from_list(TRANSITIONS_END, all_characters):
            print(c)
            t = Transition(current_state, c, current_state, c, 'RIGHT')
            transition_list.append(t)
            transition_dict[current_state].append(t.to_dict())
        t = Transition(current_state, TRANSITIONS_END, f'read_input_{state}', TRANSITIONS_END, 'RIGHT')
        transition_list.append(t)
        transition_dict[current_state].append(t.to_dict())


    #read_input_{state}
    for state in STATES:
        current_state = f'read_input_{state}'
        transition_dict[current_state] = []
        for char in ALPHABET:
            t = Transition(current_state, char, f'go_find_transitions_start_{state}_{char}', POINTER, 'LEFT')
            transition_list.append(t)
            transition_dict[current_state].append(t.to_dict())


    #go_find_transitions_start_{state}_{char}
    for state in STATES:
        for char in ALPHABET:
            current_state = f'go_find_transitions_start_{state}_{char}'
            transition_dict[current_state] = []
            for c in remove_char_from_list(TRANSITIONS_START, all_characters):
                t = Transition(current_state, c, current_state, c, 'LEFT')
                transition_list.append(t)
                transition_dict[current_state].append(t.to_dict())
            t = Transition(current_state, TRANSITIONS_START, f'go_next_transition_start_{state}_{char}', TRANSITIONS_START, 'RIGHT')
            transition_list.append(t)
            transition_dict[current_state].append(t.to_dict())

    #go_next_transition_start_{state}_{char}
    for state in STATES:
        for char in ALPHABET:
            current_state = f'go_next_transition_start_{state}_{char}'
            transition_dict[current_state] = []
            for read in remove_char_from_list(TRANSITIONS_DESCRIPTION_SEPARATOR, all_characters):
                t = Transition(current_state, read, current_state, read, 'RIGHT')
                transition_list.append(t)
                transition_dict[current_state].append(t.to_dict())
            t = Transition(current_state, TRANSITIONS_DESCRIPTION_SEPARATOR, f'read_transitions_start_{state}_{char}', TRANSITIONS_DESCRIPTION_SEPARATOR, 'RIGHT')
            transition_list.append(t)
            transition_dict[current_state].append(t.to_dict())


    #read_transitions_start_{state}_{char}
    for state in STATES:
        for char in ALPHABET:
            current_state = f'read_transitions_start_{state}_{char}'
            transition_dict[current_state] = []
            for read in remove_char_from_list(state, all_characters):
                t = Transition(current_state, read, f'go_next_transition_start_{state}_{char}', read, 'RIGHT')
                transition_list.append(t)
                transition_dict[current_state].append(t.to_dict())
            t = Transition(current_state, state, f'check_read_character_in_transition_{state}_{char}', state, 'RIGHT')
            transition_list.append(t)
            transition_dict[current_state].append(t.to_dict())


    #check_read_character_in_transition_{state}_{char}
    for state in STATES:
        for char in ALPHABET:
            current_state = f'check_read_character_in_transition_{state}_{char}'
            transition_dict[current_state] = []
            for read in remove_char_from_list(char, ALPHABET):
                t = Transition(current_state, read, f'go_next_transition_start_{state}_{char}', read, 'RIGHT')
                transition_list.append(t)
                transition_dict[current_state].append(t.to_dict())
            t = Transition(current_state, char, f'load_action_next_state', char, 'RIGHT')
            transition_list.append(t)
            transition_dict[current_state].append(t.to_dict())

    current_state = 'load_action_next_state'
    transition_dict[current_state] = []

    for state in STATES:
        t = Transition(current_state, state, f'load_action_write__{state}', state, 'RIGHT')
        transition_list.append(t)
        transition_dict[current_state].append(t.to_dict())

    print("........")
    for state in STATES:
        current_state = f'load_action_write__{state}'
        transition_dict[current_state] = []
        for char in INPUT_ALPHABET:
            t = Transition(current_state, char, f'load_direction__{state}_{char}', char, 'RIGHT')
            transition_list.append(t)
            transition_dict[current_state].append(t.to_dict())

    for state in STATES:
        for char in INPUT_ALPHABET:
            current_state = f'load_direction__{state}_{char}'
            transition_dict[current_state] = []
            t = Transition(current_state, '<', f'exec_{state}_{char}_LEFT', '<', 'RIGHT')
            transition_list.append(t)
            transition_dict[current_state].append(t.to_dict())
            t = Transition(current_state, '>', f'exec_{state}_{char}_RIGHT', '>', 'RIGHT')
            transition_list.append(t)
            transition_dict[current_state].append(t.to_dict())

    for state in STATES:
        for char in INPUT_ALPHABET:
            for direction in ["LEFT", "RIGHT"]:
                current_state = f'exec_{state}_{char}_{direction}'
                transition_dict[current_state] = []
                for read in remove_char_from_list(POINTER, ALPHABET):
                    t = Transition(current_state, read, current_state, read, 'RIGHT')
                    print(current_state, t.to_dict())
                    transition_list.append(t)
                    transition_dict[current_state].append(t.to_dict())
                if state == FINAL_STATE:
                    t = Transition(current_state, POINTER, FINAL_STATE, char, direction)
                    print(current_state, t.to_dict())
                else:
                    t = Transition(current_state, POINTER, f'read_input_{state}', char, direction)
                    print(current_state, t.to_dict())
                transition_list.append(t)
                transition_dict[current_state].append(t.to_dict())

    t = Transition(current_state, FINAL_STATE, FINAL_STATE, char, direction)
    print(current_state, t.to_dict())

                    
    import json


    output_json = {}

    output_json['name'] = 'universal'
    output_json['alphabet'] = ALPHABET
    output_json['blank'] = '.'
    output_json['states'] = ['find_initial', 'A', 'B', 'C', 'Z']
    output_json['initial'] = 'find_initial' 
    output_json['finals'] = ['Z']
    output_json['transitions'] = transition_dict

    with open("sample.json", "w") as outfile: 
        json.dump(output_json, outfile)

    print(output_json['transitions']['load_action_next_state'])

    #transitions_dict = {}
    #for transition in transition_list:
    #    print(transition.to_dict().values())
        #print(transition.to_dict())


if __name__ == '__main__':
    main()




