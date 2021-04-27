from string import ascii_lowercase as ALPHA
from string import digits as DIGIT
from typing import Dict, Final, List

ALLOWED_CHARS: Final = ALPHA + DIGIT + "."


def check_letters(words: List[str], pattern: str):
	matched: List[str] = []
	for word in words:
		for i, letter in enumerate(pattern):
			if pattern[i] != word[i] and letter in ALPHA:
				break
		else:
			matched.append(word)
	return matched


def set_numbers(words: List[str], pattern: str):
	matched = []
	for word in words:
		map_number_to_letter: Dict[str, str] = {}
		for char_pat, char_wrd in zip(pattern, word):
			if char_pat >= '1' and char_pat <= '9':
				if char_pat in map_number_to_letter:
					if map_number_to_letter[char_pat] != char_wrd:
						break
				else:
					map_number_to_letter[char_pat] = char_wrd
		else:
			matched.append(word)
	return matched


def single_pattern(words: List[str], pattern: str, initial_config=None):
	if initial_config is None:
		initial_config = {}
	for i, j in initial_config.items():
		if i in DIGIT:
			pattern = pattern.replace(i, j)
	matched_letters = check_letters(words, pattern)
	if len(matched_letters) == 0:
		return None
	matched_letters = set_numbers(matched_letters, pattern)
	if len(matched_letters) == 0:
		return None
	return matched_letters


def multi_pattern(words, patterns):
	matches = [single_pattern(words[len(pattern)], pattern) for pattern in patterns]
	if not all(matches):
		return None
	res = None
	for match in matches:
		res = multi_pattern_tuple(res, match, patterns)
	return res


def multi_pattern_tuple(list_inp_tuple, matches, patterns):
	if list_inp_tuple is None:
		return [(i, ) for i in matches]
	matched = []

	curr_pattern = patterns[len(list_inp_tuple[0])]
	for inp_tuple in list_inp_tuple:
		map_number_to_letter = {}
		for inp, pattern in zip(inp_tuple, patterns):
			for pat, i in zip(pattern, inp):
				if pat >= '1' and pat <= '9':
					map_number_to_letter[pat] = i
		temp = single_pattern(matches, curr_pattern, map_number_to_letter)
		if temp is not None:
			for match in temp:
				matched.append(tuple([*inp_tuple, match]))
	return matched
