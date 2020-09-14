def parse_snake_case(x):
    """Parse a snake case string."""
    return " ".join(s.replace("#", "").strip().title() for s in x.split("_"))