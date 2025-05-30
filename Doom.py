# pip install --force-reinstall -v "pyglet==1.5.28"
# Doom.py

import pyglet as pg
from math import cos, sin, pi
import config as C
import joueur as J
import structure as S
import rendu3D as R
import carte as CA

# Fenêtres 2D et 3D
window3d = pg.window.Window(C.AFFICHAGE.X_RES, C.AFFICHAGE.Y_RES, "Plan 3D", vsync=C.AFFICHAGE().V_SYNC)
window2d = pg.window.Window(C.AFFICHAGE.X_RES, C.AFFICHAGE.Y_RES, "Plan 2D", vsync=C.AFFICHAGE().V_SYNC)
window2d_2 = pg.window.Window(C.AFFICHAGE.X_RES, C.AFFICHAGE.Y_RES, "Plan 2D_réactif", vsync=C.AFFICHAGE().V_SYNC)

# Création d'une instance de Joueur
joueur = J.Joueur(300, 250.1, 0)

# Chargement de la carte et construction de l'arbre BSP
carte = CA.CARTE
arbreBSP = S.BSPnoeud(carte.CARTE_1())
arbreBSP.partitionage(profondeur=1000)
murs = arbreBSP.liste_mur()

print("\nArbre BSP généré :")
arbreBSP.afficher_arbre()
print("")

# Affichage des murs en debug dans la fenêtre 2D
window2d.switch_to()
for mur in murs:
    mur.debug()
    mur.tracer()

# Création d'une instance du rendu 3D
rendu_3d = R.Rendu3D(joueur)

# Création du dico contenant les actions actives (True) ou inactives (False)
actions = {
    'avancer': False,
    'reculer': False,
    'tourner_gauche': False,
    'tourner_droite': False, 
    'gauche': False, 
    'droite': False
}

# Gestion clavier
@window2d.event
def on_key_press(symbol, modifiers): # Détection d'une touche pressée
    if symbol in C.INTERFACE().T_QUITTER: # Touche Q: on quitte le jeu  
        window2d.close()
        window2d_2.close()
        window3d.close()
        pg.app.exit()
    # Touches de déplacement
    if symbol in C.JOUEUR().T_AVANCER: actions['avancer'] = True
    if symbol in C.JOUEUR().T_RECULER: actions['reculer'] = True
    if symbol in C.JOUEUR().T_STRAFE_G: actions['gauche'] = True
    if symbol in C.JOUEUR().T_STRAFE_D: actions['droite'] = True
    # Touches pour tourner
    if symbol in C.JOUEUR().T_TOURNER_G: actions['tourner_gauche'] = True
    if symbol in C.JOUEUR().T_TOURNER_D: actions['tourner_droite'] = True
    
@window2d.event
def on_key_release(symbol, modifiers): # Détection d'une touche relachée
    # Touches de déplacement
    if symbol in C.JOUEUR().T_AVANCER: actions['avancer'] = False
    if symbol in C.JOUEUR().T_RECULER: actions['reculer'] = False
    if symbol in C.JOUEUR().T_STRAFE_G: actions['gauche'] = False
    if symbol in C.JOUEUR().T_STRAFE_D: actions['droite'] = False
    # Touches pour tourner
    if symbol in C.JOUEUR().T_TOURNER_G: actions['tourner_gauche'] = False
    if symbol in C.JOUEUR().T_TOURNER_D: actions['tourner_droite'] = False

# Rendu 2D
@window2d.event
def on_draw():
    window2d.clear()
    [mur.afficher() for mur in murs]
    joueur.afficher(1)

# Rendu 2D dynamique
@window2d_2.event
def on_draw():
    window2d_2.clear()
    joueur.afficher(2)
    rendu_3d.afficher(2)

# Rendu 3D
@window3d.event
def on_draw():
    window3d.clear()
    rendu_3d.afficher(1)
    
# Tracer tous les éléments graphiques
def tracer():
    window2d.switch_to()
    joueur.tracer(1)
    window2d_2.switch_to()
    joueur.tracer(2)
    rendu_3d.tracer(2)
    window3d.switch_to()
    rendu_3d.tracer(1)

# Mise à jour des actions du joueur
def update(dt):
    if actions['avancer']: joueur.avancer(joueur.PAS, joueur.a, murs)
    if actions['reculer']: joueur.avancer(-joueur.PAS, joueur.a, murs)
    if actions['gauche']: joueur.avancer(joueur.PAS, joueur.a+pi/2, murs)
    if actions['droite']: joueur.avancer(-joueur.PAS, joueur.a+pi/2, murs)
    if actions['tourner_gauche']: joueur.tourner(joueur.ROT)
    if actions['tourner_droite']: joueur.tourner(-joueur.ROT)
    rendu_3d.calc_rendu3d(arbreBSP, [], [], [])
    tracer()

# Boucle principale (30 Hz)
pg.clock.schedule_interval(update, interval=C.MOTEUR().FPS)

if __name__ == "__main__":
    print("Version de Pyglet : ",pg.version)
    pg.app.run()