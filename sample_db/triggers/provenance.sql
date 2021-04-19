--
--  This file is part of Sample Database Model.
--  Copyright (C) 2021 INPE.
--
--  Sample Database Model is free software; you can redistribute it and/or modify it
--  under the terms of the MIT License; see LICENSE file for more details.
--

--
-- Function to validate the dataset provenance.
-- Triggered when INSERT/UPDATE in provenance validate the relationship.
--
CREATE OR REPLACE FUNCTION check_provenance()
RETURNS trigger AS $$
DECLARE
    result RECORD;
    query TEXT;
BEGIN

    query := 'WITH RECURSIVE dataset_provenance AS '
              || '( SELECT dataset_id, dataset_parent_id FROM sampledb.provenance WHERE dataset_id = $1 '
              || 'UNION SELECT e.dataset_id, e.dataset_parent_id FROM sampledb.provenance e '
		      || 'INNER JOIN dataset_provenance s ON s.dataset_parent_id = e.dataset_id ) '
		      || 'SELECT dataset_id, dataset_parent_id FROM dataset_provenance';

    FOR result IN EXECUTE query USING NEW.dataset_parent_id LOOP
        IF NEW.dataset_id = result.dataset_parent_id THEN
            RAISE EXCEPTION 'Dataset cannot be parent and child at same time';
        END IF;

    END LOOP;

END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS check_provenance_trigger
  ON sampledb.provenance;

CREATE TRIGGER check_provenance_trigger
BEFORE INSERT OR UPDATE
ON sampledb.provenance
FOR EACH ROW EXECUTE PROCEDURE check_provenance();