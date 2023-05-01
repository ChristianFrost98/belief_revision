import sympy
from sympy import *
from BeliefBase import *
import copy
import itertools


def negate_belief(b):
    variables = []
    bvars = set(filter(str.isalpha, str(b)))
    for bvar in bvars:
        if not bvar in variables:
            variables.append(bvar)

    return Not(convert_b_to_cnf(b, {v: Symbol(v) for v in variables}))


def convert_b_to_cnf_single(b):
    variables = []
    bvars = set(filter(str.isalpha, str(b)))
    for bvar in bvars:
        if not bvar in variables:
            variables.append(bvar)

    return convert_b_to_cnf(b, {v: Symbol(v) for v in variables})


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


def contains_belief_already(bb, b):
    kb_cnf = convert_bb_to_cnf(copy.deepcopy(bb))
    b_cnf = convert_b_to_cnf_single(b)
    for (belief, priority) in kb_cnf.belief_base:
        if belief == b_cnf:
            return True
    return False


def check_vacuity(bb, b):
    kb_cnf = convert_bb_to_cnf(copy.deepcopy(bb))
    belief_negated = negate_belief(b)
    contains = False
    for (belief, priority) in kb_cnf.belief_base:
        if belief == belief_negated:
            contains = True

    return not contains


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


def get_combinations(bb):
    res = []
    for n in range(1, len(bb.belief_base) + 1):
        res += itertools.combinations(bb.belief_base, n)
    return res


def from_comb_to_to_bb(combs):
    bb = BeliefBase([])
    for (b, p) in combs:
        bb.add_formula(b, p)
    return bb
