DROP TRIGGER IF EXISTS client_number_notify ON client;
CREATE TRIGGER client_number_notify
  AFTER INSERT
  ON client
  FOR EACH ROW
  EXECUTE PROCEDURE client_number_notify();