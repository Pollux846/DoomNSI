import pyglet as pg
# import des fonctions trigo du module math
from math import cos, sin, pi
# modules du jeu
import config as C
import random
from outils import *

class Except_Zneg(Exception):
    pass

class Rendu3D():
    def __init__(self, joueur):
        self.joueur = joueur
        # nouveau rendu ?
        self.nouveau = False
        # "batch" du rendu 3D
        self.quads = []
        self.lignes = []
        self.dessin = Dessin()
        self.dessin2 = Dessin()

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

    def rendu_segment(self, mur, indice, H_SOL, H_PLAF):

        if calc_PS(self.joueur.VG, mur.N) > 0 and calc_PS(self.joueur.VD, mur.N) > 0:
            return
        
        p1 = intersection(mur.A, mur.B, (self.joueur.x, self.joueur.y), self.joueur.VG, 1)
        p2 = intersection(mur.A, mur.B, (self.joueur.x, self.joueur.y), self.joueur.VD, 1)

        def abcd(X1, X2):
            a = self.projection(X1, H_SOL)
            b = self.projection(X1, H_PLAF)
            c = self.projection(X2, H_PLAF)
            d = self.projection(X2, H_SOL)
            return a,b,c,d, X1, X2

        try:
            if p1 and p2:
                a, b, c, d, A, B = abcd(p1, p2)

            elif p1:
                if calc_PS(mur.N, self.joueur.VG) < 0:
                    a, b, c, d, A, B = abcd(p1, mur.B)
                else:
                    a, b, c, d, A, B = abcd(mur.A, p1)

            elif p2:
                if calc_PS(mur.N, self.joueur.VD) < 0:
                    a, b, c, d, A, B = abcd(p2, mur.A)
                else:
                    a, b, c, d, A, B = abcd(mur.B, p2)

            else:
                N1 = (-self.joueur.VD[1], self.joueur.VD[0])
                N2 = (self.joueur.VG[1], -self.joueur.VG[0])
                t1 = calc_PS(N1, (mur.A[0] - self.joueur.x, mur.A[1] - self.joueur.y))
                t2 = calc_PS(N2, (mur.A[0] - self.joueur.x, mur.A[1] - self.joueur.y))

                if t1 > 0 and t2 > 0:
                    a, b, c, d, A, B = abcd(mur.A, mur.B)

                else: 
                    return
            
        except Except_Zneg:
            indice.append(mur.id)
            return

        var = calc_PS(mur.N, C.AFFICHAGE.V_S)
        color = list(map(lambda x: min(255, int(x*(1+var))), mur.color))
        self.quads.append((a,b,c,d, color))
        self.lignes.append((A, B))
        indice.append(mur.id)

    def calc_rendu3d(self, BSP, indice, quads, lignes):
        self.quads = quads
        self.lignes = lignes

        if BSP == None:
            return

        if BSP.droite == None and BSP.gauche == None:
           self.rendu_segment(BSP.segment, indice, BSP.segment.secteur[0], BSP.segment.secteur[1])
           return
        
        pv = calc_PV((BSP.segment.dx, BSP.segment.dy), (self.joueur.x - BSP.segment.x1, self.joueur.y - BSP.segment.y1))
        ps_g = calc_PS(BSP.segment.N, self.joueur.VG)
        ps_d = calc_PS(BSP.segment.N, self.joueur.VD)
        
        if pv > 0:
            if ps_g >= 0 or ps_d >= 0:
                self.calc_rendu3d(BSP.droite, indice, self.quads, self.lignes)
            self.rendu_segment(BSP.segment, indice, BSP.segment.secteur[0], BSP.segment.secteur[1])
            self.calc_rendu3d(BSP.gauche, indice, self.quads, self.lignes)
        
        elif pv < 0:
            if ps_g <= 0 or ps_d <= 0:
                self.calc_rendu3d(BSP.gauche, indice, self.quads, self.lignes)
            self.rendu_segment(BSP.segment, indice, BSP.segment.secteur[0], BSP.segment.secteur[1])
            self.calc_rendu3d(BSP.droite, indice, self.quads, self.lignes)

        else:
            self.calc_rendu3d(BSP.gauche, indice, quads, self.lignes)
            self.rendu_segment(BSP.segment, quads, indice, BSP.segment.secteur[0], BSP.segment.secteur[1])
            self.calc_rendu3d(BSP.droite, indice, quads, self.lignes)

    def tracer(self, dessin=1):
        if dessin == 1:
            self.dessin.reset()
            for (a,b,c,d, color) in self.quads:
                quad = [pg.shapes.Polygon(a,b,c,d, color=color, batch=self.dessin.batch)]
                self.dessin.ajout(quad)
        else:
            self.dessin2.reset()
            for mur in self.lignes:
                ligne = [pg.shapes.Line(mur[0][0], mur[0][1], mur[1][0], mur[1][1], color=(255, 255, 255, 255), batch=self.dessin2.batch)]
                self.dessin2.ajout(ligne)

    def afficher(self, dessin=1):
        if dessin == 1:
            self.dessin.dessiner()
        else:
            self.dessin2.dessiner()
