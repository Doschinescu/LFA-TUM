import random

class Grammar:
    def __init__(self):
        self.VN = {'S', 'D', 'E', 'J'}
        self.VT = {'a', 'b', 'c', 'd', 'e'}
        self.P = {
            'S': ['aD'],
            'D': ['dE', 'bJ', 'aE'],
            'J': ['cS'],
            'E': ['e', 'aE']
        }
    
    def generate_strings(self, count):
        unique_strings = set()
        valid_strings = []
        
        while len(unique_strings) < count:
            sb = []
            self.generate_string_helper('S', sb)
            generated_string = ''.join(sb)
            if generated_string not in unique_strings:
                unique_strings.add(generated_string)
                valid_strings.append(generated_string)
        
        return valid_strings
    
    def generate_string_helper(self, symbol, sb):
        productions = self.P.get(symbol)
        if productions:
            production = random.choice(productions)
            for c in production:
                if c in self.VN:
                    self.generate_string_helper(c, sb)
                else:
                    sb.append(c)


class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.final_states = set()
    
    def add_transition(self, from_state, symbol, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][symbol] = to_state
    
    def can_reach_string(self, input_string):
        current_state = self.initial_state
        found_last_a = False
        
        for symbol in input_string:
            print("Current State:", current_state, "Symbol:", symbol)
            if current_state not in self.transitions or symbol not in self.transitions[current_state]:
                print("No transition defined for symbol", symbol, "in state", current_state)
                return False
            
            current_state = self.transitions[current_state][symbol]
            if symbol == 'a':
                found_last_a = True
            
            print("New State:", current_state)
        
        if not found_last_a or current_state != 'f':
            return False
        
        return True

    def __str__(self):
        return f"States: {self.states}\nAlphabet: {self.alphabet}\nTransitions: {self.transitions}\nInitial State: {self.initial_state}\nFinal States: {self.final_states}"


if __name__ == "__main__":
    grammar = Grammar()
    finite_automaton = FiniteAutomaton()

    for symbol in grammar.P.keys():
        for production in grammar.P[symbol]:
            input_symbol = production[0]
            next_state = production[1] if len(production) > 1 else 'f'
            finite_automaton.add_transition(symbol, input_symbol, next_state)
            finite_automaton.alphabet.add(input_symbol)

    finite_automaton.states = grammar.VN
    finite_automaton.initial_state = 'S'
    finite_automaton.final_states = {'e'}

    print("Generated Strings:")
    for string in grammar.generate_strings(5):
        print(string)

    print("Finite Automaton:")
    print(finite_automaton)
    input_string = input("Enter input string: ")

    if finite_automaton.can_reach_string(input_string):
        print("Input string can be obtained via state transitions.")
    else:
        print("Input string cannot be obtained via state transitions.")
