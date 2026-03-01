import { useState, useEffect } from "react";
import { cifrarDatos } from "./crypto";
import "./App.css";

function App() {
  // Estado del formulario
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState({ texto: "", tipo: "" });

  // Estado para la lista de usuarios
  const [usuarios, setUsuarios] = useState([]);
  const [cargandoUsuarios, setCargandoUsuarios] = useState(true);

  const API_URL = import.meta.env.VITE_API_URL;

  // Cargar usuarios al iniciar
  useEffect(() => {
    cargarUsuarios();
  }, []);

  const cargarUsuarios = async () => {
    try {
      setCargandoUsuarios(true);
      const response = await fetch(`${API_URL}/api/usuarios/`);
      const data = await response.json();
      setUsuarios(data);
    } catch (error) {
      console.error("Error al cargar usuarios:", error);
    } finally {
      setCargandoUsuarios(false);
    }
  };

  const limpiarFormulario = () => {
    setUsername("");
    setPassword("");
    setEmail("");
  };

  const registrar = async () => {
    if (!username || !password || !email) {
      setMensaje({ texto: "Todos los campos son obligatorios", tipo: "error" });
      return;
    }

    setLoading(true);
    setMensaje({ texto: "", tipo: "" });

    try {
      const resKey = await fetch(`${API_URL}/api/public-key/`);
      const keyData = await resKey.json();

      const datos = { username, password, email };
      const encrypted = await cifrarDatos(datos, keyData.public_key);

      const response = await fetch(`${API_URL}/api/registro/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: encrypted })
      });

      if (response.ok) {
        setMensaje({ texto: "Usuario registrado correctamente", tipo: "exito" });
        limpiarFormulario();
        await cargarUsuarios();
      } else {
        setMensaje({ texto: "Error al registrar usuario", tipo: "error" });
      }
    } catch (error) {
      setMensaje({ texto: " Error de conexión", tipo: "error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="contenido">
        {/* Tarjeta de Registro */}
        <div className="card registro-card">
          <h2>Crear Cuenta</h2>
          <p className="subtitulo">Regístrate para comenzar</p>

          {mensaje.texto && (
            <div className={`mensaje ${mensaje.tipo}`}>
              {mensaje.texto}
            </div>
          )}

          <div className="form-group">
            <label>Usuario</label>
            <input
              type="text"
              placeholder="Ej. Juan Perez"
              value={username}
              onChange={e => setUsername(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              placeholder="ejemplo@email.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label>Contraseña</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
              disabled={loading}
            />
          </div>

          <button 
            className={`btn-registrar ${loading ? 'cargando' : ''}`}
            onClick={registrar}
            disabled={loading}
          >
            {loading ? "Registrando..." : "Registrarse"}
          </button>
        </div>

        {/* Tarjeta de Lista de Usuarios */}
        <div className="card lista-card">
          <div className="lista-header">
            <h3>Usuarios Registrados</h3>
            <button 
              className="btn-refrescar" 
              onClick={cargarUsuarios}
              disabled={cargandoUsuarios}
            >
              ↻
            </button>
          </div>

          {cargandoUsuarios ? (
            <div className="cargando-spinner">
              <div className="spinner"></div>
              <p>Cargando usuarios...</p>
            </div>
          ) : usuarios.length === 0 ? (
            <div className="sin-datos">
              <p>No hay usuarios registrados</p>
            </div>
          ) : (
            <>
              <div className="tabla-container">
                <table className="tabla-usuarios">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Usuario</th>
                      <th>Email</th>
                    </tr>
                  </thead>
                  <tbody>
                    {usuarios.map((usuario) => (
                      <tr key={usuario.id}>
                        <td className="id-col">#{usuario.id}</td>
                        <td className="username-col">{usuario.username}</td>
                        <td className="email-col">{usuario.email_mostrado}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="lista-footer">
                <p>Total de usuarios: <span className="badge">{usuarios.length}</span></p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;