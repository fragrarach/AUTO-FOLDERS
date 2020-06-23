CREATE OR REPLACE FUNCTION supplier_rename_notify()
  RETURNS trigger AS
$BODY$
DECLARE
sigm_str TEXT;
BEGIN
sigm_str := (
    SELECT application_name
    FROM pg_stat_activity
    WHERE pid IN (
        SELECT pg_backend_pid()
    )
);

IF OLD.sup_no <> NEW.sup_no THEN
    PERFORM pg_notify(
            'folders', '['
            || 'SUP RENAME' || '], [{'
            || OLD.sup_no::text || '}, {'
            || NEW.sup_no::text || '}], ['
            || sigm_str || ']'
    );
END IF;

RETURN NULL;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION supplier_rename_notify()
  OWNER TO "SIGM";
