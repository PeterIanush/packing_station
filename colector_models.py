from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Binary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class PackingStationHistory( Base ):

    __tablename__ = 'Packing_history'
    id = Column('id', Integer, primary_key=True)
    packing_datetime = Column('packing_datetime', DateTime)
    user_option = Column('user_option', String(50), nullable=False)
    shift = Column('shift', String(10), nullable=False)
    packing_station = Column('packing_station', String(100), nullable=False)
    work_station = Column('work_station', String(100), nullable=False)
    box_code = Column('box_code', String(50), nullable=False)
    box_num = Column('box_num', String(10), nullable=False)
    pn = Column('pn', String(10), nullable=False)
    dpn = Column('dpn', String(12), nullable=False)
    harness_sn = Column('harness_sn', String(50), nullable=False)
    box_ref_manifest = Column('box_ref_manifest', String(100), nullable=True)
    manifest = Column('manifest', String(100), nullable=True)
    production_sn = Column('production', String(100), nullable=False)
    line_name = Column( 'line_name', String( 50 ), nullable=False )
    def __repr__(self):
        return 'PackingStationHistory(id=' + str(self.id) + ', packing_datetime' + str(self.packing_datetime) + \
            ', user_option' + self.user_option + ', shift' + self.shift + ', packing_station' + self.packing_station + \
            ', work_station' + self.work_station + \
            ', box_code' + self.box_code + ', box_num' + self.box_num + ', pn' + self.pn + ', dpn' + self.dpn + \
            ', harness_sn' + self.harness_sn + ', box_ref_manifest' + self.box_ref_manifest + ', manifest' + self.manifest + \
            ', production_sn' + self.production_sn + ', line_name' + self.line_name + ')'

class PackingStationInfo( Base ):

    __tablename__ = 'Packing_info'
    id = Column('id', Integer, primary_key=True)
    datetime_creating = Column('datetime_creating', DateTime(timezone=False), default=func.now())
    username = Column('username', String(200), nullable=False)
    password = Column('password', String(200), nullable=False)
    salt_key = Column('salt_key', String(200), nullable=False)
    name_file = Column('name_file', String(100), nullable=False)
    name_folder = Column('name_folder', String(100), nullable=False)
    ip_address = Column('ip_address', String(100), nullable=False)
    name_packing_station = Column('name_packing_station', String(100), nullable=False)
    url_file = Column('url_file', String(200), nullable=True)
    def __repr__(self):
        return 'PacckingStationInfo( id=(), datetime_creating=(), ' \
               'username=(), password=(), salt_key=(), name_file=(), '\
               'name_folder=(), ip_address=(), name_packing_station=(), url_file=() )'\
                .format(str(self.id), str(self.datetime_creating),
                self.username, self.password, str(self.salt_key),
                self.name_file, self.name_folder, self.ip_address,
                self.name_packing_station, self.url_file)


