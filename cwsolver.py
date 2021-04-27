import argparse
import json
import math
import pickle
import shutil
from collections import Counter, defaultdict
from textwrap import dedent
from typing import Dict, List, Tuple

from main_funcs import *


def wrap(text, width=80):
	text = text.split("\n")
	res = []
	for t in text:
		res.extend(t[i:i + width] for i in range(0, len(t), width))
	return res


str.translate


def import_dict(filename: str) -> Dict[int, List[str]]:
	if filename.endswith("pickle"):
		with open(filename, "rb") as f_pickle:
			return pickle.load(f_pickle)

	if filename.endswith("json"):
		with open(filename, "r") as f_json:
			res = json.load(f_json)
		ret = {}
		for i, j in res.items():
			ret[int(i)] = j
		return ret

	with open(filename, "r") as f_txt:
		wordlist = f_txt.read().splitlines()
	words = defaultdict(list)
	for word in wordlist:
		words[len(word)].append(word)
	return dict(words)


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


def main():
	parser = argparse.ArgumentParser(description="Dictionary word solver",
	                                 epilog=wrap(
	                                     dedent("""
			Pattern must the string input that needs to be solved.
			Use letters(a-z and A-Z, FIXED) for known entries, digits(1-9, PARTIAL) for same entries and a dot(., WILDCARD) for unknown entries. For example, the pattern "1a1" prints all 3 letter words which have same first and third letter, and the second entry is the letter `a`.

			caution:
			This script is not well optimized, this should not be a problem for modern
			processors but if you are low on main memory, try using a smaller dictionary or make
			a better one. This is also not the fastest, because of the algorithm.

			example:
			(These results depend on the dictionary used, may differ for other users)

			$ /path/to/python3 %(prog)s /path/to/dict "1dg."
			edge edgy
			$ /path/to/python3 %(prog)s /path/to/dict "12121212121212"
			[!] No results found """), 80),
	                                 formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-d", "--dictionary", help="dictionary file location, support `txt`, `pickle` and `json` files")
	parser.add_argument("patterns", help="patterns to search", nargs="*")
	parser.add_argument("--rpp", help='repeat PARTIAL with PARTIAL, "21"="aa"', action="store_true")
	parser.add_argument("--rwp", "--rpw", help='repeat WILDCARD with PARTIAL, ".1"="aa"', action="store_true", dest="rwp")
	parser.add_argument("--rwf", "--rfw", help='repeat WILDCARD with FIXED, ".a"="aa"', action="store_true", dest="rwf")
	parser.add_argument("--rpf", "--rfp", help='repeat PARTIAL with FIXED, "1a"="aa"', action="store_true", dest="rpf")
	# parser.add_argument('--verbose', '-v', action='count', default=0, help="print verbose logs. Stacks up to -vvv")
	args = parser.parse_args()
	words = import_dict(args.dictionary)
	patterns = simplify_patterns(args.patterns)
	if any(len(i) not in words for i in patterns):
		raise ValueError("Dictionary does not contain any words of given length")

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
