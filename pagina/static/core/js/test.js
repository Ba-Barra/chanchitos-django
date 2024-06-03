const email = document.getElementById("chanchito-correo");

email.setCustomValidity("Chanchito correos por favor!");

email.addEventListener("input", function (event) {
  if (email.validity.typeMismatch || email.value === "") {
    email.setCustomValidity("Chanchito correos por favor!");
  } else {
    email.setCustomValidity("");
  }
});

const direccion = document.getElementById("chanchito-direccion");

direccion.setCustomValidity("Chanchito-direcciones por favor!");

direccion.addEventListener("input", function (event) {
  if (direccion.value === "") {
    direccion.setCustomValidity("Chanchito-direcciones por favor!");
  } else {
    direccion.setCustomValidity("");
  }
});


