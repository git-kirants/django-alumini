console.log('Conversation detail script loaded.');
const messagesContainer = document.getElementById('messages-container');
const conversationId = {{ conversation.id }};

// Handle form submission
document.getElementById('message-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = this;
    // Add your form submission logic here
});

function appendMessage(message) {
    // Logic to append message to the messages container
}

function pollNewMessages() {
    fetch(`/messaging/api/messages/${conversationId}/?after=${lastMessageId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                data.messages.forEach(message => appendMessage(message));
            }
        })
        .catch(error => console.error('Error:', error));
}

// Start polling
setInterval(pollNewMessages, 3000);
