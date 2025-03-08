import pandas as pd
from .models import TotalViewApiDB

def load_data_from_excel(excel_file):
    # Read the excel file using pandas
    df = pd.read_excel(excel_file)
    for index, row in df.iterrows():
        TotalViewApiDB.objects.create(
            IDUSUARIO=row['IDUSUARIO'],
            DATA_REFERENCIA=row['DATA_REFERENCIA'],
            LOGIN=row['LOGIN'],
            LOGOUT=row['LOGOUT'],
            PLATAFORMA=row['PLATAFORMA'],
            ATUALIZACAO=row['ATUALIZACAO']
        )
    
    record_count = TotalViewApiDB.objects.count()
    return record_count
