const todoList = document.getElementById('todoList');

window.addEventListener('load', function (event) {
    const data = {};``
    data.user_id = userId;

    console.log(data);

    fetch(`${apiURL}/todo?user_id=${userId}`, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            renderTasks(data.tasks.reverse());
        })
        .catch(error => {
            alert(error.message);
            event.preventDefault()
        });
});

function renderTasks(tasks) {
    // Clear existing tasks
    todoList.innerHTML = '';

    // Check if tasks exist
    if (!tasks || tasks.length === 0) {
        todoList.innerHTML = '<li>No tasks available.</li>';
        return;
    }

    // Create list items for each task
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.textContent = task.task; // Assuming each task has a 'title' property
        todoList.appendChild(li);
    });
}