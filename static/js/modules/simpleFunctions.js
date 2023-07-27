// simpleFunctions.js
import * as Main from '../main.js'; 

export async function updateTareas() {
    const responseTasks = await fetch(`/api/tasks`);
    const dataTasks = await responseTasks.json();
    Main.setTareas(dataTasks);
}


export async function updatePriorityNames() {
    const responsePriorities = await fetch(`/api/priority_names`);
    const dataPriorities = await responsePriorities.json();
    Main.setPriorityNames(dataPriorities);
}


export function sortTasks(tareas, sortByPriority = true) {
    return tareas.sort((a, b) => {
        if (sortByPriority) {
            if (a.priority < b.priority) return -1;
            if (a.priority > b.priority) return 1;
        }
        if (a.task < b.task) return -1;
        if (a.task > b.task) return 1;
        return 0;
    });
}


export function clearHouseIdOnLogout() {
    const urlPath = window.location.pathname;
    if (urlPath === '/' || urlPath === '/home') {
        sessionStorage.removeItem('house_id');
    }
}


export function clearPriorityNameForm() {
    const priorityNameForm = document.querySelector('#priorityNameForm');
    if (!priorityNameForm) return;

    priorityNameForm['priorityLevel'].value = '';
    priorityNameForm['priorityName'].value = '';
    console.log('Formulario limpiado'); 
}


export function updatePrioritySelect() {
    let prioritySelect = document.querySelector('select[name="prioridad"]');

    if (!prioritySelect) { return; }  // No intentar actualizar el select si no existe

    priorityNames = Main.getPriorityNames();
    
    priorityNames.sort((a, b) => a.level - b.level);  // Ordenar las prioridades por su nivel
    
    prioritySelect.innerHTML = '';
    priorityNames.forEach(priority => {
        const option = document.createElement('option');
        option.value = priority.level;
        option.textContent = `${priority.level}. ${priority.name}`;
        prioritySelect.appendChild(option);
    });
}
