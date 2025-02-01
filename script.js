// Variables globales pour le mode
let currentMode = 'pronostics';

// Fonction pour switcher de mode
function switchMode(mode) {
    currentMode = mode;
    const modeSwitch = document.getElementById('mode-switch');
    const pronosticsLabel = document.getElementById('pronostics-label');
    const rechercheLabel = document.getElementById('recherche-label');
    const funModeLabel = document.getElementById('fun-mode-label');

    // Réinitialiser le chat
    document.getElementById('chat-messages').innerHTML = '';

    // Mise à jour visuelle du switch
    if (mode === 'pronostics') {
        modeSwitch.style.transform = 'translateX(0%)';
        pronosticsLabel.classList.add('active');
        rechercheLabel.classList.remove('active');
        funModeLabel.classList.remove('active');
        sendInitialMessage('pronostics');
    } else if (mode === 'recherche') {
        modeSwitch.style.transform = 'translateX(100%)';
        pronosticsLabel.classList.remove('active');
        rechercheLabel.classList.add('active');
        funModeLabel.classList.remove('active');
        sendInitialMessage('recherche');
    } else if (mode === 'fun') {
        modeSwitch.style.transform = 'translateX(200%)';
        pronosticsLabel.classList.remove('active');
        rechercheLabel.classList.remove('active');
        funModeLabel.classList.add('active');
        sendInitialMessage('fun');
    }
}

// Fonction pour envoyer un message initial selon le mode
function sendInitialMessage(mode) {
    const initialMessages = {
        'pronostics': "🏆 Bienvenue en mode Pronostics ! Prêt à analyser les matchs et trouver les meilleures cotes ?",
        'recherche': "🔍 Mode Recherche activé. Posez-moi n'importe quelle question sportive !",
        'fun': "🎲 Mode Fun activé ! Prêt pour des quiz, des défis et de l'humour sportif ?"
    };

    addMessage(initialMessages[mode], 'ai', true);
}

// Modification de la fonction sendQuestion pour prendre en compte le mode
async function sendQuestion() {
    const question = userInput.value.trim();
    if (!question) return;

    // Add user message
    addMessage(question, 'user');
    userInput.value = '';

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                question: question,
                mode: currentMode  // Ajouter le mode actuel
            }),
        });

        if (!response.ok) {
            throw new Error('Erreur de communication avec le serveur');
        }

        const data = await response.json();
        addMessage(data.response, 'ai', true);
    } catch (error) {
        addMessage('Désolé, une erreur est survenue.', 'ai');
        console.error('Erreur:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const chatContainer = document.getElementById('chat-container');

    // Vérification de l'existence des éléments
    if (!userInput || !sendBtn || !chatMessages || !chatContainer) {
        console.error('Un ou plusieurs éléments essentiels sont manquants');
        return;
    }

    // Fonction de lecture à voix haute
    function lireTexteAVoixHaute(texte) {
        // Vérifier si la synthèse vocale est supportée
        if ('speechSynthesis' in window) {
            // Arrêter toute lecture en cours
            window.speechSynthesis.cancel();

            // Créer un nouvel objet utterance
            const utterance = new SpeechSynthesisUtterance(texte);
            
            // Configuration de la voix
            utterance.lang = 'fr-FR';  // Français
            utterance.rate = 0.9;      // Vitesse de lecture
            utterance.pitch = 1;       // Tonalité

            // Liste des voix disponibles
            const voices = window.speechSynthesis.getVoices();
            const voixFrancaise = voices.find(voice => 
                voice.lang === 'fr-FR' || voice.lang.startsWith('fr-')
            );

            if (voixFrancaise) {
                utterance.voice = voixFrancaise;
            }

            // Lecture à voix haute
            window.speechSynthesis.speak(utterance);
        } else {
            alert('La lecture à voix haute n\'est pas supportée sur ce navigateur.');
        }
    }

    function addMessage(message, sender, isVoiceEnabled = false) {
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message', sender === 'user' ? 'user-message' : 'ai-message');

        // Créer le contenu du message
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.textContent = message;

        // Conteneur pour les actions du message
        const messageActionsContainer = document.createElement('div');
        messageActionsContainer.classList.add('message-actions');

        // Bouton de baguette en bas du message
        const ecouteBaguette = document.createElement('button');
        ecouteBaguette.classList.add('ecoute-baguette');
        ecouteBaguette.innerHTML = '🔊 Écouter';
        ecouteBaguette.style.display = isVoiceEnabled ? 'block' : 'none';

        // Gestionnaire d'événement pour la lecture vocale
        ecouteBaguette.addEventListener('click', () => {
            const utterance = new SpeechSynthesisUtterance(message);
            utterance.lang = 'fr-FR';  // Langue française
            
            // Animation du bouton pendant la lecture
            ecouteBaguette.classList.add('speaking');
            
            utterance.onend = () => {
                ecouteBaguette.classList.remove('speaking');
            };
            
            window.speechSynthesis.speak(utterance);
        });

        // Assembler les éléments
        messageContainer.appendChild(messageContent);
        messageActionsContainer.appendChild(ecouteBaguette);
        messageContainer.appendChild(messageActionsContainer);

        // Ajouter au conteneur de messages
        chatMessages.appendChild(messageContainer);

        // Scroll automatique
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Créer le conteneur du mode switch
    const modeSwitchContainer = document.createElement('div');
    modeSwitchContainer.classList.add('mode-switch-container');
    
    modeSwitchContainer.innerHTML = `
        <div class="mode-labels">
            <span id="pronostics-label" class="mode-label active" onclick="switchMode('pronostics')">Pronostics</span>
            <span id="recherche-label" class="mode-label" onclick="switchMode('recherche')">Recherche</span>
            <span id="fun-mode-label" class="mode-label" onclick="switchMode('fun')">Fun Mode</span>
        </div>
        <div class="mode-switch-track">
            <div id="mode-switch" class="mode-switch-slider"></div>
        </div>
    `;

    // Insérer avant le conteneur de chat
    chatContainer.insertBefore(modeSwitchContainer, chatContainer.firstChild);

    // Message initial
    sendInitialMessage('pronostics');

    sendBtn.addEventListener('click', sendQuestion);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendQuestion();
        }
    });
});
