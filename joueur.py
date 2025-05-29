import pyglet as pg
from math import *
from outils import *
import config as C

class Joueur:
    def __init__(self, x, y, a):
        # position et angle
        self.x = x
        self.y = y
        self.a = a
        # Deltas de déplacement et rotation
        self.PAS = C.JOUEUR.PAS
        self.ROT = C.JOUEUR.ROT
        # Vecteurs unitaires de visée
        self.calc_V()
        # "batch" du joueur
        self.dessin1 = Dessin()
        self.dessin2 = Dessin()
        # Booléen de déplacement
        self.deplacement = True
        
    def calc_V(self):
        self.V = (cos(self.a), sin(self.a))
        self.VG = (cos(self.a+C.AFFICHAGE.D_A), sin(self.a+C.AFFICHAGE.D_A))
        self.VD = (cos(self.a-C.AFFICHAGE.D_A), sin(self.a-C.AFFICHAGE.D_A))
    
    def position(self):
        return (self.x, self.y)

    def avancer(self, pas, a, murs):
        x = self.x + pas*cos(a)
        y = self.y + pas*sin(a)
        
        collision = self.test_collision(murs, (x,y))

        #collision mur
        if collision:
            # calculer la glissage
            MP = calc_AB(self.position(), (x, y))
            k = calc_PS(MP, collision.u)
            x = self.x + k*collision.u[0]
            y = self.y + k*collision.u[1]
            # et retester la collision (peut être un coin !)
            collision = self.test_collision(murs, (x,y))

        if not collision: # aucune collision
            self.x, self.y = x, y
            self.deplacement = True

    def tourner(self, angle):
        self.a += angle
        self.calc_V()
        self.deplacement = True

    # mémorise les tracés du joueur (batch)
    def tracer(self, dessin=1):
        if dessin == 1:
            dessins = [
            # le joueur comme un cercle
            pg.shapes.Circle(self.x, self.y, 10, color =(50, 225, 30), batch = self.dessin1.batch),
            # segment "vecteur vitesse" qui pointe vers la direction de visée
            pg.shapes.Line(self.x, self.y, self.x + 20*cos(self.a), self.y + 20*sin(self.a), batch = self.dessin1.batch),
            pg.shapes.Line(self.x, self.y, self.x + 200*cos(self.a+C.AFFICHAGE.D_A), self.y + 200*sin(self.a+C.AFFICHAGE.D_A), color=(255, 0, 0), batch = self.dessin1.batch),
            pg.shapes.Line(self.x, self.y, self.x + 200*cos(self.a-C.AFFICHAGE.D_A), self.y + 200*sin(self.a-C.AFFICHAGE.D_A), color=(255, 0, 0), batch = self.dessin1.batch)
        ]
            self.dessin1.reset()
            self.dessin1.ajout(dessins)
        else:
            dessins = [
            # le joueur comme un cercle
            pg.shapes.Circle(self.x, self.y, 10, color =(50, 225, 30), batch = self.dessin2.batch),
            # segment "vecteur vitesse" qui pointe vers la direction de visée
            pg.shapes.Line(self.x, self.y, self.x + 20*cos(self.a), self.y + 20*sin(self.a), batch = self.dessin2.batch),
            pg.shapes.Line(self.x, self.y, self.x + 200*cos(self.a+C.AFFICHAGE.D_A), self.y + 200*sin(self.a+C.AFFICHAGE.D_A), color=(255, 0, 0), batch = self.dessin2.batch),
            pg.shapes.Line(self.x, self.y, self.x + 200*cos(self.a-C.AFFICHAGE.D_A), self.y + 200*sin(self.a-C.AFFICHAGE.D_A), color=(255, 0, 0), batch = self.dessin2.batch)
        ]
            self.dessin2.reset()
            self.dessin2.ajout(dessins)


    
    # dessine le joueur (batch)
    def afficher(self, dessin=1):
        if dessin == 1:
            self.dessin1.dessiner()
        else:
            self.dessin2.dessiner()

    # test de collision : renvoie le mur concerné (False sinon)       
    def test_collision(self, murs, P):
        # vecteur déplacement du jouer
        MP = calc_AB(self.position(), P)
        for mur in murs:
            AB = (mur.dx, mur.dy)
            # test 1 : Le joueur traverse-t-il (segment) la direction du mur (droite) ?
            AM = calc_AB(mur.A, self.position())
            AP = calc_AB(mur.A, P)
            pv1, pv2 = calc_PV(AB, AM), calc_PV(AB, AP)
            test1 = (pv1<0 and pv2>0) or (pv1>0 and pv2<0)
            # test 2 : La direction du joueur (droite) traverse-t-elle le mur (segment) ?
            MA = calc_AB(self.position(), mur.A)
            MB = calc_AB(self.position(), mur.B)
            pv1, pv2 = calc_PV(MP, MA), calc_PV(MP, MB)
            test2 = (pv1<=0 and pv2>=0) or (pv1>=0 and pv2<=0)
            
            if test1 and test2:
                # les segments ont une intersection : collision 
                return mur
        return False
                       
            
            
        
        
        