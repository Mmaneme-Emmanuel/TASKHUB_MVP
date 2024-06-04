const todoForm = document.getElementById('createTask');
const apiURL = 'http://127.0.0.1:5000/api';

// console.log(localStorage.userId)
const userId = localStorage.userId;

todoForm.addEventListener('submit', function (event) {
    event.preventDefault();

    console.log(event.target);

    const form = event.target;
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    data.user_id = userId;

    console.log(data);

    fetch(`${apiURL}/todo`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            console.log("Task added Successfull! ✔", data);
            location.reload()
        })
        .catch(error => {
            alert(error.message);
            event.preventDefault()
        });
});