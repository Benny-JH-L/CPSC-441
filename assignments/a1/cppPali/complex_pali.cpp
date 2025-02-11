
#include<iostream>
#include<unordered_map>
#include<vector>

using namespace std;

int complexPali(string input)
{
    unordered_map<char, int> countOfCharactersMap; // `char` is key, `int` is value (number of times the `char` occures in the `input`)
    int numSwaps = 0;

    // count the characters in the input
    for (char c : input)
        countOfCharactersMap[c]++;

    bool foundOdd = false;
    bool palindromePossible = true;
    char oddInstancedChar = ' ';
    // Go through letters and see if we have multiple letters with odd numbered occurances (a character has an odd number of instances).
    for (auto pair : countOfCharactersMap)
    {
        auto [chara, instances] = pair;

        if (instances % 2 == 1 && !foundOdd)    // check if number of instances of `chara` is odd and if an odd numbered occuring `chara` hasn't been found yet
        {
            foundOdd = true;                    // found first occurance of odd numbered `chara`
            oddInstancedChar = chara;           // set the odd instanced `chara`
        }
        // if found a `chara` that has odd occurances and there is already 
        // another `chara` found with odd numbered occurances, then this `input` cannot be made into a palindrome.
        else if (instances % 2 == 1 && foundOdd)
        {
            palindromePossible = false;
            break;
        }
    }
    if (!palindromePossible)
        return -1;          // return, can't turn `input` into a palindrome
    
    // find the index of all odd instanced character that are not in an optimal position
    vector<int> indiciesOfOddNumberedChars;
    for (size_t left = 0, right = input.length() - 1; left < right; left++, right--)
    {
        if (input[left] != input[right])
        {
            if (input[left] == oddInstancedChar)
                indiciesOfOddNumberedChars.push_back(left);
            else if (input[right] == oddInstancedChar)
                indiciesOfOddNumberedChars.push_back(right);
            else if (left + 1 == right - 1 && input[left+1] == oddInstancedChar)    // case where the middle contains a odd instanced character
                indiciesOfOddNumberedChars.push_back(left+1);
        }
        // This if-block works too.
        // if (input[left] == oddInstancedChar && input[left] != input[right])
        //     indiciesOfOddNumberedChars.push_back(left);
        // else if (input[right] == oddInstancedChar && input[left] != input[right])
        //     indiciesOfOddNumberedChars.push_back(right);
    }
  
    // If the input has a character with an odd number of instances
    if (foundOdd)
    {
        int middleIndex = input.length() / 2;
        char middleCharToSwap = input[middleIndex];
        bool foundOptimal = false;
        // Find the optimal index to swap one of the odd letters
        // such that the, odd instanced character is in the middle of the string.
        // And the swapped middle character is in a optimal position
        for (size_t left = 0, right = input.length() - 1; right > left && !foundOptimal; left++, right--)
        {
            // debug
            // cout << "left: "<<input[left]<<endl;
            // cout << "right: "<<input[right]<<endl;
            // cout << "middle char is: "<<middleCharToSwap<<endl;
            // we don't want to swap the middle with input[right] or input[left] if the left and right is the same letter
            if ((input[left] == middleCharToSwap || input[right] == middleCharToSwap) && input[left] != input[right])
            {
                for (int indexOfOdd : indiciesOfOddNumberedChars)
                {
                    // do swap
                    char tmp = input[indexOfOdd];
                    input[indexOfOdd] = input[middleIndex];
                    input[middleIndex] = tmp;
    
                    if (input[left] != input[right])    // did swap, and it was not the most optimal, undo swap and check next
                    {
                        // reverse swap
                        tmp = input[indexOfOdd];
                        input[indexOfOdd] = input[middleIndex];
                        input[middleIndex] = tmp;
                    }
                    else if (input[left] == input[right])   // was an optimal swap, break
                    {
                        numSwaps++;
                        foundOptimal = true;
                        break;
                    }
                }
            }         
        }

        // Case where we could not find the most optimal swap, swap arbitrarily the middle letter 
        // with an odd number of instances character that is not in an optimal position.
        // (Don't swap if middleIndex is already one of the odd instanced letters)
        if (!foundOptimal && input[middleIndex] != oddInstancedChar)
        {
            int arbitraryIndexOfOdd = indiciesOfOddNumberedChars[0];
            char oddLetterTmp = input[arbitraryIndexOfOdd];
            input[arbitraryIndexOfOdd] = middleCharToSwap;
            input[middleIndex] = oddLetterTmp;
            numSwaps++;
        }
    }
    
    // Compute possible palindrome
    // `left` is the index of the left pointer for the input
    // `right` is the index of the right pointer for the input 
    for (size_t left = 0, right = input.length() - 1; right > left ; left++, right--)
    {
        if (input[left] == input[right])    // letter's at input[left] is the same at input[right]
            continue;                       // keep checking
        
        // letters at index `left` and `right` are not equal,
        // find a letter at index `tmp` that is equal to the letter at index `left`, starting from index `right-1`
        for (size_t tmp = right - 1; tmp > left; tmp--)
        {
            if (input[tmp] == input[left])  // swap letters at input[tmp] and input[right], so input[left] == input[right]
            {
                char tmpChar = input[right];
                input[right] = input[tmp];  // set input[right] to input[tmp]
                input[tmp] = tmpChar;       // set input[tmp] to input[right]
                numSwaps++;                 // increment numSwaps by 1
                break;                      // exit loop
            }
        }
    }
    return numSwaps;
}

void testHelper(string input, int expectedNumSwaps)
{
    int s = complexPali(input);
    cout << input << " to pali takes: " << s << " swaps | expected swaps is: "<< expectedNumSwaps << " | same: " <<(expectedNumSwaps == s ? "True" : "False")<< endl;
}

int main()
{
    // string s = "iiikckaac";
    // cout << s.length()/2 << endl;

    testHelper("cbbici", 2);   // expected 2 swaps
    testHelper("ivicc", 2);
    testHelper("iiicccc", 2);
    testHelper("iiikckaac", 2);
    testHelper("iiikckaacc", -1);   // impossible
    testHelper("iciccci", 1);
    testHelper("icikkci", 1);
    testHelper("icikcki", 2); 
    testHelper("ergergerger", 2); 
    return 0;
}



