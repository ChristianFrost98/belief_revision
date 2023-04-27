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

    def __repr__(self):
        res = ""
        for (b, p) in self.belief_base:
            res += repr(b) + "\n"
        return res

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

    def get_symbols(self):
        variables = []
        for (belief, _) in self.belief_base:
            bvars = set(filter(str.isalpha, str(belief)))
            for bvar in bvars:
                if not bvar in variables:
                    variables.append(bvar)
        return {v: Symbol(v) for v in variables}

def convert_bb_to_cnf(bb):
    # TODO - remove demorgan ands
    new_belief_base = BeliefBase([])
    symbols = bb.get_symbols()

    for (belief, priority) in bb.belief_base:
        # Replace variables in the expression string with corresponding symbols
        for v, s in symbols.items():
            belief = belief.replace(v, str(s))

        # Parse the expression string into a Sympy expression
        new_belief_base.add_formula(sympy.to_cnf(belief), priority)

    return new_belief_base

def logical_entailment(bb, belief):
    # First, KB ∧ ¬φ is converted into CNF
    bb.add_formula(belief, 5)
    kb_cnf = convert_bb_to_cnf(bb)


    # Then, the resolution rule is applied to the resulting clauses


    searching = true
    while searching:
        searching = false
        print(f"Number of pairs: {find_pairs(kb_cnf)}")

    return false


def isNot(b2, symbol):
    if b2.func == Not and len(b2.args) == 1 and symbol in b2.args:
        return true
    elif len(b2.args) != 0:
        for arg in b2.args:
            if arg.func == Not and symbol in arg.binary_symbols:
                return true
    else:
        return b2.func == Not and symbol in b2.binary_symbols

def solve_literals(b1, b2, symbol):
    combined = Or(b1, b2)
    solved = Symbol("")
    for arg in combined.args:
        if arg != symbol and arg != Not(symbol):
            if len(solved.args) > 0:
                solved = Or(solved, arg)
            else:
                solved = arg

    return solved

def find_pairs(bb):
    symbols = bb.get_symbols()

    count = 0
    for v, s in symbols.items():
        for (b1, p1) in bb.belief_base:
            if s in b1.binary_symbols:
                for (b2, p2) in bb.belief_base:
                    if b1 != b2:
                        if s in b2.binary_symbols and isNot(b2, s):
                            res = solve_literals(b1, b2, s)
                            count += 1
    return count


def test():
    belief_base = BeliefBase([])

    # Add beliefs to the belief base
    belief_base.add_formula("A", 1)  # Priority 1
    belief_base.add_formula("B | ~A", 2)  # Priority 2
    belief_base.add_formula("C", 3)  # Priority 3
    belief_base.add_formula("D", 4)  # Priority 4

    print(logical_entailment(belief_base, "~C"))

if __name__ == "__main__":
    test()
