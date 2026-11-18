"""
Tests API TaskFlow - TP 1

Apprenez en faisant ! Ce fichier vous montre comment écrire des tests, puis vous en écrirez de similaires.

Structure de chaque test :
1. ARRANGE - Préparer les données de test
2. ACT - Faire la requête API
3. ASSERT - Vérifier la réponse
"""
from datetime import datetime, timezone
import pytest


# =============================================================================
# PARTIE 1 : TESTS EXEMPLES (Apprenez de ceux-ci !)
# =============================================================================

def test_root_endpoint(client):
    """
    EXEMPLE : Tester un point de terminaison GET simple.

    Ce test vous montre le pattern de base :
    1. Faire une requête avec client.get()
    2. Vérifier le code de statut
    3. Vérifier les données de la réponse
    """
    # ACT : Faire une requête GET
    response = client.get("/")

    # ASSERT : Vérifier la réponse
    assert response.status_code == 200
    assert "Welcome to TaskFlow API" in response.json()["message"]


def test_health_check(client):
    """EXEMPLE : Un autre test de point de terminaison GET simple."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task(client):
    """
    EXEMPLE : Tester un point de terminaison POST (création de données).

    Pattern pour les requêtes POST :
    1. Préparer les données comme un dictionnaire Python
    2. Les envoyer avec client.post()
    3. Vérifier le code de statut (201 = Créé)
    4. Vérifier les données retournées
    """
    # ARRANGE : Préparer les données
    new_task = {
        "title": "Acheter des courses",
        "description": "Lait, œufs, pain"
    }

    # ACT : Envoyer la requête POST
    response = client.post("/tasks", json=new_task)

    # ASSERT : Vérifier la réponse
    assert response.status_code == 201  # 201 = Créé

    task = response.json()
    assert task["title"] == "Acheter des courses"
    assert task["description"] == "Lait, œufs, pain"
    assert task["status"] == "todo"  # Valeur par défaut
    assert "id" in task  # Le serveur génère un ID



def test_list_tasks(client):
    """
    EXEMPLE : Tester GET avec préparation de données.

    Parfois vous devez créer des données d'abord, puis tester leur listage.
    """
    # ARRANGE : Créer quelques tâches d'abord
    client.post("/tasks", json={"title": "Tâche 1"})
    client.post("/tasks", json={"title": "Tâche 2"})

    # ACT : Obtenir la liste des tâches
    response = client.get("/tasks")

    # ASSERT : Vérifier qu'on a bien les deux tâches
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_get_task_by_id(client):
    """
    EXEMPLE : Tester GET pour une ressource spécifique.

    Pattern :
    1. Créer une tâche d'abord
    2. Obtenir son ID depuis la réponse
    3. Utiliser cet ID pour récupérer la tâche
    """
    # ARRANGE : Créer une tâche
    create_response = client.post("/tasks", json={"title": "Trouve-moi"})
    task_id = create_response.json()["id"]

    # ACT : Obtenir la tâche spécifique
    response = client.get(f"/tasks/{task_id}")

    # ASSERT : Vérifier qu'on a la bonne tâche
    assert response.status_code == 200
    assert response.json()["title"] == "Trouve-moi"


# =============================================================================
# PARTIE 2 : À VOUS ! (Exercices 1 et 2)
# =============================================================================
#
# Écrivez d'abord ces tests : ils échouent, car delete_task() et update_task()
# ne sont pas encore écrites dans src/app.py. Puis écrivez ces fonctions
# jusqu'à ce que les tests passent.
#
# Pour chaque test : supprimez la ligne pytest.fail(...), puis écrivez
# ARRANGE / ACT / ASSERT. La docstring dit ce qu'il faut vérifier.

# --- Exercice 1 : supprimer une tâche ---

def test_delete_task(client):
    # ARRANGE : Créer une tâche
    create_response = client.post("/tasks", json={"title": "Trouve-moi"})
    task_id = create_response.json()["id"]
    #ACT
    response = client.delete(f"/tasks/{task_id}")
    response_get = client.get(f"/tasks/{task_id}")
    #ASSERT
    assert response.status_code == 204

    assert response_get.status_code == 404


def test_delete_nonexistent_task(client):
    #ARRANGE : Prendre l'ID d'une tache qui n'existe pas
    task_id = 1
    #ACT: Supprimer la tâche non existante 
    response = client.delete(f"/tasks/{task_id}")
    #ASSERT: 
    assert response.status_code == 404


# --- Exercice 2 : modifier une tâche ---

def test_update_task_title(client):
    """Modifier le titre d'une tâche renvoie 200 et la tâche avec le nouveau titre."""
    #ARRANGE : creer task

    create_response = client.post("/tasks", json={"title": "Tâche 1"})
    task_id = create_response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"title": "Tâche 2"})
    assert response.status_code == 200
    assert response.json()["title"] == "Tâche 2"




def test_update_only_changes_sent_fields(client):
    """Créez une tâche avec un titre, une description et une priorité,
    puis envoyez seulement {"status": "done"} : le statut change,
    mais le titre, la description et la priorité restent identiques."""
    create_response = client.post("/tasks", json={"title": "Tâche 1", "description": "test", "priority" : "low"})
    task_time = create_response.json()["created_at"]
    task_id = create_response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"status": "done"})
    assert response.status_code == 200
    assert response.json()["title"] == "Tâche 1"
    assert response.json()["description"] == "test"
    assert response.json()["priority"] == "low"
    assert response.json()["status"] == "done"
    assert response.json()["created_at"] == task_time


def test_update_nonexistent_task(client):
    task_id = 1
    response = client.put(f"/tasks/{task_id}", json = {"title" : "a"})
    """Modifier une tâche qui n'existe pas renvoie 404."""
    assert response.status_code == 404


# =============================================================================
# PARTIE 3 : À VOUS ! (Exercice 3)
# =============================================================================
#
# Écrivez ces tests. Pour chacun : supprimez la ligne pytest.fail(...),
# puis écrivez ARRANGE / ACT / ASSERT. La docstring dit ce qu'il faut vérifier.

def test_create_task_with_empty_title(client):
    """Créer une tâche avec un titre vide ("") est refusé : 422."""
    new_task = {
        "title": "",
        "description": "Lait, œufs, pain"
    }
    new_task_2 = {
        "title": " ",
        "description": "Lait, œufs, pain"
    }
        # ACT : Envoyer la requête POST
    response = client.post("/tasks", json=new_task)
    response_2 = client.post("/tasks", json=new_task_2)
    assert response.status_code == 422
    assert response_2.status_code == 422


def test_get_nonexistent_task(client):
    # ARRANGE : tâche non existante
    task_id = 1
    #ACT
    response = client.get(f"/tasks/{task_id}")

    # ASSERT
    assert response.status_code == 404

def test_update_task_with_invalid_priority(client):
    create_response = client.post("/tasks", json={"title": "Tâche 1"})
    task_id = create_response.json()["id"]
    response = client.put(f"tasks/{task_id}", json = {"priority" : "urgent"})
    assert response.status_code == 422

def test_filter_tasks_by_status(client):
    """Créez une tâche "todo" et une tâche "done" : GET /tasks?status=done
    ne renvoie qu'une seule tâche, celle qui est terminée."""    
    create_response = client.post("/tasks", json={"title": "Tâche 1", "status" : "todo"})
    create_response_2 = client.post("/tasks", json={"title": "Tâche 2", "status" : "done"})
    task_id_1 = create_response.json()["id"]
    task_id_2 = create_response_2.json()["id"]

    response = client.get("/tasks?status=done")
    data = response.json()
    assert len(data) == 1


# =============================================================================
# BONUS (si vous avez fini)
# =============================================================================
#
# Supprimez la ligne @pytest.mark.skip(...) pour activer un test.


def test_filter_by_status_and_priority(client):
    """GET /tasks?status=todo&priority=high combine les deux filtres."""
    create_response = client.post("/tasks", json={"title": "Tâche 1", "status" : "todo", "priority" : "low"})
    create_response_2 = client.post("/tasks", json={"title": "Tâche 2", "status" : "done"})
    create_response_3 = client.post("/tasks", json={"title" :"Tâche 3", "status" : "todo", "priority" : "high"})
    create_response_4 = client.post("/tasks", json={"title": "Tâche 4", "status": "done", "priority" : "high"})
    task_id_1 = create_response.json()["id"]
    task_id_2 = create_response_2.json()["id"]
    task_id_3 = create_response_3.json()["id"]
    task_id_4 = create_response_4.json()["id"]

    response = client.get("/tasks?status=todo&priority=high")
    data = response.json()
    assert len(data) == 1


def test_create_task_with_title_too_long(client):
    """Le titre est limité à 200 caractères : 200 est accepté (201), 201 est refusé (422).
    Astuce : "a" * 200 crée un texte de 200 caractères."""
    text_valid = "a"*200
    text_invalid = "a"*201
    response_valid = client.post("/tasks", json={"title": text_valid})
    response_invalid = client.post("/tasks", json = {"title" : text_invalid})
    assert response_valid.status_code == 201
    assert response_invalid.status_code == 422

def test_search_tasks_by_title(client):
    """GET /tasks?search=... renvoie les tâches dont le titre contient la chaîne (insensible à la casse)."""
    # ARRANGE : Créer trois tâches avec des casses différentes
    client.post("/tasks", json={"title": "Rapport annuel 2024", "status": "todo"})
    client.post("/tasks", json={"title": "Faire les courses", "status": "todo"})
    client.post("/tasks", json={"title": "Écrire le RAPPORT final", "status": "todo"})

    # ACT : Chercher avec "rapport" en minuscules
    response = client.get("/tasks", params={"search": "rapport"})

    # ASSERT
    assert response.status_code == 200
    data = response.json()
    
    # On s'attend à trouver exactement 2 tâches (ignorant "Faire les courses")
    assert len(data) == 2
    
    titles = [task["title"] for task in data]
    assert "Rapport annuel 2024" in titles
    assert "Écrire le RAPPORT final" in titles

def test_search_tasks_by_assignee(client):

    #ARRANGE :
    client.post("/tasks", json={"title": "test", "assignee": "Michel"})
    client.post("/tasks", json = {"title" : "test2", "assignee": "Arthur"})

    response = client.get("/tasks", params={"assignee": "Arthur"})

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assignee = [task["assignee"] for task in data ]
    assert "Michel" not in assignee
# =============================================================================
# ASTUCES & CONSEILS
# =============================================================================

"""
PATTERNS COURANTS :

1. Tester POST (Créer) :
   response = client.post("/tasks", json={"title": "..."})
   assert response.status_code == 201

2. Tester GET (Lire) :
   response = client.get("/tasks")
   assert response.status_code == 200

3. Tester PUT (Mettre à jour) :
   response = client.put(f"/tasks/{id}", json={"title": "..."})
   assert response.status_code == 200

4. Tester DELETE (Supprimer) :
   response = client.delete(f"/tasks/{id}")
   assert response.status_code == 204

5. Tester les erreurs de validation :
   response = client.post("/tasks", json={"bad": "data"})
   assert response.status_code == 422

6. Tester les erreurs 404 (la ressource demandée n'existe pas) :
   assert response.status_code == 404

CODES DE STATUT COURANTS :
- 200 : OK (GET/PUT réussi)
- 201 : Créé (POST réussi)
- 204 : Pas de Contenu (DELETE réussi)
- 404 : Non Trouvé (la ressource n'existe pas)
- 422 : Erreur de Validation (données invalides)

RAPPELEZ-VOUS :
- La fixture `client` est automatiquement fournie par conftest.py
- Les tâches sont automatiquement effacées avant/après chaque test (fixture clean_tasks)
- Les tests doivent être indépendants (ne pas dépendre d'autres tests)
"""
