// confirm_delete_house.js

// Formularios en confirm_delete_house.html
export function deleteHouseButtonEvent() {
    const deleteHouseButton = document.getElementById('delete-house-btn');
    if (!deleteHouseButton) return;

    deleteHouseButton.addEventListener('click', async function() {
        const houseId = this.getAttribute('data-house-id');
        if (confirm('¿Estás seguro de que quieres eliminar esta casa? Esta acción no se puede deshacer.')) {
            const response = await fetch(`/auth/cancel/${houseId}`, {
                method: 'DELETE'
            });
            const data = await response.json();

            if (response.ok) {
                alert(data.message);
                window.location.href = '/home';
            } else {
                alert('Error: ' + data.message);
            }
        }
    });
}

document.getElementById('delete-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const password = document.getElementById('password').value;
    const houseId = sessionStorage.getItem('house_id');

    const response = await fetch(`/auth/confirm_password/${houseId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: password }),
    });

    const data = await response.json();

    if (response.ok) {
        const deletionConfirmed = confirm('¿Estás seguro de que quieres eliminar esta casa? Esta acción no se puede deshacer.');
        
        if (deletionConfirmed) {
            const deletionResponse = await fetch(`/auth/cancel/${houseId}`, {
                method: 'DELETE'
            });
            const deletionData = await deletionResponse.json();

            if (deletionResponse.ok) {
                alert(deletionData.message);
                window.location.href = '/home';
            } else {
                alert('Error: ' + deletionData.message);
            }
        }
    } else {
        alert('Error: ' + data.message);
    }
});
