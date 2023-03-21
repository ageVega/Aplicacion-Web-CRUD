// main.js
const taskForm = document.querySelector('#taskForm');
const taskList = document.querySelector('#taskList');

let tareas = [];

let editing = false;
let tareaId = null;


function priorityText(priority) {
    switch (parseInt(priority)) {
        case 1: return "Crítica";
        case 2: return "Urgente";
        case 3: return "Importante";
        case 4: return "Moderado";
        case 5: return "Menor";
        default: return "";
    }
}

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/api/tasks');
    const data = await response.json();
    tareas = data;
    renderTask(tareas);
});

taskForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const task = taskForm['tarea'].value;
    const priority = taskForm['prioridad'].value;

    if (!editing) {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task,
                priority
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
                priority
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
        taskItem.innerHTML = `
            <header class="d-flex justify-content-between align-items-center">
                <h3>${tarea.priority}. ${priorityText(tarea.priority)}</h3>
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
``
