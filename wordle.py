import sys, re
# word_file = '/usr/share/dict/words'
# word_file = './internet_dict/en_US.dic'
word_file = './five_wordles'


'''
input guesses:
    s-h+a+r-d
    where:
    a letter preceded by a + means it was yellow
    a letter preceded by a - means it was black
    a letter without a preceding +/- was green
'''

def init_possible_words():
    words = open(word_file, 'r')
    wordles = []
    for word in words.readlines():
        wordles.append(word.strip())
        # print(wordles[-1])
    return wordles

# parse input
excludes = []
includes = []
yellows = [[], [], [], [], []]
word = '.....'
for i in range(1, len(sys.argv)):
    guess = sys.argv[i]
    j = 0 # index into guess
    l = 0 # index into word
    while j < len(guess):
        char = guess[j]
        if char == '+':
            if not guess[j+1] in includes:
                includes.append(guess[j+1])
            if not guess[j+1] in yellows[l]:
                yellows[l].append(guess[j+1])
            j += 1
        elif char == '-':
            if not guess[j+1] in excludes:
                excludes.append(guess[j+1])
            j += 1
        else:
            if not char in includes:
                includes.append(char)
            word = word[:l] + char + word[l+1:]
        j += 1
        l += 1

print('includes:', includes)
print('excludes:', excludes)
print('yellows:', yellows)
print('word base:', word)

possibilities = init_possible_words()
base_re = [char for char in word]
for i in range(len(yellows)):
    pos = yellows[i]
    if len(pos) == 0 or word[i] != '.':
        continue
    exclude = '[^\n'
    for letter in pos:
        exclude += letter
    exclude += ']'
    base_re[i] = exclude

base_re = ''.join(base_re)
# print(base_re)

# filter for matching the word base
possibilities = re.findall(base_re, '\n'.join(possibilities))
# print(possibilities)
# print(len(possibilities))

# filter for excluding letters
reg = '[^'+''.join(excludes) + ']{5}\n'
possibilities = re.findall(reg, '\n'.join(possibilities) + '\n')
# print(possibilities)
# print(len(possibilities))


# filter for including letters
final_possibilities = []
for p_word in possibilities:
    not_in = False
    for ch in includes:
        if ch not in p_word:
            not_in = True
            break
    if not_in:
        continue
    final_possibilities.append(p_word.strip())

# print(len(final_possibilities))
print('possible matches: ', final_possibilities)
print('number of matches:', len(final_possibilities))

