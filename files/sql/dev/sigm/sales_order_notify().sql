CREATE OR REPLACE FUNCTION sales_order_notify()
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

PERFORM pg_notify(
        'folders', '['
        || 'ORD' || '], ['
        || NEW.ord_no::text || '], ['
        || sigm_str || ']'
);

RETURN NULL;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION sales_order_notify()
  OWNER TO "SIGM";
