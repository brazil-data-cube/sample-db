SET CLIENT_ENCODING TO UTF8;

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE SCHEMA bdc;

CREATE TABLE bdc.users (
  id SERIAL PRIMARY KEY,
  full_name VARCHAR,
  email     VARCHAR NOT NULL UNIQUE,
  password  VARCHAR NOT NULL
);

CREATE TABLE bdc.luc_classification_system
(
  id              SERIAL PRIMARY KEY,
  authority_name  TEXT NOT NULL,
  system_name     TEXT NOT NULL,
  description     TEXT NOT NULL,
  user_id         INTEGER NOT NULL,
  created_at      TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  updated_at      TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  FOREIGN KEY (user_id)
              REFERENCES bdc.users(id)
              MATCH FULL ON DELETE NO ACTION
);

CREATE TABLE bdc.luc_class
(
  id           SERIAL PRIMARY KEY,
  class_name   TEXT NOT NULL,
  description  TEXT NOT NULL,
  luc_classification_system_id INTEGER NOT NULL,
  parent_id    INTEGER NULL,
  user_id      INTEGER NOT NULL,
  created_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  updated_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  FOREIGN KEY (luc_classification_system_id)
              REFERENCES bdc.luc_classification_system(id)
              MATCH FULL ON DELETE NO ACTION,
  FOREIGN KEY (user_id)
              REFERENCES bdc.users(id)
              MATCH FULL ON DELETE NO ACTION,

  FOREIGN KEY (parent_id) REFERENCES bdc.luc_class(id) MATCH FULL ON DELETE NO ACTION

);

--CREATE TABLE bdc.class_mapping
--(
--  src_id       INTEGER NOT NULL,
--  target_id    INTEGER NOT NULL,
--  description  TEXT NULL,
--  degree_of_similarity NUMERIC,
--  PRIMARY KEY(src_id, target_id),
--  FOREIGN KEY (src_id)
--              REFERENCES bdc.luc_class(id)
--              MATCH FULL ON DELETE NO ACTION,
--  FOREIGN KEY (target_id)
--              REFERENCES bdc.luc_class(id)
--              MATCH FULL ON DELETE NO ACTION
--);

-- TODO: Support both location of sample and region
-- CREATE TABLE bdc.location
-- (
--   gid       SERIAL PRIMARY KEY,
--   location  GEOMETRY(POINT, 4326),
--   region    GEOMETRY(POLYGON, 4326)
-- );

CREATE TABLE bdc.observation
(
  id          SERIAL PRIMARY KEY,
  start_date  DATE NOT NULL,
  end_date    DATE NOT NULL,
  location    GEOMETRY(POINT, 4326),
  class_id    INTEGER NOT NULL,
  user_id     INTEGER NOT NULL,
  created_at  TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  updated_at  TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  FOREIGN KEY (class_id)
              REFERENCES bdc.luc_class(id)
              MATCH FULL ON DELETE NO ACTION,
  FOREIGN KEY (user_id)
              REFERENCES bdc.users(id)
              MATCH FULL ON DELETE NO ACTION
);

CREATE TABLE bdc.sample_set
(
  id          SERIAL PRIMARY KEY,
  name        VARCHAR NOT NULL,
  description TEXT,
  created_at  TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  updated_at  TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  user_id     INTEGER NOT NULL,
  luc_classification_system_id INTEGER NOT NULL,
  FOREIGN KEY (user_id)
              REFERENCES bdc.users(id)
              MATCH FULL ON DELETE NO ACTION,
  FOREIGN KEY (luc_classification_system_id)
              REFERENCES bdc.luc_classification_system(id)
              MATCH FULL ON DELETE NO ACTION
);

CREATE INDEX bdc_observation_location_idx ON bdc.observation USING GIST(location);

CREATE OR REPLACE FUNCTION bdc.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = now();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_luc_classification_system BEFORE UPDATE
    ON bdc.luc_classification_system FOR EACH ROW EXECUTE PROCEDURE
    bdc.set_updated_at();

CREATE TRIGGER update_luc_class BEFORE UPDATE
    ON bdc.luc_class FOR EACH ROW EXECUTE PROCEDURE
    bdc.set_updated_at();

CREATE TRIGGER update_observation BEFORE UPDATE
    ON bdc.observation FOR EACH ROW EXECUTE PROCEDURE
    bdc.set_updated_at();

CREATE TRIGGER update_sample_set BEFORE UPDATE
    ON bdc.sample_set FOR EACH ROW EXECUTE PROCEDURE
    bdc.set_updated_at();


INSERT INTO bdc.users ( full_name, email, password ) VALUES ( 'Admin', 'admin@admin.com', crypt('admin', gen_salt('bf')) );

INSERT INTO bdc.luc_classification_system (authority_name, system_name, description, user_id)
     VALUES ( 'Brazil Data Cubes', 'BDC', 'Brazilian Earth Observation Data Cube', 1 );

END;
