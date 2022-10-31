def reverse_words(string_list):
    '''
    Given a list of strings, return a new list where the order of the words is
    reversed
    '''
    for i in range(len(string_list)):
        sentence = string_list[i]
        words = sentence.split()
        string_list[i] = ' '.join(reversed(words))
        
    return string_list

if __name__ == "__main__":
    print(reverse_words(["Hello World", "I am here"]))
    # it should print ['World Hello', 'here am I']
