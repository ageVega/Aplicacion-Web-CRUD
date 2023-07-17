// main.js
const taskForm = document.querySelector('#taskForm');
const taskList = document.querySelector('#taskList') ? document.querySelector('#taskList') : null;
const priorityNameForm = document.querySelector('#priorityNameForm');

const houseId = '{{current_user.id}}'; 

const prioritySelect = document.querySelector('select[name="prioridad"]');

let tareas = [];
let priorityNames = [];

let editing = false;
let tareaId = null;


function priorityText(priority) {
    const priorityName = priorityNames.find(p => p.level === parseInt(priority)).name;
    return priorityName || '';
}

window.addEventListener('DOMContentLoaded', async () => {
    clearHouseIdOnLogout();
    if (taskList) {  // Agrega esta verificación
        const responseTasks = await fetch(`/api/tasks?house_id=${houseId}`);
        const dataTasks = await responseTasks.json();
        tareas = dataTasks;
    }

    const responsePriorities = await fetch(`/api/priority_levels?house_id=${houseId}`);
    const dataPriorities = await responsePriorities.json();
    priorityNames = dataPriorities;
    
    updatePrioritySelect(priorityNames);  // Llama a la nueva función

    if (taskList) {  // Agrega esta verificación
        renderTask(tareas);
    }
});


if (taskForm) { 
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const task = taskForm['tarea'].value;
        const priority = taskForm['prioridad'].value;
        const house_id = houseId;

        if (!editing) {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    task,
                    priority,
                    house_id
                })
            });

            const data = await response.json();
            tareas.push(data);
        } else {
            const response = await fetch(`/api/tasks/${tareaId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    task,
                    priority,
                    house_id
                })
            });

            const updatedTask = await response.json();
            tareas = tareas.map(tarea => tarea.id === updatedTask.id ? updatedTask : tarea);
            editing = false;
            tareaId = null;
        }

        reloadPage();
        taskForm.reset();
    });
}

if (priorityNameForm) { 
    priorityNameForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const level = priorityNameForm['priorityLevel'].value;
        const name = priorityNameForm['priorityName'].value;
        const house_id = houseId;

        // Tienes que cambiar esta URL por la correspondiente a tu ruta en Flask para actualizar el nombre de la prioridad
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

        // Aquí debes actualizar la variable priorityNames y luego llamar a la función updatePrioritySelect() y renderTask()
        priorityNames = priorityNames.map(p => p.level === updatedPriorityName.level ? updatedPriorityName : p);
        updatePrioritySelect(priorityNames);
        renderTask(tareas);
    });
}

async function reloadPage() {
    const response = await fetch('/api/tasks');
    const data = await response.json();
    tareas = data;
    renderTask(tareas);
}

function renderTask(tareas) {
    taskList.innerHTML = '';
    tareas = sortTasks(tareas, true);

    tareas.forEach(tarea => {
        const taskItem = document.createElement('li');
        taskItem.classList = 'list-group-item list-group-item-dark my-2';
        const priorityName = priorityNames.find(p => p.level === tarea.priority).name;
        taskItem.innerHTML = `
            <header class="d-flex justify-content-between align-items-center">
                <h3>${tarea.priority}. ${priorityName}</h3>
                <div>
                    <button class="btn-edit btn btn-secondary btn-sm">edit</button>
                    <button class="btn-delete btn btn-danger btn-sm">delete</button>
                </div>
            </header>
            <p>${tarea.task}</p>
        `;

        const btnDelete = taskItem.querySelector('.btn-delete');

        btnDelete.addEventListener("click", async () => {
            const response = await fetch(`/api/tasks/${tarea.id}`, {
                method: 'DELETE'
            });
            const data = await response.json();

            tareas = tareas.filter(tarea => tarea.id !== data.id);

            renderTask(tareas);
        });

        const btnEdit = taskItem.querySelector('.btn-edit');

        btnEdit.addEventListener("click", async () => {
            const response = await fetch(`/api/tasks/${tarea.id}`);
            const data = await response.json();

            taskForm["tarea"].value = data.task;
            taskForm["prioridad"].value = data.priority;

            editing = true;
            tareaId = data.id;
        });

        taskList.append(taskItem);
    });
}

function sortTasks(tareas, sortByPriority = true) {
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

function clearHouseIdOnLogout() {
    const urlPath = window.location.pathname;
    if (urlPath === '/' || urlPath === '/home') {
        sessionStorage.removeItem('user_id');
    }
}

function updatePriorityNames(priorityNames) {
    const selectPriority = taskForm['prioridad'];
    selectPriority.innerHTML = '';
    priorityNames.forEach(priority => {
        const option = document.createElement('option');
        option.value = priority.level;
        option.textContent = priority.name;
        selectPriority.appendChild(option);
    });
}

function updatePrioritySelect(priorityNames) {
    prioritySelect.innerHTML = '';
    priorityNames.forEach(priority => {
        const option = document.createElement('option');
        option.value = priority.level;
        option.textContent = `${priority.level}. ${priority.name}`;
        prioritySelect.appendChild(option);
    });
}
