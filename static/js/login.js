let alertDiv = document.getElementById("alert");
let submitButton = document.querySelector("button[type='submit']");
submitButton.addEventListener("click", function(event) {
  let usernameInput = document.getElementById("username");
  let passwordInput = document.getElementById("password");
  if (usernameInput.value === "") {
    event.preventDefault();
    alertDiv.innerHTML = "Ingrese su nombre de usuario.";
    alertDiv.style.display = "block";
    passwordInput.value = "";
    return;
  }
  if (passwordInput.value === "") {
    event.preventDefault();
    alertDiv.innerHTML = "Ingrese su contraseña.";
    alertDiv.style.display = "block";
    return;
  }
  fetch('/check_login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    },
    body: JSON.stringify({
      username: usernameInput.value,
      password: passwordInput.value
    })
  })
  .then(response => {
    if (response.status === 200) {
      window.location.href = '/';
    } else if (response.status === 401) {
      event.preventDefault();
      alertDiv.innerHTML = "Nombre de usuario o contraseña incorrectos. Por favor, inténtelo de nuevo.";
      alertDiv.style.display = "block";
      passwordInput.value = "";
    }
  })
  .catch(error => console.log(error));
  
  // agrega esta línea para evitar que la página se recargue al hacer submit
  event.preventDefault();
});