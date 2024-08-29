import nltk
import sys
from nltk.tokenize import word_tokenize
from nltk.tree import *

# nltk.download('punkt_tab')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until" | "today"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself" | "school" | "dog" | "man" | "park"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat" | "went" | "saw"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
    S -> NP VP | S Conj S
    NP -> Det N | Det N PP | N | Det Adj N | Adj N | Det N P Det N | N Conj
    VP -> V NP | V NP PP | V | Conj V | VP Conj VP | V Adv | V Adv PP | V PP
    PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # tokenize sentence and add to list
    sentence_list = word_tokenize(sentence)

    sentence_list = [x.lower() for x in sentence_list if x.isalpha()]
    return sentence_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chuncks = []
    # iterate through subtrees
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            # add shallow subtree immediately
            if len(subtree) == 1:
                chuncks.append(subtree)
            else:
                # if count of NPs is one add it to the list
                NP_count = 0
                for sub in subtree.subtrees():
                    if sub.label() == "NP":
                        NP_count += 1
                if NP_count == 1:
                    chuncks.append(subtree)
    return chuncks


if __name__ == "__main__":
    main()
