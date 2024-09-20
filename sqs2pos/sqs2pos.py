import numpy as np

def read_sqs():
    # Read bestsqs.out file
    with open(SQS, 'r') as f:
        lines = f.readlines()

    # Get matrix A (Firts 3 lines)
    A = np.zeros((3, 3))
    for i in range(3):
        A[i] = np.array([float(x) for x in lines[i].split()])

    # Get matrix B (Next 3 lines)
    B = np.zeros((3, 3))
    for i in range(3, 6):
        B[i-3] = np.array([float(x) for x in lines[i].split()])

    # Get matrix C (The rest of the lines): e.g., 0.500000 1.500000 2.000000 Fe
    n = len(lines) - 6
    C = np.zeros((n, 3))
    elements = []
    for i in range(6, len(lines)):
        C[i-6] = np.array([float(x) for x in lines[i].split()[:-1]])
        elements.append(lines[i].split()[-1])

    # Calculate the lattice vectors: a multiplication of B and A
    lattice = -np.dot(B, A)

    # Calculate the atomic positions: a multiplication of C and A
    positions = -np.dot(C, A)

    # Map positions and corresponding elements, e.g., {'element_i': positions_i}
    coordinates = {}
    for i, e in enumerate(elements):
        if e not in coordinates:
            coordinates[e] = []
        coordinates[e].append(positions[i])
    return lattice, coordinates

def make_poscar(lattice, coordinates):
    # Write the POSCAR file in Cartesian coordinates
    with open(POSCAR, 'w') as f:
        f.write(' '.join([str(x) for x in coordinates.keys()]) + '\n')
        f.write('1.0\n')
        for i in range(3):
            f.write('        ' + '    '.join(str(x).ljust(20, '0') for x in lattice[i]) + '\n')
        f.write('    ' + ''.join([str(x).ljust(8) for x in coordinates.keys()]) + '\n')
        f.write('    ' + ''.join([str(len(coordinates[x])).ljust(8) for x in coordinates.keys()]) + '\n')
        f.write('Cartesian \n')
        for e in coordinates:
            for p in coordinates[e]:
                f.write('    ' + '    '.join(str(x).ljust(20, '0') for x in p) + '\n')

if __name__ == '__main__':
    SQS = 'sqs2pos/bestsqs.out'
    POSCAR = 'sqs2pos/POSCAR.vasp'
    lattice, coordinates = read_sqs()
    make_poscar(lattice, coordinates)
    print('POSCAR.vasp file has been created.')


