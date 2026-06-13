const API_URL = "http://127.0.0.1:5000";

// ============================================================
// 1. CONTROL DE ACCESO Y ARRANQUE (DOMContentLoaded)
// ============================================================
document.addEventListener('DOMContentLoaded', async () => {
    const usuario = JSON.parse(sessionStorage.getItem('usuario'));

    // Seguridad: Permite entrar a Rol 1 (Admin) o Rol 3 (Moderador)
    if (!usuario || (usuario.id_rol !== 1 && usuario.id_rol !== 3)) {
        alert("⛔ Acceso denegado. Serás redirigido al inicio.");
        window.location.href = "/";
        return;
    }

    // Si pasó el candado, ejecutamos las cargas iniciales
    cargarPedidosAdmin();
    cargarInventarioAdmin();
    
    // NOTA: Aquí NO cargamos clientes, eso es exclusivo de superadmin.js

    // Escuchador para el formulario de creación de productos
    const formProducto = document.getElementById('form-admin-producto');
    if (formProducto) {
        formProducto.addEventListener('submit', guardarNuevoProducto);
    }
});

// ============================================================
// 2. GESTIÓN DE PRODUCTOS (Cargar, Guardar, Eliminar, Editar)
// ============================================================

// --- CARGAR INVENTARIO CON BOTONES ---
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

// --- GUARDAR NUEVO PRODUCTO ---
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
    } catch (error) {
        alert("Error de conexión con el servidor.");
    }
}

// --- ELIMINAR PRODUCTO ---
window.eliminarProducto = async function(id) {
    if (confirm("¿Seguro que deseas eliminar este producto? Esta acción no se puede deshacer.")) {
        try {
            const res = await fetch(`${API_URL}/productos/${id}`, { method: 'DELETE' });
            if (res.ok) {
                cargarInventarioAdmin();
            } else {
                alert("No se pudo eliminar el producto.");
            }
        } catch (error) {
            console.error("Error al eliminar:", error);
        }
    }
};

// --- EDITAR PRODUCTO (Precio y Stock) ---
window.editarProducto = async function(id, nombreActual, precioActual, stockActual) {
    const nuevoPrecio = prompt(`Editar PRECIO de: ${nombreActual}\nIngresa el nuevo precio:`, precioActual);
    if (nuevoPrecio === null || nuevoPrecio.trim() === "") return;

    const nuevoStock = prompt(`Editar STOCK de: ${nombreActual}\nIngresa la cantidad:`, stockActual);
    if (nuevoStock === null || nuevoStock.trim() === "") return;

    try {
        const response = await fetch(`${API_URL}/productos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                precio: parseFloat(nuevoPrecio),
                stock: parseInt(nuevoStock)
            })
        });

        if (response.ok) {
            alert("¡Producto actualizado! 🚀");
            cargarInventarioAdmin();
        } else {
            alert("Error al actualizar.");
        }
    } catch (error) {
        alert("Error de conexión.");
    }
};

// ============================================================
// 3. GESTIÓN DE PEDIDOS
// ============================================================

// --- CARGAR PEDIDOS REALIZADOS ---
async function cargarPedidosAdmin() {
    try {
        const res = await fetch(`${API_URL}/admin/ventas`);
        const pedidos = await res.json();
        const tabla = document.getElementById('lista-pedidos-admin');

        if (!tabla) return;

        tabla.innerHTML = pedidos.map(p => `
            <tr>
                <td style="font-weight:bold; color:#e84c7f;">#${p.id_pedido}</td>
                <td>${p.nombre} ${p.apellido}</td>
                <td>$${p.total.toLocaleString('es-CO')}</td>
                <td>${new Date(p.fecha_pedido).toLocaleString()}</td>
                <td><span style="background:#e3f2fd; color:#1976d2; padding:3px 8px; border-radius:10px; font-size:0.85em;">${p.nombre_estado}</span></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error("Error al cargar pedidos:", error);
    }
}