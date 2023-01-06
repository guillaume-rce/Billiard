import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

# Création de la figure et du plot
fig, ax = plt.subplots()

# Définition de la taille de la table de billard (en pouces)
longueur = 20
largeur = 10

# Définition de la position et de la vitesse initiale de la bille
x_pos = 2
y_pos = 8
x_vel = 0.5
y_vel = 0.5

# Définition de la durée de chaque pas de la simulation (en secondes)
pas_durée = 0.1

# Création de la liste de positions de la bille au cours du temps
positions = []

# Fonction qui met à jour la position de la bille en fonction de sa vitesse et vérifie si elle a atteint un bord de la table
def mettre_à_jour_position():
    global x_pos, y_pos, x_vel, y_vel

    # Mise à jour de la position de la bille en fonction de sa vitesse
    x_pos += x_vel
    y_pos += y_vel

    # Vérifie si la bille a atteint un bord de la table et inverse la vitesse en conséquence
    if x_pos > longueur or x_pos < 0:
        x_vel *= -1
    if y_pos > largeur or y_pos < 0:
        y_vel *= -1

# Fonction de mise à jour de l'animation
def animate(i):
    global positions

    # Mise à jour de la position de la bille
    mettre_à_jour_position()

    # Ajout de la nouvelle position de la bille à la liste de positions
    positions.append((x_pos, y_pos))

    # Conversion de la liste de positions en un tableau numpy
    positions2 = np.array(positions)

    # Effacement des anciennes positions de la bille
    ax.clear()

    # Dessin de la bille sur la table de billard
    ax.plot(positions2[:,0], positions2[:,1], 'bo')

    # Ajout des labels aux axes
    ax.set_xlabel("Longueur (pouces)")
    ax.set_ylabel("Largeur (pouces)")

# Création de l'animation
anim = animation.FuncAnimation(fig, animate, interval=pas_durée*1000)

# Affichage de l'animation
plt.show()
