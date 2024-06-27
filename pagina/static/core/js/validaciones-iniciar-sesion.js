/*Validacion de correo en iniciar sesion*/
const emailSesion = document.getElementById("emailSesion");
const contrasenaSesion = document.getElementById("contrasenaSesion");

emailSesion.addEventListener("input", function () {
  if (emailSesion.validity.typeMismatch || emailSesion.value === "") {
    emailSesion.setCustomValidity("Un chanchi-correo por favor!");
  } else {
    emailSesion.setCustomValidity("");
  }
});



