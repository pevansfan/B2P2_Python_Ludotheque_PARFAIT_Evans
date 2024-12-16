from flask import Flask, jsonify, redirect, url_for  # Importation de Flask pour créer l'application et jsonify pour retourner des réponses JSON
import ludo2  # Importation du module contenant les fonctions de récupération des jeux

# Création d'une instance de l'application Flask
app = Flask(__name__)

@app.route('/games', methods=['GET'])
def list_games():
    """
    Route pour lister tous les jeux de société.

    Cette route appelle la fonction `getGames` du module `ludo2` pour récupérer 
    une liste de jeux de société. Les jeux sont ensuite retournés sous forme de JSON.

    Returns:
        Response: Un objet JSON contenant la liste des jeux si elle est récupérée avec succès,
                  ou un message d'erreur HTML si une erreur survient.
    """
    games = ludo2.getGames()  # Appel de la fonction pour récupérer la liste des jeux
    if games is None:
        # Si une erreur survient, retourne un message d'erreur HTML
        return "<p>Impossible de récupérer les jeux.</p>"
    # Retourne la liste des jeux en format JSON
    return jsonify(games)

@app.route('/games/<int:game_id>', methods=['GET'])
def game_details(game_id):
    """
    Route pour afficher les détails d'un jeu spécifique.

    Cette route utilise l'identifiant du jeu (`game_id`) pour appeler la fonction 
    `getGameDetails` du module `ludo2` et récupérer les détails d'un jeu. 
    Les détails sont retournés sous forme de JSON.

    Args:
        game_id (int): L'identifiant unique du jeu.

    Returns:
        Response: Un objet JSON contenant les détails du jeu si trouvé,
                  ou un message d'erreur HTML si le jeu n'existe pas.
    """
    game = ludo2.getGameDetails(game_id)  # Appel de la fonction pour récupérer les détails du jeu
    if game is None:
        # Si aucun jeu n'est trouvé, retourne un message d'erreur HTML
        return "<p>Jeu non trouvé.</p>"
    # Retourne les détails du jeu en format JSON
    return jsonify(game)

@app.route('/')
def index():
    return redirect(url_for('list_games'))

# Point d'entrée principal de l'application
if __name__ == '__main__':
    # Lancement de l'application Flask sur le port 5000 avec le mode debug activé
    app.run(port=5000, debug=True)
