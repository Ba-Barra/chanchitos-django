
const nombreRegistro = document.getElementById("nombreRegistro");

nombreRegistro.setCustomValidity("Chanchi-nombres por favor!");

nombreRegistro.addEventListener("input", function (event) {
  console.log("entrando a la funcion");
  if (nombreRegistro.value === "") {
    nombreRegistro.setCustomValidity("Chanchi-nombres por favor!");
  } else {
    nombreRegistro.setCustomValidity("");
  }
});
/*Validacion del email*/
const emailRegistro = document.getElementById("emailRegistro");

emailRegistro.setCustomValidity("Chanchi-emails por favor!");

emailRegistro.addEventListener("input", function (event) {
  if (emailRegistro.value === "" || !emailRegistro.value.includes("@")) {
    emailRegistro.setCustomValidity("Chanchi-emails por favor!");
  } else {
    emailRegistro.setCustomValidity("");
  }
});
/*Validacion del tamaño de la contraseña */
const contrasenaRegistro = document.getElementById("contrasenaRegistro");
contrasenaRegistro.setCustomValidity("No es muy chanchi-segura eh");
contrasenaRegistro.addEventListener("input", function (event) {
  console.log("entra esta wea o no");
  if (contrasenaRegistro.value.length < 8) {
    contrasenaRegistro.setCustomValidity("No es muy chanchi-segura eh");
  } else {
    contrasenaRegistro.setCustomValidity("");
  }
});

/*Validacion de la confimación de las contraseñas*/
const contrasenaConfirmar = document.getElementById("contrasenaConfirmar");

contrasenaConfirmar.setCustomValidity("Las chanchi-contraseñas no son iguales");

contrasenaConfirmar.addEventListener("input", function (event) {
  if (contrasenaConfirmar.value !== contrasenaRegistro.value) {
    contrasenaConfirmar.setCustomValidity(
      "Las chanchi-contraseñas no son iguales!"
    );
  } else {
    contrasenaConfirmar.setCustomValidity("");
  }
});
