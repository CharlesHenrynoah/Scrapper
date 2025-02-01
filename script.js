// Variables globales pour le mode et la lecture
let currentMode = 'expert';
let isSpeaking = false;
let isPaused = false;
let currentSpeechSynthesis = null;
let currentUtterance = null;
let pausedPosition = 0;
let lastAIMessage = ''; // Variable globale pour stocker le dernier message de l'IA

// Fonction pour switcher de mode
function switchMode(mode) {
    currentMode = mode;
    const modeSwitch = document.getElementById('mode-switch');
    const expertBtn = document.getElementById('expert-btn');
    const funBtn = document.getElementById('fun-btn');
    
    // Mise à jour visuelle du switch et des boutons
    if (mode === 'expert') {
        modeSwitch.style.transform = 'translateX(0%)';
        expertBtn.classList.add('active');
        funBtn.classList.remove('active');
    } else if (mode === 'fun') {
        modeSwitch.style.transform = 'translateX(100%)';
        expertBtn.classList.remove('active');
        funBtn.classList.add('active');
    }
}

// Fonction de lecture/pause/reprise
function toggleSpeech(textToSpeak = null) {
    const speechText = textToSpeak || lastAIMessage;
    const listenBtn = document.getElementById('listen-btn');
    
    if (!speechText) {
        listenBtn.style.display = 'none';
        return;
    }

    listenBtn.style.display = 'block';
    
    // Si une synthèse vocale est en cours
    if (currentSpeechSynthesis) {
        if (isSpeaking && !isPaused) {
            // En cours de lecture, mettre en pause
            currentSpeechSynthesis.pause();
            isPaused = true;
            isSpeaking = false;
            listenBtn.textContent = '▶️ Reprendre';
            listenBtn.classList.remove('speaking');
            listenBtn.classList.add('paused');
        } else if (isPaused) {
            // En pause, reprendre
            currentSpeechSynthesis.resume();
            isPaused = false;
            isSpeaking = true;
            listenBtn.textContent = '⏸️ Pause';
            listenBtn.classList.remove('paused');
            listenBtn.classList.add('speaking');
        }
    } else {
        // Nouvelle lecture
        currentSpeechSynthesis = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance(speechText);
        utterance.lang = 'fr-FR'; // Langue française
        
        utterance.onstart = () => {
            isSpeaking = true;
            isPaused = false;
            listenBtn.textContent = '⏸️ Pause';
            listenBtn.classList.add('speaking');
            listenBtn.classList.remove('paused');
        };
        
        utterance.onend = () => {
            isSpeaking = false;
            isPaused = false;
            currentSpeechSynthesis = null;
            listenBtn.textContent = '🔊 Écouter';
            listenBtn.classList.remove('speaking', 'paused');
        };
        
        currentSpeechSynthesis.speak(utterance);
    }
}

// Fonction pour réinitialiser la synthèse vocale
function resetSpeechSynthesis() {
    if (currentSpeechSynthesis) {
        currentSpeechSynthesis.cancel();
        currentSpeechSynthesis = null;
    }
    
    isSpeaking = false;
    isPaused = false;
    
    // Réinitialiser le bouton de lecture
    const listenBtn = document.getElementById('listen-btn');
    listenBtn.style.display = 'none';
    listenBtn.textContent = '🔊 Écouter';
    listenBtn.classList.remove('paused', 'speaking');
}

// Modification de la fonction sendQuestion pour prendre en compte le mode
async function sendQuestion() {
    const userInput = document.getElementById('user-input');
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
        
        // Préparer le bouton d'écoute
        const listenBtn = document.getElementById('listen-btn');
        listenBtn.style.display = 'block';
        listenBtn.onclick = () => toggleSpeech(data.response);
    } catch (error) {
        addMessage('Désolé, une erreur est survenue.', 'ai');
        console.error('Erreur:', error);
    }
}

// Modification de la fonction sendMessage pour prendre en compte le mode
async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (message === '') return;

    // Ajouter le message de l'utilisateur
    addMessage(message, 'user');
    userInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message,
                mode: currentMode  // Ajouter le mode actuel
            }),
        });

        if (!response.ok) {
            throw new Error('Erreur de réponse du serveur');
        }

        const data = await response.json();
        addMessage(data.response, 'ai', true);
        
        // Préparer le bouton d'écoute
        const listenBtn = document.getElementById('listen-btn');
        listenBtn.style.display = 'block';
        listenBtn.onclick = () => toggleSpeech(data.response);
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

    // Fonction pour envoyer un message
    async function sendMessage() {
        const message = userInput.value.trim();
        
        if (message === '') return;

        // Ajouter le message de l'utilisateur
        addMessage(message, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: message,
                    mode: currentMode  // Utiliser le mode actuel
                }),
            });

            if (!response.ok) {
                throw new Error('Erreur de réponse du serveur');
            }

            const data = await response.json();
            addMessage(data.response, 'ai', true);
            
            // Préparer le bouton d'écoute
            const listenBtn = document.getElementById('listen-btn');
            listenBtn.style.display = 'block';
            listenBtn.onclick = () => toggleSpeech(data.response);
        } catch (error) {
            addMessage('Désolé, une erreur est survenue.', 'ai');
            console.error('Erreur:', error);
        }
    }

    // Événement pour le bouton d'envoi
    sendBtn.addEventListener('click', sendMessage);

    // Événement pour la touche Entrée
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Créer le conteneur du mode switch
    const modeSwitchContainer = document.createElement('div');
    modeSwitchContainer.classList.add('mode-switch-container');
    
    modeSwitchContainer.innerHTML = `
        <div class="mode-buttons">
            <button id="expert-btn" class="mode-btn active" onclick="switchMode('expert')">Mode Expert</button>
            <button id="fun-btn" class="mode-btn" onclick="switchMode('fun')">Fun Mode</button>
        </div>
        <div class="mode-switch-track">
            <div id="mode-switch" class="mode-switch-slider" style="transform: translateX(100%);"></div>
        </div>
    `;

    // Insérer avant le conteneur de chat
    chatContainer.insertBefore(modeSwitchContainer, chatContainer.firstChild);

    // Fonction pour faire défiler jusqu'au bas
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Gestion du mode Expert/Fun
    let currentMode = 'expert'; // Mode par défaut
});

function addMessage(message, sender, isAI = false) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Si c'est un message de l'IA, mettre à jour le dernier message
    if (isAI) {
        // Réinitialiser la synthèse vocale avant de mettre à jour
        resetSpeechSynthesis();
        
        lastAIMessage = message;
        const listenBtn = document.getElementById('listen-btn');
        
        // Mettre à jour le bouton de lecture
        if (message && message.trim() !== '') {
            listenBtn.style.display = 'block';
            listenBtn.onclick = () => toggleSpeech();
        } else {
            listenBtn.style.display = 'none';
        }
    }
}

// Ajouter un écouteur global pour réinitialiser la synthèse vocale
document.addEventListener('DOMContentLoaded', () => {
    const listenBtn = document.getElementById('listen-btn');
    listenBtn.style.display = 'none'; // Cacher par défaut
    
    window.addEventListener('beforeunload', resetSpeechSynthesis);
});

function showLoadingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const loadingElement = document.createElement('div');
    loadingElement.classList.add('loading-indicator');
    loadingElement.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner-circle"></div>
            <div class="spinner-ring"></div>
        </div>
        <div class="loading-text">Chargement en cours...</div>
    `;
    chatMessages.appendChild(loadingElement);
}

function hideLoadingIndicator() {
    const loadingElement = document.querySelector('.loading-indicator');
    if (loadingElement) {
        loadingElement.remove();
    }
}

// Modifier la fonction d'envoi pour inclure le chargement
function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (message) {
        showLoadingIndicator(); // Afficher l'indicateur de chargement
        
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message, mode: currentMode })
        })
        .then(response => response.json())
        .then(data => {
            hideLoadingIndicator(); // Masquer l'indicateur de chargement
            addMessage(message, 'user'); // Ajouter le message de l'utilisateur
            addMessage(data.response, 'ai', true); // Ajouter la réponse de l'IA
            userInput.value = '';
        })
        .catch(error => {
            hideLoadingIndicator(); // Masquer l'indicateur en cas d'erreur
            console.error('Erreur:', error);
            addMessage('Désolé, une erreur est survenue.', 'ai', true);
        });
    }
}
