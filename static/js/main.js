// main.js
import * as TaskManager     from './modules/taskManager.js';
import * as PriorityManager from './modules/priorityManager.js';
import * as UserManager     from './modules/userManager.js';

import { editing, tareaId } from './modules/taskManager.js'; 

export const houseId = sessionStorage.getItem('house_id');

export let tareas = [];
export let priorityNames = [];

async function initializeApp() {
    UserManager.deleteHouseButtonEvent();

    TaskManager.taskFormEvent(tareas, priorityNames, editing, tareaId, houseId);
    TaskManager.sortTasks(tareas);

    PriorityManager.priorityFormEvent(priorityNames, houseId);
    PriorityManager.resetPriorityEvent();
    PriorityManager.setWeekdayNamesEvent();
    PriorityManager.clearPriorityNameForm();
}

window.addEventListener('DOMContentLoaded', async () => {
    await initializeApp();

    UserManager.clearHouseIdOnLogout();

    const taskList = document.querySelector('#taskList') ? document.querySelector('#taskList') : null;
    if (taskList) {  
        const responseTasks = await fetch(`/api/tasks?house_id=${houseId}`);
        const dataTasks = await responseTasks.json();
        tareas = dataTasks;
    
        const responsePriorities = await fetch(`/api/priority_levels?house_id=${houseId}`);
        responsePriorities.json().then(dataPriorities => {
            priorityNames = dataPriorities;    
            PriorityManager.updatePrioritySelect(priorityNames);
            TaskManager.renderTask(tareas, priorityNames);
        });
    }
    
});
