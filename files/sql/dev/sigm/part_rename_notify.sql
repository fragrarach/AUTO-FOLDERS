DROP TRIGGER IF EXISTS part_rename_notify ON part;
CREATE TRIGGER part_rename_notify
  AFTER UPDATE
  ON part
  FOR EACH ROW
  EXECUTE PROCEDURE part_rename_notify();
