// priorityManager.js
import { priorityNames } from '../main.js'; 


export function updatePrioritySelect(priorityNames) {
    let prioritySelect = document.querySelector('select[name="prioridad"]');

    if (!prioritySelect) { return; }  // No intentar actualizar el select si no existe
    
    priorityNames.sort((a, b) => a.level - b.level);  // Ordenar las prioridades por su nivel
    
    prioritySelect.innerHTML = '';
    priorityNames.forEach(priority => {
        const option = document.createElement('option');
        option.value = priority.level;
        option.textContent = `${priority.level}. ${priority.name}`;
        prioritySelect.appendChild(option);
    });
}

export function priorityFormEvent(priorityNames, houseId) {
    const priorityNameForm = document.querySelector('#priorityNameForm');
    if (!priorityNameForm) return;
    
    priorityNameForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const level = priorityNameForm['priorityLevel'].value;
        const name = priorityNameForm['priorityName'].value;
        const house_id = houseId;

        const response = await fetch(`/api/priority_names/${level}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name,
                house_id
            })
        });

        const updatedPriorityName = await response.json();

        priorityNames = priorityNames.map(p => p.level === updatedPriorityName.level ? updatedPriorityName : p);

        //updatePrioritySelect(priorityNames);
        clearPriorityNameForm();
    });
}

export function resetPriorityEvent() {
    const resetPriorityNamesForm = document.querySelector('#resetPriorityNamesForm');
    if (!resetPriorityNamesForm) return;
    
    resetPriorityNamesForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const response = await fetch('/api/reset_priority_names', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const updatedPriorityNames = await response.json();
            priorityNames = updatedPriorityNames;
            updatePrioritySelect(priorityNames);
        }
    });
}

export function setWeekdayNamesEvent() {
    const setWeekdayNamesForm = document.querySelector('#setWeekdayNamesForm');
    if (!setWeekdayNamesForm) return;

    setWeekdayNamesForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const response = await fetch('/api/set_weekday_priority_names', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const updatedPriorityNames = await response.json();
            priorityNames = updatedPriorityNames;
            updatePrioritySelect(priorityNames);
        }
    });
}


export function clearPriorityNameForm() {
    const priorityNameForm = document.querySelector('#priorityNameForm');
    if (!priorityNameForm) return;

    priorityNameForm['priorityLevel'].value = '';
    priorityNameForm['priorityName'].value = '';
    console.log('Formulario limpiado'); 
}
