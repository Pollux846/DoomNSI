# config.py - Configuration centralisée pour le moteur DoomNSI
# Ce fichier contient uniquement des constantes organisées par thématiques

import pyglet.window.key as keys
from math import tan, radians

# Paramètres d'interface utilisateur
class INTERFACE():
	T_QUITTER = [keys.ESCAPE, keys.X] # Touches pour quitter

# Paramètres d'affichage
class AFFICHAGE():
	X_RES, Y_RES = 1100, 800
	DX_RES, DY_RES = X_RES//2, Y_RES//2
	V_SYNC = True
	ANGLE_VISION = radians(90)
	D_A = ANGLE_VISION/2
	D_Z = (X_RES/2)/tan(ANGLE_VISION/2)
	V_S = (0.4, 0)

# Paramètres du joueur
class JOUEUR():
	PAS = 10.0 	# Vitesse de déplacement
	ROT = 0.2 	# Vitesse de rotation (en radians)

	T_AVANCER    = [keys.UP, keys.Z]
	T_RECULER    = [keys.DOWN, keys.S]
	T_TOURNER_G  = [keys.LEFT]
	T_TOURNER_D  = [keys.RIGHT]
	T_STRAFE_G   = [keys.Q]
	T_STRAFE_D   = [keys.D]

# Paramètres du moteur
class MOTEUR():
	FPS = 1/30.0 # Fréquence de mise à jour

# Palette de couleurs utilisables
class COULEUR():
	BLEU    = (59, 156, 198)
	ROUGE   = (222, 31, 31)
	ORANGE  = (254, 127, 1)
	VIOLET  = (171, 11, 218)
	VERT    = (15, 126, 29)
	ROSE    = (238, 119, 236)
	CYAN    = (60, 240, 240)
	JAUNE   = (254, 254, 1)