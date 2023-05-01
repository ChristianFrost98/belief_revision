from revision import *
from test_utils import *


def agm_success_postulate():
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
    # Test 1.1 - Adding false belief results in not adding belief
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
    # Test 1.1 - Adding false belief results in not adding belief
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
    # Test 1.1 - Adding false belief results in not adding belief
    belief_base = create_test_bb()

    new_clause = "~a"
    new_clause_priority = 1
    bb, p = revision(belief_base, new_clause, new_clause_priority)

    if ("a", 4) not in bb.belief_base:
        print("Consistency: Passed test")
    else:
        print("Consistency: Failed test")


def agm_consistency_postulate_dont_alter():
    # Test 1.1 - Adding false belief results in not adding belief
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
    # Test 1.1 - Adding false belief results in not adding belief
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
