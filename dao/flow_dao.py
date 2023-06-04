from datetime import datetime, timezone

from dao.base_dao import BaseDAO
from dao.customer_dao import CustomerDAO
from models.customer_model import CustomerModel
from models.flow_model import FlowModel


class FlowDAO(BaseDAO):
    def __init__(self, conn):
        self.customer_dao = CustomerDAO(conn)
        super().__init__(conn)

    def get_or_create_flow(self, phone_number: str, customer: CustomerModel) -> FlowModel:
        query = """
            SELECT
                f.id as flow_id,
                f.customer_id,
                instance_id,
                f.start_date
            FROM
                flow f
            JOIN customer c on c.id = f.customer_id
            WHERE
                c.phone_number = %s
                AND end_date IS NULL
        """
        if flow := self._find_one_by_parameters(query, (phone_number,)):
            return FlowModel(**flow, is_new=False)

        return self.create_flow(customer)

    def create_flow(self, customer: CustomerModel) -> FlowModel:
        start_date = datetime.now(timezone.utc)
        query = """
            INSERT INTO flow (customer_id, start_date)
            VALUES (%s, %s)
        """
        flow_id = self._execute(query, (customer.customer_id, start_date))
        return FlowModel(flow_id=flow_id, customer_id=customer.customer_id, start_date=start_date, is_new=True)

    def set_instance_id(self, instance_id: int, flow_id: str):
        query = """
            UPDATE
                flow
            SET
                instance_id = %s
            WHERE
                id = %s
        """
        return self._execute(query, (flow_id, instance_id))

    def finish_flow(self, instance_id: str):
        query = """
            UPDATE
                flow
            SET
                end_date = NOW()
            WHERE
                instance_id = %s
        """
        return self._execute(query, (instance_id,))
