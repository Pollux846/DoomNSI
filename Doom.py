# Séance 5 du 09/04/2024
# Création du module structure (classe Mur)

# pip install --force-reinstall -v "pyglet==1.5.28"

# module pyglet principal (qu'on nenomme en pg pour plus de simplicité)
import pyglet as pg
# import des fonctions trigo du module math
from math import cos, sin, pi
# modules du jeu
import joueur as J
import structure as S

# création de la fenêtre pour le plan 2D
# résolution : 320x200 pour le Doom de l'époque
window2d = pg.window.Window(1200, 800, "Plan 2D", vsync=True)
window3d = pg.window.Window(1200, 800, "Plan 3D", vsync=True)

# Création d'une instance de Joueur
joueur = J.Joueur(600,400,0)

# Création d'instances de Mur
murs = [S.Mur(400,100,800,100), S.Mur(800,100,1000,300), S.Mur(1000,300,1000,500), S.Mur(800,700,1000,500),
        S.Mur(400,700,800,700), S.Mur(200,500,400,700), S.Mur(200,300,200,500), S.Mur(200,300,400,100)
        ]
[mur.debug() for mur in murs]
[mur.tracer() for mur in murs]

# création du dico contenant les actions actives (True) ou inactives (False)
actions = { 'avancer': False, 'reculer': False,
            'tourner_gauche': False, 'tourner_droite': False, 'gauche': False, 'droite': False}

# détection d'un touche pressée au clavier
@window2d.event
def on_key_press(symbol, modifiers):
    # Touche Q : on quitte le jeu  
    if symbol == pg.window.key.ESCAPE: pg.app.exit()
    # touches de déplacement
    if symbol == pg.window.key.Z: actions['avancer'] = True
    if symbol == pg.window.key.S: actions['reculer'] = True
    if symbol == pg.window.key.Q: actions['gauche'] = True
    if symbol == pg.window.key.D: actions['droite'] = True
    # touches pour tourner
    if symbol == pg.window.key.LEFT: actions['tourner_gauche'] = True
    if symbol == pg.window.key.RIGHT: actions['tourner_droite'] = True
    
          
# détection d'un touche relâchée au clavier
@window2d.event
def on_key_release(symbol, modifiers):
    # touches de déplacement
    if symbol == pg.window.key.Z: actions['avancer'] = False
    if symbol == pg.window.key.S: actions['reculer'] = False
    if symbol == pg.window.key.Q: actions['gauche'] = False
    if symbol == pg.window.key.D: actions['droite'] = False
    # touches pour tourner
    if symbol == pg.window.key.LEFT: actions['tourner_gauche'] = False
    if symbol == pg.window.key.RIGHT: actions['tourner_droite'] = False

# évènement principal : rendu graphique
@window2d.event
def on_draw():
    window2d.clear()
    joueur.afficher()
    [mur.afficher() for mur in murs]

def update(dt):
    if actions['avancer']: joueur.avancer(joueur.PAS, joueur.a, murs)
    if actions['reculer']: joueur.avancer(-joueur.PAS, joueur.a, murs)
    if actions['gauche']: joueur.avancer(joueur.PAS, joueur.a+pi/2, murs)
    if actions['droite']: joueur.avancer(-joueur.PAS, joueur.a+pi/2, murs)
    if actions['tourner_gauche']: joueur.tourner(0.2)
    if actions['tourner_droite']: joueur.tourner(-0.2)
    if joueur.deplacement:
        joueur.tracer()
        joueur.deplacement = False

# boucle principale (30 Hz)
pg.clock.schedule_interval(update, 1/30.0)

# lancement du jeu
pg.app.run()