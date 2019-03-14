-- Trigger: purchase_order_notify on purchase_order_header

-- DROP TRIGGER purchase_order_notify ON purchase_order_header;

CREATE TRIGGER purchase_order_notify
  AFTER INSERT
  ON purchase_order_header
  FOR EACH ROW
  EXECUTE PROCEDURE purchase_order_notify();
