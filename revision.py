from utils import *
import copy


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
                    if solved is None:
                        solved = arg
                    else:
                        solved = Or(solved, arg)
    return solved


def resolve(bb):
    symbols = bb.get_symbols()

    for v, s in symbols.items():
        for (b1, p1) in bb.belief_base:
            if isTrue(b1, s):
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


def logical_entailment(bb, b, p):
    # First, KB ∧ ¬φ is converted into CNF
    kb_cnf = convert_bb_to_cnf(bb)
    kb_cnf.add_formula(negate_belief(b), p)

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


def revision(bb, b, p):
    # Check if contains already
    if contains_belief_already(bb, b):
        return (bb, bb.get_total_priority())

    # Check for vacuity
    constellations = []
    bb_combinations = get_combinations(bb)
    for combination in bb_combinations:
        bb = from_comb_to_to_bb(combination)

        if check_vacuity(bb, b):
            constellations.append((bb, bb.get_total_priority()))
        else:
            entails = logical_entailment(copy.deepcopy(bb), b, p)
            if entails:
                constellations.append((bb, bb.get_total_priority()))

    if constellations:
        max_priority = max(constellations, key=lambda x: x[1])
        max_priority[0].add_formula(b, p)
        return max_priority
    else:
        bb.remove_formula(b)
        return (bb, bb.get_total_priority())
