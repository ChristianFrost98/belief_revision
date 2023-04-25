import sympy
from sympy import *
from sympy.logic.boolalg import *
from sympy.abc import *
from sympy.parsing.sympy_parser import parse_expr

# Initialize the belief base as an empty list
belief_base = []
highest_priority = 0


class BeliefBase:

    def __init__(self, belief_base):
        self.belief_base = belief_base

    # Add a new formula to the belief base with a priority
    def add_formula(self, formula, priority):
        global highest_priority
        self.belief_base.append((formula, priority))
        if priority > highest_priority:
            highest_priority = priority

    # Remove a formula from the belief base
    def remove_formula(self, formula):
        self.belief_base[:] = [f for f in self.belief_base if f[0] != formula]

    # Check if a formula is in the belief base
    def contains_formula(self, formula):
        return any(f[0] == formula for f in self.belief_base)

    # Get the priority of a formula in the belief base
    def get_priority(self, formula):
        return next((f[1] for f in self.belief_base if f[0] == formula), None)

    # Update the priority of a formula in the belief base
    def update_priority(self, formula, new_priority):
        global highest_priority
        for i, f in enumerate(self.belief_base):
            if f[0] == formula:
                self.belief_base[i] = (formula, new_priority)
                if new_priority > highest_priority:
                    highest_priority = new_priority
                break

    # Get the formulas in the belief base sorted by priority
    def get_sorted_formulas(self):
        return [f[0] for f in sorted(self.belief_base, key=lambda x: x[1])]


def convert_to_cnf(bb):
    new_belief_base = BeliefBase([])

    for (belief, priority) in bb.belief_base:
        # Define symbols for all variables in the expression
        variables = set(filter(str.isalpha, belief))
        symbols = {v: Symbol(v) for v in variables}

        # Replace variables in the expression string with corresponding symbols
        for v, s in symbols.items():
            belief = belief.replace(v, str(s))

        # Parse the expression string into a Sympy expression
        new_belief_base.add_formula(sympy.sympify(belief), priority)

    return new_belief_base

"""
def contraction(belief_base, formula):
    # If the new formula is already in the belief base, return the belief base
    if contains_formula(formula):
        return belief_base

    cnf_string = convert_to_CNF(new_belief_base)

    # Add the new formula to the belief base
    add_formula(formula, highest_priority + 1)
"""

def test():
    belief_base = BeliefBase([])

    # Add beliefs to the belief base
    belief_base.add_formula("P", 1)  # Priority 1
    belief_base.add_formula("Q", 2)  # Priority 2
    belief_base.add_formula("P | D & C", 3)  # Priority 3
    belief_base.add_formula("~P & R", 4)  # Priority 4

    # Get all beliefs in the belief base
    beliefs = belief_base.get_sorted_formulas()
    print(beliefs)
    # Output: ['P', 'Q', 'P & Q', '~P | R']
    """
    # Get the priority of a specific belief
    priority = get_priority('P & Q')
    print(priority)
    # Output: 3

    # Check if a belief is in the belief base
    print(contains_formula('P & Q'))
    # Output: True

    # Update the priority of a belief
    update_priority('P & Q', 1)
    print(get_sorted_formulas())
    # Output: ['P & Q', 'P', 'Q', '~P | R']

    # Remove a belief from the belief base
    remove_formula('P & Q')
    print(get_sorted_formulas())
    # Output: ['P', 'Q', '~P | R']
    
    print(belief_base)
    """
    # print(convert_to_cnf(belief_base))
    # print(is_cnf(q | p | r))
    # print(to_cnf(~(A | B) | D))
    # print(parse_expr('p | q | r'))

    print(convert_to_cnf(belief_base))


if __name__ == "__main__":
    test()
