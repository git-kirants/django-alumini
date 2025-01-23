console.log('Conversation detail script loaded.');

document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('messages-container');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.querySelector('textarea[name="content"]');
    
    if (!messagesContainer || !messageForm || !messageInput) {
        console.error('Required elements not found');
        return;
    }

    const conversationId = messagesContainer.dataset.conversationId;
    let lastMessageId = messagesContainer.dataset.lastMessageId || 0;

    // Handle form submission
    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const content = messageInput.value.trim();
        if (!content) return;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(messageForm.action || window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: new URLSearchParams({
                'content': content
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                messageInput.value = '';
                appendMessage(data.message);
                lastMessageId = data.message.id;
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            } else {
                console.error('Error sending message:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function appendMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-4 ${message.is_sender ? 'ml-auto' : ''} max-w-[85%] md:max-w-[75%]`;
        messageDiv.setAttribute('data-message-id', message.id);
        
        messageDiv.innerHTML = `
            <!-- Message content -->
            <div class="${message.is_sender ? 'bg-blue-600/90' : 'bg-slate-700/90'} 
                        backdrop-blur-md rounded-xl px-3 py-2 md:px-4 md:py-2 shadow-lg text-white text-sm md:text-base">
                ${message.content}
            </div>
            <!-- Message metadata -->
            <div class="flex items-center mt-1 ${message.is_sender ? 'justify-end' : ''} space-x-2">
                <span class="text-xs text-slate-400">
                    ${message.timestamp}
                </span>
                ${!message.is_sender ? `
                    <button onclick="window.location.href='/messaging/report_message/${message.id}/'"
                            class="text-xs text-slate-400 hover:text-red-400 transition-colors duration-200">
                        <i class="fas fa-flag"></i>
                    </button>
                ` : ''}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function pollNewMessages() {
        fetch(`/messaging/api/messages/${conversationId}/?after=${lastMessageId}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success' && data.messages) {
                    data.messages.forEach(message => {
                        appendMessage({
                            id: message.id,
                            content: message.content,
                            timestamp: message.timestamp,
                            is_sender: message.is_sender
                        });
                        lastMessageId = Math.max(lastMessageId, message.id);
                    });
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Start polling if we have a conversation ID
    if (conversationId) {
        setInterval(pollNewMessages, 3000);
    }

    // Initial scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
});
