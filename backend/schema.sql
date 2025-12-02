-- Schema SQL para la base de datos del hotel

CREATE DATABASE IF NOT EXISTS hotel_db;
USE hotel_db;

-- Tabla de usuarios con sistema de autenticación
CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  rol ENUM('admin', 'empleado', 'cliente') DEFAULT 'cliente',
  email VARCHAR(255) UNIQUE NOT NULL,
  telefono VARCHAR(20),
  password VARCHAR(255) NOT NULL,
  direccion VARCHAR(255),
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de hospedajes
CREATE TABLE IF NOT EXISTS hospedajes (
  id_hospedaje INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  descripcion TEXT,
  capacidad INT NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  foto VARCHAR(255),
  disponibilidad TINYINT(1) DEFAULT 1,
  tipo VARCHAR(50),
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de reservas
CREATE TABLE IF NOT EXISTS reservas (
  id_reserva INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_hospedaje INT NOT NULL,
  fecha_checkin DATE NOT NULL,
  fecha_checkout DATE NOT NULL,
  cant_personas INT NOT NULL,
  importe_total DECIMAL(10,2) NOT NULL,
  estado ENUM('pendiente', 'confirmada', 'cancelada', 'completada') DEFAULT 'pendiente',
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_reserva_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
  CONSTRAINT fk_reserva_hospedaje FOREIGN KEY (id_hospedaje) REFERENCES hospedajes(id_hospedaje) ON DELETE CASCADE
);

-- Datos de prueba con contraseñas hasheadas reales
-- Credenciales: admin@hotel.com/admin123, empleado@hotel.com/empleado123, juan@example.com/cliente123, maria@example.com/maria123
INSERT INTO usuarios (nombre, email, telefono, password, direccion, rol) VALUES
('Administrador', 'admin@hotel.com', '111-000-000', 'scrypt:32768:8:1$or72Sam7ocC2TuV4$f773db7f25e6c84a3ced9f534aad6f7d49830466714f429c2d130ac25df4d0ab5aadcb03727c9fd5612d8605372e97a9d242b43a93249d5dfa4b848adc0ff81b', 'Oficina Principal', 'admin'),
('Empleado Hotel', 'empleado@hotel.com', '111-111-111', 'scrypt:32768:8:1$bZyTs4X56ndJnFLg$5725743840c7a0ca5e4a0edba83931df855332c067ca2a7533176c2f46bffdd7535708e86c2940f138ff86b47a0c651f06be4b88ab15f62f60b48e6ea68f5e01', 'Hotel Reception', 'empleado'),
('Juan Pérez', 'juan@example.com', '111-222-333', 'scrypt:32768:8:1$JJ5cThGxdnTj5LBM$0c7c079c9cfea005cd3ecf4b8b4bac193a50bb2256061ff174d913913a378acab505aa39381cdbbaa954a6e2eddc9efddda9495390364e1ad1008e76dc22098c', 'Calle Falsa 123', 'cliente'),
('María Gómez', 'maria@example.com', '222-333-444', 'scrypt:32768:8:1$8Wn9kvInXIK7ktiN$7c90369929ed200cd281a44ee0634e28648a4898d03b5e7e20f2aab92a5d2d116ea4cf63b052abe195ef18643c62fdda4986a99d46848e97d7be130269a2edde', 'Av. Siempre Viva 742', 'cliente');

INSERT INTO hospedajes (nombre, descripcion, capacidad, precio, foto, disponibilidad, tipo) VALUES
('Suite Presidencial', 'Amplia suite con vista al mar y jacuzzi privado', 4, 350.00, 'suite_presidencial.jpg', 1, 'suite'),
('Habitación Doble Superior', 'Cómoda habitación con balcón y vista a la ciudad', 2, 150.00, 'doble_superior.jpg', 1, 'doble'),
('Habitación Familiar', 'Espaciosa habitación con dos camas y área de estar', 6, 220.00, 'familiar.jpg', 1, 'familiar'),
('Habitación Individual', 'Acogedora habitación individual con escritorio', 1, 80.00, 'individual.jpg', 1, 'individual'),
('Junior Suite', 'Suite moderna con minibar y área de trabajo', 2, 195.00, 'junior_suite.jpg', 1, 'suite');

INSERT INTO reservas (id_usuario, id_hospedaje, fecha_checkin, fecha_checkout, cant_personas, importe_total, estado) VALUES
(3, 1, '2025-12-20', '2025-12-25', 2, 1750.00, 'confirmada'),
(4, 2, '2025-11-01', '2025-11-03', 1, 300.00, 'pendiente'),
(3, 3, '2025-12-15', '2025-12-18', 4, 660.00, 'confirmada'),
(4, 5, '2025-11-25', '2025-11-28', 2, 585.00, 'pendiente');
