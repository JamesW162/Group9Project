from autocorrect import Speller
import sys

input_text = sys.argv[1]

speller = Speller()
print(speller(input_text))
