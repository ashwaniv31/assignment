import datetime
import mysql.connector as c


class accessData:
    def __init__(self):
        self.con = c.connect(
            host="localhost",
            port=3306,
            user="ashwani",
            password="Ashwani_123",
            database="mydb1",
            db="python"
        )

        stmt = "SHOW TABLES LIKE 'users'"
        cursor = self.con.cursor()
        cursor.execute(stmt)
        result = cursor.fetchall()
        if not result:
            query = """
                    CREATE TABLE `mydb1`.`users` (
                          `ID` INT NOT NULL AUTO_INCREMENT,
                          `first_name` VARCHAR(50) NOT NULL,
                          `last_name` VARCHAR(50) NOT NULL,
                          `mobile_no` VARCHAR(15) NOT NULL,
                          `address` VARCHAR(100) NULL,
                          `created` DATE NOT NULL,
                          `updated` DATE NULL,
                          PRIMARY KEY (`ID`));
                    """
            cursor.execute(query)
            cursor.close()
            self.con.commit()

    def fetchData(self, querry):
        cursor = self.con.cursor()
        cursor.execute(querry)
        result = cursor.fetchall()
        myJSON = []
        for i in range(len(result)):
            myJSON.append({
                "Id": result[i][0],
                "firstName": result[i][1],
                "lastName": result[i][2],
                "mobileNo": result[i][3],
                "address": result[i][4],
                "created": result[i][5],
                "updated": result[i][6]
            })
        return myJSON

    def addData(self, values):
        querry = "INSERT INTO users(first_name,last_name,mobile_No,Address,created) values(%s,%s,%s,%s,%s)"
        cursor = self.con.cursor()
        cursor.execute(querry, values)
        cursor.close()
        self.con.commit()

    def delete(self, querry):
        cursor = self.con.cursor()
        cursor.execute(querry)
        cursor.close()
        self.con.commit()

    def getData(self, id):
        cursor = self.con.cursor()
        cursor.execute(f"select * from users where id={id}")
        result = cursor.fetchall()
        return result

    def updateData(self,values,id):
        cursor = self.con.cursor()
        query = f"update users set first_name='{values[0]}',last_name='{values[1]}',mobile_no='{values[2]}',address='{values[3]}',updated='{str(datetime.datetime.now())}' where id={id}"
        cursor.execute(query)
        cursor.close()
        self.con.commit()
