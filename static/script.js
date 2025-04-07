let session = {};

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    appendMessage('You: ' + message);
    input.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message, session: session })
    })
    .then(response => {
        if (response.status === 403) {
            window.location.href = '/login';
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            appendMessage('Bot: ' + data.response);
            session = data.session;
        }
    });
}

function appendMessage(text) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});