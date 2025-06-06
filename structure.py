# structure.py

import pyglet as pg
import outils as O
from math import sqrt

class Mur:
    def __init__(self, xA, yA, xB, yB, id, secteur_gauche=None, secteur_droit=None):
        self.id = id
        
        # Coordonnées des extrémités du mur
        self.x1, self.y1 = xA, yA
        self.x2, self.y2 = xB, yB
        self.A = (self.x1, self.y1)
        self.B = (self.x2, self.y2)

        # Etendue du mur (coordonnées du vecteur AB)
        self.dx = xB - xA
        self.dy = yB - yA

        # Longueur du mur
        self.l = sqrt(self.dx**2+self.dy**2)

        # Vecteur directeur (unitaire)
        self.u = (self.dx/self.l, self.dy/self.l)

        # Vecteur normale (unitaire) (orthogonal)
        self.N = (self.u[1], -self.u[0])

        # Batch pour affichage Pyglet
        self.dessin = O.Dessin()

        # Secteur
        self.secteur_gauche = secteur_gauche
        self.secteur_droit = secteur_droit
        self.is_portail = secteur_gauche and secteur_droit

    def tracer(self):
        # Affiche le mur comme un segment + son ID au milieu
        self.dessin.ajout([pg.shapes.Line(self.x1, self.y1, self.x2, self.y2, color=O.random_color(), batch=self.dessin.batch)])
        
        self.dessin.ajout([
            pg.text.Label(str(self.id),
                          self.x1 + self.dx//2, 
                          self.y1 + self.dy//2, 
                          color=(255, 255, 255, 255), 
                          font_name="Arial", 
                          batch=self.dessin.batch)
        ])

    def afficher(self):
        self.dessin.dessiner()
        
    def debug(self):
        print(f"Mur de {self.A} à {self.B}, longueur = {self.l}, u = {self.u}, n = {self.N}")

class Secteur:
    def __init__(self, murs, sol=0, plafond=0, couleur=(255, 255, 255)):
        self.murs = murs
        self.sol = sol
        self.plaf = plafond
        self.color = couleur

        for mur in murs:
            if mur.secteur_gauche == None:
                mur.secteur_gauche = self
            elif mur.secteur_droit == None:
                mur.secteur_droit = self
                mur.is_portail = mur.secteur_gauche and mur.secteur_droit
                mur.id = f"portail-{mur.id}"


class BSPnoeud:
    def __init__(self, murs):
        self.segment = murs[0]
        self.murs = murs[1:]
        self.droite = None
        self.gauche = None

    def partitionage(self, profondeur=1000):
        if profondeur <= 0 or self.murs == None:
            return

        droite = []
        gauche = []

        for mur in self.murs:

            t1 = O.calc_PV((self.segment.dx, self.segment.dy), (mur.x1 - self.segment.x1, mur.y1 - self.segment.y1))
            t2 = O.calc_PV((self.segment.dx, self.segment.dy), (mur.x2 - self.segment.x2, mur.y2 - self.segment.y2))

            if t1 * t2 < 0:
                p = O.intersection(mur.A, mur.B, self.segment.A, self.segment.u, 0)

                def PV_arrondi(a, b):
                    t = O.calc_PV(a, b)
                    return 0.0 if abs(t) < 1e-7 else t

                t3 = PV_arrondi((self.segment.dx, self.segment.dy), (mur.x1 - self.segment.x1, mur.y1 - self.segment.y1))
                t4 = PV_arrondi((self.segment.dx, self.segment.dy), (p[0] - self.segment.x2, p[1] - self.segment.y2))
                t5 = PV_arrondi((self.segment.dx, self.segment.dy), (p[0] - self.segment.x1, p[1] - self.segment.y1))
                t6 = PV_arrondi((self.segment.dx, self.segment.dy), (mur.x2 - self.segment.x2, mur.y2 - self.segment.y2))
        

                # Attention, la droite est toujours dans le sens du vecteur normale du segment
                if t3 > 0 or t4 > 0:
                    gauche.append(Mur(mur.x1, mur.y1, p[0], p[1], str(mur.id) + "g", mur.secteur_gauche, mur.secteur_droit))
                else:
                    droite.append(Mur(mur.x1, mur.y1, p[0], p[1], str(mur.id) + "d", mur.secteur_gauche, mur.secteur_droit))

                if t5 > 0 or t6 > 0:
                    gauche.append(Mur(p[0], p[1], mur.x2, mur.y2, str(mur.id) + "g", mur.secteur_gauche, mur.secteur_droit))
                else:
                    droite.append(Mur(p[0], p[1], mur.x2, mur.y2, str(mur.id) + "d", mur.secteur_gauche, mur.secteur_droit))

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

    def liste_mur(self, liste=[]):
        liste.append(self.segment)
        if self.droite:
            liste = self.droite.liste_mur(liste)
        if self.gauche:
            liste = self.gauche.liste_mur(liste)
        return liste
        