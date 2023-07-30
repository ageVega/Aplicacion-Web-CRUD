// dashboard.js
import * as Main            from '../main.js'; 
import * as SimpleFunctions from './simpleFunctions.js';

// Formularios en dashboard.html        ////////////////////////////////
export function taskFormSubmit(houseId) {
    const taskForm = document.querySelector('#taskForm');
    if (!taskForm) return;
    
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        let tareas = Main.getTareas();
        let editing = Main.getEditing();
        let tareaId = Main.getTareaId();

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
            Main.setTareas(tareas);
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
            tareaId = null;

            Main.setTareas(tareas);
            Main.setEditing(editing);
            Main.setTareaId(tareaId);
        }

        taskForm.reset();
        renderTasks(Main.getTareas(), Main.getPriorityNames());
    });
}

export async function updatePriorityNames() {
    const responsePriorities = await fetch(`/api/priority_names`);
    const dataPriorities = await responsePriorities.json();
    Main.setPriorityNames(dataPriorities);
}

export function updatePrioritySelect() {
    let prioritySelect = document.querySelector('select[name="prioridad"]');

    if (!prioritySelect) { return; }  // No intentar actualizar el select si no existe

    let priorityNames = Main.getPriorityNames();  // Obtenemos priorityNames desde el módulo principal
    
    priorityNames.sort((a, b) => a.level - b.level);  // Ordenar las prioridades por su nivel
    
    prioritySelect.innerHTML = '';
    priorityNames.forEach(priority => {
        const option = document.createElement('option');
        option.value = priority.level;
        option.textContent = `${priority.level}. ${priority.name}`;
        prioritySelect.appendChild(option);
    });
}

export async function updateTareas() {
    const responseTasks = await fetch(`/api/tasks`);
    const dataTasks = await responseTasks.json();
    Main.setTareas(dataTasks);
}

export function renderTasks(tareas, priorityNames) {
    if (!taskList) return;

    taskList.innerHTML = '';
    tareas = SimpleFunctions.sortTasks(tareas, true);

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

            renderTasks(tareas, priorityNames);
        });

        const btnEdit = taskItem.querySelector('.btn-edit');

        btnEdit.addEventListener("click", async () => {
            const response = await fetch(`/api/tasks/${tarea.id}`);
            const data = await response.json();

            taskForm["tarea"].value = data.task;
            taskForm["prioridad"].value = data.priority;

            Main.setEditing(true);
            Main.setTareaId(data.id);
        });

        taskList.append(taskItem);
    });
}
