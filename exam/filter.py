import string 

def filter_string(inp):

    # raise ValueError if any numbers
    for char in inp:
        if char.isdigit():
            raise ValueError("String should not have any numbers")


    punct = """.,""'';?!"""
    for c in inp:
        if c in punct:
            inp = inp.replace(c, "")
    inp = inp.capitalize()

    return inp
