from colector_models import PackingStationHistory, PackingStationInfo
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datetime import datetime

import urllib3

class TakeInfo():

    def __init__(self):
        pass





class Colector_CSV():

    datetime_format = "%d-%m-%Y %H:%M:%S"
    def __init__(self):
        self.init_session_kanban()
        self.read_files()

    def read_files(self):
        self.lines = None
        with open('//10.49.150.154/History/2018_11_12/DayReport2.txt') as f:
            self.lines = f.read().split(sep="\n")
            print(self.lines)
        #[1:] - there is skip header
        for row in self.lines[1:]:

            list_row = row.split(sep=",")

            if len(list_row) == 14:
                 paking_date, packing_time, user_option, shift, packing_station, work_station, box_code, box_num, pn, dpn, harness_sn, _, _, production_sn = list_row

                 date_time = datetime.strptime((paking_date + ' ' + packing_time), Colector_CSV.datetime_format)

                 self.write_db(date_time=date_time, user_option=user_option, shift=shift, packing_station=packing_station, work_station=work_station, box_code=box_code, pn=pn, dpn=dpn, box_num=box_num, \
                      harness_sn=harness_sn, box_ref_manifest='|', manifest='|', production_sn=production_sn, line_name='ABM02')

            else:
                print('incorect data list_row')

    def init_session_kanban(self):
        engine = create_engine("mssql+pyodbc://sa:Prettl!@#4@kanban")
        db_ses = sessionmaker(bind=engine)
        self.db_session = db_ses()

    def write_db(self, date_time, user_option, shift, packing_station, work_station, box_code, pn, dpn, box_num, \
                 harness_sn, box_ref_manifest, manifest, production_sn, line_name):
        print( str(date_time) + '--' + user_option + '--' + shift + '--' + packing_station + '--' + work_station + '--' + box_code + '--' + pn + '--' + dpn + '--' + box_num + '--' + \
            harness_sn + '--' + box_ref_manifest + '--' + manifest + '--' + production_sn )

        try:
            packing_history = PackingStationHistory( packing_datetime=date_time, user_option=user_option, shift=shift, \
                                                     packing_station=packing_station, work_station=work_station, box_code=box_code, \
                                                     box_num=box_num, pn=pn, dpn=dpn, \
                                                     harness_sn=harness_sn, box_ref_manifest=box_ref_manifest, manifest=manifest, \
                                                     production_sn=production_sn, line_name=line_name )
            self.db_session.add(packing_history)

            self.db_session.commit()
        except:
            print('Error in data')

    def take_data_info(self):

        self.username = self.db_session.query( PackingStationInfo.username ).text()

if __name__ == '__main__':
    colector = Colector_CSV()
    colector.read_files()
