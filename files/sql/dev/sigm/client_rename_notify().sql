CREATE OR REPLACE FUNCTION client_rename_notify()
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

IF OLD.cli_no <> NEW.cli_no THEN
    PERFORM pg_notify(
            'folders', '['
            || 'PRT RENAME' || '], [{'
            || OLD.cli_no::text || '}, {'
            || NEW.cli_no::text || '}], ['
            || sigm_str || ']'
    );
END IF;

RETURN NULL;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION client_rename_notify()
  OWNER TO "SIGM";
