#!/usr/bin/python3

"""
DESCRIPTION:
    Template code for the Dynamic Programming assignment in the Algorithms in Sequence Analysis course at the VU.
    
INSTRUCTIONS:
    Complete the code (compatible with Python 3!) upload to CodeGrade via corresponding Canvas assignment.

AUTHOR:
    <Nikolaos Bounatsos - nbo222>
"""



import argparse
import pickle



def parse_args():
    "Parses inputs from commandline and returns them as a Namespace object."

    parser = argparse.ArgumentParser(prog = 'python3 align.py',
        formatter_class = argparse.RawTextHelpFormatter, description =
        '  Aligns the first two sequences in a specified FASTA\n'
        '  file with a chosen strategy and parameters.\n'
        '\n'
        'defaults:\n'
        '  strategy = global\n'
        '  substitution matrix = pam250\n'
        '  gap penalty = 2')
        
    parser.add_argument('fasta', help='path to a FASTA formatted input file')
    parser.add_argument('output', nargs='*', 
        help='path to an output file where the alignment is saved\n'
             '  (if a second output file is given,\n'
             '   save the score matrix in there)')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
        help='print the score matrix and alignment on screen', default=False)
    parser.add_argument('-s', '--strategy', dest='strategy',
        choices=['global','semiglobal','local'], default="global")
    parser.add_argument('-m', '--matrix', dest='substitution_matrix',
        choices=['pam250','blosum62','identity'], default='pam250')
    parser.add_argument('-g', '--gap_penalty', dest='gap_penalty', type=int,
        help='must be a positive integer', default=2)

    args = parser.parse_args()

    args.align_out = args.output[0] if args.output else False
    args.matrix_out = args.output[1] if len(args.output) >= 2 else False
                      # Fancy inline if-else statements. Use cautiously!
                      
    if args.gap_penalty <= 0:
        parser.error('gap penalty must be a positive integer')

    return args



def load_substitution_matrix(name):
    "Loads and returns the specified substitution matrix from a pickle (.pkl) file."
    # Substitution matrices have been prepared as nested dictionaries:
    # the score of substituting A for Z can be found with subst['A']['Z']
    # NOTE: Only works if working directory contains the correct folder and file!
    
    with open('substitution_matrices/%s.pkl' % name, 'rb') as f:
        subst = pickle.load(f)
    return subst
    
    

def load_sequences(filepath):
    "Reads a FASTA file and returns the first two sequences it contains."
    
    seq1 = []
    seq2 = []
    with open(filepath,'r') as f:
        for line in f:
            if line.startswith('>'):
                if not seq1:
                    current_seq = seq1
                elif not seq2:
                    current_seq = seq2
                else:
                    break # Stop if a 3rd sequence is encountered
            else:
                current_seq.append(line.strip())
    
    if not seq2:
        raise Exception('Error: Not enough sequences in specified FASTA file.')
    
    seq1 = ''.join(seq1)
    seq2 = ''.join(seq2)
    return seq1, seq2



def align(seq1, seq2, strategy, substitution_matrix, gap_penalty):
    "Do pairwise alignment using the specified strategy and parameters."
    # This function consists of 3 parts:
    #
    #   1) Initialize a score matrix as a "list of lists" of the appropriate length.
    #      Fill in the correct values for the first row and column given the strategy.
    #        (local / semiglobal = 0  --  global = stacking gap penalties)
    #   2) Fill in the rest of the score matrix using Dynamic Programming, accounting
    #      for the selected alignment strategy, substitution matrix and gap penalty.
    #   3) Perform the correct traceback routine on your filled in score matrix.
    #
    # Both the resulting alignment (sequences with gaps and the corresponding score)
    # and the filled in score matrix are returned as outputs.
    #
    # NOTE: You are strongly encouraged to think about how you can reuse (parts of)
    #       your code between steps 2 and 3 for the different strategies!
    
    
    ### 1: Initialize
    M = len(seq1)+1
    N = len(seq2)+1
    score_matrix = []
    for i in range(M):
        row = []
        score_matrix.append(row)
        for j in range(N):
            row.append(0)
    if strategy == 'global':
        #####################
        # START CODING HERE #
        #####################
        # Change the zeroes in the first row and column to the correct values.

        for i in range(1, M):
            score_matrix[i][0] = score_matrix[i-1][0] - gap_penalty

        for j in range(1, N):
            score_matrix[0][j] = score_matrix[0][j-1] - gap_penalty

        #####################
        #  END CODING HERE  #
        #####################

    
    
    ### 2: Fill in Score Matrix
 
    #####################
    # START CODING HERE #
    #####################

    def dp_function(): 
        max_list=[]

        # diagoneal
        var_diagoneal = score_matrix[i-1][j-1] + substitution_matrix[seq1[i-1]][seq2[j-1]]

        # downwards
        var_down = score_matrix[i][j-1] - gap_penalty

        # rightwards
        var_right = score_matrix[i-1][j] - gap_penalty

        max_list.extend([var_diagoneal, var_down, var_right])
        return max(max_list)

    for i in range(1,M):
        for j in range(1,N):
            score_matrix[i][j] = dp_function()

    # for i in range(M):
    #     print(score_matrix[i])

    #####################
    #  END CODING HERE  #
    #####################   

    ### 3: Traceback
    
    #####################
    # START CODING HERE #
    #####################   
    i=M-1
    j=N-1
    def tracing(i,j):
        total_score = 0
        aligned_seq1 = ''
        aligned_seq2 = ''
        cnt1 = M - 2
        cnt2 = N - 2
        while (i>1 or j>1):      
            
            # diagoneal
            var_diagoneal = score_matrix[i-1][j-1]

            # downwards
            var_down = score_matrix[i][j-1]

            # rightwards
            var_right = score_matrix[i-1][j]

            max_dict={
                (i-1,j-1) : var_diagoneal,
                (i,j-1) : var_down,
                (i-1,j) : var_right
            }

            max_value = max(max_dict.values())
            coords = max(max_dict, key=max_dict.get)
            prev_i = i
            prev_j = j
            i = coords[0]
            j = coords[1]

            if(prev_i-1 == i and prev_j-1 == j):
                aligned_seq1 = seq1[cnt1] + aligned_seq1
                aligned_seq2 = seq2[cnt2] + aligned_seq2
                cnt1 -= 1
                cnt2 -= 1
            elif(prev_i-1 == i and prev_j == j):
                aligned_seq1 = seq1[cnt1] + aligned_seq1
                aligned_seq2 = '-' + aligned_seq2
                cnt1 -= 1
            elif(prev_i == i and prev_j-1 == j):
                aligned_seq1 = '-' + aligned_seq1
                aligned_seq2 = seq2[cnt2] + aligned_seq2
                cnt2 -= 1
            if(i==1 or j==1):
                aligned_seq1 = seq1[cnt1] + aligned_seq1
                aligned_seq2 = seq2[cnt2] + aligned_seq2
            total_score += max_value
        return total_score, aligned_seq1, aligned_seq2

    x=0
    aligned_seq1 = ''
    aligned_seq2 = ''
    align_score = score_matrix[M-1][N-1]
    x, aligned_seq1, aligned_seq2 = tracing(i,j)
    print(aligned_seq1)
    print(aligned_seq2)
    #####################
    #  END CODING HERE  #
    #####################   


    alignment = (aligned_seq1, aligned_seq2, align_score)
    return (alignment, score_matrix)



def print_score_matrix(s1,s2,mat):
    "Pretty print function for a score matrix."
    
    # Prepend filler characters to seq1 and seq2
    s1 = '-' + s1
    s2 = ' -' + s2
    
    # Print them around the score matrix, in columns of 5 characters
    print(''.join(['%5s' % aa for aa in s2])) # Convert s2 to a list of length 5 strings, then join it back into a string
    for i,row in enumerate(mat):               # Iterate through the rows of your score matrix (and keep count with 'i').
        vals = ['%5i' % val for val in row]    # Convert this row's scores to a list of strings.
        vals.insert(0,'%5s' % s1[i])           # Add this row's character from s2 to the front of the list
        print(''.join(vals))                   # Join the list elements into a single string, and print the line.



def print_alignment(a):
    "Pretty print function for an alignment (and alignment score)."
    
    # Unpack the alignment tuple
    seq1 = a[0]
    seq2 = a[1]
    score = a[2]
    
    # Check which positions are identical
    match = ''
    for i in range(len(seq1)): # Remember: Aligned sequences have the same length!
        match += '|' if seq1[i] == seq2[i] else ' ' # Fancy inline if-else statement. Use cautiously!
            
    # Concatenate lines into a list, and join them together with newline characters.
    print('\n'.join([seq1,match,seq2,'','Score = %i' % score]))



def save_alignment(a,f):
    "Saves two aligned sequences and their alignment score to a file."
    with open(f,'w') as out:
        out.write(a[0] + '\n') # Aligned sequence 1
        out.write(a[1] + '\n') # Aligned sequence 2
        out.write('Score: %i' % a[2]) # Alignment score


    
def save_score_matrix(m,f):
    "Saves a score matrix to a file in tab-separated format."
    with open(f,'w') as out:
        for row in m:
            vals = [str(val) for val in row]
            out.write('\t'.join(vals)+'\n')
    


def main(args = False):
    # Process arguments and load required data
    if not args: args = parse_args()
    
    sub_mat = load_substitution_matrix(args.substitution_matrix)
    seq1, seq2 = load_sequences(args.fasta)

    # Perform specified alignment
    strat = args.strategy
    gp = args.gap_penalty
    alignment, score_matrix = align(seq1, seq2, strat, sub_mat, gp)

    # If running in "verbose" mode, print additional output
    if args.verbose:
        print_score_matrix(seq1,seq2,score_matrix)
        print('') # Insert a blank line in between
        print_alignment(alignment)
    
    # Save results
    if args.align_out: save_alignment(alignment, args.align_out)
    if args.matrix_out: save_score_matrix(score_matrix, args.matrix_out)



if __name__ == '__main__':
    main()