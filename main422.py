from sympy import *
import sympy
from sympy.logic.boolalg import *
from sympy.abc import *
import itertools
import copy

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

    def equals(self, new_bb):
        for (b, p) in self.belief_base:
            if not new_bb.contains_formula(b):
                return False
        return True

    def get_total_priority(self):
        total = 0
        for (_, p) in self.belief_base:
            total += p
        return total

def convert_b_to_cnf(belief, symbols):
    # Replace variables in the expression string with corresponding symbols
    for v, s in symbols.items():
        belief = belief.replace(v, str(s))

    # Parse the expression string into a Sympy expression
    return sympy.to_cnf(belief)

def convert_bb_to_cnf(bb):
    new_belief_base = BeliefBase([])
    symbols = bb.get_symbols()

    for (belief, priority) in bb.belief_base:
        new_belief_base.add_formula(convert_b_to_cnf(belief, symbols), priority)

    bb_no_and = remove_and(new_belief_base)

    return bb_no_and

def remove_and(bb):
    new_bb = BeliefBase([])
    for (b, p) in bb.belief_base:
        if b.func == And:
            new_bb.add_formula(b.args[0], p)
            new_bb.add_formula(b.args[1], p)
        else:
            new_bb.add_formula(b, p)
    return new_bb

def logical_entailment(bb, belief):
    # First, KB ∧ ¬φ is converted into CNF
    bb.add_formula("~"+belief, 5)
    kb_cnf = convert_bb_to_cnf(bb)

    res_bb = None
    searching = true
    while searching:
        tmp_bb = resolve(kb_cnf)

        if len(tmp_bb.belief_base) == 0:
            return true

        if res_bb is not None and tmp_bb.equals(res_bb):
            searching = false
            if len(res_bb.belief_base) > 0:
                return false
            else:
                return true
        else:
            res_bb = copy.deepcopy(tmp_bb)

    return false



def isNot(b2, symbol):
    if b2.func == Not and len(b2.args) == 1 and symbol in b2.args:
        return true
    else:
        for arg in b2.args:
            if arg.func == Not and len(arg.args) == 1 and symbol in arg.binary_symbols:
                return true
        return false

def isTrue(b1, symbol):
    if b1.func != Not and len(b1.args) == 0 and symbol == b1:
        return true
    elif b1.func == Not and len(b1.args) == 1 and symbol in b1.binary_symbols:
        return false
    else:
        for arg in b1.args:
            if len(arg.args) == 0 and symbol in arg.binary_symbols and arg.func != Not:
                return true
        return false

def solve_literals(b1, b2):
    combined = Or(b1, b2)
    combined_symbols = combined.binary_symbols
    solved = None

    for s in combined_symbols:
        have_compli_lit = False
        for arg in combined.args:
            if isTrue(arg, s):
                for arg2 in combined.args:
                    if s in arg2.binary_symbols and isNot(arg2, s):
                        have_compli_lit = True

        if not have_compli_lit:
            for arg in combined.args:
                if isTrue(arg, s) or isNot(arg, s):
                    if solved == None:
                        solved = arg
                    else:
                        solved = Or(solved, arg)
    return solved

def resolve(bb):
    symbols = bb.get_symbols()

    count = 0
    for v, s in symbols.items():
        for (b1, p1) in bb.belief_base:
            if isTrue(b1,s):
                for (b2, p2) in bb.belief_base:
                    if b1 != b2:
                        if s in b2.binary_symbols and isNot(b2, s):
                            bb.remove_formula(b1)
                            bb.remove_formula(b2)
                            solved = solve_literals(b1, b2)
                            if solved is not None:
                                bb.add_formula(solve_literals(b1, b2), 666)
                                return bb
                            else:
                                return BeliefBase([])
    return bb


def get_combinations(bb):
    res = []
    for n in range(1, len(bb.belief_base)+1):
        res += itertools.combinations(bb.belief_base, n)
    return res


def from_comb_to_to_bb(combs):
    bb = BeliefBase([])
    for (b, p) in combs:
        bb.add_formula(b, p)
    return bb


def contraction(bb, b):
    bb_combinations = get_combinations(bb)

    constellations = []
    for combination in bb_combinations:
        bb = from_comb_to_to_bb(combination)

        entails = logical_entailment(copy.deepcopy(bb), b)
        if entails:
            constellations.append((bb, bb.get_total_priority()))

    if constellations:
        max_priority = max(constellations, key=lambda x: x[1])
        return max_priority
    else:
        print("The list of constellations is empty.")

    return constellations



def test():
    belief_base = BeliefBase([])

    # Add beliefs to the belief base
    belief_base.add_formula("~r | p | s ", 1)  # Priority 1
    belief_base.add_formula("~p | r | r", 2)  # Priority 2
    belief_base.add_formula("~s | r", 3)  # Priority 3
    belief_base.add_formula("~r", 4)  # Priority 3

    new_clause = "~p"
    b, p = contraction(belief_base,new_clause)
    print("Belief base entails new belief")
    print(b)
    print("Max priority achievable:")
    print(p)
    # Extend
    b.add_formula(new_clause,5)
    print("Belief base after revision")
    print(b)

    # Solve literal test
    #belief_base.add_formula("~p",5)
   # bb_cnf = convert_bb_to_cnf(belief_base)
    #solve_literals(bb_cnf.belief_base[0][0], bb_cnf.belief_base[1][0])

if __name__ == "__main__":
    test()
