CREATE OR REPLACE FUNCTION part_rename_notify()
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

IF OLD.prt_no <> NEW.prt_no THEN
    PERFORM pg_notify(
            'folders', '['
            || 'PRT RENAME' || '], [{'
            || OLD.prt_no::text || '}, {'
            || NEW.prt_no::text || '}], ['
            || sigm_str || ']'
    );
END IF;

RETURN NULL;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION part_rename_notify()
  OWNER TO "SIGM";
