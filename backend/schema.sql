-- Schema SQL para la base de datos `ids`
-- Ejecutar en MySQL (por ejemplo: mysql -u root -p ids < schema.sql)

CREATE DATABASE IF NOT EXISTS hotel_db;
USE hotel_db;

CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255),
  rol VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  telefono VARCHAR(20),
  password VARCHAR(255),
  direccion VARCHAR(255),
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hospedajes (
  id_hospedaje INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255),
  descripcion TEXT,
  capacidad INT,
  precio DECIMAL(10,2),
  foto VARCHAR(255),
  disponibilidad TINYINT(1) DEFAULT 1,
  tipo VARCHAR(50),
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reservas (
  id_reserva INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT,
  id_hospedaje INT,
  fecha_checkin DATE,
  fecha_checkout DATE,
  cant_personas INT,
  importe_total DECIMAL(10,2),
  estado VARCHAR(50) DEFAULT 'pendiente',
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_reserva_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
  CONSTRAINT fk_reserva_hospedaje FOREIGN KEY (id_hospedaje) REFERENCES hospedajes(id_hospedaje) ON DELETE CASCADE
);

-- Datos de prueba
INSERT INTO usuarios (nombre, email, telefono, password, direccion) VALUES
('Juan Perez', 'juan@example.com', '111-222-333', 'pass1', 'Calle Falsa 123'),
('María Gómez', 'maria@example.com', '222-333-444', 'pass2', 'Av. Siempre Viva 742');

INSERT INTO hospedajes (nombre, descripcion, capacidad, precio, foto, disponibilidad, tipo) VALUES
('Cabaña La Montaña', 'Cabaña acogedora en las sierras', 4, 120.00, 'cabaña1.jpg', 1, 'cabaña'),
('Depto Centro', 'Departamento céntrico cerca de todo', 2, 75.50, 'depto1.jpg', 1, 'departamento');

INSERT INTO reservas (id_usuario, id_hospedaje, fecha_checkin, fecha_checkout, cant_personas, importe_total, estado) VALUES
(1, 1, '2025-12-20', '2025-12-25', 2, 600.00, 'confirmada'),
(2, 2, '2025-11-01', '2025-11-03', 1, 151.00, 'pendiente');
