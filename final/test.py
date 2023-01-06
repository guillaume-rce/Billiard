from modules.elements import Ball

# Créer une liste de balles
balls = []

# Créer quelques balles et les ajouter à la liste
balls.append(Ball(0, 0, tags=["red"]))
balls.append(Ball(1, 1, tags=["blue"]))
balls.append(Ball(2, 2, tags=["green"]))

# Récupérer une balle en utilisant la méthode get_by_id
id_to_find = 2
found_ball = Ball.get_by_id(id_to_find)

# Afficher la balle trouvée, ou un message indiquant qu'elle n'a pas été trouvée
if found_ball:
    print(found_ball)
else:
    print(f"Aucune balle avec l'ID {id_to_find} n'a été trouvée.")
