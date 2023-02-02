import numpy as np

def mk_adj(fname):
    with open(fname, 'r') as f:
        lines= f.readlines()
    ln = []
    dim = 0
    for idx,l in enumerate(lines):
        if l.startswith( "EDGE_LENGTH_SECTION"):
            ln = lines[idx:]
        if l.startswith("DIMENSION:"):
            dim = int(l[len("DIMENSION:"):])
    ln = ln[1:-1]
    adj = np.zeros((dim,dim))
    for l in ln:
        x= l[:-1].strip().split(" ")
        adj[int(x[0])-1,int(x[1])-1] = int(x[2])
    return adj + adj.T



def mk_adj_from_coords(fname):
    with open(fname, 'r') as f:
        lines= f.readlines()
    ln = []
    dim = 0
    for idx,l in enumerate(lines):
        if l.startswith( "NODE_COORD_SECTION"):
            ln = lines[idx:]
        if l.startswith("DIMENSION:"):
            dim = int(l[len("DIMENSION:"):])
    ln = ln[1:-1]
    adj = np.zeros((dim,dim))
    print("dim", dim)
    for l in ln:
        x= l[:-1].strip().split(" ")
        for l in ln:
            y= l[:-1].strip().split(" ")
            adj[int(x[0])-1,int(y[0])-1] = ((float(x[2])-float(y[2]))**2 + (float(x[1])-float(y[1]))**2)**(1/2)
    return adj + adj.T