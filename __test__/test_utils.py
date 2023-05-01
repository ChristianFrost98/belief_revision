from BeliefBase import *

def create_test_bb():
    belief_base = BeliefBase([])

    # New knowledge is most important
    belief_base.add_formula("~a | b | c ", 1)
    belief_base.add_formula("~b | a | e ", 2)
    belief_base.add_formula("~c | a", 3)
    belief_base.add_formula("d", 4)

    return belief_base