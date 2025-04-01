# fichier de configuration
# -> définit les variables statiques (constantes) pour le jeu
# -> une classe par catégorie pour ne pas tout mélanger

import pyglet.window.key as keys

# CONSTANTES RELATIVES A L'INTERFACE
class INTERFACE():
	# touches pour quitter
	T_QUITTER = [keys.ESCAPE, keys.X]

# CONSTANTES RELATIVES A L'AFFICHAGE
class AFFICHAGE():
	# résolution
	X_RES, Y_RES = 640, 480
	# coordonnées du centre
	DX_RES, DY_RES = X_RES//2, Y_RES//2
	# Synchronisation du rafraîchissement d'écran
	V_SYNC = True
	# Distance à l'écran virtuel de projection
	D_Z = 500.

# CONSTANTES RELATIVES AU JOUEUR
class JOUEUR():
	# vitesses de translation et rotation
	PAS, ROT = 10.0, 0.2
	# touches pour déplacement
	T_AVANCER, T_RECULER = [keys.UP, keys.Z], [keys.DOWN, keys.S]
	T_TOURNER_G, T_TOURNER_D = [keys.LEFT], [keys.RIGHT]
	T_STRAFE_G, T_STRAFE_D = [keys.Q], [keys.D]

# CONSTANTES RELATIVES AU MOTEUR
class MOTEUR():
	# taux de rafraîchissement des mises à jour
	FPS = 1/30.