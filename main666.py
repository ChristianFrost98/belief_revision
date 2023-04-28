import sympy
from sympy import Symbol


class Belief:
    def __init__(self, belief, priority):
        self.belief = belief
        self.priority = priority

    def __repr__(self):
        return "(" + self.belief + ")"


def init_belief_base():
    b1 = Belief("P | D -> C", 1)
    b2 = Belief("P | D & C", 2)
    b3 = Belief("P | ~D -> C", 3)

    bb = [b1, b2, b3]
    sympys = to_sympy(bb)

    for (belief,priority) in sympys:
        print(f"Belief: {belief}, w. priority: {priority}")


def to_sympy(bb):
    exprs = []
    for b in bb:
        exprs.append((parse_sympy(b.belief), b.priority))
    return exprs


def parse_sympy(expr_str):
    # Define symbols for all variables in the expression
    variables = set(filter(str.isalpha, expr_str))
    symbols = {v: Symbol(v) for v in variables}

    # Replace variables in the expression string with corresponding symbols
    for v, s in symbols.items():
        expr_str = expr_str.replace(v, str(s))

    # Replace implication and biconditional operators with Sympy equivalents
    expr_str = expr_str.replace("->", ">>")
    expr_str = expr_str.replace("<->", "~xor")

    # Parse the expression string into a Sympy expression
    expr = sympy.sympify(expr_str)

    return expr



if __name__ == "__main__":
    init_belief_base()