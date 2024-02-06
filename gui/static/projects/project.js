const onMessageCallbacks = {
    'task_create': handleCreate,
    'task_update': handleUpdate,
    'task_delete': handleDelete,
};


function setupSocket(projectId) {
    const socketSingle = new WebSocket(`ws://127.0.0.1:8000/ws/${projectId }`);

    socketSingle.onmessage = function (e) {
        console.log('Received message:', e.data);
        if (e.data === 'connected') {
            return;
        }
        const event = JSON.parse(e.data);
        const type = event.type;
        onMessageCallbacks[type](event.task);
    };
}

function setupDeleteProject(projectId) {
    document.getElementById('project-delete-icon')?.addEventListener('click', function () {
        fetch(`http://localhost:8000/api/projects/${projectId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(() => window.location.href = '/projects')
            .then(() => console.log(`Project {{ project.id }} deleted`))
            .catch(err => alert(err));
    });
}

function handleCreate(task) {
    fetch(`http://localhost:8000/tasks/${task.id}/card`)
        .then(response => response.text())
        .then(data => {
            const taskDiv = document.createElement('div');
            taskDiv.innerHTML = data;
            const column = document.getElementById(`column-${justifyStatus(task.status)}`);
            column.appendChild(taskDiv.querySelector('.task'));
            setupTask(task.id);
        });
}

function handleUpdate(task) {
    const taskDiv = document.getElementById(`task-${task.id}`);
    const taskIdField = taskDiv?.querySelector('.task-id');
    const taskTitleField = taskDiv?.querySelector('.task-title');
    const taskTypeField = taskDiv?.querySelector('.task-type');
    const taskStatusField = taskDiv?.querySelector('.task-status');
    const taskAssigneeField = taskDiv?.querySelector('.task-assignee');

    taskTitleField.innerHTML = task.title;
    taskTypeField.innerHTML = task.type;
    taskStatusField.innerHTML = `Status: ${task.status}`;
    taskAssigneeField.innerHTML = `Assignee: ${task.assignee}`;

    const taskHeader = taskDiv.querySelector('.task-header');
    taskHeader.classList.remove('STORY', 'BUG', 'RESEARCH');
    taskHeader.classList.add(task.type);

    const column = document.getElementById(`column-${justifyStatus(task.status)}`);
    column.appendChild(taskDiv);
}

function handleDelete(task) {
    const taskDiv = document.getElementById(`task-${task.id}`);
    taskDiv?.remove();
}

function justifyStatus(status) {
    return status.toLowerCase().replace(' ', '-');
}

function setupTask(id) {
    const taskDiv = document.getElementById(`task-${id}`);
    const taskBody = document.getElementById(`task-body-${id}`);

    taskBody.addEventListener('click', function () {
        window.location.href = `/tasks/${id}`;
    });

    const statusP = document.getElementById(`${id}-status`);

    let columnOpen = document.getElementById('column-open');
    let columnInProgress = document.getElementById('column-in-progress');
    let columnDone = document.getElementById('column-done');

    const leftArrow = document.getElementById(`left-arrow-${id}`);
    const rightArrow = document.getElementById(`right-arrow-${id}`);

    leftArrow.addEventListener('click', function () {
        const currStatus = statusP.innerText.split(' ')[1];
        const newStatus = currStatus === 'DONE' ? 'IN PROGRESS' : 'OPEN';
        updateStatus(newStatus);
    });
    rightArrow.addEventListener('click', function () {
        const currStatus = statusP.innerText.split(' ')[1];
        const newStatus = currStatus === 'OPEN' ? 'IN PROGRESS' : 'DONE';
        updateStatus(newStatus);
    });

    const deleteIcon = document.getElementById(`delete-${id}`);
    deleteIcon.addEventListener('click', function () {
        fetch(`http://localhost:8000/api/tasks/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(() => taskDiv.remove())
            .then(() => console.log(`Task ${id} deleted`))
            .catch(err => console.log(err));
    });

    function updateStatus(newStatus) {
        fetch(`http://localhost:8000/api/tasks/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: newStatus
            })
        }).then(() => {
            console.log(`Status of task ${id} updated to ${newStatus}`);
        })
            .then(() => {
                const statusP = document.getElementById(`${id}-status`);
                statusP.innerText = `Status: ${newStatus}`;
                moveTask(newStatus);
            })
            .catch(err => console.log(err));
    }

    function moveTask(newStatus) {
        columnOpen = columnOpen || document.getElementById('column-open');
        columnInProgress = columnInProgress || document.getElementById('column-in-progress');
        columnDone = columnDone || document.getElementById('column-done');
        switch (newStatus) {
            case 'OPEN':
                columnOpen.appendChild(taskDiv);
                break;
            case 'IN PROGRESS':
                columnInProgress.appendChild(taskDiv);
                break;
            case 'DONE':
                columnDone.appendChild(taskDiv);
                break;
        }
    }
}