document.addEventListener("DOMContentLoaded", () => {
    const contenedor = document.getElementById("lista-carrito");
    const totalDiv = document.getElementById("total");
    const btnVaciar = document.getElementById("vaciar-carrito");
    const API_URL = window.location.origin;

    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    function renderCarrito() {
        if (!contenedor) return;
        contenedor.innerHTML = "";

        if (carrito.length === 0) {
            contenedor.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:30px;">Tu carrito está vacío.</td></tr>';
            if (totalDiv) totalDiv.textContent = "$0";
            return;
        }

        let total = 0;
        carrito.forEach((item, index) => {
            const subtotal = item.precio * item.cantidad;
            total += subtotal;

            const imagenSrc = "/static/imagenes/image_default.jpeg";
            
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <img src="${imagenSrc}" class="img-carrito" width="50">
                        <span>${item.nombre}</span>
                    </div>
                </td>
                <td>$${item.precio.toLocaleString()}</td>
                <td>
                    <div class="cantidad-controles">
                        <button class="btn-restar" data-index="${index}">-</button>
                        <span style="margin:0 10px;">${item.cantidad}</span>
                        <button class="btn-sumar" data-index="${index}">+</button>
                    </div>
                </td>
                <td>$${subtotal.toLocaleString()}</td>
                <td><button class="btn-eliminar" data-index="${index}">❌</button></td>
            `;
            contenedor.appendChild(tr);
        });

        if (totalDiv) totalDiv.textContent = `$${total.toLocaleString()}`;
    }

    // --- MANEJO DE CLICS CON ACTUALIZACIÓN DE BASE DE DATOS ---
    contenedor?.addEventListener("click", async (e) => {
        const target = e.target;
        const index = target.getAttribute("data-index");
        if (index === null) return;

        const producto = carrito[index];

        // --- BOTÓN SUMAR (+) ---
        // Ahora descuenta del stock real en la DB antes de sumar en el carrito
        if (target.classList.contains("btn-sumar")) {
            try {
                const res = await fetch(`${API_URL}/descontar_stock`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ id: producto.id })
                });

                if (res.ok) {
                    carrito[index].cantidad++;
                    actualizarTodo();
                } else {
                    const error = await res.text();
                    console.log("ERROR BACKEND:", error); 
                    alert("¡Lo sentimos! No hay más unidades disponibles de este producto.");
                }
            } catch (error) {
                console.error("Error al comunicar con el servidor:", error);
            }
        }

        // --- BOTÓN RESTAR (-) ---
        if (target.classList.contains("btn-restar")) {
            await fetch(`${API_URL}/sumar_stock`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ id: producto.id, cantidad: 1 })
            });

            if (carrito[index].cantidad > 1) {
                carrito[index].cantidad--;
            } else {
                carrito.splice(index, 1);
            }
            actualizarTodo();
        }

        // --- BOTÓN ELIMINAR (X) ---
        if (target.classList.contains("btn-eliminar")) {
            await fetch(`${API_URL}/sumar_stock`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ id: producto.id, cantidad: producto.cantidad })
            });

            carrito.splice(index, 1);
            actualizarTodo();
        }
    });

    function actualizarTodo() {
        localStorage.setItem("carrito", JSON.stringify(carrito));
        renderCarrito();
    }

    btnVaciar?.addEventListener("click", async () => {
        if (!confirm("¿Vaciar todo el carrito?")) return;

        for (let prod of carrito) {
            await fetch(`${API_URL}/sumar_stock`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ id: prod.id, cantidad: prod.cantidad })
            });
        }
        carrito = [];
        actualizarTodo();
    });

    renderCarrito();

    window.finalizarCompra = async () => {
        const usuario = JSON.parse(sessionStorage.getItem('usuario'));
        if (!usuario) return alert("Debes iniciar sesión primero.");
        if (carrito.length === 0) return alert("Tu carrito está vacío.");

        try {
            const res = await fetch(`${API_URL}/finalizar-compra`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    id_usuario: usuario.id_usuario,
                    total: carrito.reduce((acc, i) => acc + (i.precio * i.cantidad), 0),
                    carrito: carrito
                })
            });
            if (res.ok) {
                alert("✨ ¡Compra exitosa! Gracias por confiar en Milagro's Beauty.");
                localStorage.removeItem("carrito");
                window.location.href = "/";
            }
        } catch (e) { alert("Error de conexión con el servidor."); }
    };

// === FINALIZAR COMPRA (BASE DE DATOS + WHATSAPP) ===
    const btnWhatsapp = document.getElementById('btn-whatsapp');
    if (btnWhatsapp) {
        btnWhatsapp.addEventListener('click', async () => {
            const usuario = JSON.parse(sessionStorage.getItem('usuario'));
            // Usamos la variable de carrito que ya debes tener arriba en tu carrito.js
            const carritoActual = JSON.parse(localStorage.getItem('carrito')) || [];
            
            if (!usuario) {
                alert('Debes iniciar sesión para finalizar tu pedido.');
                return;
            }
            if (carritoActual.length === 0) {
                alert('Tu carrito está vacío.');
                return;
            }

            // Calculamos el total
            const totalCompra = carritoActual.reduce((acc, item) => acc + (item.precio * item.cantidad), 0);

            // Cambiamos el texto del botón mientras carga
            btnWhatsapp.textContent = "Procesando pedido...";
            btnWhatsapp.disabled = true;

            try {
                // 1. Guardar en Base de Datos (Flask)
                const response = await fetch(`${API_URL}/finalizar-compra`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        id_usuario: usuario.id_usuario,
                        total: totalCompra, 
                        carrito: carritoActual
                    })
                });

                if (response.ok) {
                    // 2. Si se guardó en MySQL, armamos WhatsApp
                    let mensaje = ` ¡Hola Milagro's Beauty!\n\n *NUEVO PEDIDO*\n\n*Datos del Cliente:*\n Nombre: ${usuario.nombre} ${usuario.apellido}\n Teléfono: ${usuario.telefono}\n\n*Productos:*\n`;
                    carritoActual.forEach(item => {
                        mensaje += `- ${item.cantidad}x ${item.nombre} ($${item.precio.toLocaleString('es-CO')})\n`;
                    });

                    mensaje += `\n *Total: $${totalCompra.toLocaleString('es-CO')}*\n\n¡Quedo atento(a) para confirmar mi pedido! `;

                    // RECUERDA PONER TU NÚMERO AQUÍ (Con código de país, ej: 573000000000):
                    const numeroTienda = "573246454318"; 
                    const url = `https://wa.me/${numeroTienda}?text=${encodeURIComponent(mensaje)}`;
                    
                    // Limpiamos el carrito PRIMERO
                    localStorage.removeItem('carrito');

                    // Redirigimos directamente usando href en la misma pestaña. 
                    // Esto fuerza al celular a abrir la app de WhatsApp de manera segura 
                    // y evita el bloqueo por "await".
                    window.location.replace(url);

                } else {
                    const errorText = await response.text();
                    console.log("ERROR WHATSAPP:", errorText);
                    alert("Hubo un problema en el servidor");

                    btnWhatsapp.textContent = "💬 Finalizar Pedido por WhatsApp";
                    btnWhatsapp.disabled = false;
                }
            } catch (error) {
                console.error("Error de conexión:", error);
                alert("Error de conexión con el servidor. Intenta nuevamente en unos segundos.");
                btnWhatsapp.textContent = "💬 Finalizar Pedido por WhatsApp";
                btnWhatsapp.disabled = false;
            }
        });
    }






});