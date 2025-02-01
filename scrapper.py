import requests
from flask import Flask, request, jsonify, send_from_directory
import os
import re
from post_scrapper import GeminiSynthesizer
from collections import defaultdict
import hashlib
import random

app = Flask(__name__, static_folder='.', static_url_path='')

# Initialiser le synthétiseur Gemini
gemini_synthesizer = GeminiSynthesizer("AIzaSyD8LKVDXO5zAFYbINcKHII-fiDa6rDexR4")

# Stockage du contexte des conversations
contextes_conversations = defaultdict(list)

def generer_cle_session(adresse_ip):
    """
    Génère une clé de session unique basée sur l'adresse IP.
    """
    return hashlib.md5(adresse_ip.encode()).hexdigest()

def extraire_mots_cles(question):
    """
    Extrait les mots-clés principaux d'une question.
    """
    # Liste de mots à ignorer
    mots_ignores = {'qui', 'quoi', 'comment', 'pourquoi', 'où', 'quand', 'est', 'ce', 'que', 'un', 'une', 'des', 'de', 'la', 'le', 'les'}
    
    # Nettoyer et tokenizer la question
    mots = re.findall(r'\b\w+\b', question.lower())
    
    # Filtrer les mots-clés significatifs
    mots_cles = [mot for mot in mots if mot not in mots_ignores and len(mot) > 2]
    
    return mots_cles

def trouver_contexte_pertinent(question, contexte_precedent):
    """
    Trouve le contexte pertinent dans les messages précédents.
    """
    mots_cles_question = set(extraire_mots_cles(question))
    
    for message_precedent, reponse_precedente in reversed(contexte_precedent):
        mots_cles_precedent = set(extraire_mots_cles(message_precedent))
        
        # Calcul du recouvrement des mots-clés
        intersection = mots_cles_question.intersection(mots_cles_precedent)
        
        # Si intersection significative, retourner le contexte
        if len(intersection) > 0:
            return f"Contexte précédent : {message_precedent}\nRéponse précédente : {reponse_precedente}\n\n"
    
    return ""

def est_demande_ludique(question):
    """
    Détermine si la question est une demande de jeu ou d'activité ludique.
    """
    mots_cles_ludiques = [
        "jeu", "quiz", "devinette", "challenge", "test", "questionnaire", 
        "jouer", "game", "énigme", "sport quiz", "football quiz"
    ]
    
    question_lower = question.lower()
    
    # Vérification des mots-clés
    for mot in mots_cles_ludiques:
        if mot in question_lower:
            return True
    
    # Vérification des structures de phrases
    patterns_ludiques = [
        r"fais-moi un jeu",
        r"veux-tu jouer",
        r"jouons à",
        r"un quiz sur",
        r"teste-moi sur"
    ]
    
    for pattern in patterns_ludiques:
        if re.search(pattern, question_lower):
            return True
    
    return False

def generer_jeu_sportif(question):
    """
    Génère un jeu ou un quiz sportif interactif via Gemini.
    """
    prompt = f"""
    Crée un mini-jeu ou un quiz sportif interactif basé sur cette demande : {question}
    
    Format de réponse :
    Titre du Jeu
    Règles/Instructions
    Première Question/Défi
    
    Assure-toi que le jeu soit :
    - Amusant et engageant
    - Lié au sport
    - Interactif
    - Avec des règles claires
    """
    
    try:
        # Utiliser Gemini pour générer le jeu
        reponse_jeu = gemini_synthesizer.synthétiser_réponse(prompt)
        return reponse_jeu
    except Exception as e:
        return f"Erreur de génération de jeu : {str(e)}"

def est_question_sportive(question):
    """
    Vérifie si la question est liée au sport.
    """
    # Mots-clés sportifs
    mots_cles_sport = [
        # Sports
        'football', 'tennis', 'basketball', 'rugby', 'handball', 'volleyball', 
        'cyclisme', 'natation', 'athlétisme', 'ski', 'hockey', 'baseball', 
        'cricket', 'golf', 'boxe', 'arts martiaux', 'marathon', 'course',
        
        # Compétitions
        'coupe', 'championnat', 'ligue', 'tournoi', 'mondial', 'olympique', 
        'grand chelem', 'euro', 'mondial', 'champions league',
        
        # Personnalités sportives
        'messi', 'ronaldo', 'nadal', 'federer', 'mbappé', 'neymar', 'pogba', 
        'djokovic', 'serena williams', 'usain bolt', 'michael jordan',
        
        # Termes sportifs
        'match', 'équipe', 'joueur', 'score', 'victoire', 'défaite', 'classement', 
        'transfert', 'entraîneur', 'tactique', 'stratégie', 'performance',
        
        # Types de questions sportives
        'pronostic', 'statistiques', 'résultat', 'record', 'meilleur', 'champion',
        'jeu', 'quiz', 'challenge'
    ]
    
    # Types de questions non sportives à rejeter
    mots_hors_sport = [
        'politique', 'économie', 'météo', 'santé', 'médecine', 'cuisine', 
        'voyage', 'technologie', 'science', 'philosophie', 'histoire générale', 
        'astronomie', 'géographie', 'musique', 'cinéma', 'art'
    ]
    
    question_lower = question.lower()
    
    # Vérifier les mots-clés sportifs
    for mot in mots_cles_sport:
        if mot in question_lower:
            return True
    
    # Rejeter explicitement les sujets hors sport
    for mot in mots_hors_sport:
        if mot in question_lower:
            return False
    
    return False

def generer_reponse_expert_sport(question):
    """
    Génère une réponse d'expert sportif adaptée.
    """
    reponses_standard = [
        " En tant qu'expert sportif, je me concentre uniquement sur les sujets liés au sport.",
        " Ma mission est de fournir des informations, analyses et conseils sportifs.",
        " Je suis spécialisé dans l'expertise sportive : actualités, statistiques, analyses de performance.",
        " Mon domaine d'expertise se limite au monde du sport. Je ne peux pas répondre à des questions hors de ce cadre."
    ]
    
    return random.choice(reponses_standard)

def condenser_reponse(reponse_longue):
    """
    Condense une réponse longue en une version ultra-concise.
    """
    try:
        # Utiliser Gemini pour synthétiser la réponse
        reponse_synthetisee = gemini_synthesizer.synthétiser_réponse(reponse_longue)
        return reponse_synthetisee
    except Exception as e:
        # Revenir à la méthode de condensation originale si Gemini échoue
        condensations = {
            "Qui a gagné la CAN": "La Côte d'Ivoire a remporté la CAN 2024 en battant le Nigeria 2-1, son 3ème titre.",
            "messi est plus fort": "Messi domine : 8 Ballons d'Or, Coupe du Monde 2022, technique supérieure.",
            "qui est le meilleur footaballer entre messi et cr7": "Messi légèrement supérieur : 8 Ballons d'Or, Coupe du Monde 2022."
        }
        
        # Recherche approximative de la question
        for cle, reponse_condensee in condensations.items():
            if cle.lower() in reponse_longue.lower():
                return reponse_condensee
        
        # Si pas de correspondance, tronquer à 3 lignes
        lignes = reponse_longue.split('\n')
        return '\n'.join(lignes[:3]) + ('...' if len(lignes) > 3 else '')

def poser_question_perplexity(question, adresse_ip):
    # Prétraitement et filtrage de la question
    est_pertinent, reponse_standard = gemini_synthesizer.filtrer_question(question)
    
    if not est_pertinent:
        return reponse_standard
    
    # Générer une clé de session
    cle_session = generer_cle_session(adresse_ip)
    
    # Récupérer le contexte de la conversation
    contexte_conversation = contextes_conversations[cle_session]
    
    # Trouver un contexte pertinent
    contexte_pertinent = trouver_contexte_pertinent(question, contexte_conversation)
    
    # Vérifier si c'est une demande ludique
    if est_demande_ludique(question):
        reponse = generer_jeu_sportif(question)
    else:
        # Préparer le prompt avec contexte
        prompt_complet = contexte_pertinent + question
        
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "Bearer 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"
        }

        payload = {
            "model": "sonar-pro",
            "messages": [
                {
                    "role": "system",
                    "content": "Vous êtes un expert en sport. Soyez précis et concis. Utilisez le contexte de conversation si pertinent."
                },
                {
                    "role": "user",
                    "content": prompt_complet
                }
            ]
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code != 200:
                error_detail = response.json().get('error', {}).get('message', 'Erreur inconnue')
                reponse = f"Erreur {response.status_code}: {error_detail}"
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                reponse = result['choices'][0]['message']['content']
            else:
                reponse = "Pas de réponse de l'API"
        
        except Exception as e:
            reponse = f"Erreur lors de la requête : {str(e)}"
    
    # Mettre à jour le contexte de la conversation
    contexte_conversation.append((question, reponse))
    
    return condenser_reponse(reponse)

@app.route('/')
def index():
    return send_from_directory('.', 'client.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Réponse vide avec un code de statut 204 (No Content)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question', '')
    adresse_ip = request.remote_addr or '127.0.0.1'
    
    if not question:
        return jsonify({"response": "Aucune question posée"}), 400
    
    response = poser_question_perplexity(question, adresse_ip)
    return jsonify({"response": response})

@app.route('/chat', methods=['POST'])
def handle_chat():
    data = request.json
    message = data.get('message', '')
    mode = data.get('mode', 'pronostics')  # Mode par défaut

    try:
        # Sélectionner la stratégie de réponse en fonction du mode
        if mode == 'pronostics':
            response = generer_pronostic(message)
        elif mode == 'recherche':
            response = recherche_sportive(message)
        elif mode == 'fun':
            response = mode_fun(message)
        else:
            response = "Mode non reconnu. Retour au mode Pronostics."

        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"response": f"Erreur : {str(e)}"}), 500

def generer_pronostic(message):
    """
    Génère un pronostic sportif basé sur le message.
    """
    synthesizer = GeminiSynthesizer("AIzaSyD8LKVDXO5zAFYbINcKHII-fiDa6rDexR4")
    return synthesizer.generer_reponse_pronostic(message)

def recherche_sportive(message):
    """
    Effectue une recherche sportive détaillée.
    """
    synthesizer = GeminiSynthesizer("AIzaSyD8LKVDXO5zAFYbINcKHII-fiDa6rDexR4")
    prompt = f"""
    Mode Recherche : Analyse approfondie sur le sujet suivant.
    Fournis une réponse détaillée, technique et informative.
    Sujet : {message}
    """
    return synthesizer._requete_gemini(prompt)

def mode_fun(message):
    """
    Mode Fun avec des réponses humoristiques et interactives.
    """
    synthesizer = GeminiSynthesizer("AIzaSyD8LKVDXO5zAFYbINcKHII-fiDa6rDexR4")
    prompt = f"""
    Mode Fun : Transforme ce message en une réponse ludique et humoristique.
    Ajoute de l'humour, des jeux de mots et de l'interaction.
    Message : {message}
    """
    return synthesizer._requete_gemini(prompt)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
