// simpleFunctions.js

export function clearHouseIdOnLogout() {
    const urlPath = window.location.pathname;
    if (urlPath === '/' || urlPath === '/home') {
        sessionStorage.removeItem('house_id');
    }
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

export function clearPriorityNameForm() {
    const priorityNameForm = document.querySelector('#priorityNameForm');
    if (!priorityNameForm) return;

    priorityNameForm['priorityLevel'].value = '';
    priorityNameForm['priorityName'].value = '';
}
