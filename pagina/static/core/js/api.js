const outputElement = document.getElementById("output");

fetch("https://api.ipify.org/?format=json&callback=?").then(async (data) => {
  const ip = await data.json().then((data) => data.ip);
  const API_URL = `http://ip-api.com/json/${ip}`;
  fetch(API_URL)
    .then((response) => {
      if (!response.ok) {
        throw new Error("la respuesta del net callampin bombim");
      }
      return response.json();
    })

    .then((data) => {
      console.log(data);
      const reg = document.getElementById(data.region);
      reg.setAttribute("selected", true);
    });
});
