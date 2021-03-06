import argparse
import json
import math
import pickle
import shutil
from collections import Counter, defaultdict
from textwrap import dedent
from typing import Dict, Final, List, Tuple

ALPHA: Final = "abcdefghijklmnopqrstuvwxyz"
DIGIT: Final = "123456879"
ALLOWED_CHARS: Final = ALPHA + DIGIT + "."


def import_dict(filename: str) -> Dict[int, List[str]]:
	if filename.endswith("pickle"):
		with open(filename, "rb") as fpickle:
			return pickle.load(fpickle)

	if filename.endswith("json"):
		with open(filename, "r") as fjson:
			res = json.load(fjson)
		ret = {}
		for i, j in res.items():
			ret[int(i)] = j
		return ret

	with open(filename, "r") as ftxt:
		wordlist = ftxt.read().splitlines()
	words = defaultdict(list)
	for word in wordlist:
		words[len(word)].append(word)
	return dict(words)


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


def single_pattern(words: List[str], pattern: str, intial_config=None):
	if intial_config is None:
		intial_config = {}
	for i, j in intial_config.items():
		if i in DIGIT:
			pattern = pattern.replace(i, j)
	matched_letters = check_letters(words, pattern)
	if len(matched_letters) == 0:
		return None
	matched_letters = set_numbers(matched_letters, pattern)
	if len(matched_letters) == 0:
		return None
	return matched_letters


def simplify_patterns(patterns: List[str]):
	counter = Counter("".join(patterns))
	res = []
	for pattern in patterns:
		pattern = pattern.lower().strip()
		for i in pattern:
			if i not in ALLOWED_CHARS:
				raise ValueError(f"[!] Disallowed character `{i}` in pattern `{pattern}`")
			if i in DIGIT and counter[i] == 1:
				pattern = pattern.replace(str(i), ".")
		res.append(pattern)
	return res


def print_list(lst: List[str]):
	zfill_len = len(lst[0])
	term_len = shutil.get_terminal_size(fallback=(0, 0)).columns
	columns = math.floor((term_len + 1) / (zfill_len + 1))
	if columns == 0:
		columns = 1
	buffer = (" ".join(lst[i:i + columns]) for i in range(0, len(lst), columns))
	for i in buffer:
		print(i)


def print_tuples(tup: Tuple):
	print_list([f"({','.join(i)})" for i in tup])


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


def multi_pattern(words, patterns):
	matches = [single_pattern(words[len(pattern)], pattern) for pattern in patterns]
	if not all(matches):
		return None
	res = None
	for match in matches:
		res = multi_pattern_tuple(res, match, patterns)
	return res


def main():
	parser = argparse.ArgumentParser(description="Dictionary word solver",
	                                 epilog=dedent("""
			Pattern must the string input that needs to be solved.
			Use letters(a-z and A-Z) for known entries, digits(1-9) for same entries and a dot(.)
			for unknown entries. For example, the pattern "1a1" prints all 3 letter words
			which have same first and third letter, and the second entry is the letter `a`.

			caution:
			This script is not well optimized, this should not be a problem for modern
			processors but if you are low on main memory, try using a smaller dictionary or make
			a better one. This is also not the fastest, because of the algorithm.

			example:
			(These results depend on the dictionary used, may differ for other users)

			$ /path/to/python3 %(prog)s /path/to/dict "1dg."
			edge edgy
			$ /path/to/python3 %(prog)s /path/to/dict "12121212121212"
			[!] No results found """),
	                                 formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument(
	    "dictionary",
	    help="dictionary file location, support `txt`, `pickle` and `json` files",
	)
	parser.add_argument(
	    "patterns",
	    help="patterns to search",
	    nargs="*",
	)

	args = parser.parse_args()
	words = import_dict(args.dictionary)
	patterns = simplify_patterns(args.patterns)

	if len(patterns) == 0:
		text = input("Enter pattern: ")
		if len(text) > 1:
			splat = text.split()
			if len(splat) == 1:
				print_list(single_pattern(words[len(text)], text))
			else:
				print_tuples(multi_pattern(words, splat))
	elif len(patterns) == 1:
		res = single_pattern(words[len(patterns[0])], patterns[0])
		if res is None:
			print("[!] No results found")
		else:
			print_list(res)
	else:
		res = multi_pattern(words, patterns)
		if res is None:
			print("[!] No results found")
		else:
			print_tuples(res)


if __name__ == "__main__":
	main()
