document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.task-checkbox').forEach(function(checkbox) {
        checkbox.addEventListener('click', function() {
            const taskId = checkbox.getAttribute('data-action-url').split('/').pop();
            
            fetch(checkbox.getAttribute('data-action-url'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ task_id: taskId }),
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    console.error('Error toggling task completion:', data.error);
                } else {
                    location.reload();
                }
            })
            .catch(error => {
                console.error('Error toggling task completion:', error);
            });
        });
    });

    // Function to get the CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});


