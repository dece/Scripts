#!/usr/bin/env python3
# encoding: utf-8

"""
File: britamerican.py
Author: Paul Lajoie-Mazenc
Description: Checks for british and american spellings in a file. This is just
a basic thing, it may have lots of false positives/negatives.

Inspired from Nicholas J. Higham's “Handbook of Writing for the Mathematical
Sciences”
"""

import re
import argparse

# Words that have a different spelling
# (british, american) spelling
WORDS = [('behaviour', 'behavior'), ('colour', 'color'),
         ('catalogue', 'catalog'), ('centre', 'center'), ('defence', 'defense'),
         ('grey', 'gray'), ('manoeuvre', 'maneuver'),
         ('marvellous', 'marvelous'), ('modelled', 'modeled'),
         ('modelling', 'modeling'), ('skilful', 'skillful'),
         ('speciality', 'specialty'), ('acknowledgement', 'acknowledgment'),
         ('benefited', 'benefitted'), ('encyclopaedia', 'encyclopedia'),
         ('focused', 'focussed'), ('judgement', 'judgment'),
         ('appendices', 'appendixes'), ('formulae', 'formulas'),
         ('indices', 'indexes'), ('lemmata', 'lemmas'),
         ('vertices', 'vertexes'), ('optimisation', 'optimization')]
BRITISH = [word[0] for word in WORDS]
AMERICAN = [word[1] for word in WORDS]

# Exceptions for the *ise words, mostly verbs
# All the other *ise verbs should be *ise in british and *ize in american
EXCEPTIONS = ['advise', 'arise', 'circumcise', 'comprise', 'compromise',
    'concise', 'demise', 'despise', 'devise', 'disguise', 'excise', 'exercise',
    'expertise', 'franchise', 'guise', 'improvise', 'incise', 'likewise',
    'otherwise', 'precise', 'premise', 'promise', 'reprise', 'revise', 'rise',
    'size', 'scriptsize', 'footnotesize', 'supervise', 'surmise', 'surprise',
    'televise', 'treatise', 'wise']

# Detects words
re_words = re.compile('\\w+')
# Gets the *ise[ds] and *ize[ds]
re_ise = re.compile('\\b\\w+ise[ds]?\\b')
re_ize = re.compile('\\b\\w+ize[ds]?\\b')
# Gets the *yse[ds] and *yze[ds]
re_yse = re.compile('\\b\\w+yse[ds]?\\b')
re_yze = re.compile('\\b\\w+yze[ds]?\\b')
# The word ends with a d or an s
re_suffix = re.compile('^\\w+[ds]$')


def parse_args():
    """ Parses the arguments of the command line """
    parser = argparse.ArgumentParser(
            description="Checks a file for british and american spellings")

    parser.add_argument('files', metavar="files", type=str, nargs='+',
            help='file where to check the spellings')

    return parser.parse_args()

def check_british(text):
    """ Checks text for british words """
    return [word for word in text if word in BRITISH]

def check_american(text):
    """ Checks text for american words """
    return [word for word in text if word in AMERICAN]

def check_ise(text):
    """ Checks for words ending in ise[ds]? """
    return re_ise.findall(text)

def check_ize(text):
    """ Checks for words ending in ize[ds]? """
    return re_ize.findall(text)

def check_yse(text):
    """ Checks for words ending in yse[ds]? """
    return re_yse.findall(text)

def check_yze(text):
    """ Checks for words ending in yze[ds]? """
    return re_yze.findall(text)

def root(word):
    """ Gets the root of a word (ie removes the 'd' or 's' of past participle or plurals/conjugation """
    if re_suffix.match(word):
        return word[:-1]
    return word

def remove_exceptions(words):
    """ Removes exceptions from the resulting words """
    return [word for word in words if root(word) not in EXCEPTIONS]

def get_words(line):
    """ Gets the american and british spellings in text """
    british = []
    american = []

    line = line.lower()

    # British/American words
    words = re_words.findall(line)
    british.extend(check_british(words))
    american.extend(check_american(words))

    # -ise/-ize verbs
    british.extend(check_ise(line))
    american.extend(check_ize(line))

    # -yse/-yze verbs
    british.extend(check_yse(line))
    american.extend(check_yze(line))

    british = remove_exceptions(british)
    american = remove_exceptions(american)

    return british, american

def check_line(line, index):
    """ Checks the text for american and british spellings
    
    The formatting is correctly aligned for < 10,000 lines"""
    british, american = get_words(line)
    british_prefix = '\033[91m' + "UK" + '\033[0m'
    american_prefix = '\033[92m' + "US" + '\033[0m'
    if len(british) > 0 or len(american) > 0:
        pad = ''
        print("{:<4d}: ".format(index + 1), end='')
        if len(british) > 0:
            print("{}: {}".format(british_prefix, british))
            pad = ' '*6
        if len(american) > 0:
            print("{}{}: {}".format(pad, american_prefix, american))

def main():
    """ Main function """
    files = parse_args().files

    for file_ in files:
        try:
            fd = open(file_)
            lines = fd.readlines()
            fd.close()
        except IOError:
            print("Couldn't read file {}, skipping it".format(file_))
            break

        print(file_)
        for index, line in enumerate(lines):
            check_line(line, index)

if __name__ == '__main__':
    main()
