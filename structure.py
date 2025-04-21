# module pyglet principal (qu'on nenomme en pg pour plus de simplicité)
import pyglet as pg
from outils import *
# outils mathématiques
from math import sqrt

class Mur:
    def __init__(self, xA, yA, xB, yB, color):
        self.color = color
        # un mur est un segment 2D entre deux points
        self.x1, self.y1 = xA, yA
        self.x2, self.y2 = xB, yB
        self.A = (self.x1, self.y1)
        self.B = (self.x2, self.y2)
        # étendue du mur (coordonnées du vecteur AB)
        self.dx = xB - xA
        self.dy = yB - yA
        # longueur du mur
        self.l = sqrt(self.dx**2+self.dy**2)
        # vecteur directeur (unitaire)
        self.u = (self.dx/self.l, self.dy/self.l)
        # vecteur orthogonal (unitaire)
        self.N = (self.u[1], -self.u[0])
        # "batch" du mur
        self.dessin = Dessin()

    def tracer(self):
        # le mur comme un segment
        self.dessin.ajout([pg.shapes.Line(self.x1,self.y1,self.x2,self.y2, batch=self.dessin.batch)])

    def afficher(self):
        self.dessin.dessiner()
        
    def debug(self):
        print("Mur ({},{})->({},{})".format(self.x1,self.y1,self.x2,self.y2))
        print("-> longueur l :", self.l)
        print("-> étendue dx et dy :",self.dx,",",self.dy)
        print("-> vecteur directeur u :",self.u)
        print("-> vecteur orthogonal N :",self.N)
        