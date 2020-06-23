DROP TRIGGER IF EXISTS supplier_rename_notify ON supplier;
CREATE TRIGGER supplier_rename_notify
  AFTER UPDATE
  ON supplier
  FOR EACH ROW
  EXECUTE PROCEDURE supplier_rename_notify();