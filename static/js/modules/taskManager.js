// taskManager.js
export let editing = false;
export let tareaId = null;

const taskList = document.querySelector('#taskList') ? document.querySelector('#taskList') : null;

export function renderTask(tareas, priorityNames) {
    if (!taskList) return;

    taskList.innerHTML = '';
    tareas = sortTasks(tareas, true);

    tareas.forEach(tarea => {
        const taskItem = document.createElement('li');
        taskItem.classList = 'list-group-item list-group-item-dark my-2';
        const priority = priorityNames.find(p => p.level === tarea.priority);
        const priorityName = priority ? priority.name : 'Nombre de prioridad no encontrado';
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

            renderTask(tareas, priorityNames);
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

export function taskFormEvent(tareas, priorityNames, editing, tareaId, houseId) {
    const taskForm = document.querySelector('#taskForm');
    if (!taskForm) return;
    
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const tarea = taskForm['tarea'].value;
        const prioridad = taskForm['prioridad'].value;
        const house_id = houseId;

        if (!editing) {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    task: tarea,
                    priority: prioridad,
                    house_id
                })
            });

            const newTask = await response.json();
            tareas.push(newTask);
        } else {
            const response = await fetch(`/api/tasks/${tareaId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    task: tarea,
                    priority: prioridad,
                })
            });

            const updatedTask = await response.json();
            tareas = tareas.map(tarea => tarea.id === updatedTask.id ? updatedTask : tarea);
            editing = false;
        }

        taskForm.reset();
        renderTask(tareas, priorityNames);
    });
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
