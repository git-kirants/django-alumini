function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function markAsRead(notificationId) {
    fetch(`/notifications/mark-read/${notificationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            const notification = document.getElementById(`notification-${notificationId}`);
            notification.classList.remove('border-l-4', 'border-blue-500');
            const markReadBtn = notification.querySelector('button[onclick^="markAsRead"]');
            if (markReadBtn) markReadBtn.remove();
        }
    })
    .catch(error => console.error('Error:', error));
}

function deleteNotification(notificationId) {
    if (!confirm('Are you sure you want to delete this notification?')) return;
    fetch(`/notifications/delete/${notificationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            const notification = document.getElementById(`notification-${notificationId}`);
            notification.classList.add('opacity-0');
            setTimeout(() => notification.remove(), 200);
        }
    })
    .catch(error => console.error('Error:', error));
}

function markAllAsRead() {
    fetch('/notifications/mark-all-read/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            document.querySelectorAll('.border-l-4').forEach(notification => {
                notification.classList.remove('border-l-4', 'border-blue-500');
            });
        }
    })
    .catch(error => console.error('Error:', error));
}

function clearAllNotifications() {
    if (!confirm('Are you sure you want to delete all notifications? This action cannot be undone.')) return;
    fetch('/notifications/clear-all/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            const notifications = document.querySelectorAll('[id^="notification-"]');
            notifications.forEach(notification => {
                notification.classList.add('opacity-0');
            });
            setTimeout(() => {
                const container = document.getElementById('notifications-container');
                container.innerHTML = '<div class="text-center py-12">No Notifications</div>';
            }, 200);
        }
    })
    .catch(error => console.error('Error:', error));
}
