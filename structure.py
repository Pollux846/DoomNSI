# module pyglet principal (qu'on nenomme en pg pour plus de simplicité)
import pyglet as pg
import outils as O
# outils mathématiques
from math import sqrt

class Mur:
    def __init__(self, xA, yA, xB, yB, color, id):
        self.color = color
        self.id = id
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
        self.dessin = O.Dessin()

    def tracer(self):
        # le mur comme un segment
        self.dessin.ajout([pg.shapes.Line(self.x1,self.y1,self.x2,self.y2, batch=self.dessin.batch)])
        self.dessin.ajout([pg.text.Label(str(self.id), self.x1 + self.dx//2, self.y1 + self.dy//2, color=(255, 255, 255, 255), batch=self.dessin.batch)])

    def afficher(self):
        self.dessin.dessiner()
        
    def debug(self):
        print("Mur ({},{})->({},{})".format(self.x1,self.y1,self.x2,self.y2))
        print("-> longueur l :", self.l)
        print("-> étendue dx et dy :",self.dx,",",self.dy)
        print("-> vecteur directeur u :",self.u)
        print("-> vecteur orthogonal N :",self.N)


class BSPnoeud:
    def __init__(self, murs):
        self.segment = murs[0]
        self.murs = murs[1:]
        self.droite = None
        self.gauche = None

    def partitionage(self, profondeur):
        if profondeur < 0 or self.murs == None:
            return

        droite = []
        gauche = []
    
        p1 = (int(self.segment.x1 - 10000 * self.segment.u[0]), int(self.segment.y1 - 10000 * self.segment.u[1]))
        p2 = (int(self.segment.x2 + 10000 * self.segment.u[0]), int(self.segment.y2 + 10000 * self.segment.u[1]))

        for mur in self.murs:

            t1 = O.calc_PV((self.segment.dx, self.segment.dy), (mur.x1 - self.segment.x1, mur.y1 - self.segment.y1))
            t2 = O.calc_PV((self.segment.dx, self.segment.dy), (mur.x2 - self.segment.x2, mur.y2 - self.segment.y2))

            if t1 * t2 < 0:
                p = O.intersection(mur.A, mur.B, self.segment.A, self.segment.B)

                def PV_arrondi(a, b):
                    t = O.calc_PV(a, b)
                    return 0.0 if abs(t) < 1e-7 else t

                t3 = PV_arrondi((self.segment.dx, self.segment.dy), (mur.x1 - self.segment.x1, mur.y1 - self.segment.y1))
                t4 = PV_arrondi((self.segment.dx, self.segment.dy), (p[0] - self.segment.x2, p[1] - self.segment.y2))
                t5 = PV_arrondi((self.segment.dx, self.segment.dy), (p[0] - self.segment.x1, p[1] - self.segment.y1))
                t6 = PV_arrondi((self.segment.dx, self.segment.dy), (mur.x2 - self.segment.x2, mur.y2 - self.segment.y2))
        

                # Attention, la droite est toujours dans le sens du vecteur normale du segment
                if t3 > 0 or t4 > 0:
                    gauche.append(Mur(mur.x1, mur.y1, p[0], p[1], mur.color, str(mur.id) + "g"))
                else:
                    droite.append(Mur(mur.x1, mur.y1, p[0], p[1], mur.color, str(mur.id) + "d"))

                if t5 > 0 or t6 > 0:
                    gauche.append(Mur(p[0], p[1], mur.x2, mur.y2, mur.color, str(mur.id) + "g"))
                else:
                    droite.append(Mur(p[0], p[1], mur.x2, mur.y2, mur.color, str(mur.id) + "d"))

            elif t1 > 0 or t2 > 0:
                gauche.append(mur)

            else:
                droite.append(mur)

        if droite:
            self.droite = BSPnoeud(droite)
            self.droite.partitionage(profondeur-1)

        if gauche:
            self.gauche = BSPnoeud(gauche)
            self.gauche.partitionage(profondeur-1)
    
    def afficher_arbre(self, profondeur=0):
        print("  " * profondeur + f"{profondeur}: {self.segment.A} -> {self.segment.B} [{self.segment.id}]")
        if self.droite:
            self.droite.afficher_arbre(profondeur + 1)
        if self.gauche:
            self.gauche.afficher_arbre(profondeur + 1)
        