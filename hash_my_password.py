from datetime import datetime
from simplecrypto import encrypt, decrypt
from base64 import b64encode, b64decode

import easygui
from colector_models import PackingStationInfo
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import logging

class WriteHashCredantials():

    def __init__(self):
        self.init_session_kanban()
        s = self.take_data_info()
        easygui.msgbox( str( s ) )
        self.make_config_packing_station()


    def make_config_packing_station(self):

        packing_config = easygui.multpasswordbox( 'Connection data for Packing station', 'Packing Station',
                                                  ["DayReport2", "Folder", "Ip address packing station",
                                                   "Name Packing station", "Login", "Password"] )


        salt_key = int(datetime.timestamp(datetime.now()))
        name_file = packing_config[0]
        name_folder = packing_config[1]
        ip_address = packing_config[2]
        name_p_s = packing_config[3]
        cipher_login = encrypt(packing_config[4], str(salt_key))
        cipher_password = encrypt(packing_config[5], str(salt_key))
        print(cipher_password)
        encoded_cipher_login = b64encode(str(cipher_login).encode('utf-8'))
        encoded_cipher_password = b64encode(str(cipher_password).encode('utf-8'))
        url_file = '\\10.49.150.154\\History\\2018_11_15'
        if cipher_password != None:
            self.write_credentials(login=str(encoded_cipher_login), password=str(encoded_cipher_password), salt_key=salt_key,
                                   name_file=name_file, name_folder=name_folder, ip_address=ip_address,
                                   name_packing_station=name_p_s, url_file=url_file)
        else:
            logging.warning('Incorect data')

    def init_session_kanban(self):

        engine = create_engine("mssql+pyodbc://@kanban")
        db_ses = sessionmaker(bind=engine)
        self.db_session = db_ses()


    def write_credentials(self, login, password, salt_key, name_file, name_folder,
                          ip_address, name_packing_station, url_file):


        print(type(salt_key))
        packing_info = PackingStationInfo( username=login, password=password, salt_key=str(salt_key),
                                           name_file=name_file, name_folder=name_folder, ip_address=ip_address,
                                           name_packing_station=name_packing_station, url_file=url_file)
        self.db_session.add(packing_info)
        self.db_session.commit()



    def take_data_info(self):

        user = self.db_session.query( PackingStationInfo.username ).first()
        password = self.db_session.query( PackingStationInfo.password ).first()
        salt_key = self.db_session.query( PackingStationInfo.salt_key ).first()
        print(password[0])
        #cipher_password = b64decode(password[0]).decode('utf-8')
        #print(cipher_password)

        print(salt_key[0])
        #decrypt_user = decrypt(user[0], salt_key[0])

        #return b64decode(decrypt_user.decode('utf-8'))





if __name__ == '__main__':
    credentials = WriteHashCredantials()



