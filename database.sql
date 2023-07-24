--Creación de la base de datos
CREATE DATABASE productos;
--Creación de la tabla
CREATE TABLE productos (
  id INT PRIMARY KEY AUTO_INCREMENT,
  referencia VARCHAR(100),
  stock INT,
  parent_id INT,
  nivel VARCHAR(10),
  FOREIGN KEY (parent_id) REFERENCES productos (id)
);
--Inserción de datos
INSERT INTO productos (id, referencia, stock, parent_id, nivel)
VALUES (1, 'Aceites', NULL, NULL, '1'),
       (2, 'Motor', NULL, 1, '1.1'),
       (3, 'Minerales', NULL, 2, '1.1.1'),
       (4, 'Castrol 20w50', 15, 3, '1.1.1.1'),
       (5, 'Valvoline 15w', 12, 3, '1.1.1.2'),
       (6, 'Sintéticos', NULL, 2, '1.1.2'),
       (7, 'Shell Helix Ultra SN 5w30', 50, 6, '1.1.2.1'),
       (8, 'Castrol 5w30', 20, 6, '1.1.2.2'),
       (9, 'Semi-sintético', NULL, 2, '1.1.3'),
       (10, 'Shell 5w30', 14, 9, '1.1.3.1'),
       (11, 'Valvoline 5w30', 20, 9, '1.1.3.2');

--Consulta para obtener los datos deseados
SELECT
  nivel as Referencia,
  referencia as Descripcion,
  (
    SELECT COALESCE(SUM(stock), 0)
    FROM productos p2
    WHERE p2.nivel LIKE CONCAT(p1.nivel, '%')
  ) AS Stock
FROM productos p1
ORDER BY nivel ASC;