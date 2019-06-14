SET CLIENT_ENCODING TO UTF8;

BEGIN;

CREATE SCHEMA bdc;

CREATE TABLE bdc.luc_classification_system
(
  id              SERIAL PRIMARY KEY,
  authority_name  TEXT NOT NULL,
  system_name     TEXT NOT NULL,
  description     TEXT NOT NULL
);

CREATE TABLE bdc.luc_class
(
  id           SERIAL PRIMARY KEY,
  class_name   TEXT NOT NULL,
  description  TEXT NOT NULL,
  luc_classification_system_id INTEGER NOT NULL,
  parent_id    INTEGER NULL,
  FOREIGN KEY (luc_classification_system_id)
              REFERENCES bdc.luc_classification_system(id)
              MATCH FULL ON DELETE NO ACTION,

  FOREIGN KEY (parent_id) REFERENCES bdc.luc_class(id) MATCH FULL ON DELETE NO ACTION

);

CREATE TABLE bdc.class_mapping
(
  src_id       INTEGER NOT NULL,
  target_id    INTEGER NOT NULL,
  description  TEXT NULL,
  degree_of_similarity NUMERIC,
  PRIMARY KEY(src_id, target_id),
  FOREIGN KEY (src_id)
              REFERENCES bdc.luc_class(id)
              MATCH FULL ON DELETE NO ACTION,
  FOREIGN KEY (target_id)
              REFERENCES bdc.luc_class(id)
              MATCH FULL ON DELETE NO ACTION
);

CREATE TABLE bdc.location
(
  gid       SERIAL PRIMARY KEY,
  location  GEOMETRY(POINT, 4326),
  region    GEOMETRY(POLYGON, 4326)
);

CREATE TABLE bdc.observation
(
  id          SERIAL PRIMARY KEY,
  start_date  DATE NOT NULL,
  end_date    DATE NOT NULL,
  location    GEOMETRY(POINT, 4326),
  class_id    INTEGER NOT NULL,
  FOREIGN KEY (class_id)
              REFERENCES bdc.luc_class(id)
              MATCH FULL ON DELETE NO ACTION
);

INSERT INTO bdc.luc_classification_system (authority_name, system_name, description)
     VALUES ( 'Brazil Data Cubes', 'BDC', 'Brazilian Earth Observation Data Cube' );

END;
