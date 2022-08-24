#############################################################
# FILE : hangman.py
# WRITER : Ilan Vysokovsky, ilan.vys, 207375528
# EXERCISE : intro2cs1 ex4 2021
# DESCRIPTION: A program simultaing the hangman game,
# using an intercative interface, keeping score and supporting 
# multiple rounds.
#############################################################
import hangman_helper

def update_word_pattern(word, pattern, letter):
    '''
    Recieves a word, a letter and updates the pattern recieved,
    to reveal the letter in the pattern if it exists in the word.
    :param word: The secret word
    :param pattern: The current pattern with letters guessed revealed
    :param letter: The letter guessed
    :return: A new pattern with revealed letter if itws in the word
    '''
    new_pattern = list(pattern)
    if letter in word:
        for i in range(0, len(word)):
            if letter == word[i]:
                new_pattern[i] = letter

    return "".join(new_pattern)

def validate_word_list_length(word_suggestions_lst):
    '''
    Filteres words from the words list, 
    to match the allowed length of the list
    :param word_suggestions_lst: The word list to filter from
    :return: a list with the possible words to match the pattern
    '''
    allowed_hint_len = hangman_helper.HINT_LENGTH
    
    if len(word_suggestions_lst) > allowed_hint_len:
        short_word_suggestions_lst = []
        for i in range(0, allowed_hint_len):
            index = int(i * len(word_suggestions_lst) / allowed_hint_len)
            short_word_suggestions_lst.append(word_suggestions_lst[index])
            
        return short_word_suggestions_lst
    else:
        return word_suggestions_lst
        
def filter_words_list(words, pattern, wrong_guess_lst):
    '''
    Filteres words from the words list, 
    matching the already revealed letters in the pattern,
    and letters appearing in the wrong_guess_lst.
    :param words: The word list to filter from
    :param pattern: The current pattern with letters guessed revealed
    :param wrong_guess_lst: The list with letters guessed,
    but don't appear in the word
    :return: a list with the possible words to match the pattern
    '''
    pattern_to_lst = list(pattern)
    possible_words = []
    for word in words:
        if len(word) == len(pattern):
            word_to_lst = list(word)
            correct_letter_indexs = True
            
            # Go over all the letters in the word
            for i in range(0, len(word_to_lst)):
                if word_to_lst[i] in wrong_guess_lst or \
                    (pattern_to_lst[i] != "_" and \
                        word_to_lst[i] != pattern_to_lst[i]) or \
                            (pattern_to_lst[i] == "_" and word_to_lst[i] in pattern): 
                    correct_letter_indexs = False
                    break
                
            if correct_letter_indexs:  
                possible_words.append("".join(word))
    possible_words = validate_word_list_length(possible_words)
    return possible_words


def check_valid_letter_input(guess, wrong_guess_lst, pattern):
    '''
    Validates that the letter input is correct,
    and also that the letter doesnt already appear
    in the list of letters guessed.
    :param guess: The guess input
    :param wrong_guess_lst: The list with letters guessed but 
    don't appear in the word
    :param pattern: The current pattern with letters guessed revealed
    :return: True if input is valid, otherwise False
    '''
    if len(guess) > 1 or not guess.isalpha() or guess.lower() != guess:
        return False
    if guess in wrong_guess_lst or guess in pattern:
        return False
    return True

def update_letter(score, guess, word, pattern, wrong_guess_lst):
    '''
    Updates the letter guessed and adds it to the pattern 
    if exists in the word, otherwise adds it to the wrong guesses 
    of letters list
    :param score: The current game score
    :param guess: The guess input
    :param word: The secret word
    :param pattern: The current pattern with letters guessed revealed
    :param wrong_guess_lst: The list with letters guessed
    but don't appear in the word
    :return: updated score, pattern and wrong_guess_lst
    '''
    score -= 1
    if guess in word:
        pattern = update_word_pattern(word, pattern, guess)
        appearences_num = 0
        for letter in list(pattern):
            if letter == guess:
                appearences_num += 1
        score += int(appearences_num * (appearences_num + 1) / 2)
    else:
        wrong_guess_lst.append(guess)
        
    return score, pattern, wrong_guess_lst

def update_word(score, guess, word, pattern):
    '''
    Checks if the guessed word is the secret word,
    if so it calculates a bonus for the score.
    If the guessed word is incorrect, it just removes 1 point from score.
    :param score: The current game score
    :param guess: The guess input
    :param word: The secret word
    :param pattern: The current pattern with letters guessed revealed
    :return: updated score and pattern
    '''
    score -= 1
    if guess == word:
        appearences_num = 0
        for letter in list(pattern):
            if "_" == letter:
                appearences_num += 1
        pattern = word
        score += int(appearences_num * (appearences_num + 1) / 2)
    
    return score, pattern

def update_hint(words_list, score, wrong_guess_lst, pattern):
    '''
    Calculates a list of possible word that fit the pattern
    with allowed length, prints the list, and updates the score.
    :param words_list: List of all the words to iterate over
    :param score: The current game score
    :param pattern: The current pattern with letters guessed revealed
    :param wrong_guess_lst: The list with letters guessed but
    don't appear in the word
    :return: updated score
    '''
    score -= 1
    word_suggestions_lst = filter_words_list(
        words_list, pattern, wrong_guess_lst)
    
    hangman_helper.show_suggestions(word_suggestions_lst)
    return score

        
def run_single_game(words_list, score):
    '''
    Runs one iteration of Hangman game, 
    chooses a word from the words_list,
    and keeps score.
    :param score: The initial game score
    :param words_list: The word list to choose the secret word from
    :return: score at the end of the game
    '''
    word = hangman_helper.get_random_word(words_list)
    wrong_guess_lst = []
    pattern = '_' * len(word)
    
    # Game round
    while (pattern != word and score > 0):
        hangman_helper.display_state(
            pattern, wrong_guess_lst, score , "Let's go!")
        input_type, guess = hangman_helper.get_input()
        
        if input_type == hangman_helper.LETTER:
            if check_valid_letter_input(guess, wrong_guess_lst, pattern):
                score, pattern, wrong_guess_lst = update_letter(
                    score, guess, word, pattern, wrong_guess_lst)
            else:
                continue
            
        if input_type == hangman_helper.WORD:
            score, pattern = update_word(score, guess, word, pattern)
                
        if input_type == hangman_helper.HINT:
            score = update_hint(words_list, score, wrong_guess_lst, pattern)
            continue

    if (score > 0):    
        hangman_helper.display_state(
            pattern, wrong_guess_lst, score, "You won!")
    else:
        hangman_helper.display_state(
            pattern, wrong_guess_lst, score, f"You lost! The word was {word}")
        
    return score

def main():
    '''
    Runs one iteration of Hangman game, 
    chooses a word from the words_list,
    and keeps score.
    :param score: The initial game score
    :param words_list: The word list to choose the secret word from
    :return: score at the end of the game
    '''
    words_list = hangman_helper.load_words()
    games_played = 0
    answer = True
    score = hangman_helper.POINTS_INITIAL
    
    while(answer):
        score = run_single_game(words_list, score)
        games_played += 1
        if score > 0:
            answer = hangman_helper.play_again(
                f"Games played: {games_played}. \
                Points Earned: {score}. Want another round?")
        else:    
            answer = hangman_helper.play_again(
                f"Nice Streak! Games played: {games_played}. \
                    Points Earned: {score}. Want to start over?")
            if answer:
                score = hangman_helper.POINTS_INITIAL
                games_played = 0

if __name__ == "__main__":
    main()