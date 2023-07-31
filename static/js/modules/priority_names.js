// priority_names.js
import * as Main            from '../main.js'; 
import * as SimpleFunctions from './simpleFunctions.js';

// Formularios en priority_names.html
export function priorityNameFormUpdate(priorityNames, houseId) {
    const priorityNameForm = document.querySelector('#priorityNameForm');
    if (!priorityNameForm) return;
    
    priorityNameForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const level = priorityNameForm['priorityLevel'].value;
        const name = priorityNameForm['priorityName'].value;
        const house_id = houseId;

        const response = await fetch(`/priorities/priority_names/${level}`, {
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

        SimpleFunctions.clearPriorityNameForm();
    });
}

function FormSubmitHandler(formId, apiEndpoint) {
    const form = document.querySelector(formId);
    if (!form) return;
    
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const response = await fetch(apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const updatedPriorityNames = await response.json();
            Main.setPriorityNames(updatedPriorityNames);

            window.location.href = '/dashboard';
        }
    });
}

export function resetPriorityNamesButton() {
    FormSubmitHandler('#resetPriorityNamesForm', '/priorities/reset_priority_names');
}

export function setEmptyNamesButton() {
    FormSubmitHandler('#setEmptyNamesForm', '/priorities/set_empty_priority_names');
}

export function setWeekdayNamesButton() {
    FormSubmitHandler('#setWeekdayNamesForm', '/priorities/set_weekday_priority_names');
}
