# fichier de configuration
# -> définit les variables statiques (constantes) pour le jeu
# -> une classe par catégorie pour ne pas tout mélanger

import pyglet.window.key as keys
from math import tan, radians

# CONSTANTES RELATIVES A L'INTERFACE
class INTERFACE():
	# touches pour quitter
	T_QUITTER = [keys.ESCAPE, keys.X]

# CONSTANTES RELATIVES A L'AFFICHAGE
class AFFICHAGE():
	# résolution
	X_RES, Y_RES = 1100, 800
	# coordonnées du centre
	DX_RES, DY_RES = X_RES//2, Y_RES//2
	# Synchronisation du rafraîchissement d'écran
	V_SYNC = True
	# Distance à l'écran virtuel de projection
	ANGLE_VISION = radians(80)
	D_A = ANGLE_VISION/2
	D_Z = (X_RES/2)/tan(ANGLE_VISION/2)
	V_S = (0.4, 0)

# CONSTANTES RELATIVES AU JOUEUR
class JOUEUR():
	# vitesses de translation et rotation
	PAS = 10.0
	ROT = 0.2
	# touches pour déplacement
	T_AVANCER = [keys.UP, keys.Z]
	T_RECULER = [keys.DOWN, keys.S]
	T_TOURNER_G = [keys.LEFT]
	T_TOURNER_D = [keys.RIGHT]
	T_STRAFE_G = [keys.Q]
	T_STRAFE_D = [keys.D]

# CONSTANTES RELATIVES AU MOTEUR
class MOTEUR():
	# taux de rafraîchissement des mises à jour
	FPS = 1/30.0
	
class COULEUR():
	BLEU = (59, 156, 198)
	ROUGE = (222, 31, 31)
	ORANGE = (254, 127, 1)
	VIOLET = (171, 11, 218)
	VERT = (15, 126, 29)
	ROSE = (238, 119, 236)
	CYAN = (60, 240, 240)
	JAUNE = (254, 254, 1)