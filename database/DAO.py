from database.DB_connect import DBConnect
from model.Arco import Arco
from model.retailer import Retailer


class DAO:

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT DISTINCT YEAR(date) AS year
            FROM go_daily_sales
            ORDER BY year
        """
        cursor.execute(query)
        result = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRetailersByCountry(country):
        """
        Restituisce tutti i retailer appartenenti alla nazione scelta.
        """
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT retailer_id, retailer_name, country
            FROM go_retailers
            WHERE country = %s
        """

        cursor.execute(query, (country,))
        result = [Retailer(**row) for row in cursor]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(country, year, idMap):
        """
        Restituisce gli archi del grafo:
        due retailer sono collegati se hanno venduto almeno un prodotto in comune
        nello stesso anno.
        Peso = numero di prodotti in comune.
        """
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT r1.retailer_id AS r1,
                   r2.retailer_id AS r2,
                   COUNT(DISTINCT ds1.product_id) AS peso
            FROM go_daily_sales ds1, go_daily_sales ds2,
                 go_retailers r1, go_retailers r2
            WHERE r1.retailer_id = ds1.retailer_id
              AND r2.retailer_id = ds2.retailer_id
              AND r1.country = %s
              AND r2.country = %s
              AND YEAR(ds1.date) = %s
              AND YEAR(ds2.date) = %s
              AND ds1.product_id = ds2.product_id
              AND r1.retailer_id < r2.retailer_id
            GROUP BY r1.retailer_id, r2.retailer_id
            HAVING COUNT(DISTINCT ds1.product_id) > 0
        """

        cursor.execute(query, (country, country, year, year))
        result = []
        for row in cursor:
            id1 = row["r1"]
            id2 = row["r2"]
            peso = row["peso"]

            if id1 in idMap and id2 in idMap:
                result.append(Arco(idMap[id1], idMap[id2], peso))

        cursor.close()
        conn.close()
        return result
