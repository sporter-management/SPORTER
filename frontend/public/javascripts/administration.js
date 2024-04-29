// Verifica si la URL actual es /administrar
if (window.location.pathname === '/administration') {
    // Ejecuta el codigo cuando se carga la página en /administrar
    fetch( document.getElementById("APIBaseURL").value + 'api/user/') 
        .then(response => response.json())
        .then(data => {
            const userData = data.search_result;
            const tableBody = document.getElementById('userData');

            userData.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.nombre}</td>
                    <td>${user.usuario}</td>
                    <td>${user.correo}</td>
                    <td>
                        <button onclick="openModal('${user.nombre}', '${user.correo}', '${user.is_admin}', '${user.usuario}')">Modificar</button>
                        <button onclick="deleteUser(${user.id})">Eliminar</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error:', error));
}



// Logica para abrir el modal con los datos del usuario seleccionado para editar
function openModal(nombre, correo, is_admin, username) {
    const editNombre = document.getElementById('editNombre');
    const editCorreo = document.getElementById('editCorreo');
    const editIsAdmin = document.getElementById("editIsAdmin");
    
    editNombre.value = nombre;
    editCorreo.value = correo;
    editIsAdmin.checked = is_admin == "true" ? 1 : 0;
    
    const modal = new bootstrap.Modal(document.getElementById('editModal'));
    modal.show();
    
    // Agrega un evento clic al boton "Guardar cambios" dentro del modal
    const editSubmitBtn = document.getElementById('editSubmit');
    editSubmitBtn.addEventListener('click', function(event) {
        event.preventDefault();
        
        // Obtiene los valores actualizados de los campos de nombre y correo
        const nuevoNombre = editNombre.value;
        const nuevoCorreo = editCorreo.value;
        const nuevoIsAdmin = editIsAdmin.checked ? 1 : 0;

        // Crea un objeto FormData y agrega los campos de nombre y correo
        const formData = new FormData();
        formData.append('nombre', nuevoNombre);
        formData.append('correo', nuevoCorreo);
        formData.append('is_admin', nuevoIsAdmin);
        formData.append("usuario", username)

        // Envía los datos de edición al servidor utilizando FormData
        fetch( document.getElementById("APIBaseURL").value + 'api/user/actualizar', {
            method: 'POST',
            credentials: "include",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.mensaje); // Muestra el mensaje de éxito o error
            modal.hide(); // Cierra el modal después de enviar el formulario
        })
    });
}


function deleteUser(id) {
    const confirmacion = confirm("¿Estás seguro de que deseas eliminar este usuario?");

    // Si el usuario confirma la eliminacion
    if (confirmacion) {
        fetch( document.getElementById("APIBaseURL").value + `api/user/eliminar/${id}`, {
            method: 'POST',
            credentials: "include",
        })
        .then(response => response.json())
        .then(data => {
            alert(data.mensaje); 
            // Si se elimina bien, recarga la pagina
            if (data.status === 200) {
                window.location.reload();
            }
        })
    }
}
