def frequency_get(multilinestr):
    mulLine = ""
    str_list = multilinestr.split()
    str2 = []
    for i in str_list:
        if i not in str2:
            str2.append(i)
    for i in range(0, len(str2)):
        mulLine += str2[i] + ': ' + str(str_list.count(str2[i]))
    
    return mulLine
