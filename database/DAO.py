from database.DB_connect import DBConnect
from model.name import Name


class DAO():


    @staticmethod
    def getAllRatings():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct avg_rating 
                    from ratings
                    order by avg_rating asc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["avg_rating"])

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllNodes(voto1, voto2):

        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct n.*
                from ratings r, movie m, role_mapping rm, names n 
                where n.id = rm.name_id 
                and rm.movie_id = m.id 
                and m.id = r.movie_id 
                and r.avg_rating between %s and %s
                and n.date_of_birth is not null"""

            cursor.execute(query, (voto1, voto2))

            for row in cursor:
                result.append(Name(**row))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllEdges(voto1, voto2):

        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct n1.id as id1, n2.id as id2,
                sum(cast(replace(m1.worlwide_gross_income, "$", "") as int)) as peso
                from ratings r1, movie m1, role_mapping rm1, names n1,
                    ratings r2, movie m2, role_mapping rm2, names n2
                where n1.id = rm1.name_id 
                and rm1.movie_id = m1.id 
                and m1.id = r1.movie_id 
                and r1.avg_rating >= %s and r1.avg_rating <= %s
                and n1.date_of_birth is not null
                and n2.id = rm2.name_id 
                and rm2.movie_id = m2.id 
                and m2.id = r2.movie_id 
                and r2.avg_rating >= %s and r2.avg_rating <=%s
                and n2.date_of_birth is not null
                and n1.id < n2.id
                and rm1.movie_id = rm2.movie_id 
                and m1.worlwide_gross_income is not null
                and m2.worlwide_gross_income is not null
                group by n1.id, n2.id"""

            cursor.execute(query, (voto1, voto2, voto1, voto2))

            for row in cursor:
                result.append((row["id1"], row["id2"], row["peso"]))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllNames():

        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                    from names"""

            cursor.execute(query, )

            for row in cursor:
                result.append(Name(**row))

            cursor.close()
            cnx.close()

        return result