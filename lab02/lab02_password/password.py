def check_password(password):
    '''
    Takes in a password, and returns a string based on the strength of that password.

    The returned value should be:
    * "Strong password", if at least 12 characters, contains at least one number, at least one uppercase letter, at least one lowercase letter.
    * "Moderate password", if at least 8 characters, contains at least one number.
    * "Poor password", for anything else
    * "Horrible password", if the user enters "password", "iloveyou", or "123456"
    '''

    if password == "password" or password == "iloveyou" or password == "123456":
        return "Horrible password"
        
    if len(password) >= 12 and has_number(password) and has_lower_and_upper(password):
        return "Strong password"    
    elif len(password) >= 8 and has_number(password):
        return "Moderate password"
    else:
        return "Poor password"
        
def has_number(password):
    for char in password:
        if char.isdigit():
            return True
    return False

def has_lower_and_upper(password):
    if password.islower() or password.isupper():
        return False
    return True

if __name__ == '__main__':
    print(check_password("ihearttrimesters"))
    # What does this do?
