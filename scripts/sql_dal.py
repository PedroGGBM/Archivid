from logging import NOTSET, exception
from os import name
import sqlite3
from common import load_configuration_item

def connect_to_db():

        connection_string = load_configuration_item("connection_string")

        try:
            con = sqlite3.connect(connection_string)
            return con
        except:
            return None

class SQL_DAL:

    def __init__(self):  
        self.keys_by_table = {
            "users":["id","user_name","email","hashed_pass","salt"],
            "studio_gronda_proj":["id","property_type","location","image_str"],
            "studio_client":["id","property_type","location","image_str"],
            "studio_talent":["id","property_type","location","image_str"]
        }
        self.conn_obj = connect_to_db()   

    def _table_names_sanity_check(self,table_to_fetch):
        
        if table_to_fetch in self.keys_by_table.keys():
            return True
        else:
            return False

    def _create_insert_query_pholder(self,table,len_tuple_record_values):
        query= f'insert into {table} values ('

        query += ''.join(['?,' for i in range(len_tuple_record_values-1)])
        query+='?)'
        return query

    def load_record_by_column(self,table_name,column_value, column_id):
        records= self.load_table_records(table_name)
        filter_to_pass = lambda x:x[column_id]==column_value 
        
        filtered= list(filter(filter_to_pass,records))
        if len(filtered)==1:
            return filtered[0]
        if len(filtered)==0:
            return None
        raise Exception("More than one item share the same id on the table")

    def load_record_by_id(self,table_name,id):
        records= self.load_table_records(table_name)
        filter_to_pass = lambda x:x[0]==id 
        
        filtered= list(filter(filter_to_pass,records))
        if len(filtered)==1:
            return filtered[0]
        if len(filtered)==0:
            return None
        raise Exception("More than one item share the same id on the table")

    def load_table_records(self, table_name):
        con_obj = self.conn_obj
        if con_obj is None:
            raise Exception("Couldnt connect to sql")
        
        is_sane= self._table_names_sanity_check(table_name)
        if not is_sane:
            raise Exception("invalid table name")
        
        query= f'SELECT * FROM {table_name}'
        cursor = con_obj.execute(query)
        return cursor # lazy iteration

    def insert_record(self,table_name, tuple_values):
        con_obj = self.conn_obj
        if con_obj is None:
            raise Exception("Couldnt connect to sql")
        
        is_sane= self._table_names_sanity_check(table_name)
        if not is_sane:
            raise Exception("invalid table name")

        if len(tuple_values)!=len(self.keys_by_table[table_name]):
            raise Exception("Values badly formated")
        
        safe_prefix = self._create_insert_query_pholder(table_name,len(tuple_values))
        
        cursor = con_obj.cursor()

        cursor.execute(safe_prefix,tuple_values)
        con_obj.commit()
        
    def insert_many_records(self,table_name, list_tuple_values):
        con_obj = self.conn_obj
        if con_obj is None:
            raise Exception("Couldnt connect to sql")
        
        is_sane= self._table_names_sanity_check(table_name)
        if not is_sane:
            raise Exception("invalid table name")
        
        for tuple_value in list_tuple_values:
            if len(tuple_value)!=len(self.keys_by_table[table_name]):
                raise Exception("Values badly formated")
        
        safe_prefix = self._create_insert_query_pholder(table_name, len(list_tuple_values[0]))
        
        cursor = con_obj.cursor()

        cursor.executemany(safe_prefix,list_tuple_values)
        con_obj.commit()

    def remove_record(self,table_name,item_id):
        con_obj = self.conn_obj
        if con_obj is None:
            raise Exception("Couldnt connect to sql")
        
        is_sane= self._table_names_sanity_check(table_name)
        if not is_sane:
            raise Exception("invalid table name")

        cursor = con_obj.cursor()
        sql_update_query = f'DELETE from {table_name} where id = ?' # updated to avoid SQL injection
        cursor.execute(sql_update_query, (item_id,))
        con_obj.commit()




