function sendMessage(event) {
    event.preventDefault();
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    const conversationId = document.getElementById('conversation-id').value;

    if (message) {
        fetch(`/messaging/send-message-ajax/${conversationId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                messageInput.value = '';
                // Fetch and display new messages immediately after sending
                fetchAndDisplayMessages(conversationId);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function fetchAndDisplayMessages(conversationId) {
    fetch(`/messaging/api/messages/${conversationId}/`)
        .then(response => response.json())
        .then(data => {
            const messagesContainer = document.getElementById('messages-container');
            messagesContainer.innerHTML = ''; // Clear existing messages
            
            data.messages.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.className = `message ${message.is_sender ? 'sent' : 'received'}`;
                messageElement.innerHTML = `
                    <p class="message-content">${message.content}</p>
                    <small class="message-timestamp">${message.timestamp}</small>
                `;
                messagesContainer.appendChild(messageElement);
            });
            
            // Scroll to bottom after updating messages
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(error => console.error('Error:', error));
} 