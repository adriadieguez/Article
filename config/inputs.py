import sys

def reading():
    # GenGM options
    tree = sys.argv[1]
    case = 1
    num_lengths = len(sys.argv)
    lengths = []
    if (sys.argv[2].startswith("L")):
        for i in range(2, num_lengths):
            lengths.append(int(sys.argv[i][1:]))
            case = 2
        return tree, case, lengths, None
    else:
        t = int(sys.argv[2])
        L = int(sys.argv[3])
        return tree, case, t, L
    
