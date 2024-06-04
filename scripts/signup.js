const apiURL = 'http://127.0.0.1:5000/api';

const signupForm = document.getElementById('signupForm')

console.log(signupForm)

signupForm.addEventListener('submit', function (event) {
    event.preventDefault();

    console.log(event.target);

    const form = event.target;
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // console.log(data);

    fetch(`${apiURL}/signup`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert("Sign Up Successfull! ✔");
            event.preventDefault()
            window.location.href = "/signin.html";
        })
        .catch(error => {
            alert(error.message);
            event.preventDefault()
        });
});
