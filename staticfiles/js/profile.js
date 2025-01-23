document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.getElementById('message-form');
    const messagesContainer = document.getElementById('messages-container');

    if (messageForm) {
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(messageForm);
            fetch('{% url "messaging:send_message_ajax" conversation.id %}', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Add new message to the container
                    const messageHTML = `
                        <div class="mb-4 ml-auto max-w-[75%]">
                            <div class="bg-blue-600 text-white rounded-lg px-4 py-2">
                                ${data.message.content}
                            </div>
                            <div class="flex items-center mt-1 justify-end">
                                <span class="text-xs text-gray-500">
                                    ${data.message.timestamp}
                                </span>
                            </div>
                        </div>
                    `;
                    messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
                    messageForm.reset();
                }
            });
        });
    }
});
