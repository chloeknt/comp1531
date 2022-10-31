def magic(square):
    if not all([len(i) == len(square) for i in square]):
        return "Invalid data: missing or repeated number"

    n = len(square)
    
    temp = []
    for i in range(n):
        for j in range(n):
            if square[i][j] not in temp:
                temp.append(square[i][j])
            else:
                return (f"Invalid data: missing or repeated number")
    
    for i in range(n):
        sum_row = 0
        sum_col = 0
        for j in range(n):
            sum_row += square[i][j]
            sum_col += square[j][i]
        if sum_row != sum_col: 
            return "Not a magic square"
    
    return "Magic square"
