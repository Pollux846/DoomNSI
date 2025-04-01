import pyglet as pg
# import des fonctions trigo du module math
from math import cos, sin, pi
# modules du jeu
import config as C
import joueur as J
import structure as S
from outils import *

class Except_Zneg(Exception):
    pass

class rendu_3d():
    def __init__(self, joueur):
        self.joueur = joueur
        # nouveau rendu ?
        self.nouveau = False
        # "batch" du rendu 3D
        self.quads = [] 
        self.dessin = Dessin()

    def projection(self, P, h):
        # calcul du coefficient de Thalès
        MP = calc_AB(self.joueur.position(), P)
        Z = calc_PS(MP, self.joueur.V)
        if Z < 0:
            raise Except_Zneg("Le mur est derriere le joueur")
        k = C.AFFICHAGE().D_Z / Z  
        # calcul des coordonnées de projection
        X = calc_PV(MP, self.joueur.V) * k + C.AFFICHAGE().DX_RES
        Y = h * k + C.AFFICHAGE().DY_RES
        return (X,Y)

    def calc_rendu3d(self, murs):
        H_SOL, H_PLAF = 0, 100
        # reset
        self.quads = []
        for mur in murs:
            try:
                A = self.projection(mur.A, H_SOL)
                B = self.projection(mur.A, H_PLAF)
                C = self.projection(mur.B, H_PLAF)
                D = self.projection(mur.B, H_SOL)
            except Except_Zneg:
                continue
            self.quads.append((A,B,C,D))

    def tracer(self):
        self.dessin.reset()
        for (A,B,C,D) in self.quads:
            quad = [pg.shapes.Line(A[0],A[1],B[0],B[1], batch = self.dessin.batch),
                    pg.shapes.Line(B[0],B[1],C[0],C[1], batch = self.dessin.batch),
                    pg.shapes.Line(C[0],C[1],D[0],D[1], batch = self.dessin.batch),
                    pg.shapes.Line(D[0],D[1],A[0],A[1], batch = self.dessin.batch)]
            self.dessin.ajout(quad)

    def afficher(self):
        self.dessin.dessiner()