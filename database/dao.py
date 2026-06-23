from unittest import result

from flet.core import row

from database.DB_connect import DBConnect
from model.user import User

class Dao:
    def __init__(self):
        pass

    @staticmethod
    def read_all_users():
        print("Executing read from database using SQL query")

        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT * FROM Users """

        cursor.execute(query)

        for row in cursor:
            user = User(
                row["user_id"],
                row["votes_funny"],
                row["votes_useful"],
                row["votes_cool"],
                row["name"],
                row["average_stars"],
                row["review_count"]
            )

            results.append(user)

        cursor.close()
        cnx.close()

        return results

    @staticmethod
    def get_business_counts():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
        SELECT user_id, COUNT(DISTINCT business_id) as num_bus
        FROM Reviews            
        GROUP BY user_id
        """
        cursor.execute(query)
        result = {row['user_id']: row['num_bus'] for row in cursor}
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_shared_businesses():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
        SELECT R1.user_id AS U1, R2.user_id AS U2, COUNT(DISTINCT R1.business_id) as peso
        FROM Reviews R1
        JOIN Reviews AS R2 on R1.business_id = R2.business_id
        WHERE R1.user_id < R2.user_id
        GROUP BY R1.user_id, R2.user_id
        """
        cursor.execute(query)
        result = [(row['U1'], row['U2'], row['peso']) for row in cursor]
        cursor.close()
        cnx.close()
        return result



