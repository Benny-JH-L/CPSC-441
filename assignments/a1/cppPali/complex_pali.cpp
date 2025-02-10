
#include<iostream>
#include<unordered_map>
#include<vector>

using namespace std;

int complexPali(string input)
{
    unordered_map<char, int> countOfCharactersMap; // `char` is key, `int` is value
    int numSwaps = 0;

    // count the charactes in the input
    for (char c : input)
        countOfCharactersMap[c]++;
    
    // If the input is odd length, determine if there is only 1 char that is odd numbered
    if (input.length() % 2 == 1)
    {
        bool foundOdd = false;
        bool palindromePossible = true;
        char oddInstancedChar = ' ';
        // Go through letters and see if we have multiple letters with odd numbered occurances
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
        
        // find the index of all odd instanced character
        vector<int> indiciesOfOddNumberedChars;
        for (size_t i = 0; i < input.length(); i++)
        {
            if (input[i] == oddInstancedChar)
                indiciesOfOddNumberedChars.push_back(i);
        }

        int middleIndex = input[input.length() / 2];
        char middleCharToSwap = input[middleIndex];
        bool foundOptimal = false;
        // Find the optimal index to swap one of the odd letters
        // such that the, odd instanced character is in the middle of the string.
        // And the swapped middle character is in a optimal position
        for (size_t left = 0, right = input.length() - 1; right > left && !foundOptimal; left++, right--)
        {
            if (input[left] == middleCharToSwap || input[right] == middleCharToSwap)
            {
                for (int indexOfOdd : indiciesOfOddNumberedChars)
                {
                    // do swap
                    char tmp = input[indexOfOdd];
                    input[indexOfOdd] = input[middleIndex];
                    input[middleIndex] = tmp;
    
                    if (input[left] != input[right])    // did swap, and it was not the most optimal, reverse swap and check next
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

            /*
            // if (input[left] == input[middleCharToSwap])
            // {
            // }
            // else if (input[right] == input[middleCharToSwap])
            // {    
            //     for (int indexOfOdd : indiciesOfOddNumberedChars)
            //     {
            //         // do swap
            //         char tmp = input[indexOfOdd];
            //         input[indexOfOdd] = input[middleCharToSwap];
            //         input[middleCharToSwap] = tmp;

            //         if (input[left] != input[right])    // did swap, and it was not the most optimal, reverse swap and check next
            //         {
            //             // reverse swap
            //             tmp = input[indexOfOdd];
            //             input[indexOfOdd] = input[middleCharToSwap];
            //             input[middleCharToSwap] = tmp;
            //         }
            //         else if (input[left] == input[right])   // was an optimal swap, break
            //         {
            //             foundOptimal = true;
            //             break;
            //         }
            //     }
            // }
            */
            
        }

        // Case where we could not find the most optimal swap, swap arbitrarily with middle letter 
        // and an odd instanced character (numbered letter).
        if (!foundOptimal)
        {
            char oddLetterTmp = input[indiciesOfOddNumberedChars[0]];
            input[indiciesOfOddNumberedChars[0]] = middleCharToSwap;
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
    return 0;
}



