let conversationHistory = [];
let lastAgent = null;

document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});

function appendMessage(sender, message, agentName = null) {
    const messagesDiv = document.getElementById('messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'You' ? 'user' : 'agent');
    
    const senderLabel = document.createElement('div');
    senderLabel.classList.add('message-sender');
    senderLabel.textContent = sender === 'You' ? 'You' : (agentName || 'Support');
    
    const bubble = document.createElement('div');
    bubble.classList.add('message-bubble');
    bubble.textContent = message;
    
    messageDiv.appendChild(senderLabel);
    messageDiv.appendChild(bubble);

    if (sender !== 'You') {
        const voiceBtn = document.createElement('button');
        voiceBtn.classList.add('voice-btn');
        voiceBtn.textContent = '🔊 Listen';
        voiceBtn.onclick = () => playVoice(message);
        messageDiv.appendChild(voiceBtn);
    }

    messagesDiv.appendChild(messageDiv);
    document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;
}

async function playVoice(text) {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/voice', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();

    } catch (error) {
        console.error('Voice error:', error);
    }
}

async function sendMessage() {
    const userInputField = document.getElementById('user-input');
    const userInput = userInputField.value.trim();

    if (userInput === '') return;

    appendMessage('You', userInput);
    conversationHistory.push({ role: 'user', content: userInput });
    
    userInputField.value = '';

    try {
        const response = await fetch('http://127.0.0.1:8000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: userInput,
                context: { 
                    history: conversationHistory,
                    last_agent: lastAgent
                }
            })
        });

        const data = await response.json();
        appendMessage('Agent', data.response, data.agent_used);
        conversationHistory.push({ role: 'assistant', content: data.response });
        if (data.agent_used) lastAgent = data.agent_used.replace('_agent', '');

    } catch (error) {
        appendMessage('Agent', 'Sorry, there was an error processing your request.');
        console.error('Error:', error);
    }
}