from revision import *
from test_utils import *


def agm_success_postulate():
    #Test 1.1 - Checks when we add a formula that it is added to the belief base
    # Create belief base
    belief_base = create_test_bb()

    new_clause = "~p"
    new_clause_priority = 1
    bb, p = revision(belief_base, new_clause, new_clause_priority)

    is_added = False
    for (b, p) in bb.belief_base:
        if b == new_clause:
            is_added = True

    if is_added:
        print("Success add: Passed test")
    else:
        print("Success add: Failed test")


def agm_inclusion_postulate():
    # Test 1.2 - Checks if new belief base is added will result in a belief base that is a superset of the old belief base
    belief_base = create_test_bb()

    new_clause = "z"
    new_clause_priority = 1
    bb, p = revision(belief_base, new_clause, new_clause_priority)

    # Add new clause to B + phi
    belief_base.add_formula(new_clause, new_clause_priority)
    if len(bb.belief_base) <= len(belief_base.belief_base):
        print("Inclusion: Passed test")
    else:
        print("Inclusion: Failed test")


def agm_vacuity_postulate():
    # Test 1.3 - checks  if we negate the belief we want to add, and it is not present, we add the belief.
    belief_base = create_test_bb()

    new_clause = "z"
    new_clause_priority = 1
    bb, p = revision(belief_base, new_clause, new_clause_priority)

    belief_base.add_formula(new_clause, new_clause_priority)
    if belief_base.equals(bb):
        print("Vacuity: Passed test")
    else:
        print("Vacuity: Failed test")


def agm_consistency_postulate_alter():
    # Test 1.4 - Adding consistent belief results in adding belief
    belief_base = create_test_bb()

    new_clause = "~a"
    new_clause_priority = 1
    bb, p = revision(belief_base, new_clause, new_clause_priority)

    if ("a", 4) not in bb.belief_base:
        print("Consistency: Passed test")
    else:
        print("Consistency: Failed test")


def agm_consistency_postulate_dont_alter():
    # Test 1.5 - Adding false belief results in not adding belief
    belief_base = create_test_bb()

    new_clause = "a"
    new_clause_priority = 1
    bb, p = revision(belief_base, new_clause, new_clause_priority)

    altered = False
    for (belief, p) in belief_base.belief_base:
        if (belief, p) not in bb.belief_base:
            altered = True

    if not altered:
        print("Consistency: Passed test")
    else:
        print("Consistency: Failed test")


def agm_extensionality_postulate():
    # Test 1.6 - Adding belief that is already in belief base results in not changing belief base
    belief_base = create_test_bb()

    new_clause = "a"
    new_clause_priority = 1
    bb, p = revision(belief_base, new_clause, new_clause_priority)

    altered = False
    for (belief, p) in belief_base.belief_base:
        if (belief, p) not in bb.belief_base:
            altered = True

    if not altered:
        print("Extentionality: Passed test")
    else:
        print("Extentionality: Failed test")


if __name__ == "__main__":
    # Success postulate
    agm_success_postulate()

    # Inclusion postulate
    agm_inclusion_postulate()

    # Vacuity postulate
    agm_vacuity_postulate()

    # Consistency
    agm_consistency_postulate_alter()
    agm_consistency_postulate_dont_alter()

    # Extensionality
    agm_extensionality_postulate()
