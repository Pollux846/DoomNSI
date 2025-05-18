import pyglet as pg
# import des fonctions trigo du module math
from math import cos, sin, pi
# modules du jeu
import config as C
import random
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
        if Z <= 0:
            raise(Except_Zneg)
        k = Z / C.AFFICHAGE().D_Z
        # calcul des coordonnées de projection
        X = calc_PV(MP, self.joueur.V) / k + C.AFFICHAGE().DX_RES
        Y = h / k + C.AFFICHAGE().DY_RES
        return (X,Y)

    def rendu_segment(self, segment, indice, H_SOL, H_PLAF):
        try:
            a = self.projection(segment.A, H_SOL)
            b = self.projection(segment.A, H_PLAF)
            c = self.projection(segment.B, H_PLAF)
            d = self.projection(segment.B, H_SOL)
        except Except_Zneg:
            indice.append(segment.id)
            return

        var = calc_PS(segment.N, C.AFFICHAGE.V_S)
        color = list(map(lambda x: min(255, int(x*(1+var))), segment.color))
        self.quads.append((a,b,c,d, color))
        indice.append(segment.id)

    def calc_rendu3d(self, BSP, indice, quads):
        H_SOL, H_PLAF = -50, 60
        # reset
        self.quads = quads

        if BSP == None:
            return

        if BSP.droite == None and BSP.gauche == None:
           self.rendu_segment(BSP.segment, indice, H_SOL, H_PLAF)
           return
        
        pv = calc_PV((BSP.segment.dx, BSP.segment.dy), (self.joueur.x - BSP.segment.x1, self.joueur.y - BSP.segment.y1))
        
        if pv > 0:
            self.calc_rendu3d(BSP.droite, indice, self.quads)
            self.rendu_segment(BSP.segment, indice, H_SOL, H_PLAF)
            self.calc_rendu3d(BSP.gauche, indice, self.quads)
        
        elif pv < 0:
            self.calc_rendu3d(BSP.gauche, indice, self.quads)
            self.rendu_segment(BSP.segment, indice, H_SOL, H_PLAF)
            self.calc_rendu3d(BSP.droite, indice, self.quads)

        else:
            self.calc_rendu3d(BSP.gauche, indice, quads)
            self.rendu_segment(BSP.segment, quads, indice, H_SOL, H_PLAF)
            self.calc_rendu3d(BSP.droite, indice, quads)

    def tracer(self):
        self.dessin.reset()
        for (a,b,c,d, color) in self.quads:
            r = random.randint(1, 255)
            quad = [pg.shapes.Polygon(a,b,c,d, color=color, batch=self.dessin.batch)]
            self.dessin.ajout(quad)

    def afficher(self):
        self.dessin.dessiner()