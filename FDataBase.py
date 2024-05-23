import math
import sqlite3
import time
from _datetime import datetime


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def reg(self, pid, nom, name, email, tel, password, role):
        try:
            self.__cur.execute("INSERT INTO Utilisateur VALUES(?, ?, ?, ?, ?, ?, ?)",
                               (pid, nom, name, email, tel, password, role))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error" + str(e))
            return False
        return True

    def checkReg(self, pid):
        try:
            self.__cur.execute("SELECT * FROM Utilisateur WHERE PASSPORT_ID = ?", (pid, ))
            res = self.__cur.fetchall()
            if res:
                return False
        except sqlite3.Error as e:
            print("Error:    " + str(e))
            return False
        return True

    def passwordLog(self, pid):
        try:
            self.__cur.execute("SELECT PASSWORD FROM Utilisateur WHERE PASSPORT_ID = ?", (pid, ))
            res = self.__cur.fetchone()
            if res:
                return res[0]
        except sqlite3.Error as e:
            print("Error:    " + str(e))
        return False

    def role(self, pid):
        try:
            self.__cur.execute("SELECT ID_ROLE FROM Utilisateur WHERE PASSPORT_ID = ?", (pid, ))
            res = self.__cur.fetchone()
            if res:
                return res[0]
        except sqlite3.Error as e:
            print("Error:    " + str(e))
        return False

    def get_books(self):
        try:
            # self.__cur.execute("SELECT * FROM LIVRE_DESCRIPTION")
            self.__cur.execute("SELECT * FROM LIVRE")
            books = self.__cur.fetchall()
            return books
        except sqlite3.Error as e:
            print("Error: " + str(e))
            return []

    def get_authors(self, book):
        try:
            self.__cur.execute('''SELECT A.ID, (A.NOM || ' ' || A.PRENOM) AS AUTHOR FROM Livre L 
            INNER JOIN Livre_ECRIRE_Auteurs E ON L.ID = E.ID_LIVRE INNER JOIN Auteurs A ON A.ID = E.ID
            WHERE L.ID = ?''', (book, ))
            books = self.__cur.fetchall()
            return books
        except sqlite3.Error as e:
            print("Error: " + str(e))
            return []

    def get_genres(self, book):
        try:
            self.__cur.execute('''SELECT G.ID, G.TITRE FROM Livre L INNER JOIN Livre_CONTIENT_Genres C ON C.ID_LIVRE = L.ID
                    INNER JOIN Genre G ON C.ID = G.ID WHERE L.ID = ?''', (book, ))
            books = self.__cur.fetchall()
            return books
        except sqlite3.Error as e:
            print("Error: " + str(e))
            return []

    def genres(self):
        try:
            self.__cur.execute("SELECT * FROM GENRE")
            res = self.__cur.fetchall()
        except sqlite3.Error as e:
            print("Error:   " + str(e))
            return False
        return res

    def authors(self):
        try:
            self.__cur.execute("SELECT ID, (NOM || ' ' || PRENOM) FROM Auteurs")
            res = self.__cur.fetchall()
        except sqlite3.Error as e:
            print("Error:   " + str(e))
            return False
        return res

    def book(self, b_id):
        try:
            self.__cur.execute("SELECT * FROM LIVRE WHERE ID = ?", (b_id, ))
            res = self.__cur.fetchone()
        except sqlite3.Error as e:
            print("Error:   " + str(e))
            return False
        return res

    def genre(self, g):
        try:
            self.__cur.execute('''SELECT L.* FROM Livre L INNER JOIN Livre_CONTIENT_Genres C ON C.ID_LIVRE = L.ID
                    INNER JOIN Genre G ON C.ID = G.ID WHERE G.ID = ?''', (g, ))
            res = self.__cur.fetchall()
        except sqlite3.Error as e:
            print("Error:   " + str(e))
            return False
        return res

    def author(self, a):
        try:
            self.__cur.execute('''SELECT L.* FROM Livre L 
            INNER JOIN Livre_ECRIRE_Auteurs E ON L.ID = E.ID_LIVRE INNER JOIN Auteurs A ON A.ID = E.ID
            WHERE A.ID = ?''', (a, ))
            res = self.__cur.fetchall()
        except sqlite3.Error as e:
            print("Error:   " + str(e))
            return False
        return res

    def author_id(self, a):
        try:
            self.__cur.execute("SELECT (NOM || ' ' || PRENOM) FROM Auteurs WHERE ID = ?", (a, ))
            res = self.__cur.fetchone()
        except sqlite3.Error as e:
            print("Error:   " + str(e))
            return False
        return res

    def genre_id(self, a):
        try:
            self.__cur.execute("SELECT TITRE FROM Genre WHERE ID = ?", (a, ))
            res = self.__cur.fetchone()
        except sqlite3.Error as e:
            print("Error:   " + str(e))
            return False
        return res

    # def genre_id1(self, a):
    #     try:
    #         self.__cur.execute("SELECT ID FROM Genre WHERE TITRE = ?", (a, ))
    #         res = self.__cur.fetchone()
    #     except sqlite3.Error as e:
    #         print("Error:   " + str(e))
    #         return False
    #     return res

    def exem_book(self, a):
        try:
            self.__cur.execute("SELECT ID_LIVRE FROM Exemplaires WHERE ID = ?", (a, ))
            res = self.__cur.fetchone()
        except sqlite3.Error as e:
            print("Error:   " + str(e))
            return False
        return res

    def exemplaire(self, l):
        try:
            self.__cur.execute('''SELECT E.*, T.NOM_ETAT FROM Exemplaires E INNER JOIN Etat T ON E.ID__ETAT = T.ID
                    WHERE E.ID_LIVRE = ?''', (l, ))
            res = self.__cur.fetchall()
        except sqlite3.Error as e:
            print("Error:   " + str(e))
            return False
        return res

    def searchByName(self, s):
        try:
            self.__cur.execute("SELECT * FROM LIVRE WHERE TITRE LIKE ?", ('%'+s+'%',))
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error:    " + str(e))
        return []

    def searchByAuthors(self, s):
        try:
            # self.__cur.execute("SELECT DISTINCT LivreID, IMG, LivreTitre, DESCRIPTION, NB_EX FROM LIVRE_DESCRIPTION WHERE AUTHOR LIKE ?", ('%'+s+'%',))
            self.__cur.execute("SELECT ID, (NOM || ' ' || PRENOM) FROM Auteurs WHERE (NOM || ' ' || PRENOM) LIKE ?", ('%'+s+'%',))
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error:    " + str(e))
        return []

    def searchByGenre(self, s):
        try:
            # self.__cur.execute("SELECT DISTINCT LivreID, IMG, LivreTitre, DESCRIPTION, NB_EX FROM LIVRE_DESCRIPTION WHERE GenreTitre LIKE ?", ('%'+s+'%',))
            self.__cur.execute("SELECT ID, TITRE FROM GENRE WHERE TITRE LIKE ?", ('%'+s+'%',))
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error:    " + str(e))
        return []

    def check_reservation(self, date_d, date_a):
        try:
            self.__cur.execute("SELECT DATERESD, DATERESRET FROM Application "
                               "WHERE (date(DATERESD) <= date(?) AND date(DATERESRET) >= date(?)) OR "
                               "(date(DATERESD) <= date(?) AND date(DATERESRET) >= date(?)) OR"
                               "(date(DATERESD) >= date(?) AND date(DATERESRET) <= date(?)) OR "
                               "(date(DATERESD) >= date(?) AND date(DATERESRET) <= date(?))",
                               (date_a, date_a, date_d, date_d, date_a, date_d, date_a, date_d))
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error:    " + str(e))
        return []

    def isert_res(self, dd, da, idp, ex):
        try:
            self.__cur.execute("INSERT INTO Application (DATERES, DATERESD, DATERESRET, ID_PASSPORT, ID__EXEMPLAIRES) VALUES(?, ?, ?, ?, ?)",
                               (datetime.today(), dd, da, idp, ex))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error" + str(e))
            return False
        return True

    def getUser(self, id_user):
        try:
            self.__cur.execute("SELECT * FROM Utilisateur WHERE ID = ? LIMIT 1", (id_user,))
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error:    " + str(e))
        return False

    def myRes(self, id_user):
        try:
            self.__cur.execute("SELECT A.DATERESD, A.DATERESRET, L.ID, L.TITRE FROM Application A INNER JOIN Exemplaires E ON A.ID__EXEMPLAIRES = E.ID "
                               "INNER JOIN Livre L ON L.ID = E.ID_LIVRE WHERE A.ID_PASSPORT = ?", (id_user,))
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error:    " + str(e))
        return []

    def users(self):
        try:
            self.__cur.execute(
                "SELECT PASSPORT_ID, (NOM || ' ' || PRENOM) FROM Utilisateur")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error:    " + str(e))
        return []


    def etats(self):
        try:
            self.__cur.execute("SELECT * FROM ETAT")
            books = self.__cur.fetchall()
            return books
        except sqlite3.Error as e:
            print("Error: " + str(e))
            return []

    def addEx(self, imgEx, an, p, lang, prix, em, m_e, id_l, id_et):
        try:
            self.__cur.execute("INSERT INTO Exemplaires VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (imgEx, an, p, lang, prix, em, m_e, id_l, id_et))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False
        return True

    def id_l(self, s):
        try:
            self.__cur.execute("SELECT ID FROM Livre WHERE TITRE = ?",
                               (s,))
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False
        return []

    def id_a(self, s1, s2):
        try:
            self.__cur.execute("SELECT ID FROM Auteurs WHERE NOM = ? AND PRENOM = ?",
                               (s1, s2))
            res = self.__cur.fetchone()[0]
            if res:
                return res
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False
        return []

    def id_g(self, s):
        try:
            self.__cur.execute("SELECT ID FROM Genre WHERE TITRE = ?",
                               (s,))
            res = self.__cur.fetchone()[0]
            if res:
                return res
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False
        return []

    def addAuthor(self, nom, prenom):
        try:
            self.__cur.execute("INSERT INTO Auteurs VALUES(NULL, ?, ?)",
                               (nom, prenom))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False
        return True

    def addGenre(self, g):
        try:
            self.__cur.execute("INSERT INTO Genre VALUES(NULL, ?)",
                               (g, ))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False
        return True

    def addLEA(self, idA, idL):
        try:
            self.__cur.execute("INSERT INTO Livre_ECRIRE_Auteurs VALUES(?, ?)",
                               (idA, idL))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False
        return True

    def addLCG(self, idG, idL):
        try:
            self.__cur.execute("INSERT INTO Livre_CONTIENT_Genres VALUES(?, ?)",
                               (idG, idL))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False
        return True

    def addBook(self, titre, imgL, descr):
        try:
            self.__cur.execute("INSERT INTO Livre VALUES(NULL, ?, ?, ?, ?)",
                               (imgL, titre, descr, 0))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False
        return True

    def plusEx(self, idl):
        try:
            self.__cur.execute("UPDATE Livre SET NB_EX = NB_EX+1 "
                               "WHERE ID = ?",
                               (idl, ))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False
        return True

    # def searchByAuthors(self, authors):
    #     try:
    #         self.__cur.execute(f"CREATE VIEW FIND AS SELECT * FROM LIVRE_DESCRIPTION")
    #         for author in authors:
    #             self.__cur.execute(
    #                 f"CREATE VIEW FIND1 AS SELECT LivreID FROM FIND WHERE AuthorID = {author}")
    #             self.__cur.execute(f"DROP VIEW FIND")
    #             self.__cur.execute(f"CREATE VIEW FIND AS SELECT * FROM FIND1 INNER JOIN LIVRE_DESCRIPTION ON LIVRE_DESCRIPTION.LivreID = FIND.LivreID")
    #             self.__cur.execute(f"DROP VIEW FIND1")
    #         self.__cur.execute(f"SELECT * FROM FIND")
    #         res = self.__cur.fetchall()
    #         self.__cur.execute(f"DROP VIEW FIND")
    #         if res:
    #             self.__cur.execute(f"DROP VIEW FIND")
    #             return res
    #     except sqlite3.Error as e:
    #         print(str(e))
    #     return []
    #
    # def searchByGenres(self, genres):
    #     try:
    #         self.__cur.execute(f"CREATE VIEW FIND AS SELECT * FROM LIVRE_DESCRIPTION")
    #         for genre in genres:
    #             self.__cur.execute(
    #                 f"CREATE VIEW FIND1 AS SELECT LivreID FROM FIND WHERE GenreID = {genre}")
    #             self.__cur.execute(f"DROP VIEW FIND")
    #             self.__cur.execute(
    #                 f"CREATE VIEW FIND AS SELECT * FROM FIND1 INNER JOIN LIVRE_DESCRIPTION ON LIVRE_DESCRIPTION.LivreID = FIND.LivreID")
    #             self.__cur.execute(f"DROP VIEW FIND1")
    #         self.__cur.execute(f"SELECT * FROM FIND")
    #         res = self.__cur.fetchall()
    #         self.__cur.execute(f"DROP VIEW FIND")
    #         if res:
    #             return res
    #     except sqlite3.Error as e:
    #         print(str(e))
    #     return []
    #
    #
    # def searchByName(self, title):
    #     try:
    #         self.__cur.execute(
    #             f"SELECT * FROM LIVRE_DESCRIPTION WHERE LivreTitre LIKE '%{title}%' ORDER BY LivreTitre")
    #         res = self.__cur.fetchall()
    #     except sqlite3.Error as e:
    #         print(str(e))
    #     return []
    #
