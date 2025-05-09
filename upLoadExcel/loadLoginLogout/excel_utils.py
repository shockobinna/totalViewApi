import pandas as pd
from django.utils import timezone
from .models import TotalViewApiDB
from datetime import datetime

import logging
logger = logging.getLogger(__name__)


def load_data_from_excel(excel_file):
    REQUIRED_COLUMNS = ['IDUSUARIO', 'DATA_REFERENCIA', 'LOGIN', 'LOGOUT', 'ATUALIZACAO']
    logger.info("excel_utils.load_data_from_excel called.")

    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        logger.info("Excel file read successfully.")
    except Exception as e:
        logger.error(f"Failed to read Excel file: {e}")
        return {'status': 'error', 'message': f'Erro ao ler o arquivo Excel: {str(e)}'}

    df.columns = df.columns.str.strip().str.upper()
    logger.debug(f"Columns found: {list(df.columns)}")

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        logger.warning(f"Missing required columns: {missing_columns}")
        return {
            'status': 'error',
            'message': f'O arquivo Excel está faltando as colunas obrigatórias: {", ".join(missing_columns)}'
        }

    df = df.dropna(subset=['IDUSUARIO'])
    logger.info(f"Rows after dropping null IDUSUARIO: {len(df)}")

    df['PLATAFORMA'] = 'genesis_vivo'
    df['DATA_REFERENCIA'] = pd.to_datetime(df['DATA_REFERENCIA'], errors='coerce').dt.date

    invalid_rows = []
    valid_rows = []

    for idx, row in df.iterrows():
        invalid_dates = []
        cleaned_row = row.copy()

        for date_column in ['LOGIN', 'LOGOUT', 'ATUALIZACAO']:
            date_value = row[date_column]

            if pd.isnull(date_value):
                invalid_dates.append(date_column)
                continue

            try:
                if not isinstance(date_value, datetime):
                    date_value = pd.to_datetime(date_value, format="%Y-%m-%d %H:%M:%S.%f", errors='raise')
                aware_date = timezone.make_aware(date_value, timezone.get_current_timezone())
                cleaned_row[date_column] = aware_date
            except Exception as e:
                invalid_dates.append(date_column)

        if invalid_dates:
            logger.warning(f"Invalid date(s) at row {idx + 2}: {invalid_dates}")
            invalid_rows.append({
                'row_index': idx + 2,
                'invalid_dates': invalid_dates,
                'data': row.to_dict()
            })
        else:
            valid_rows.append(cleaned_row)

    if invalid_rows:
        logger.info(f"Found {len(invalid_rows)} invalid rows. Aborting insert.")
        return {'status': 'error', 'invalid_rows': invalid_rows}

    objs = [
        TotalViewApiDB(
            IDUSUARIO=int(row['IDUSUARIO']),
            DATA_REFERENCIA=row['DATA_REFERENCIA'],
            LOGIN=row['LOGIN'],
            LOGOUT=row['LOGOUT'],
            PLATAFORMA=row['PLATAFORMA'],
            ATUALIZACAO=row['ATUALIZACAO']
        )
        for row in valid_rows
    ]

    TotalViewApiDB.objects.bulk_create(objs, batch_size=2000)
    logger.info(f"Inserted {len(objs)} rows into the database successfully.")

    return {'status': 'success', 'inserted_rows': len(objs)}
