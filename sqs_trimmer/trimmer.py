import numpy as np

def get_A_matrix():
    # Read bestsqs.out file
    with open(BESTSQS, 'r') as f:
        lines = f.readlines()

    # Get matrix A (Firts 3 lines)
    A = np.zeros((3, 3))
    for i in range(3):
        A[i] = np.array([float(x) for x in lines[i].split()])
    return A

def get_B_list():
    B_list = []
    B = []
    with open(SQSCELL, 'r') as f:
        # Skip the first line (number of B_list)
        next(f)
        for line in f:
            line = line.strip()
            if line:
                # Convert line to list of floats
                row = list(map(float, line.split()))
                B.append(row)
                
                if len(B) == 3:
                    B_list.append(B)
                    B = []
            else:
                # Skip empty lines
                continue
    return B_list


def trim():
    # Get A matrix
    A = get_A_matrix()
    # Get B matrices
    B_list = get_B_list()

    abc_list, ang_list = [], []
    for i, B in enumerate(B_list):
        B = np.array(B)
        X = -np.dot(B, A)
        a = np.linalg.norm(X[0])
        b = np.linalg.norm(X[1])
        c = np.linalg.norm(X[2])
        alpha = np.arccos(np.dot(X[1], X[2]) / (b * c)) * 180 / np.pi
        beta = np.arccos(np.dot(X[0], X[2]) / (a * c)) * 180 / np.pi
        gamma = np.arccos(np.dot(X[0], X[1]) / (a * b)) * 180 / np.pi
        abc_std = np.std([a, b, c])
        abc_list.append([i, a, b, c, abc_std])
        ang_std = np.std([alpha, beta, gamma])
        ang_list.append([i, alpha, beta, gamma, ang_std])
        
    # Normalize all the abc_std and ang_std
    abc_std_list = np.array([abc[4] for abc in abc_list])
    abc_std_norm = abc_std_list / np.max(abc_std_list)
    for i, abc in enumerate(abc_list):
        abc.append(abc_std_norm[i])
    ang_std_list = np.array([ang[4] for ang in ang_list])
    ang_std_norm = ang_std_list / np.max(ang_std_list)
    for i, ang in enumerate(ang_list):
        ang.append(ang_std_norm[i])

    # Calculate the final score using the sum of abc_std_norm and ang_std_norm
    final_score_list = []
    for i, abc in enumerate(abc_list):
        final_score = abc[5] + ang_list[i][5]
        final_score_list.append([abc[0], final_score])

    # Sort the final_score_list based on the final score 
    final_score_list = sorted(final_score_list, key=lambda x: x[1])

    # Get the First Nth B matrices, abc_list, and ang_list
    indices = [x[0] for x in final_score_list[:N_OUTPUT]]
    B_list = [B_list[i] for i in indices]
    abc_list = [abc_list[i] for i in indices]
    ang_list = [ang_list[i] for i in indices]

    # Print the final results
    for i, B in enumerate(B_list):
        print(f'B_{i+1} matrix:')
        for row in B:
            print(' '.join([f'{x:.6f}' for x in row]))
        print(f'a/b/c/std/std_norm: {abc_list[i][1]:.6f} {abc_list[i][2]:.6f} {abc_list[i][3]:.6f} {abc_list[i][4]:.6f} {abc_list[i][5]:.6f}')
        print(f'alpha/beta/gamma/std/std_norm: {ang_list[i][1]:.6f} {ang_list[i][2]:.6f} {ang_list[i][3]:.6f} {ang_list[i][4]:.6f} {ang_list[i][5]:.6f}')
        print(f'final score: {final_score_list[i][1]:.6f}')
        print()

    # Write the final B matrices to sqscell.out file
    with open(f'{SQSCELL[:-4]}_trimmed.out', 'w') as f:
        f.write(f'{N_OUTPUT}\n\n')
        for B in B_list:
            for row in B:
                f.write(' '.join([f'{x:.6f}' for x in row]) + '\n')
            f.write('\n')

if __name__ == '__main__':
    BESTSQS = 'sqs_trimmer/bestsqs.out'
    SQSCELL = 'sqs_trimmer/sqscell.out'
    N_OUTPUT = 1
    trim()




