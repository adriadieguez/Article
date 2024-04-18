import sys

def reading():
    # GenGM options
    tree = sys.argv[1]
    case = 1
    num_lengths = len(sys.argv)
    lengths = []
    name = None
    if sys.argv[-2].startswith("L"):
        for i in range(2, num_lengths - 1):
            lengths.append(int(sys.argv[i][1:]))
            case = 2
        name = sys.argv[-1]
        return tree, case, lengths, None, name
    else:
        t = int(sys.argv[2])
        L = int(sys.argv[3])
        name = sys.argv[-1]
        return tree, case, t, L, name

    