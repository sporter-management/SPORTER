import { requestURL } from "/static/javascripts/catalogRequestHelpers.js";

import {
  clearAlerts,
  displayResponseMessages,
} from "/static/javascripts/alertMessages.js";

document.addEventListener("DOMContentLoaded", async function () {
  const nombreElement = document.getElementById("nombre");
  const descripcionElement = document.getElementById("descripcion");
  const precioElement = document.getElementById("precio");
  const existenciasElement = document.getElementById("existencias");
  const imagenElement = document.getElementById("imagen");
  const imagenDisplay = document.getElementById("image_display");
  const productEtiqueta = document.querySelector("#select");

  await fetch("http://127.0.0.1:5000/api/etiqueta/leer/")
    .then((resp) => resp.json())
    .then((datos) => {
      datos.forEach((etiqueta) => {
        let optionEtiqueta = document.createElement("option");
        optionEtiqueta.textContent = etiqueta.nombre;
        optionEtiqueta.setAttribute("value", `${etiqueta.id}`);
        productEtiqueta.appendChild(optionEtiqueta);
      });
    });

  function handleImageSelect(event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        imagenDisplay.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  // Attach event listener to imagenElement
  imagenElement.addEventListener("change", handleImageSelect);

  await fetch(requestURL + document.querySelector("#productID").value)
    .then((response) => response.json())
    .then((data) => {
      nombreElement.value = data["nombre"];
      descripcionElement.value = data["descripcion"];
      precioElement.value = data["precio"];
      existenciasElement.value = data["existencias"];
      productEtiqueta.value = data.etiqueta["id"];
      imagenDisplay.src = `data:image/jpeg;base64,${data["imagen"]}`;
      // imagenElement.value = data["img_orig_name"];
    });

  const sumbitBtn = document.getElementById("sumbitUpdate");

  sumbitBtn.addEventListener("click", async function () {
    const updateForm = new FormData();
    updateForm.append("id", window.location.href.split("/").reverse()[0]);
    updateForm.append("nombre", nombreElement.value);
    updateForm.append("descripcion", descripcionElement.value);
    updateForm.append("precio", precioElement.value);
    updateForm.append("existencias", existenciasElement.value);
    updateForm.append("filename", imagenElement.files[0]);
    updateForm.append("id_etiqueta", productEtiqueta.value);
    const requestInfo = {
      method: "POST",
      body: updateForm,
    };

    await fetch(requestURL + "/actualizar", requestInfo)
      .then((response) =>
        response
          .json()
          .then((data) => ({ status_code: response.status, data: data }))
      )
      .then((obj) => {
        console.log(obj);
        clearAlerts();
        displayResponseMessages(obj);
      });
  });
});
