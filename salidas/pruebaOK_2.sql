CREATE TABLE ventas (cliente VARCHAR(255), compra DECIMAL);
SELECT cliente, compra FROM ventas WHERE total > 100;
UPDATE ventas SET total = 110 WHERE cliente = 'Pedro';
DROP TABLE ventas;
