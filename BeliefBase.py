import sympy
from sympy import *
from sympy.abc import *


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
        self.belief_base.append((formula, priority))

    # Remove a formula from the belief base
    def remove_formula(self, formula):
        self.belief_base[:] = [f for f in self.belief_base if f[0] != formula]

    # Check if a formula is in the belief base
    def contains_formula(self, formula):
        return any(f[0] == formula for f in self.belief_base)

    # Get the priority of a formula in the belief base
    def get_priority(self, formula):
        return next((f[1] for f in self.belief_base if f[0] == formula), None)

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
