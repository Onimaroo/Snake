from upemtk import *
from time import sleep
from random import randint

#Diagne Ben 

# dimensions du jeu ( + initialisations)
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases
lstpomme = [] #Liste des coordonnees de la pomme
lstsnake = [] #Liste des coordonnees de la pomme
croissance = 0
mordu = 0

def case_vers_pixel(case):
    """
	Fonction recevant les coordonnées d'une case du plateau sous la 
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les 
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
	prend en compte la taille de chaque case, donnée par la variable 
	globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes): 
    """Fonction qui affiche la pomme (pommes: Coordonnees de la pomme)"""
    x, y = case_vers_pixel(pommes) # Coordonnees de la pomme qu'on convertit en pixels
    cercle(x, y, taille_case/2, couleur='darkred', remplissage='red')
    rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7, couleur='darkgreen', remplissage='darkgreen')
              
def affiche_serpent(serpent): 
    """Fonction qui affiche le serpent (serpent: Coordonnees du serpent)"""
    global lstsnake, mordu #On appelle les variables importantes qui sont en dehors de la fonction
    lst = []
    x, y = case_vers_pixel(serpent)  # Coordonnees de la pomme qu'on convertit en pixels
    cercle(x, y, taille_case/2 + 1, couleur='darkgreen', remplissage='green') #On cree le cercle
    if direction != (0, 0): #Si le serpent ne bouge pas (pour eviter de stocker des coordonnees inutiles dans le tableau:
        lstsnake = lstsnake + [[serpent[0], serpent[1]]] #On ajoute la coordonnee actuelle du serpent dans un tableau qui va lister toutes les coordonnees du serpent 
        if croissance >= 1: #Croissance etant la variable incrementée quand le serpent 'mange' une pomme
            i = croissance #On stocke au compteur la valeur de croissance
            while i > 0:
                x2, y2 = lstsnake[len(lstsnake) - i - 1][0], lstsnake[len(lstsnake) - i - 1][1] # On cree deux variables x2 et y2 qui vont respectivement prendre la valeur de l'abscisse et de l'ordonnee d'une des coordonnees precedentes du serpent (-1 pour eviter de prendre une valeur en dehors de la liste et -i pour prendre la i-eme valeur de la liste en partant du sens oppose, qui sont les valeurs qui nous interesse).
                x2, y2 = case_vers_pixel(lstsnake[len(lstsnake) - i - 1]) #On convertit ces valeurs en pixel
                lst.append((x2, y2)) #On ajoute ces valeurs convertis dans une liste pour la collision entre la tete et le corps du serpent
                corps = cercle(x2, y2 , taille_case/2 + 1, couleur='green', remplissage='green') #On cree le corps
                i = i - 1 #On desincremente
    if (x,y) in lst: #Si la tete du serpent atteint l'une des coordonnes de son corps:
        mordu += 1 #On incremente cette variable de 1 pour verifier la condition qui est dans la boucle principale du programme.
    
def change_direction(direction, touche): 
    """Fonction qui gere la valeur de la direction (Direction: la valeur de la direction, Touche: L'evenement qu'on appelle grace a upemtk)"""
    if touche == 'Up' and direction != (0, 1): #Pour eviter de prendre le chemin oppose et ainsi se mordre la queue instantanement
        return (0, -1)
    elif touche == 'Down' and direction != (0, -1):
        return (0, 1)
    elif touche == 'Left' and direction != (1, 0):
        return (-1, 0)
    elif touche == 'Right' and direction != (-1, 0):
        return (1, 0)
    else:
        # pas de changement !
        return direction
        
def deplacement(serpent, direction):
    """Fonction permettant au serpent de se deplacer (serpent: Coordonnees du serpent, direction: valeur de la direction)"""
    #On ajoute, aux coordonnees du serpent, les valeurs de la direction qui dependent de la touche pressee. Le cercle va ainsi etre re-dessine a sa nouvelle position une fois affiche.
    serpent[0] = serpent[0] + direction[0]
    serpent[1] = serpent[1] + direction[1]
 
def limite(serpent): 
    """Fonction gerant les limites du jeu si le joueur joue au jeu normal (serpent: coordonnees du serpent)"""
    if serpent[0] < 0 or serpent[0] > 40 or serpent[1] < 0 or serpent[1] > 30:
        return False
           
def arene(serpent): 
    """Fonction gerant l'arene torique si le joueur joue au mode torique (serpent: coordonnees du serpent)"""
    if serpent[0] < 0:
        serpent[0] = largeur_plateau
    if serpent[0] > 40:
        serpent[0] = 0
    if serpent[1] < 0:
        serpent[1] = hauteur_plateau
    if serpent[1] > 30:
        serpent[1] = 0
        
        
def reception(serpent, pommes): 
    """Fonction gerant la collision entre la pomme et le serpent. (serpent: coordonnees du serpent, pommes: coordonnees de la pomme)"""
     
    if serpent[0] == pommes[0] and serpent[1] == pommes[1]:
        return True
             

# programme principal
if __name__ == "__main__":

    # initialisation du jeu
    framerate = 10   # taux de rafraîchissement du jeu en images/s
    direction = (0, 0)  # direction initiale du serpent
    while True: #Bouche qui gere le choix du mode
        choix = input('Choose game mode : 1 for the original game, 2 for toric version:  ')
        if choix == "1" or choix == "2":
            print("Understood. Have fun!")
            break
        else:
            print('Input error.')
    cree_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
    serpent2 = [largeur_plateau//2, hauteur_plateau//2]
    pomme = [randint(2, largeur_plateau - 2), randint(2, hauteur_plateau - 2)] #On soustrait de 2 pour eviter que la pomme apparaisse au bord de l'interface
    score = 0

    #Ecran de debut
    while True:
        texte(300, 200, "READY ? (Press any button to start)", couleur="green", ancrage = 'center', tag='ready')
        attend_ev()
        break
    #Boucle principale
    while True:
        # affichage des objets
        efface_tout()
        affiche_pommes(pomme)   #On prend comme parametre les coordonnees initialisees de la pomme
        affiche_serpent(serpent2)  # Pareil pour le serpent
        deplacement(serpent2, direction) #
        if choix == "1": #Si le joueur a choisi de jouer au jeu normal:
            if limite(serpent2) == False: #Si le serpent atteint l'une des bords de l'arene:
                #On affiche l'ecran de fin
                sleep(2) #On freeze le programme pendant 2 secondes pour eviter l'affichage immediat de l'ecran
                efface_tout()
                texte(300, 200, "GAME OVER (Press any button to quit)", couleur="red", ancrage = 'center')
                texte(300, 250, "Your score: {}".format(score), couleur="black", ancrage= 'center', taille=16)
                attend_ev()
                break #On sort de la boucle pour fermer la fenetre
        if choix == "2": #Si le joueur a choisi de jouer au jeu en mode torique:
            arene(serpent2) #On appelle la fonction qui gere ce mode.
        if mordu >= 1: #Si le serpent se mord la queue:
            #On affiche aussi l'ecran de fin
            sleep(2)
            efface_tout()
            texte(300, 200, "GAME OVER (Press any button to quit)", couleur="red", ancrage = 'center')
            texte(300, 250, "Your score: {}".format(score), couleur="black", ancrage= 'center', taille=16)
            attend_ev()
            break
        texte(400, 40, "Score: {}".format(score), couleur="black", ancrage= 'sw', taille=16) #Affichage du score
        rectangle(0, 0, taille_case * largeur_plateau, taille_case * hauteur_plateau, epaisseur = 5, couleur ='black') #Bords de l'arene
        if reception(serpent2, pomme) == True:
            score += 100 #On incremente la valeur du score
            pomme = [randint(2, largeur_plateau - 2), randint(2, hauteur_plateau - 2)] #La pomme prend de nouvelles coordonees
            affiche_pommes(pomme) #Puis on affiche la pomme dans sa nouvelle position
            croissance += 1 #Cette variable est importante pour la croissance du serpent (voir la fonction affiche_serpent)
            framerate = framerate + 2 #Le jeu accelere a chaque pomme mangee
        mise_a_jour() #On met a jour pour pouvoir afficher les objets

        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            break
        elif ty == 'Touche':
            if touche(ev) == 'space': # Espace = Bouton de pause
                while True:
                    texte(300, 225, "P A U S E", couleur="black", ancrage= 'center', taille=16)
                    if touche(attend_ev()) == 'space':
                        break
            else:
                direction = change_direction(direction, touche(ev))

        # attente avant rafraîchissement
        sleep(1/framerate)

    # fermeture et sortie
    sleep(1) #On ajoute un timer de 1 seconde pour éviter que la fenêtre se ferme immédiatement.
    ferme_fenetre()

