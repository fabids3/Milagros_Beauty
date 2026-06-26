const API_URL = "http://127.0.0.1:5000";

document.addEventListener('DOMContentLoaded', () => {
    console.log("🚀 Panel Super Admin cargando...");
    const usuario = JSON.parse(sessionStorage.getItem('usuario'));

    // Seguridad: Solo Super Admin (Rol 1)
    if (!usuario || usuario.id_rol !== 1) {
        alert("⛔ Acceso denegado. Solo el Super Administrador puede entrar aquí.");
        window.location.href = "/";
        return;
    }

    // --- 1. CARGAS INICIALES ---
    cargarVentas();
    cargarTablaClientes(usuario.id_usuario);
    cargarInventarioAdmin(); 
    cargarInfoEmpresa();

    // --- 2. GESTIÓN DE MODERADORES ---
    const btnMostrarForm = document.getElementById('btn-mostrar-form-mod');
    if (btnMostrarForm) {
        btnMostrarForm.addEventListener('click', () => {
            const formContainer = document.getElementById('seccion-crear-mod');
            formContainer.style.display = (formContainer.style.display === 'none' || formContainer.style.display === '') ? 'block' : 'none';
        });
    }

    const formMod = document.getElementById('form-nuevo-moderador');
    if (formMod) {
        formMod.addEventListener('submit', async (e) => {
            e.preventDefault();
            const datos = {
                nombre: document.getElementById('mod-nombre').value,
                apellido: document.getElementById('mod-apellido').value,
                telefono: document.getElementById('mod-telefono').value,
                correo: document.getElementById('mod-correo').value,
                password: document.getElementById('mod-password').value
            };
            try {
                const res = await fetch(`${API_URL}/admin/moderadores/nuevo`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datos)
                });
                if (res.ok) { 
                    alert("¡Moderador creado exitosamente!"); 
                    e.target.reset(); 
                    document.getElementById('seccion-crear-mod').style.display = 'none';
                }
            } catch (err) { alert("Error de conexión."); }
        });
    }

    // --- 3. EDITAR TÍTULO ---
    const btnEditarTitulo = document.getElementById('btn-editar-titulo');
    if (btnEditarTitulo) {
        btnEditarTitulo.addEventListener('click', async () => {
            const nuevoTitulo = prompt("Ingresa el nuevo título para tu tienda:");
            if (nuevoTitulo && nuevoTitulo.trim() !== "") {
                try {
                    const response = await fetch(`${API_URL}/admin/configuracion/titulo`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ titulo: nuevoTitulo })
                    });
                    if (response.ok) alert("¡Título actualizado con éxito!");
                } catch (error) { alert("Error de conexión."); }
            }
        });
    }

    // --- 4. ESCUCHADOR CREAR PRODUCTOS ---
    const formProducto = document.getElementById('form-admin-producto');
    if (formProducto) {
        formProducto.addEventListener('submit', guardarNuevoProducto);
    }
});

// ============================================================
// FUNCIONES DE CARGA Y GESTIÓN
// ============================================================

async function cargarVentas() {
    const tbody = document.getElementById('tabla-ventas');
    if (!tbody) return;
    try {
        const res = await fetch(`${API_URL}/admin/ventas`);
        const ventas = await res.json();
        tbody.innerHTML = ventas.map(v => `
            <tr>
                <td style="font-weight:bold; color:#e84c7f;">#${v.id_pedido}</td>
                <td>${v.nombre} ${v.apellido}</td>
                <td>${new Date(v.fecha_pedido).toLocaleString('es-CO')}</td>
                <td style="color:#4CAF50; font-weight:bold;">$${Number(v.total).toLocaleString('es-CO')}</td>
                <td><span style="background:#ffebee; color:#e84c7f; padding:5px 10px; border-radius:15px; font-size:12px; font-weight:bold;">${v.nombre_estado}</span></td>
            </tr>
        `).join('');
    } catch (e) { console.error("Error ventas:", e); }
}

async function cargarTablaClientes(idAdmin) {
    const tbody = document.getElementById('tabla-clientes');
    if (!tbody) return;
    try {
        const res = await fetch(`${API_URL}/admin/clientes?id_usuario=${idAdmin}`);
        const clientes = await res.json();
        tbody.innerHTML = clientes.map(c => `
            <tr>
                <td>${c.id_usuario}</td>
                <td>${c.nombre} ${c.apellido}</td>
                <td>${c.correo}</td>
                <td>${c.telefono || 'N/A'}</td>
            </tr>
        `).join('');
    } catch (e) { console.error("Error clientes:", e); }
}

function cargarInfoEmpresa() {
    const formInfo = document.getElementById('form-info-empresa');
    if (!formInfo) return;

    fetch(`${API_URL}/configuracion/info`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('info-sobre').value = data.sobre_nosotros || '';
            document.getElementById('info-mision').value = data.mision || '';
            document.getElementById('info-vision').value = data.vision || '';
            document.getElementById('info-ubicacion').value = data.ubicacion || '';
        });

    formInfo.addEventListener('submit', async (e) => {
        e.preventDefault();
        const datosInfo = {
            sobre_nosotros: document.getElementById('info-sobre').value,
            mision: document.getElementById('info-mision').value,
            vision: document.getElementById('info-vision').value,
            ubicacion: document.getElementById('info-ubicacion').value
        };
        try {
            const response = await fetch(`${API_URL}/admin/configuracion/info`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(datosInfo)
            });
            if (response.ok) alert("¡Información guardada correctamente!");
        } catch (error) { alert("Error al conectar."); }
    });
}

// ============================================================
// FUNCIONES DE INVENTARIO Y PRODUCTOS
// ============================================================

async function cargarInventarioAdmin() {
    try {
        const res = await fetch(`${API_URL}/productos`);
        const productos = await res.json();
        const tabla = document.getElementById('tabla-inventario');

        if (!tabla) return;

        if (productos.length === 0) {
            tabla.innerHTML = '<tr><td colspan="5" style="text-align:center;">No hay productos en la base de datos.</td></tr>';
            return;
        }

        tabla.innerHTML = productos.map(p => `
            <tr>
                <td>${p.id_producto}</td>
                <td>${p.nombre}</td>
                <td style="color:#4CAF50; font-weight:bold;">$${p.precio.toLocaleString('es-CO')}</td>
                <td>${p.stock}</td>
                <td>
                    <button onclick="editarProducto(${p.id_producto}, '${p.nombre}', ${p.precio}, ${p.stock})" 
                            style="background:#ff9800; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer; margin-right:5px;">✏️ Editar</button>
                    <button onclick="eliminarProducto(${p.id_producto})" 
                            style="background:#f44336; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer;">🗑️ Eliminar</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error("Error al cargar inventario:", error);
    }
}

async function guardarNuevoProducto(e) {
    e.preventDefault();
    const nuevoProd = {
        nombre: document.getElementById('admin-nombre').value,
        precio: parseFloat(document.getElementById('admin-precio').value),
        contenido: document.getElementById('admin-contenido').value,
        stock: parseInt(document.getElementById('admin-stock').value),
        imagen: document.getElementById('admin-imagen').value,
        id_categoria: parseInt(document.getElementById('admin-categoria').value),
        descripcion: document.getElementById('admin-desc').value,
        ideal_para: document.getElementById('admin-ideal').value,
        beneficios: document.getElementById('admin-beneficios').value,
        ingredientes: document.getElementById('admin-ingredientes').value,
        modo_uso: document.getElementById('admin-uso').value
    };

    try {
        const res = await fetch(`${API_URL}/admin/productos/nuevo`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(nuevoProd)
        });

        if (res.ok) {
            alert("¡Producto guardado exitosamente! ✨");
            e.target.reset();
            cargarInventarioAdmin();
        } else {
            const error = await res.json();
            alert("Error: " + (error.error || "No se pudo guardar."));
        }
    } catch (error) { alert("Error de conexión con el servidor."); }
}

window.eliminarProducto = async function(id) {
    if (confirm("¿Seguro que deseas eliminar este producto? Esta acción no se puede deshacer.")) {
        try {
            const res = await fetch(`${API_URL}/productos/${id}`, { method: 'DELETE' });
            if (res.ok) { cargarInventarioAdmin(); } 
            else { alert("No se pudo eliminar el producto."); }
        } catch (error) { console.error("Error al eliminar:", error); }
    }
};

window.editarProducto = async function(id, nombreActual, precioActual, stockActual) {
    const nuevoPrecio = prompt(`Editar PRECIO de: ${nombreActual}\nIngresa el nuevo precio:`, precioActual);
    if (nuevoPrecio === null || nuevoPrecio.trim() === "") return;

    const nuevoStock = prompt(`Editar STOCK de: ${nombreActual}\nIngresa la cantidad:`, stockActual);
    if (nuevoStock === null || nuevoStock.trim() === "") return;

    try {
        const response = await fetch(`${API_URL}/productos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ precio: parseFloat(nuevoPrecio), stock: parseInt(nuevoStock) })
        });

        if (response.ok) {
            alert("¡Producto actualizado! 🚀");
            cargarInventarioAdmin();
        } else { alert("Error al actualizar."); }
    } catch (error) { alert("Error de conexión."); }
};