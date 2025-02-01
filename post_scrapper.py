import requests
import json
import re
import random

class ChatbotPronostics:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        # Styles de réponse
        self.styles = {
            "technique": [
                "Analyse précise des stats : ",
                "Décryptage chiffré : ",
                "Focus technique : "
            ],
            "pépite": [
                " Pépite du jour : ",
                " Coup de cœur : ",
                " Pronostic exclusif : "
            ],
            "engagement": [
                " Prêt pour l'action ? ",
                " On se lance ? ",
                " Le sport, c'est maintenant ! "
            ]
        }
        
        # Termes de paris
        self.termes_paris = [
            "cote", "handicap", "over/under", "mises", "value bet", 
            "moneyline", "back", "lay", "bankroll", "freebet", "value"
        ]
        
        # Expressions d'opinion
        self.expressions_opinion = [
            "Je pense que", "je crois vraiment en", 
            "je m'attends à", "je vois bien", "j'opte pour"
        ]
        
        # Nuances
        self.nuances = [
            "Attention à", "mais si", "peut-être que", 
            "ou alors", "honnêtement", "à voir"
        ]

    def _requete_gemini(self, prompt):
        """
        Méthode générique pour faire une requête à Gemini.
        """
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}", 
                headers={"Content-Type": "application/json"}, 
                data=json.dumps(payload)
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"Erreur Gemini : {response.status_code}"
        
        except Exception as e:
            return f"Erreur de requête : {str(e)}"

    def generer_reponse_pronostic(self, question):
        """
        Génère une réponse de pronostic sportif en se concentrant précisément sur la question.
        """
        # Extraction du sport spécifique
        sport = self._extraire_sport(question)
        
        # Liste de pronostics prédéfinis par sport
        pronostics_exemples = {
            "basket": [
                {
                    "match": "Lakers vs Celtics - NBA",
                    "analyse_technique": {
                        "Lakers": {
                            "victoires_saison": 28,
                            "points_moyens": 112.5,
                            "performance_domicile": "Excellente"
                        },
                        "Celtics": {
                            "victoires_saison": 32,
                            "points_moyens": 115.3,
                            "performance_exterieur": "Solide"
                        }
                    },
                    "pepite": "LeBron James de retour, 28.5 points de moyenne sur les 5 derniers matchs",
                    "pronostic": {
                        "type_pari": "Handicap Celtics -3.5",
                        "cote": 1.95,
                        "pari_combine": "Celtics Victoire + Over 220.5 points",
                        "cote_totale": 2.30
                    },
                    "value_bet": "Parier sur plus de 220.5 points total"
                },
                {
                    "match": "Warriors vs Nuggets - NBA",
                    "analyse_technique": {
                        "Warriors": {
                            "victoires_saison": 25,
                            "points_moyens": 108.7,
                            "performance_domicile": "Variable"
                        },
                        "Nuggets": {
                            "victoires_saison": 35,
                            "points_moyens": 118.2,
                            "performance_exterieur": "Très forte"
                        }
                    },
                    "pepite": "Nikola Jokic en forme monster, 25.3 points, 11.7 rebonds de moyenne",
                    "pronostic": {
                        "type_pari": "Victoire Nuggets",
                        "cote": 1.75,
                        "pari_combine": "Nuggets Victoire + Jokic +20 points",
                        "cote_totale": 2.45
                    },
                    "value_bet": "Pari sur performance individuelle de Jokic"
                }
            ],
            "football": [
                {
                    "match": "Liverpool vs Manchester City",
                    "analyse_technique": {
                        "Liverpool": {
                            "victoires": 7,
                            "buts_moyens": 2.3,
                            "forme": "Excellente"
                        },
                        "Manchester City": {
                            "victoires": 8,
                            "buts_moyens": 2.5,
                            "possession": "75%"
                        },
                        "confrontations_directes": {
                            "victoires_city": 3,
                            "nuls": 2,
                            "victoires_liverpool": 1
                        }
                    },
                    "pepite": "Kevin De Bruyne de retour, taux de passes décisives : 0.4/match",
                    "pronostic": {
                        "type_pari": "Both Teams To Score (BTTS)",
                        "cote": 1.75,
                        "pari_combine": "Victoire City + BTTS",
                        "cote_totale": 2.40
                    },
                    "value_bet": "Parier sur plus de 2.5 buts"
                },
                {
                    "match": "PSG vs Real Madrid",
                    "analyse_technique": {
                        "PSG": {
                            "victoires": 6,
                            "buts_moyens": 2.1,
                            "domicile": "Très fort"
                        },
                        "Real Madrid": {
                            "victoires": 7,
                            "buts_moyens": 2.4,
                            "exterieur": "Solide"
                        }
                    },
                    "pepite": "Mbappé en forme, 5 buts sur les 3 derniers matchs",
                    "pronostic": {
                        "type_pari": "Victoire PSG",
                        "cote": 2.10,
                        "pari_combine": "PSG + Over 2.5 buts",
                        "cote_totale": 2.75
                    },
                    "value_bet": "Pari sur Mbappé buteur"
                }
            ],
            "tennis": [
                {
                    "match": "Nadal vs Djokovic",
                    "analyse_technique": {
                        "Nadal": {
                            "victoires_recentes": 4,
                            "pourcentage_services": "68%",
                            "surface_preference": "Terre battue"
                        },
                        "Djokovic": {
                            "victoires_recentes": 5,
                            "pourcentage_services": "72%",
                            "surface_preference": "Toutes surfaces"
                        }
                    },
                    "pepite": "Nadal en légère baisse de forme, mais toujours dangereux",
                    "pronostic": {
                        "type_pari": "Victoire Djokovic",
                        "cote": 1.90,
                        "pari_combine": "Djokovic en 3 sets",
                        "cote_totale": 2.20
                    },
                    "value_bet": "Pari sur nombre de sets"
                }
            ]
        }

        # Vérifier si le sport est supporté
        if sport not in pronostics_exemples:
            return self._reponse_sport_non_supporte(sport, question)
        
        # Sélectionner un pronostic aléatoire pour ce sport
        pronostic = random.choice(pronostics_exemples[sport])

        # Générer la réponse stylisée
        reponse_stylisee = self._formater_pronostic(pronostic, sport, question)
        
        return reponse_stylisee

    def _extraire_sport(self, question):
        """
        Extrait le sport mentionné dans la question.
        """
        sports_mapping = {
            "basket": ["basket", "nba", "basketball"],
            "football": ["foot", "football", "ligue", "championnat"],
            "tennis": ["tennis", "roland", "wimbledon"],
            "rugby": ["rugby"],
            "handball": ["handball"]
        }
        
        question_lower = question.lower()
        
        for sport, mots_cles in sports_mapping.items():
            if any(mot in question_lower for mot in mots_cles):
                return sport
        
        return "general"

    def _reponse_sport_non_supporte(self, sport, question_originale):
        """
        Gère les questions sur des sports non supportés.
        """
        reponses = [
            f"⚠️ Désolé, je n'ai pas encore de pronostics détaillés pour le sport '{sport}'. "
            "Mes analyses sont actuellement concentrées sur le basket, football et tennis. "
            f"Ta question originale était : {question_originale}",
            
            f"🏆 Sport '{sport}' non couvert actuellement. "
            "Mes experts sont en train de développer des analyses pour ce domaine. "
            "En attendant, je peux te parler de basket, football ou tennis !",
            
            f"🎲 Pas de pronostics pour {sport} pour le moment. "
            "Mais je suis toujours partant pour discuter sport ! "
            "As-tu une question sur la NBA, la Premier League ou Roland Garros ?"
        ]
        
        return random.choice(reponses)

    def _formater_pronostic(self, pronostic, sport, question_originale):
        """
        Formate un pronostic avec une structure claire et directe.
        """
        # Styles de formatage
        style_technique = random.choice(self.styles['technique'])
        style_pépite = random.choice(self.styles['pépite'])
        style_engagement = random.choice(self.styles['engagement'])
        
        # Termes de paris et expressions
        terme_paris = random.choice(self.termes_paris)
        expression_opinion = random.choice(self.expressions_opinion)
        nuance = random.choice(self.nuances)

        # Construction de la réponse
        reponse = f"""🎯 PRONOSTIC {sport.upper()}

📍 MATCH : {pronostic['match']}

🔍 ANALYSE TECHNIQUE :
{self._formater_stats_techniques(pronostic['analyse_technique'])}

🌟 PÉPITE DU JOUR :
{pronostic['pepite']}

💰 PRONOSTIC PRINCIPAL :
• {terme_paris} : {pronostic['pronostic']['type_pari']} 
• Cote : {pronostic['pronostic']['cote']}

🔥 PARI COMBINÉ :
{pronostic['pronostic']['pari_combine']}
Cote totale : {pronostic['pronostic']['cote_totale']}

💡 VALUE BET :
{pronostic['value_bet']}

🎲 CONSEIL :
{expression_opinion}, ce pronostic va faire des étincelles ! 
{nuance}, rejoins-moi sur Telegram pour plus de pronostics exclusifs !

❓ Et toi, tu vois comment ce match ?"""
        
        return reponse

    def _formater_stats_techniques(self, analyse_technique):
        """
        Formate les statistiques techniques de manière lisible.
        """
        stats_formatees = []
        for equipe, stats in analyse_technique.items():
            stats_equipe = " | ".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in stats.items()])
            stats_formatees.append(f"• {equipe.upper()} : {stats_equipe}")
        
        return "\n".join(stats_formatees)

    def _est_question_sportive(self, question):
        """
        Vérifie si la question concerne le sport.
        """
        mots_cles_sport = [
            'football', 'tennis', 'basket', 'rugby', 'match', 'équipe', 
            'championnat', 'ligue', 'coupe', 'pronostic', 'cote', 
            'paris', 'sport', 'joueur', 'victoire', 'défaite'
        ]
        
        question_lower = question.lower()
        return any(mot in question_lower for mot in mots_cles_sport)

    def _reponse_hors_sport(self):
        """
        Réponse standard pour les questions hors sport.
        """
        reponses = [
            " Je suis un expert en paris sportifs, pas un consultant universel ! Parlons foot, tennis ou sport ?",
            " Mon terrain, c'est le sport. Tu as une question sur un match, des stats ou des pronostics ?",
            " Désolé, mon expertise se limite au monde sportif. Un pronostic, un conseil de pari ?"
        ]
        return random.choice(reponses)

class GeminiSynthesizer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.chatbot_pronostics = ChatbotPronostics(api_key)
        
        # Dictionnaire de jeux sportifs avec leurs générateurs
        self.jeux_sportifs = {
            "tennis": self.generer_quiz_tennis,
            "football": self.generer_quiz_football,
            "sport": self.generer_quiz_general
        }
    
    def filtrer_question(self, question):
        """
        Filtre et évalue la pertinence d'une question.
        """
        # Utiliser le chatbot de pronostics pour évaluer
        if not self.chatbot_pronostics._est_question_sportive(question):
            return False, self.chatbot_pronostics._reponse_hors_sport()
        
        return True, None
    
    def synthétiser_réponse(self, texte_original):
        """
        Synthétise un texte en utilisant le style de pronostics.
        """
        # Si c'est une question sportive, utiliser le chatbot de pronostics
        if self.chatbot_pronostics._est_question_sportive(texte_original):
            return self.chatbot_pronostics.generer_reponse_pronostic(texte_original)
        
        # Sinon, utiliser la synthèse standard
        prompt = f"Synthétise ce texte en 2-3 lignes, en gardant l'essentiel : {texte_original}"
        
        try:
            texte_synthetise = self._requete_gemini(prompt)
            
            # Nettoyer le texte
            texte_synthetise = re.sub(r'^[*\s]+|[*\s]+$', '', texte_synthetise)
            
            return f" {texte_synthetise}"
        except Exception as e:
            return f" Erreur de synthèse : {str(e)}"

    def _requete_gemini(self, prompt):
        """
        Méthode générique pour faire une requête à Gemini.
        """
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95
            }
        }
        
        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}", 
                headers={"Content-Type": "application/json"}, 
                data=json.dumps(payload)
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"Erreur Gemini : {response.status_code}"
        
        except Exception as e:
            return f"Erreur de requête : {str(e)}"

    def generer_quiz_tennis(self, contexte=""):
        """
        Génère un quiz interactif spécifique au tennis avec une chaîne de pensée.
        """
        prompt = f"""
        Génère un quiz de tennis interactif avec une approche de chaîne de pensée :

        Étape 1 - Réflexion : 
        - Choisis un aspect unique du tennis
        - Réfléchis à une question qui testera les connaissances de manière originale

        Étape 2 - Génération de la question :
        - Crée une question qui nécessite une réflexion
        - Inclut des indices subtils
        - Rend la question engageante

        Étape 3 - Contexte et Indices :
        - Ajoute un contexte historique ou anecdotique
        - Prépare des indices progressifs

        Exemple de structure :
        Défi Tennis : [Titre du défi]
        Question : [Question originale]
        Indice 1 : [Premier indice subtil]
        Réponse attendue : [Réponse avec explication]

        {contexte}
        """

        # Utiliser la chaîne de pensée de Gemini
        reponse = self._requete_gemini(prompt)
        return f" {reponse}"

    def generer_quiz_football(self, contexte=""):
        """
        Génère un quiz de football avec une approche similaire.
        """
        prompt = f"""
        Crée un quiz de football interactif avec une approche de chaîne de pensée :
        - Choisis un aspect tactique ou historique unique
        - Génère une question qui stimule la réflexion
        - Inclut des indices progressifs

        {contexte}
        """
        
        reponse = self._requete_gemini(prompt)
        return f" {reponse}"

    def generer_quiz_general(self, contexte=""):
        """
        Génère un quiz sportif générique.
        """
        prompt = f"""
        Crée un quiz sportif interactif qui :
        - Couvre différents sports
        - Pose des questions originales
        - Stimule la réflexion et la curiosité

        {contexte}
        """
        
        reponse = self._requete_gemini(prompt)
        return f" {reponse}"

# Exemple d'utilisation
if __name__ == "__main__":
    api_key = "AIzaSyD8LKVDXO5zAFYbINcKHII-fiDa6rDexR4"
    synthesizer = GeminiSynthesizer(api_key)
    
    # Test du quiz de tennis
    print(synthesizer.generer_quiz_tennis())
