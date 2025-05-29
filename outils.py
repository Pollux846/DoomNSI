import pyglet as pg
import random

# Produit vectoriel (coordonnée z en 2D)
def calc_PV(u, v):
    return u[0]*v[1]-u[1]*v[0]

# Produit scalaire
def calc_PS(u, v):
    return u[0]*v[0] + u[1]*v[1]

# Vecteur entre 2 points
def calc_AB(A, B):
    return (B[0] - A[0], B[1] - A[1])

def random_color():
    return (random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))


def intersection(A, B, M, u, type=0):

    AB = (B[0]-A[0], B[1]-A[1])
    AM = (M[0]-A[0], M[1]-A[1])
    denom = calc_PV(AB, u)

    if denom == 0:
        return None
    
    t = calc_PV(AM, u) / denom
    s = calc_PV(AM, AB) / denom

    if type == 0:
        if 0 <= t <= 1:
            return (A[0] + t * AB[0], A[1] + t * AB[1])
    else:
        if 0 <= t <= 1 and s >= 0:
            return (A[0] + t * AB[0], A[1] + t * AB[1])
    
    return None



# batch avec ses références
class Dessin:
    def __init__(self):
        self.batch = pg.graphics.Batch()
        self.dessins = []

    def ajout(self, dessins):
        self.dessins.extend(dessins)

    def reset(self):
        self.dessins = []
        
    def dessiner(self):
        self.batch.draw()
