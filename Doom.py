# pip install --force-reinstall -v "pyglet==1.5.28"

# module pyglet principal (qu'on nenomme en pg pour plus de simplicité)
import pyglet as pg
# import des fonctions trigo du module math
from math import cos, sin, pi
# modules du jeu
import config as C
import joueur as J
import structure as S
import rendu3D as R
import carte as C

# création de la fenêtre pour le plan 2D et le rendu 3D
# résolution : 320x200 pour le Doom de l'époque
window3d = pg.window.Window(1100, 800, "Plan 3D", vsync=C.AFFICHAGE().V_SYNC)
window2d = pg.window.Window(1100, 800, "Plan 2D", vsync=C.AFFICHAGE().V_SYNC)

# Création d'une instance de Joueur
joueur = J.Joueur(300,250.1,0)

# Création d'instances de Mur
map = 

arbreBSP = S.BSPnoeud(map)
arbreBSP.partitionage(profondeur=1000)
print("")
arbreBSP.afficher_arbre()
print("")

window2d.switch_to()
[mur.debug() for mur in map]
[mur.tracer() for mur in map]

# Création d'une instance du rendu 3D
rendu_3d = R.rendu_3d(joueur)

# création du dico contenant les actions actives (True) ou inactives (False)
actions = { 'avancer': False, 'reculer': False,
            'tourner_gauche': False, 'tourner_droite': False, 'gauche': False, 'droite': False}

# détection d'un touche pressée au clavier
@window2d.event
def on_key_press(symbol, modifiers):
    # Touche Q : on quitte le jeu  
    if symbol in C.INTERFACE().T_QUITTER: 
        window2d.close()
        window3d.close()
        pg.app.exit()
    # touches de déplacement
    if symbol in C.JOUEUR().T_AVANCER: actions['avancer'] = True
    if symbol in C.JOUEUR().T_RECULER: actions['reculer'] = True
    if symbol in C.JOUEUR().T_STRAFE_G: actions['gauche'] = True
    if symbol in C.JOUEUR().T_STRAFE_D: actions['droite'] = True
    # touches pour tourner
    if symbol in C.JOUEUR().T_TOURNER_G: actions['tourner_gauche'] = True
    if symbol in C.JOUEUR().T_TOURNER_D: actions['tourner_droite'] = True
    
          
# détection d'un touche relâchée au clavier
@window2d.event
def on_key_release(symbol, modifiers):
    # touches de déplacement
    if symbol in C.JOUEUR().T_AVANCER: actions['avancer'] = False
    if symbol in C.JOUEUR().T_RECULER: actions['reculer'] = False
    if symbol in C.JOUEUR().T_STRAFE_G: actions['gauche'] = False
    if symbol in C.JOUEUR().T_STRAFE_D: actions['droite'] = False
    # touches pour tourner
    if symbol in C.JOUEUR().T_TOURNER_G: actions['tourner_gauche'] = False
    if symbol in C.JOUEUR().T_TOURNER_D: actions['tourner_droite'] = False

# évènement principal : rendu graphique
@window2d.event
def on_draw():
    window2d.clear()
    [mur.afficher() for mur in map]
    joueur.afficher()
    
@window3d.event
def on_draw():
    window3d.clear()
    rendu_3d.afficher()
    
# trace tous les éléments dans la bonne fenêtre
def tracer():
    window2d.switch_to()
    joueur.tracer()
    window3d.switch_to()
    rendu_3d.tracer()

# boucle principale
def update(dt):
    # actions du joueur
    if actions['avancer']: joueur.avancer(joueur.PAS, joueur.a, map)
    if actions['reculer']: joueur.avancer(-joueur.PAS, joueur.a, map)
    if actions['gauche']: joueur.avancer(joueur.PAS, joueur.a+pi/2, map)
    if actions['droite']: joueur.avancer(-joueur.PAS, joueur.a+pi/2, map)
    if actions['tourner_gauche']: joueur.tourner(joueur.ROT)
    if actions['tourner_droite']: joueur.tourner(-joueur.ROT)
    # rendu 3D
    rendu_3d.calc_rendu3d(arbreBSP, [], [])
    tracer()

# boucle principale (30 Hz)
pg.clock.schedule_interval(update, interval=C.MOTEUR().FPS)

# version de pyglet
print("Version de Pyglet : ",pg.version)
# lancement du jeu
pg.app.run()