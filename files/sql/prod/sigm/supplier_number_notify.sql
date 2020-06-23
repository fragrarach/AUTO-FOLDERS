DROP TRIGGER IF EXISTS supplier_number_notify ON supplier;
CREATE TRIGGER supplier_number_notify
  AFTER INSERT
  ON supplier
  FOR EACH ROW
  EXECUTE PROCEDURE supplier_number_notify();