# Initialize the belief base as an empty list
belief_base = []

# Add a new formula to the belief base with a priority
def add_formula(formula, priority):
    belief_base.append((formula, priority))

# Remove a formula from the belief base
def remove_formula(formula):
    belief_base[:] = [f for f in belief_base if f[0] != formula]

# Check if a formula is in the belief base
def contains_formula(formula):
    return any(f[0] == formula for f in belief_base)

# Get the priority of a formula in the belief base
def get_priority(formula):
    return next((f[1] for f in belief_base if f[0] == formula), None)

# Update the priority of a formula in the belief base
def update_priority(formula, new_priority):
    for i, f in enumerate(belief_base):
        if f[0] == formula:
            belief_base[i] = (formula, new_priority)
            break

# Get the formulas in the belief base sorted by priority
def get_sorted_formulas():
    return [f[0] for f in sorted(belief_base, key=lambda x: x[1])]

def test():
    # Add beliefs to the belief base
    add_formula('P', 1)    # Priority 1
    add_formula('Q', 2)    # Priority 2
    add_formula('P & Q', 3)    # Priority 3
    add_formula('~P | R', 4)   # Priority 4

    # Get all beliefs in the belief base
    beliefs = get_sorted_formulas()
    print(beliefs)
    # Output: ['P', 'Q', 'P & Q', '~P | R']

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

if __name__ == "__main__":
    test()

