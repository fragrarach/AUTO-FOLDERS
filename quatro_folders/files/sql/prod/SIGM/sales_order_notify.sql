DROP TRIGGER IF EXISTS sales_order_notify ON order_header;
CREATE TRIGGER sales_order_notify
  AFTER INSERT
  ON order_header
  FOR EACH ROW
  EXECUTE PROCEDURE sales_order_notify();
