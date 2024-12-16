import requests
import xml.etree.ElementTree as ET

# URLs de l'API pour récupérer la collection de jeux et les détails des jeux
collection_games_url = 'https://api.geekdo.com/xmlapi/collection/megtrinity'
games_details_url = 'https://api.geekdo.com/xmlapi/boardgame/'

def getGames():
    """
    Récupère la liste des jeux de société à partir de l'API XML.

    La fonction effectue une requête HTTP GET à l'URL spécifiée, analyse la réponse XML,
    extrait les informations sur chaque jeu (id, nom, année, joueurs, temps de jeu, vignette),
    puis les retourne sous forme de liste.

    Returns:
        list: Une liste de jeux, chaque jeu étant représenté par un dictionnaire contenant
              id, title, lst_published_year, players, playtime, thumbnail.
        None: Si une erreur survient lors de la requête ou du traitement des données.
    """
    try:
        # Envoi d'une requête GET à l'URL de l'API
        response = requests.get(collection_games_url)

        # Vérification du statut HTTP de la réponse
        if response.status_code == 200 or response.status_code == 201:
            data = response.text  # Contenu XML de la réponse

            # Analyse du XML
            root = ET.fromstring(data)
            games = []  # Liste pour stocker les jeux

            # Parcours de chaque élément "item" dans le XML
            for item in root.findall('item'):
                game = {}  # Initialisation du dictionnaire pour chaque jeu

                # ID du jeu
                game_id = item.attrib.get('objectid')

                # Nom du jeu
                title_element = item.find('name')
                title = title_element.text if title_element is not None else "Inconnu"

                # Année de publication
                year_element = item.find('yearpublished')
                year_published = year_element.text if year_element is not None else "Inconnu"

                # Section des statistiques
                stats = item.find('stats')

                # Min et max des joueurs
                minplayers = stats.attrib.get('minplayers') if stats is not None else "?"
                maxplayers = stats.attrib.get('maxplayers') if stats is not None else "?"
                players = f"{minplayers}-{maxplayers}"  # Format du nombre de joueurs

                # Temps de jeu minimum et maximum
                minplaytime = stats.attrib.get('minplaytime') if stats is not None else "?"
                maxplaytime = stats.attrib.get('maxplaytime') if stats is not None else "?"
                playtime = f"{minplaytime}-{maxplaytime} min" if minplaytime != maxplaytime else f"{maxplaytime} min"

                # Lien de la vignette du jeu
                thumbnail_element = item.find('thumbnail')
                thumbnail = thumbnail_element.text if thumbnail_element is not None else "Pas de vignette"

                # Ajout des informations dans le dictionnaire
                game["id"] = game_id
                game["title"] = title
                game["lst_published_year"] = year_published
                game["players"] = players
                game["playtime"] = playtime
                game["thumbnail"] = thumbnail

                # Ajout du jeu à la liste
                games.append(game)

            return games  # Retourne la liste des jeux
        else:
            # Gestion des erreurs HTTP
            print("Erreur HTTP, code:", response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        # Gestion des erreurs liées à la requête
        print("Erreur lors de la requête :", e)
        return None

def getGameDetails(game_id):
    """
    Récupère et retourne les détails d'un jeu spécifique par ID.

    Args:
        game_id (str): L'identifiant du jeu à récupérer.

    Returns:
        dict: Un dictionnaire contenant les détails du jeu (titre, description, image, etc.).
        None: En cas d'erreur ou si le jeu n'existe pas.
    """
    try:
        # Envoi d'une requête GET pour récupérer les détails du jeu
        response = requests.get(f"{games_details_url}{game_id}")

        if response.status_code == 200 or response.status_code == 201:
            # Analyse du XML de la réponse
            root = ET.fromstring(response.text)
            game_data = root.find('boardgame')  # Extraction des données principales
            if game_data is None:
                return None  # Pas de données pour cet ID

            # Extraction des catégories
            categories = [category.text for category in game_data.findall("boardgamecategory")]

            # Extraction des extensions
            expansions = [expansion.text for expansion in game_data.findall("boardgameexpansion")]

            # Calcul du temps de jeu
            minplaytime = game_data.find('minplaytime').text if game_data.find('minplaytime') is not None else "?"
            maxplaytime = game_data.find('maxplaytime').text if game_data.find('maxplaytime') is not None else "?"
            playtime = f"{minplaytime}-{maxplaytime} min" if minplaytime != maxplaytime else f"{maxplaytime} min"

            # Titre du jeu (recherche du titre principal)
            title = "Inconnu"
            for title_element in game_data.findall('name'):
                if title_element.attrib.get('primary') == "true":
                    title = title_element.text
                    break

            # Préparation des détails dans un dictionnaire
            dict_details = {
                "id": game_data.attrib.get("objectid"),
                "title": title,
                "description": game_data.find('description').text if game_data.find('description') is not None else "No description",
                "image": game_data.find('image').text if game_data.find('image') is not None else "No image",
                "players": f"{game_data.find('minplayers').text}-{game_data.find('maxplayers').text}" if game_data.find('minplayers') is not None and game_data.find('maxplayers') is not None else "N/A",
                "playtime": playtime,
                "categories": ", ".join(categories),
                "expansions": expansions,
            }

            return dict_details  # Retourne les détails du jeu
        else:
            return None  # En cas d'erreur HTTP
    except requests.exceptions.RequestException as e:
        # Gestion des erreurs liées à la requête
        print("Erreur lors de la récupération des détails du jeu :", e)
        return None
