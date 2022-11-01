from functools import reduce

def drykiss(my_list):
    # Use min function to find minimum value in list
    my_min = min(my_list)

    # Use list slicing to find product of first four and last four elements
    result = reduce((lambda x, y: x * y), my_list[:4])
    product = reduce((lambda x, y: x * y), my_list[-4:])

    # Return the results
    result = (my_min, result, product)
    return result

if __name__ == '__main__':
    # Get user input all in one line
    input_string = input("Enter five numbers: ")
    nums = input_string.split()
    my_list = [int(nums[0]), int(nums[1]), int(nums[2]), int(nums[3]), int(nums[4])]
    result = drykiss(my_list)

    print("Minimum: " + str(result[0]))
    print("Product of first 4 numbers: ")
    print(f"  {result[1]}")
    print("Product of last 4 numbers")
    print(f"  {result[2]}")
