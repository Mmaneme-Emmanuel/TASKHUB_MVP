const apiURL = 'http://127.0.0.1:5000/api';
const signinForm = document.getElementById('signinForm');

signinForm.addEventListener('submit', function (event) {
    event.preventDefault();

    console.log(event.target);

    const form = event.target;
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    console.log(data);

    fetch(`${apiURL}/signin`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            // console.log(data.data);
            localStorage.userId = data.data.id;
            alert("Sign in Successfull! ✔");
            event.preventDefault()
            window.location.href = "/todo.html";
        })
        .catch(error => {
            alert("Sign in failed! 💔");
            event.preventDefault()
        });
});