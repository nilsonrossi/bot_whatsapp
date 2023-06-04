from dao.base_dao import BaseDAO
from models.customer_model import CustomerModel


class CustomerDAO(BaseDAO):
    def get_or_create_customer(self, phone_number: str, profile_name: str) -> CustomerModel:
        query = """
            SELECT
                id as customer_id,
                profile_name,
                phone_number,
                gender_opt
            FROM
                customer
            WHERE phone_number = %s
        """
        if customer := self._find_one_by_parameters(query, (phone_number,)):
            return CustomerModel(**customer)
        return self.create_customer(phone_number, profile_name)

    def create_customer(self, phone_number: str, profile_name: str) -> CustomerModel:
        query = """
            INSERT INTO customer (phone_number, profile_name)
            VALUES (%s, %s)
        """
        customer_id = self._execute(query, (phone_number, profile_name))
        return CustomerModel(customer_id=customer_id, phone_number=phone_number, profile_name=profile_name, is_new=True)

    def update_customer(self, customer_id: int, gender_opt: int):
        query = """
            UPDATE
                customer
            SET
                gender_opt = %s
            WHERE
                id = %s
        """
        return self._execute(query, (gender_opt, customer_id))
