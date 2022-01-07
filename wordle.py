# wordle.py v0.0.1
# Wordle Solver by Kelsey Glenn

import json
from collections import defaultdict

with open('dict.json') as w:
  words = json.load(w)['words']

possible_words = words
word_count = len(words)
letter_count = 5 * word_count


#letter_frequency
def calc_letter_freq(possible_words):
  letter_freq = defaultdict(int)
  for word in possible_words:
    for char in word:
      letter_freq[char] += 1
  return letter_freq


# rank words by sum frequency
def score_words(possible_words):
  freq = calc_letter_freq(possible_words)
  scores = defaultdict(int)
  for word in possible_words:
    used_chars = []
    for char in word:
      if char not in used_chars:
        scores[word] += freq[char]
        used_chars.append(char)
      else:
        pass
  return scores


# return a dictionary of miss chars and indexes of soft and hard hits
def word_constraints_from_feedback(guess, feedback):
  word_constraints = {
    'misses': [],
    'soft_hits': defaultdict(list),
    'hard_hits': defaultdict(list)
  }

  for i in range(len(guess)):
    if feedback[i] == 'm':
      if guess[i] not in word_constraints['misses']:
        word_constraints['misses'].append(guess[i])
    # store index of soft hits to avoid placement
    elif feedback[i] == 's':
      word_constraints['soft_hits'][guess[i]].append(i)
    # store index of hard hits to ensure placement
    else:
      word_constraints['hard_hits'][guess[i]].append(i)
  
  return word_constraints


# check word against constraints and save possible ones
def update_possible_words(possible_words, guess, feedback):
  constraints = word_constraints_from_feedback(guess, feedback)
  new_words = []
  for word in possible_words:
    possible = True
    
    # elim anything missing the hard hits
    for char in constraints['hard_hits'].keys():
      for i in constraints['hard_hits'][char]:
        if word[i] != guess[i]:
          possible = False
        if possible == False:
          break

    if possible == False:
      pass

    # if it doesnt miss a hard hit, test e/ character
    else:
      for i in range(len(word)):
        if word[i] in constraints['misses']:
          possible = False
          break
        elif word[i] in constraints['soft_hits'].keys():
          # if it guesses a soft hit in the same position, skip it
          if i in constraints['soft_hits'][word[i]]:
            possible = False
            break
          else:
            pass
        else: 
          pass
    if possible == True:
      new_words.append(word)

  return new_words


n_guesses = 0
current_words = possible_words
while n_guesses < 6:
  scores = score_words(current_words)
  words_ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
  ranked_scores = [(words_ranked[i], scores[words_ranked[i]]) for i in range(len(words_ranked))]

  print('Total Possibilities: ' + str(len(current_words)))
  print('Top 10 Guesses')
  for score in ranked_scores[:10]:
    print(f'{score[0][0]}: {score[0][1]}')
  guess = input('Enter guess: ')
  feedback = input('Enter hard/soft/miss feedback in format "hhssm": ')
  print('\n------------------------------------------------------\n')
  current_words = update_possible_words(current_words, guess, feedback)

  n_guesses += 1
