from collections import defaultdict
import unicodedata
import string
import itertools
import sys
import argparse


class LigmaFinder:
    def __init__(self):
        """
        Initializes the tables
        """
        self.fancy_table = {}
        self.lookup_table = defaultdict(list)
        self._populate_tables()


    def _populate_tables(self):
        for i in range(0, sys.maxunicode + 1):

            # Skip standard ASCII
            if i < 128:
                continue

            char = chr(i)

            # NOTE: 1. Must be a valid identifier part per PEP 3131
            # if not char.isidentifier():
            #     continue

            norm = unicodedata.normalize('NFKC', char)

            # Add if usefull ascii expansion
            if norm and all(chars in string.ascii_letters for chars in norm):

                self.fancy_table[char] = norm
                self.lookup_table[norm].append(char)


    def print_full_table(self):

        print(f"--- PEP 3131 Identifiers Normalizing to ASCII ---")
        print("-" * 85)
        print(f"{'Code':<9} | {'Char':<4} | {'NFKC':<4} | {'Name'}")
        print("-" * 85)

        # Iterate over the stored table to avoid re-scanning logic
        sorted_chars = sorted(self.fancy_table.keys(), key=ord)

        for char in sorted_chars:
            code_point = ord(char)
            norm = self.fancy_table[char]
            try:
                name = unicodedata.name(char)
            except ValueError:
                name = "-"

            print(f"U+{code_point:04X}{'':<3} | {char:<4} | {norm:<4} | {name}")


    def print_lookuptable(self):

        print("\n--- Lookup Table (ASCII -> Fancy Variants) ---")
        print(f"{'Target':<10} | {'Count':<5} | {'Variants'}")
        print("-" * 80)
        
        # sort alphabetically
        sorted_keys = sorted(self.lookup_table.keys(), key=lambda x: (-len(x), x))
        
        for key in sorted_keys:
            variants = self.lookup_table[key]
            # Limit to first 15
            variants_str = ", ".join(variants[:15])
            if len(variants) > 15:
                variants_str += f", ... ({len(variants)-15} more)"
                
            print(f"{key:<10} | {len(variants):<5} | {variants_str}")


    def print_useful_slices(self, word):
        for key in self.lookup_table.keys():
            if len(key) > 1 and key in word:
                print(f"key:{key} in word {word}")

    def _greedy_compile(self, word, max_candidates=1):

        compiled_words = []

        # greedy algorithm to find shortest
        i = 0
        n = len(word)
        while  i < n:
            found = False 

            # Look for longest match first
            for j in range(n, i, -1):
                chunk = word[i:j]
                
                if chunk in self.lookup_table:
                    compiled_words.append(self.lookup_table[chunk])
                    found = True
                    i = j
                    break

            if not found:
                compiled_words.append([word[i]])
                i += 1

        # permutations
        iterator = ("".join(combo) for combo in itertools.product(*compiled_words))

        if max_candidates is None:
            return list(iterator)

        return list(itertools.islice(iterator, max_candidates))

    def _compile(self, word, max_candidates=1):
        letter_options = []

        for c in word:
            candidates = self.lookup_table[c]
            
            # strict check: if a char has no variants, fail the whole compile
            if candidates:
                letter_options.append(candidates)
            else:
                return None

        iterator = ("".join(combo) for combo in itertools.product(*letter_options))

        if max_candidates is None:
            return list(iterator)
        
        return list(itertools.islice(iterator, max_candidates))

    def compile(self, word, greedy=True, max_candidates=1):
        if greedy:
            return self._greedy_compile(word, max_candidates=max_candidates)
        else:
            return self._compile(word, max_candidates=max_candidates)


def main():
    parser = argparse.ArgumentParser(description="Compile ASCII words into PEP 3131 valid Unicode variants.")
    parser.add_argument("words", nargs="*", help="Words to compile (e.g. 'exit(flag)')")
    parser.add_argument("-m", "--max", type=int, default=5, help="Max candidates to generate per word")
    parser.add_argument("--no-greedy", action="store_true", help="Disable greedy slicing (strict char-by-char)")
    parser.add_argument("--table", action="store_true", help="Print the full Unicode character table")
    parser.add_argument("--lookup", action="store_true", help="Print the expansion lookup table")
    parser.add_argument("--print-slices", nargs="+", help="Print slises for word")
    
    args = parser.parse_args()

    # Initialize
    ligma = LigmaFinder()

    # Handle Table printing
    if args.table:
        ligma.print_full_table()
        return

    if args.lookup:
        ligma.print_lookuptable()
        return

    if args.print_slices:
        for word in args.print_slices:
            ligma.print_useful_slices(word)
        return

    # Determine inputs (args or default demo)
    words_to_process = args.words
    if not words_to_process:
        print("No words provided. Running demo...", file=sys.stderr)
        words_to_process = ["exit", "print(flag)", "exit(flag)"]

    # Process words
    greedy_mode = not args.no_greedy
    
    for word in words_to_process:
        print(f"\n--- Compiling: '{word}' (Greedy: {greedy_mode}) ---")
        
        res = ligma.compile(word, greedy=greedy_mode, max_candidates=args.max)
        
        if res:
            for r in res:
                print(f"{r}\t({len(r)})")
        else:
            print("No results found (Try removing --no-greedy if the word contains punctuation)")


if __name__ == "__main__":
    main()
