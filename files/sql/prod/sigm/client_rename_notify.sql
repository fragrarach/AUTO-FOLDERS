DROP TRIGGER IF EXISTS client_rename_notify ON client;
CREATE TRIGGER client_rename_notify
  AFTER UPDATE
  ON client
  FOR EACH ROW
  EXECUTE PROCEDURE client_rename_notify();