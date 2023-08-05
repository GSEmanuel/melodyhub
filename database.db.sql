BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "evento" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"nombre"	TEXT,
	"artista"	TEXT,
	"genero"	TEXT,
	"id_ubicacion"	INTEGER,
	"hora_inicio"	TEXT,
	"descripcion"	TEXT,
	"imagen"	BLOB,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "usuario" (
	"id"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"contraseña"	TEXT,
	"historial_eventos"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ruta" (
	"id_evento"	INTEGER,
	"id_usuario"	INTEGER
);
CREATE TABLE IF NOT EXISTS "ubicacion" (
	"id"	INTEGER NOT NULL,
	"direccion"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "review" (
	"id"	INTEGER,
	"id_evento"	INTEGER NOT NULL,
	"id_usuario"	INTEGER,
	"calificacion"	TEXT,
	"comentario"	TEXT,
	PRIMARY KEY("id_evento" AUTOINCREMENT)
);
COMMIT;
