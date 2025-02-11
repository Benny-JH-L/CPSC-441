

def complexPali(input_str):
    countOfCharactersMap = {}
    numSwaps = 0
    
    # count the characters (letters) in the input
    for char in input_str:
        if char in countOfCharactersMap:
            countOfCharactersMap[char] += 1
        else:
            countOfCharactersMap[char] = 1

    #debug
    # for key, value in countOfCharactersMap.items():
    #     print(key, "->", value)
    
    foundOdd = False
    palindromePossible = True
    oddInstancedChar = ' '
    
    # Go through letters and see if we have multiple letters with odd numbered occurances (a character has an odd number of instances).
    for chara, instances in countOfCharactersMap.items():
        
        if (instances % 2 == 1 and not foundOdd):
            foundOdd = True
            oddInstancedChar = chara
        # if found a `chara` that has odd occurances and there is already 
        # another `chara` found with odd numbered occurances, then this `input` cannot be made into a palindrome.
        elif (instances % 2 == 1 and foundOdd):
            palindromePossible = False
            break
    
    if (not palindromePossible):
        return "False|-1"       # return, can't turn `input` into a palindrome
            
    # find the index of all odd instanced character that are not in an optimal position
    indiciesOfOddNumberedChars = []
    left = 0                        # "points" to the left of the string and will move inwards (moves right)
    right = len(input_str) - 1      # "points" to the right of the string and will move inwards (moves left)
    while(left < right):
        
        if (input_str[left] != input_str[right]):
            if (input_str[left] == oddInstancedChar):
                indiciesOfOddNumberedChars.append(left)
            elif (input_str[right] == oddInstancedChar):
                indiciesOfOddNumberedChars.append(right)
            elif (left + 1 == right - 1 and input_str[left+1] == oddInstancedChar):    # case where the middle contains a odd instanced character
                indiciesOfOddNumberedChars.append(left+1)
        
        left += 1
        right -= 1
        
    # If the input has a character with an odd number of instances
    if (foundOdd):
        middleIndex = int(len(input_str) / 2)
        middleCharToSwap = input_str[middleIndex]
        foundOptimal = False
        # Find the optimal index to swap one of the odd letters
        # such that the, odd instanced character is in the middle of the string.
        # And the swapped middle character is in a optimal position
        left = 0                        # "points" to the left of the string and will move inwards (moves right)
        right = len(input_str) - 1      # "points" to the right of the string and will move inwards (moves left)
        while (right > left and not foundOptimal):
            
            if ((input_str[left] == middleCharToSwap or input_str[right] == middleCharToSwap) and input_str[left] != input_str[right]):
                for indexOfOdd in indiciesOfOddNumberedChars:
                    # Do Swap
                    input_str = swapAtIndex(input_str, indexOfOdd, middleIndex)
                    
                    if (input_str[left] != input_str[right]):    # did swap, and it was not the most optimal, undo swap and check next
                        input_str = swapAtIndex(input_str, indexOfOdd, middleIndex)
                        
                    elif (input_str[left] == input_str[right]):  # was an optimal swap, break
                        numSwaps += 1
                        foundOptimal = True
                        break
            left += 1
            right -= 1
        
        # Case where we could not find the most optimal swap, swap arbitrarily the middle letter 
        # with an odd number of instances character that is not in an optimal position.
        # (Don't swap if middleIndex is already one of the odd instanced letters)
        if (not foundOptimal and input_str[middleIndex] != oddInstancedChar):
            input_str = swapAtIndex(input_str, indiciesOfOddNumberedChars[0], middleIndex)
            numSwaps += 1

    # Compute possible palindrome
    # `left` is the index of the left pointer for the input
    # `right` is the index of the right pointer for the input 
    left = 0
    right = len(input_str) - 1
    while (right > left):
        if (input_str[left] == input_str[right]):   # letter's at input[left] is the same at input[right]
            left += 1
            right -= 1
            continue                                # keep checking
        
        # letters at index `left` and `right` are not equal,
        # find a letter at index `tmp` that is equal to the letter at index `left`, starting from index `right-1`
        tmp = right - 1
        while (tmp > left):
            if (input_str[tmp] == input_str[left]):  # swap letters at input[tmp] and input[right], so input[left] == input[right]
                input_str = swapAtIndex(input_str, right, tmp)  # swap the characters at indicies `right` and `tmp`, then update `input`
                numSwaps += 1                                   # increment numSwaps by 1
                break                                           # exit loop
            tmp -= 1
        
        left += 1
        right -= 1
    
    return f"True|{numSwaps}"

def swapAtIndex(input_str, index1, index2):
    input_str_list = list(input_str)
    input_str_list[index1], input_str_list[index2] = input_str_list[index2], input_str_list[index1]
    return ''.join(input_str_list)

def testHelper(input_str, expectedNumSwaps):
    canMake, swaps = complexPali(input_str).split('|')
    print(input_str, "to pali takes:", swaps, "swaps | expected is", expectedNumSwaps, "| same:", (int(swaps) == expectedNumSwaps))



testHelper("cbbici", 2)   # expected 2 swaps
testHelper("ivicc", 2)
testHelper("iiicccc", 2)
testHelper("iiikckaac", 2)
testHelper("iiikckaacc", -1)   # impossible
testHelper("iciccci", 1)
testHelper("icikkci", 1)
testHelper("icikcki", 2)
testHelper("ergergerger", 2)

