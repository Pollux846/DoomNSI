# Séance 4 du 13/02/2024
# création du module joueur

# module pyglet principal (qu'on nenomme en pg pour plus de simplicité)
import pyglet as pg
# import des fonctions trigo du module math
from math import *
from outils import *

class Joueur: # la classe Joueur
    def __init__(self, x, y, a):
        # position et angle
        self.x = x
        self.y = y
        self.a = a
        self.deplacement = True
        self.PAS = 10
        self.V = (cos(self.a), sin(self.a))
        self.PROFONDEUR = 1
        # "batch" du joueur
        self.batch = pg.graphics.Batch()
        self.dessin = {}
    def avancer(self, pas, a, murs):
        x = self.x + pas*cos(a)
        y = self.y + pas*sin(a)
        collision = self.test_collision(murs, (x,y))
        #collision mur
        if collision:
            MP = calc_AB((self.x, self.y), (x, y))
            k = calc_PS(MP, collision.u)
            x = self.x+k*collision.u[0]
            y = self.y+k*collision.u[1]
            collision = self.test_collision(murs, (x,y))
        if not collision:
            self.x, self.y = x, y
            #print("-", end="")
            self.deplacement = True

    def tourner(self, angle):
        self.a += angle
        self.deplacement = True
    def tracer(self):
        # le joueur comme un cercle
        self.dessin['corps'] = pg.shapes.Circle(self.x, self.y, 10, color =(50, 225, 30), batch = self.batch)
        # segment "vecteur vitesse" qui pointe vers la direction de visée
        self.dessin['visée'] = pg.shapes.Line(self.x, self.y, self.x + 20*cos(self.a), self.y + 20*sin(self.a), batch = self.batch)
    def afficher(self):
        self.batch.draw()
        
    def test_collision(self, murs, P):
        MP = calc_AB((self.x, self.y), P)
        for mur in murs:
            AB = (mur.dx, mur.dy)
            AM = calc_AB((mur.x1, mur.y1), (self.x, self.y))
            AP = calc_AB((mur.x1, mur.y1), P)
            pv1, pv2 = calc_PV(AB, AM), calc_PV(AB, AP)
            test1 = (pv1<0 and pv2>0) or (pv1>0 and pv2<0)
            
            MA = calc_AB((self.x, self.y), (mur.x1, mur.y1))
            MB = calc_AB((self.x, self.y), (mur.x2, mur.y2))
            pv1, pv2 = calc_PV(MP, MA), calc_PV(MP, MB)
            test2 = (pv1<=0 and pv2>=0) or (pv1>=0 and pv2<=0)
            
            if test1 and test2:
                return mur
        
        return False
                       
            
            
        
        
        