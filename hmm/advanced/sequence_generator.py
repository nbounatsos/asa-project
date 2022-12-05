#!/usr/bin/python3

"""
DESCRIPTION:
    Template code for the FIRST Advanced Question of the Hidden Markov Models
    assignment in the Algorithms in Sequence Analysis course at the VU.

INSTRUCTIONS:
    Complete the code (compatible with Python 3!) upload to CodeGrade via
    corresponding Canvas assignment. Note this script will be graded manually,
    if and only if your "hmm.py" script succesfully implements Baum-Welch
    training! Continuous Feedback will not be available for this script.

AUTHOR:
    Nikolaos Bounatsos #2768686
"""

import os
from argparse import ArgumentParser, RawTextHelpFormatter
from hmm_utility import load_tsv
from numpy.random import choice



def parse_args():
    #####################
    # START CODING HERE #
    #####################
    # Implement a simple argument parser (WITH help documentation!) that parses
    # the information needed by main() from commandline. Take a look at the
    # argparse documentation, the parser in hmm_utility.py or align.py
    # (from the Dynamic Programming exercise) for hints on how to do this.

    parser = ArgumentParser(prog = 'python3 sequence_generator.py',
        formatter_class = RawTextHelpFormatter, description =
        '  Generates sequences from given transmission and emission matrices')

    # Positionals
    parser.add_argument('transition', help='path to a TSV formatted transition matrix')
    parser.add_argument('emission', help='path to a TSV formatted emission matrix')


    # Optionals
    parser.add_argument('-n', dest='seq_num', type=int, default=1,
    help='The number of sequences to generate. Default: 1') 
    parser.add_argument('-o', dest='out_dir', default= os.getcwd()+'/seq.fasta',
    help='path to a directory where output files are saved\n'
             '  (directory will be made if it does not exist)\n'
             '  (file names and contents depend on algorithm)')
     
    return parser.parse_args()
    
    #####################
    #  END CODING HERE  #
    #####################


def generate_sequence(A,E):
    #####################
    # START CODING HERE #
    #####################
    # Implement a function that generates a random sequence using the choice()
    # function, given a Transition and Emission matrix.
    
    for k in E:
        emittingStates = list(E[k].keys())
        break

    allStates = list(A.keys())
    cur_state = 'B'
    emit = ''
    sequence = ''
    
    while True:
        cur_state = ''.join(choice(allStates, 1, p=generate_probabilities(cur_state,A,allStates)))
        if cur_state == 'E':
            break
        emit = choice(emittingStates,1, p=generate_probabilities(cur_state,E,emittingStates))
        sequence += sequence.join(emit)
    #####################
    #  END CODING HERE  #
    #####################
    
    return sequence


def generate_probabilities(state, ar, states):
    p = []
    for i in states:
        p.append(ar[state][i])
    return p


def main():
    args = parse_args()
    N = args.seq_num               # The number of sequences to generate
    out_file = args.out_dir        # The file path to which to save the sequences
    A = load_tsv(args.transition)    # Transition matrix
    E = load_tsv(args.emission)    # Emission matrix
    with open(out_file,'w') as f:
        for i in range(N):
            seq = generate_sequence(A,E)
            f.write('>random_sequence_%i\n%s\n' % (i,seq))
        
    #####################
    #  END CODING HERE  #
    #####################
    


if __name__ == "__main__":
    main()
