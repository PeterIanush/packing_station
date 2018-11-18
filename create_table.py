from sqlalchemy import create_engine
from colector_models import PackingStationHistory

engine = create_engine("mssql+pyodbc://sa:Prettl!@#4@kanban")
PackingStationHistory.metadata.create_all(engine)