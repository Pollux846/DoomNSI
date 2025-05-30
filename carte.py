from structure import Mur, Secteur
import config as C


piece = [Mur(400,100,200,300, 0), Mur(200,300,200,500, 1), Mur(200,500,400,700, 2), Mur(400,700,800,700, 3), Mur(800,700,1000,500, 4),
          Mur(1000,500,1000,300, 5), Mur(1000,300,800,100, 6), Mur(800,100,400,100, 7)]

piece2 = [Mur(200,300,150,300, 34), Mur(150,300,150,250, 35), Mur(150,250,200,150, 36), Mur(200,150,150,150, 37), Mur(150,150,50,250, 38),
          Mur(50,250,50,650, 39), Mur(50,650,150,750, 40), Mur(150,750,200,750, 41), Mur(200,750,150,650, 42), Mur(150,650,150,500, 43), Mur(150,500,200,500, 43), piece[1]]

pilier0 = [Mur(500,450,550,450, 8), Mur(550,450,550,500, 9), Mur(550,500,500,500, 10), Mur(500,500,500,450, 11)]
pilier1 = [Mur(400,500,450,500, 8), Mur(450,500,450,550, 9), Mur(450,550,400,550, 10), Mur(400,550,400,500, 11)]
pilier2 = [Mur(500,200,550,200, 12), Mur(550,200,550,250, 13), Mur(550,250,500,250, 14), Mur(500,250,500,200, 15)]
pilier3 = [Mur(800,400,850,400, 16), Mur(850,400,850,450, 17), Mur(850,450,800,450, 18), Mur(800,450,800,400, 19)]
pilier4 = [Mur(500,400,600,350, 20), Mur(600,350,650,400, 21), Mur(650,400,500,400, 22)]
pilier5 = [Mur(600,300,700,200, 23), Mur(700,200,750,220, 24), Mur(750,220,600,300, 25)]
pilier6 = [Mur(600,550,650,600, 26), Mur(650,600,750,500, 27), Mur(750,500,700,650, 28), Mur(700,650,650,650, 29), Mur(650,650,600,550, 30)]
pilier7 = [Mur(300,400,400,250, 31), Mur(400,250,420,270, 32), Mur(420,270,300,400, 33)]

class CARTE:
    def CARTE_1():
        secteur1_murs = pilier1 + pilier2 + pilier3 + pilier4 + pilier5 + pilier7 + piece

        secteur1 = Secteur(secteur1_murs, sol=-50, plafond=60, couleur=C.COULEUR.CYAN)
        secteur2 = Secteur(pilier6, sol=-50, plafond=20, couleur=C.COULEUR.ROUGE)
        secteur3 = Secteur(piece2, sol=-50, plafond=60, couleur=C.COULEUR.ORANGE)

        return secteur1.murs + secteur2.murs + secteur3.murs