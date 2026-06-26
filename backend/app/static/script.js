const API_URL = window.location.origin;
let todosLosProductos = []; // Guardamos los productos aquí

document.addEventListener('DOMContentLoaded', () => {

    // === 1. LÓGICA DE VENTANAS MODALES (MOVIDO DESDE HTML) ===
    const loginLink = document.getElementById('login-link');
    const loginModal = document.getElementById('login-section-modal');
    const registerModal = document.getElementById('register-section-modal');
    const overlay = document.getElementById('login-overlay');
    const btnAbrirRegistro = document.getElementById('btn-abrir-registro');
    const closeBtns = document.querySelectorAll('.close-btn');

    // Abrir login si no hay sesión
    if (loginLink) {
        loginLink.addEventListener('click', (e) => {
            const usuario = JSON.parse(sessionStorage.getItem('usuario'));
            if (!usuario) {
                e.preventDefault();
                if(loginModal && overlay) {
                    loginModal.style.display = 'block';
                    overlay.style.display = 'block';
                    document.body.classList.add('modal-open');
                }
            }
        });
    }

    // Cambiar a registro
    if (btnAbrirRegistro) {
        btnAbrirRegistro.addEventListener('click', () => {
            if(loginModal) loginModal.style.display = 'none';
            if(registerModal) registerModal.style.display = 'block';
        });
    }

    // Cerrar modales
    const cerrarTodo = () => {
        if(loginModal) loginModal.style.display = 'none';
        if(registerModal) registerModal.style.display = 'none';
        if(overlay) overlay.style.display = 'none';
        document.body.classList.remove('modal-open');
    };

    if (closeBtns) closeBtns.forEach(btn => btn.addEventListener('click', cerrarTodo));
    if (overlay) overlay.addEventListener('click', cerrarTodo);


    // === 2. CARGAR PRODUCTOS (CON DETECTOR DE CAÍDAS) ===
    async function cargarProductos(idCategoria = null) {
        const contenedor = document.getElementById('contenedor-productos');
        if (!contenedor) return;

        try {
            if (todosLosProductos.length === 0) {
                const response = await fetch(`${API_URL}/productos`);
                // Detector de caída: si MySQL está apagado
                if (!response.ok) {
                    console.error("Base de datos fuera de línea.");
                    window.location.href = "/mantenimiento";
                    return;
                }
                todosLosProductos = await response.json();
            }

            contenedor.innerHTML = '';
            let productosAMostrar = [];

            if (idCategoria === null || idCategoria === "0") {
                // Modo Inicio: 2 de cada categoría
                const categoriasUnicas = [...new Set(todosLosProductos.map(p => p.id_categoria))];
                categoriasUnicas.forEach(catId => {
                    const prodsDeCat = todosLosProductos.filter(p => p.id_categoria === catId);
                    productosAMostrar = productosAMostrar.concat(prodsDeCat.slice(0, 2));
                });
            } else {
                // Modo Menú: Todos los de esa categoría
                productosAMostrar = todosLosProductos.filter(p => p.id_categoria == idCategoria);
            }

            // Dibujar las tarjetas
            productosAMostrar.forEach(p => {
                const div = document.createElement('div');
                div.className = 'producto';
                const precioReal = Number(p.precio);
                div.innerHTML = `
                    <img src="/static/imagenes/image_default.jpeg" alt="${p.nombre}">
                    <h3>${p.nombre}</h3>
                    <p class="precio">$${precioReal.toLocaleString('es-CO')}</p>
                    <button class="btn-agregar" 
                        data-id="${p.id_producto}" 
                        data-nombre="${p.nombre}" 
                        data-precio="${precioReal}" 
                        data-imagen="${p.imagen}">
                        Agregar al Carrito
                    </button>
                `;
                contenedor.appendChild(div);
            });
        } catch (error) {
            // Detector de caída total: si Flask está apagado
            console.error("Error crítico de conexión:", error);
            window.location.href = "/mantenimiento";
        }
    }

    // === EVENTOS DEL MENÚ DESPLEGABLE ===
    document.querySelectorAll('.cat-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const idCat = e.target.getAttribute('data-id');
            cargarProductos(idCat);
            document.getElementById('contenedor-productos').scrollIntoView({ behavior: 'smooth' });
            document.getElementById('input-buscador').value = '';
        });
    });


    // === 3. VERIFICAR SESIÓN Y ROLES (ADMIN / MODERADOR) ===
    function verificarSesion() {
        const navUl = document.querySelector('.nav ul');
        const usuario = JSON.parse(sessionStorage.getItem('usuario'));
        const menuAdmin = document.getElementById('menu-admin');

        if (usuario && navUl) {
            // Evaluar rol y mostrar el botón correspondiente
            if (menuAdmin) {
                if (usuario.id_rol === 1) {
                    menuAdmin.style.display = 'inline-block';
                    menuAdmin.innerHTML = '<a href="/superadmin" style="color: #ff0000; font-weight: bold;">👑 Panel Admin</a>';
                } else if (usuario.id_rol === 3) {
                    menuAdmin.style.display = 'inline-block';
                    menuAdmin.innerHTML = '<a href="/admin" style="color: #ff9800; font-weight: bold;">🛠️ Panel Moderador</a>';
                }
            }

            const loginLinkEl = document.getElementById('login-link') || Array.from(navUl.querySelectorAll('a')).find(a => a.textContent.includes('Sesión'));
            if (loginLinkEl) loginLinkEl.parentElement.remove();

            const liSaludo = document.createElement('li');
            liSaludo.innerHTML = `Hola, ${usuario.nombre}`;
            
            const liLogout = document.createElement('li');
            liLogout.innerHTML = `<a href="#" id="btn-logout" style="background:#ccc; padding:5px 10px; border-radius:5px; color:#333; margin-left:10px;">Cerrar Sesión</a>`;

            navUl.appendChild(liSaludo);
            navUl.appendChild(liLogout);

            document.getElementById('btn-logout').addEventListener('click', (e) => {
                e.preventDefault();
                sessionStorage.removeItem('usuario');
                window.location.reload();
            });
        }
    }

    // === 4. LÓGICA DE LOGIN ===
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-pass').value;

            try {
                const response = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ correo: email, password: password })
                });
                const data = await response.json();
                if (response.ok) {
                    sessionStorage.setItem('usuario', JSON.stringify(data.user));
                    window.location.reload();
                } else {
                    alert(data.mensaje || "Error en el inicio de sesión");
                }
            } catch (error) {
                alert("Error al conectar con el servidor.");
            }
        });
    }

    // === 5. LÓGICA DE REGISTRO ===
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // --- NUEVO: VALIDAR TÉRMINOS Y CONDICIONES ---
            const aceptaTerminos = document.getElementById('acepta-terminos');
            if (!aceptaTerminos.checked) {
                alert("Debes aceptar los términos y condiciones para registrarte.");
                return;
            }

            // --- 🔒 NUEVO: VALIDACIÓN DE CONTRASEÑA ---
            const passwordInput = document.getElementById('register-pass').value;
            // La regla exige: min 8 caracteres, 1 minúscula, 1 mayúscula, 1 número, 1 símbolo
            const reglaPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
            
            if (!reglaPassword.test(passwordInput)) {
                alert("⚠️ Contraseña débil. Debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un símbolo (ej: @, #, $, % o *).");
                return; // Detiene el proceso y no envía nada a la base de datos
            }
            // ------------------------------------------

            // Si la contraseña es fuerte, armamos los datos como siempre
            const datos = {
                nombre: document.getElementById('register-nombre').value,
                apellido: document.getElementById('register-apellido').value,
                telefono: document.getElementById('register-telefono').value,
                correo: document.getElementById('register-email').value,
                password: passwordInput // Usamos la que ya pasó la prueba
            };

            try {
                const response = await fetch(`${API_URL}/registrar`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datos)
                });
                const result = await response.json();
                if (response.ok) {
                    alert("¡Registro exitoso! Ya puedes iniciar sesión.");
                    window.location.reload();
                } else {
                    alert("Error: " + (result.error || result.mensaje));
                }
            } catch (error) {
                console.error("Error en registro:", error);
                alert("No se pudo conectar con el servidor.");
            }
        });
    }

    // === 6. AGREGAR AL CARRITO (Local) ===
    document.getElementById('contenedor-productos')?.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-agregar')) {
            const btn = e.target;
            const id_producto = btn.getAttribute('data-id');
            const nombre = btn.getAttribute('data-nombre');
            const precio = parseFloat(btn.getAttribute('data-precio'));
            const imagen = btn.getAttribute('data-imagen');

            let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
            const existe = carrito.find(item => item.id === id_producto);

            if (existe) {
                existe.cantidad++;
            } else {
                carrito.push({ id: id_producto, nombre, precio, imagen, cantidad: 1 });
            }
            localStorage.setItem('carrito', JSON.stringify(carrito));
            actualizarBurbujaCarrito();
        }
    });

    // === 7. BURBUJA DEL CARRITO ===
    function actualizarBurbujaCarrito() {
        const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
        const burbuja = document.getElementById('cart-count');
        const totalProductos = carrito.reduce((acc, item) => acc + item.cantidad, 0);

        if (burbuja) {
            if (totalProductos > 0) {
                burbuja.textContent = totalProductos;
                burbuja.style.display = 'flex';
            } else {
                burbuja.style.display = 'none';
            }
        }
    }

    // === 8. CARGAR TÍTULO TIENDA (Dinámico) ===
    async function cargarTituloTienda() {
        try {
            const response = await fetch(`${API_URL}/configuracion/titulo`);
            if (response.ok) {
                const data = await response.json();
                document.title = data.titulo;
                const logoText = document.querySelector('.logo');
                if (logoText) logoText.innerHTML = `${data.titulo}<span></span>`;
            }
        } catch (error) {
            console.error("Error al cargar el título de la tienda:", error);
        }
    }

    // === 9. CARGAR SOBRE NOSOTROS (Dinámico) ===
    async function cargarInfoEmpresa() {
        try {
            const response = await fetch(`${API_URL}/configuracion/info`);
            if (response.ok) {
                const data = await response.json();
                const elSobre = document.getElementById('txt-sobre');
                const elMision = document.getElementById('txt-mision');
                const elVision = document.getElementById('txt-vision');
                const elUbicacion = document.getElementById('txt-ubicacion');

                if(elSobre) elSobre.textContent = data.sobre_nosotros;
                if(elMision) elMision.textContent = data.mision;
                if(elVision) elVision.textContent = data.vision;
                if(elUbicacion) elUbicacion.textContent = data.ubicacion;
            }
        } catch (error) {
            console.error("Error al cargar la información de la empresa:", error);
        }
    }



// ============================================================
    // LÓGICA DEL BUSCADOR EN TIEMPO REAL 
    // ============================================================
    const inputBuscador = document.getElementById('input-buscador');
    
    if (inputBuscador) {
        inputBuscador.addEventListener('input', (e) => {
            const textoBusqueda = e.target.value.toLowerCase(); // Lo que escribe el cliente
            const tarjetasProductos = document.querySelectorAll('.producto'); // <-- ¡AQUÍ ESTABA EL ERROR!
            
            tarjetasProductos.forEach(tarjeta => {
                // Leemos todo el texto de la tarjeta (título y precio)
                const contenidoTarjeta = tarjeta.innerText.toLowerCase(); 
                
                // Si coincide con la búsqueda, se muestra. Si no, se oculta suavemente.
                if (contenidoTarjeta.includes(textoBusqueda)) {
                    tarjeta.style.display = ''; 
                } else {
                    tarjeta.style.display = 'none'; 
                }
            });
        });
    }

// ============================================================
    // Terminos y Condiciones
    // ============================================================


    const abrirTerminos = document.getElementById("abrir-terminos");
    const modalTerminos = document.getElementById("modal-terminos");
    const cerrarTerminos = document.getElementById("cerrar-terminos");

    if (abrirTerminos) {
        abrirTerminos.addEventListener("click", (e) => {
            e.preventDefault();
            modalTerminos.style.display = "flex";
        });
    }

    if (cerrarTerminos) {
        cerrarTerminos.addEventListener("click", () => {
            modalTerminos.style.display = "none";
        });
    }















    // === INICIALIZADORES AL CARGAR LA PÁGINA ===
    cargarTituloTienda();
    cargarInfoEmpresa();
    cargarProductos(null);
    verificarSesion();
    actualizarBurbujaCarrito();


    


}); // Fin del DOMContentLoaded