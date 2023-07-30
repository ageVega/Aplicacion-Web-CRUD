// config.js

// Formularios en config.html           ////////////////////////////////
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
