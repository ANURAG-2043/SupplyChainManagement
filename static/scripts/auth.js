// document.getElementById('login-form').addEventListener('submit', function(event) {
//     event.preventDefault(); // Prevent default form submission
//     window.location.href = '/dashboard'; // Redirect to the dashboard
// });

document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const email = document.querySelector("input[name='email']").value;
    const password = document.querySelector("input[name='password']").value;

    window.location.href = "/dashboard";

    // fetch("/auth/login", {
    //     method: "POST",
    //     headers: {
    //         "Content-Type": "application/json"
    //     },
    //     body: JSON.stringify({ email, password })
    // })
    // .then(response => response.json())
    // .then(data => {
    //     if (data.access_token) {
    //         window.location.href = "/dashboard";
    //     } else {
    //         alert("Login failed. Please check your email or password.");
    //     }
    // })
    // .catch(error => {
    //     console.error("Error:", error);
    // });
});
