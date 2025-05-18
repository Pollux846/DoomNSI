# Module d'outils divers
from turtle import position
import pyglet as pg

# produit vectoriel (coordonnée z)
def calc_PV(u, v):
    return u[0]*v[1]-u[1]*v[0]

# produit scalaire
def calc_PS(u, v):
    return u[0]*v[0] + u[1]*v[1]

# vecteur entre 2 points
def calc_AB(A, B):
    return (B[0] - A[0], B[1] - A[1])

def intersection(A, B, C, D):
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C
    x4, y4 = D

    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x4 - x3
    dy2 = y4 - y3

    denom = dx1 * dy2 - dy1 * dx2

    t = ((x3 - x1) * dy2 - (y3 - y1) * dx2) / denom

    if 0 <= t <= 1:
        inter_x = x1 + t * dx1
        inter_y = y1 + t * dy1
        return (inter_x, inter_y)
    else:
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
