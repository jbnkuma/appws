#!/usr/bin/env python3

import apsw
import sys
import logging
import os
import binascii
import configparser

__docfomat_= "restructuredtext"

"""
    :author: Jesus Becerril Navarrete
    :organization: uknow
    :contact: jesusbn5@gmail.com
    :requires: python == 3

"""

class  Logs:
    def __init__(self,file_log='/home/jbnkuma/myapp.log'):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file_log)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.hdlr.setFormatter(formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.DEBUG)
    def  info_log(self, message):
        self.logger.info(message)

    def error_log(self, message):
        self.logger.error(message)

    def close_logs(self):
        self.logger.removeHandler(self.hdlr)
        self.hdlr.close()


class DataBase:
    """Clase que manipula la base de datos del servidor el gestor es sqlite"""
    ##      self.ip_dinamica = ip_dinamica

    def __init__(self, file2logs, db):
        self.write_logs = Logs(file2logs)
        self.db = db

    #---Query
    def dataSearch(self, statements, table, provisory, data):
        """Funcion que realiza un query o busqueda dentro de las tablas de la base de sqlite"""

        global cursor, connection
        self.write_logs.info_log("Searching the database: %s in table %s " % (self.db, table))

        try:
            connection = apsw.Connection(self.db)
            cursor = connection.cursor()

            if provisory != "" and data != "":
                statement = "SELECT " + statements + "  FROM " + table + provisory
                cursor.execute(statement, data)
                return cursor, connection

            if provisory != "" and data == "":
                statement= "SELECT " + statements + "  FROM " + table + provisory
                cursor.execute(statement)
                return cursor, connection

            if provisory == "":
                statement = "SELECT " + statements + "  FROM " + table
                cursor.execute(statement)

                return cursor, connection

        except IOError:
            self.write_logs.error_log("There were problems in the database to perform the query"
            + "({0}): {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
            cursor()
            connection.close()

            #---Insert

    def insertion(self, table, statements, provisory, data):
        """Funcion que realiza la inscersion de datos en una tabla de sqlite"""

        self.write_logs.info_log("Incerting data in the database: %s in table %s " % (self.db, table))
        try:
            connection = apsw.Connection(self.db)
            cursor = connection.cursor()

            statement = "INSERT INTO " + table + statements + "VALUES" + provisory
#            self.write_logs.info_log(statement)
#            self.write_logs.info_log(data)
            cursor.execute(statement, data)
            cursor.close()
            connection.close()
            return "ok"


        except IOError:
            self.write_logs.error_log("There were problems in the database to perform the query:    "
            + "({0}): {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
            return "error"
            #---Total

    def totalData(self, column, table):
        """"Funcion que contabiliza el numero total de registros de en una tabla"""
        try:
            self.write_logs.info_log("Obtaining the total data in the table %s  column %s " % (table, column))
            connection = apsw.Connection(self.db)
            cursor = connection.cursor()
            statement = "SELECT  COUNT(" + column + ") FROM " + table
            total_column= cursor.execute(statement)
            return int(total_column.fetchone()[0])

        except IOError:
            self.write_logs.error_log("here were problems in the database to perform the query"
            + "({0}): {1}".format(sys.exc_info()[0],sys.exc_info()[1]))

    def multi_data_insert(self, table, statements, provisory, information):
        self.write_logs.info_log("Please wait storing information")
        try:
            for data in information:
                self.insertion(table, statements, provisory, data)
        except IOError:
            self.write_logs.error_log("here were problems in the database to perform the query"
                                      + "({0}): {1}".format(sys.exc_info()[0],sys.exc_info()[1]))

        #---Drop

    def tableDelete(self, table):
        """Funcion que borra una tabla de la base de datos"""
        try:
            self.write_logs.info_log("We proceed to clear the table: %s" % table)
            connection = apsw.Connection(self.db)
            cursor = connection.cursor()

            statement = "DROP TABLE IF EXISTS  " + table
            cursor.execute(statement)
        ##        conn.commit()
            cursor.close()
            connection.close()
        except IOError:
            self.write_logs.error_log("It presented a problem when performing the operation in the database"
            + "({0}): {1}".format(sys.exc_info()[0], sys.exc_info()[1]))

    def dataErase(self, table, provisory):
        """Funcion que borra datos de una tabla"""
        try:
            self.write_logs.info_log("Removal takes place the data in Table %s " % table)
            connection =  apsw.Conectiont(self.db)
            cursor = connection.cursor()
            statement = "DELETE FROM " + table + provisory
            cursor.execute(statement)
            cursor.close()
            connection.close()

        except IOError:
            self.write_logs.error_log("It presented a problem when performing the operation in the database"
            + "({0}): {1}".format(sys.exc_info()[0], sys.exc_info()[1]))

        #---Create_table

    def createTable(self, table_name, values):
        """Funcion para la creacion de la base de datos"""
        try:
            self.write_logs.info_log("It was made the creation of the table %s , in the database %s" %
            (table_name,self.db))
            connection = apsw.Connection(self.db)
            cursor = connection.cursor()
            statement = "CREATE TABLE IF NOT EXISTS  " + table_name + values
            cursor.execute(statement)
            cursor.close()
            connection.close()

        except IOError:
            self.write_logs.error_log("It presented a problem when performing the operation in the database"
            + "({0}): {1}".format(sys.exc_info()[0], sys.exc_info()[1]))

class UploadConfig:
    def __init__(self):
        self.file_config = "~/PycharmProjects/appws/src/service.conf"

    def get_config(self):
        try:
            conf = configparser.ConfigParser()
            conf.read(['service.conf', os.path.expanduser(self.file_config)])
            file2log = conf.get("config", "file_log")
            file2database = conf.get("config", "database")
            return file2log,file2database

        except IOError:
            print ("It presented a problem when performing the operation in the database"
            + "({0}): {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
            return ""

class nodata(Exception):
    def __init__(self, data):
        print ("The data value is null ")

class SessionGenerator:
    def get_session(self):

        session_hash = binascii.b2a_hex(os.urandom(128))
        return session_hash