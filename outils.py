def calc_PV(u, v):
    return u[0]*v[1]-u[1]*v[0]

def calc_PS(u, v):
    return u[0]*v[0] + u[1]*v[1]

def calc_AB(A, B):
    return (B[0] - A[0], B[1] - A[1])