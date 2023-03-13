pip install opencv-pythonimport cv2
import numpy as np

# Ouvrir la caméra
cap = cv2.VideoCapture(0)

while True:
    # Lire une frame
    _, frame = cap.read()

    # Appliquer un filtre de flou pour enlever le bruit
    image_blur = cv2.GaussianBlur(frame, (5,5), 0)

    # Convertir l'image en niveaux de gris
    image_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)

    # Appliquer la détection de cercles à l'image en niveaux de gris
    circles = cv2.HoughCircles(image_gray, cv2.HOUGH_GRADIENT, 1.5, 10)

    # Si des cercles ont été détectés
    if circles is not None:
        # Convertir les coordonnées des cercles en entiers
        circles = np.round(circles[0, :]).astype("int")

        # Pour chaque cercle
        for (x, y, r) in circles:
            # Dessiner un cercle autour de la boule de billard
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    # Afficher l'image avec les cercles détectés
    cv2.imshow("Boules de billard détectées", frame)

    # Attendre que l'utilisateur appuie sur une touche pour quitter
    if cv2.waitKey(1) == ord('q'):
        break

# Fermer la caméra et la fenêtre
cap.release()
cv2.destroyAllWindows()
