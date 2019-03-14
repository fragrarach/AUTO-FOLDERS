-- Trigger: sales_order_notify on order_header

-- DROP TRIGGER sales_order_notify ON order_header;

CREATE TRIGGER sales_order_notify
  AFTER INSERT
  ON order_header
  FOR EACH ROW
  EXECUTE PROCEDURE sales_order_notify();
