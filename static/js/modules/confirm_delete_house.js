// confirm_delete_house.js

export function deleteHouseButtonEvent() {
    const deleteForm = document.getElementById('delete-form');
    if (!deleteForm) return;

    deleteForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const password = document.getElementById('password').value;
        const houseId = sessionStorage.getItem('house_id');

        // Primero, confirma la contraseña
        const confirmResponse = await fetch(`/auth/confirm_password/${houseId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: password }),
        });

        const confirmData = await confirmResponse.json();

        if (!confirmResponse.ok) {
            alert('Error: ' + confirmData.message);
            return;
        }

        // Si la contraseña es correcta, pregúntale al usuario si realmente quiere eliminar la casa
        const deleteConfirmed = confirm('¿Estás seguro de que quieres eliminar esta casa? Esta acción no se puede deshacer.');
        
        if (!deleteConfirmed) {
            return;
        }

        // Finalmente, realiza la petición para eliminar la casa
        const deleteResponse = await fetch(`/auth/cancel/${houseId}`, {
            method: 'DELETE'
        });
        const deleteData = await deleteResponse.json();

        if (!deleteResponse.ok) {
            alert('Error: ' + deleteData.message);
            return;
        }

        alert(deleteData.message);
        window.location.href = '/home';
    });
}
