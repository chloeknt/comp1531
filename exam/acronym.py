def acronym_make(inputs):
    outputs = []
    for s in inputs:
        acro = ""
        phrase = s.split()
        print(phrase)
        for c in phrase:
            if not_vowel(c[0]):
                acro += c[0].upper()
        if len(acro) > 10:
            outputs.append("N/A")
        else:
            outputs.append(acro)
    return outputs

def not_vowel(c):
    vowels = "aeiouAEIOU"
    if c in vowels:
        return False
    return True
