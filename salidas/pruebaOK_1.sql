CREATE TABLE alumnos (nota DECIMAL, nombre VARCHAR(255));
SELECT nota, nombre FROM alumnos WHERE nota > 5 + 1;
UPDATE alumnos SET nota = 100 - 20.1 * 5 + 8 WHERE nombre = 'Enzo';
DROP TABLE alumnos;
