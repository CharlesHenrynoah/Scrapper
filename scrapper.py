import requests

def poser_question_perplexity(question):
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
                "content": "Vous êtes un expert en sport. Soyez précis et concis."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            error_detail = response.json().get('error', {}).get('message', 'Erreur inconnue')
            print(f"Réponse complète de l'API : {response.json()}")
            return f"Erreur {response.status_code}: {error_detail}"
        
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return "Pas de réponse de l'API"
            
    except Exception as e:
        return f"Erreur lors de la requête : {str(e)}"

# Test avec différentes questions
questions = [
    "Qui est considéré comme le meilleur joueur de football en 2024 ? Donnez des statistiques récentes pour justifier.",
    "Quels sont les favoris pour la Ligue des Champions 2024 ?",
    "Donnez les statistiques de Mbappé pour la saison 2023-2024."
]

for question in questions:
    print("\nQuestion :", question)
    print("Réponse :", poser_question_perplexity(question))
