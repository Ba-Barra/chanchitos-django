$(document).ready(() => {
    $(".update-cart").click((e) => {
      const buy = e.target.dataset.buy || e.currentTarget.dataset.buy;
      const productId =
        e.target.dataset.product || e.currentTarget.dataset.product;
      const action = e.target.dataset.action || e.currentTarget.dataset.action;
      if (user === "AnonymousUser") {
        return;
      } else {
        updateUserOrder(productId, action, buy === "true");
      }
    });
  });
  
  function updateUserOrder(productId, action, buy = false) {
    const url = "/actualizar_chanchi_carrito/";
  
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ productId, action }),
    })
      .then((response) => response.json())
      .then((data) => {
        location.reload();
      });
  }