# pip install --force-reinstall -v "pyglet==1.5.28"

import pyglet as pg
from math import cos, sin, pi
import config as C
import joueur as J
import structure as S
import rendu3D as R
import carte as CA

# Création de la fenêtre pour le plan 2D et le rendu 3D
window3d = pg.window.Window(1100, 800, "Plan 3D", vsync=C.AFFICHAGE().V_SYNC)
window2d = pg.window.Window(1100, 800, "Plan 2D", vsync=C.AFFICHAGE().V_SYNC)
window2d_2 = pg.window.Window(1100, 800, "Plan 2D_réactif", vsync=C.AFFICHAGE().V_SYNC)

# Création d'une instance de Joueur
joueur = J.Joueur(300,250.1,0)

# Carte -> Arbre BSP -> Liste de murs
map = CA.CARTE.CARTE_1
arbreBSP = S.BSPnoeud(map)
arbreBSP.partitionage(profondeur=1000)
murs = arbreBSP.liste_mur()

print("\nArbre BSP généré :")
arbreBSP.afficher_arbre()
print("")

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

# détection d'un touche pressée au clavier
@window2d.event
def on_key_press(symbol, modifiers):
    # Touche Q : on quitte le jeu  
    if symbol in C.INTERFACE().T_QUITTER: 
        window2d.close()
        #window2d_2.close()
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
    [mur.afficher() for mur in murs]
    joueur.afficher(1)

@window2d_2.event
def on_draw():
    window2d_2.clear()
    joueur.afficher(2)
    rendu_3d.afficher(2)
    
@window3d.event
def on_draw():
    window3d.clear()
    rendu_3d.afficher(1)
    
# trace tous les éléments dans la bonne fenêtre
def tracer():
    window2d.switch_to()
    joueur.tracer(1)
    window2d_2.switch_to()
    joueur.tracer(2)
    rendu_3d.tracer(2)
    window3d.switch_to()
    rendu_3d.tracer(1)

# boucle principale
def update(dt):
    # actions du joueur
    if actions['avancer']: joueur.avancer(joueur.PAS, joueur.a, murs)
    if actions['reculer']: joueur.avancer(-joueur.PAS, joueur.a, murs)
    if actions['gauche']: joueur.avancer(joueur.PAS, joueur.a+pi/2, murs)
    if actions['droite']: joueur.avancer(-joueur.PAS, joueur.a+pi/2, murs)
    if actions['tourner_gauche']: joueur.tourner(joueur.ROT)
    if actions['tourner_droite']: joueur.tourner(-joueur.ROT)
    # rendu 3D
    rendu_3d.calc_rendu3d(arbreBSP, [], [], [])
    tracer()

# boucle principale (30 Hz)
pg.clock.schedule_interval(update, interval=C.MOTEUR().FPS)

if __name__ == "__main__":
    # version de pyglet
    print("Version de Pyglet : ",pg.version)
    # lancement du jeu
    pg.app.run()