DROP TRIGGER IF EXISTS part_number_notify ON part;
CREATE TRIGGER part_number_notify
  AFTER INSERT
  ON part
  FOR EACH ROW
  EXECUTE PROCEDURE part_number_notify();
