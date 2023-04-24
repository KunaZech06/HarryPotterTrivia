document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.querySelector('#login-form');
  const registerForm = document.querySelector('#register-form');

  if (loginForm) {
      loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const username = document.querySelector('#username').value;
        const password = document.querySelector('#password').value;
        loginUser(username, password);
  });
}

  if (registerForm) {
    registerForm.addEventListener('submit', function(event) {
      event.preventDefault();
      const username = document.querySelector('#username').value;
      const password = document.querySelector('#password').value;
      const confirmPassword = document.querySelector('#confirm-password').value;
      if (password !== confirmPassword) {
        alert("Passwords do not match!");
      } else {
        registerUser(username, password);
      }
    });
  }
});

function loginUser(username, password) {
  // Replace with your actual API call to login the user
  console.log('Login:', { username, password });
  // After successful login, redirect the user to the dashboard page
  window.location.href = 'dashboard.html';
}

function registerUser(username, password) {
  // Replace with your actual API call to register the user
  console.log('Register:', { username, password });
  // After successful registration, redirect the user to the login page
  window.location.href = 'login.html';
}

