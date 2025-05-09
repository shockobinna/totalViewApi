import pandas as pd
from django.utils import timezone
from .models import TotalViewApiDB
from datetime import datetime

def load_data_from_excel(excel_file):
    REQUIRED_COLUMNS = ['IDUSUARIO', 'DATA_REFERENCIA', 'LOGIN', 'LOGOUT', 'ATUALIZACAO']

    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
    except Exception as e:
        return {'status': 'error', 'message': f'Erro ao ler o arquivo Excel: {str(e)}'}

    # Clean column names
    df.columns = df.columns.str.strip().str.upper()

    # Check if all required columns exist
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        return {
            'status': 'error',
            'message': f'O arquivo Excel está faltando as colunas obrigatórias: {", ".join(missing_columns)}'
        }

    # Drop rows where IDUSUARIO is null
    df = df.dropna(subset=['IDUSUARIO'])

    # Ensure PLATAFORMA is always "genesis_vivo"
    df['PLATAFORMA'] = 'genesis_vivo'

    # Convert DATA_REFERENCIA to date
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
            except Exception:
                invalid_dates.append(date_column)
                cleaned_row[date_column] = row[date_column]

        if invalid_dates:
            invalid_rows.append({
                'row_index': idx + 2,
                'invalid_dates': invalid_dates,
                'data': row.to_dict()
            })
        else:
            valid_rows.append(cleaned_row)

    if invalid_rows:
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

    return {'status': 'success', 'inserted_rows': len(objs)}

# import pandas as pd
# from django.utils import timezone
# from .models import TotalViewApiDB
# from datetime import datetime

# def load_data_from_excel(excel_file):
#     # Read Excel file
#     df = pd.read_excel(excel_file, engine='openpyxl')

#     # Clean column names (remove spaces, convert to uppercase for safety)
#     df.columns = df.columns.str.strip().str.upper()

#     # Drop rows where IDUSUARIO is null (since it's required)
#     df = df.dropna(subset=['IDUSUARIO'])

#     # Ensure PLATAFORMA is always "genesis_vivo"
#     df['PLATAFORMA'] = 'genesis_vivo'

#     # Convert DATA_REFERENCIA to date (without time zone), keep invalid as None
#     df['DATA_REFERENCIA'] = pd.to_datetime(df['DATA_REFERENCIA'], errors='coerce').dt.date

#     # List to collect invalid rows for user correction
#     invalid_rows = []

#     # Prepare cleaned rows for database insert
#     valid_rows = []

#     # Loop over rows and validate date columns manually
#     for idx, row in df.iterrows():
#         invalid_dates = []
#         cleaned_row = row.copy()

#         # Check and parse date columns
#         for date_column in ['LOGIN', 'LOGOUT', 'ATUALIZACAO']:
#             date_value = row[date_column]

#             if pd.isnull(date_value):  # Empty cells are invalid
#                 invalid_dates.append(date_column)
#                 continue

#             try:
#                 # Attempt to parse the date
#                 if not isinstance(date_value, datetime):
#                     # If it's a string, attempt parsing
#                     # date_value = pd.to_datetime(date_value, dayfirst=True)  # dayfirst=True if your format is dd/mm/yyyy
#                     date_value = pd.to_datetime(date_value, format="%Y-%m-%d %H:%M:%S.%f", errors='raise')


#                 # If parsed successfully, make timezone aware
#                 aware_date = timezone.make_aware(date_value, timezone.get_current_timezone())
#                 cleaned_row[date_column] = aware_date
#             except Exception:
#                 # If parsing failed, mark as invalid and keep original string
#                 invalid_dates.append(date_column)
#                 cleaned_row[date_column] = row[date_column]  # Keep original value

#         if invalid_dates:
#             # If any invalid dates found, add row to invalid_rows for reporting
#             invalid_rows.append({
#                 'row_index': idx + 2,  # +2 to match Excel row numbers (header + 1-indexed)
#                 'invalid_dates': invalid_dates,
#                 'data': row.to_dict()  # Keep original data to show user
#             })
#         else:
#             # All dates valid, prepare cleaned row for DB insertion
#             valid_rows.append(cleaned_row)

#     # 🚨 If there are invalid rows, return them to user without inserting anything
#     if invalid_rows:
#         return {'status': 'error', 'invalid_rows': invalid_rows}

#     # ✅ If all rows are valid, proceed to insert
#     objs = [
#         TotalViewApiDB(
#             IDUSUARIO=int(row['IDUSUARIO']),
#             DATA_REFERENCIA=row['DATA_REFERENCIA'],
#             LOGIN=row['LOGIN'],
#             LOGOUT=row['LOGOUT'],
#             PLATAFORMA=row['PLATAFORMA'],
#             ATUALIZACAO=row['ATUALIZACAO']
#         )
#         for row in valid_rows
#     ]

#     # Bulk insert
#     TotalViewApiDB.objects.bulk_create(objs, batch_size=2000)

#     return {'status': 'success', 'inserted_rows': len(objs)}

# import pandas as pd
# from datetime import datetime
# from django.utils import timezone
# from your_app.models import TotalViewApiDB

# def load_data_from_excel(excel_file):
#     try:
#         # Read Excel file
#         df = pd.read_excel(excel_file, engine='openpyxl')

#         # Clean column names (remove spaces, convert to uppercase for safety)
#         df.columns = df.columns.str.strip().str.upper()

#         # Check if required columns exist, raise KeyError if missing
#         required_columns = {'IDUSUARIO', 'PLATAFORMA', 'DATA_REFERENCIA', 'LOGIN', 'LOGOUT', 'ATUALIZACAO'}
#         missing_columns = required_columns - set(df.columns)
#         if missing_columns:
#             raise KeyError(f"Missing required columns: {', '.join(missing_columns)}")

#         # Drop rows where IDUSUARIO is null (since it's required)
#         df = df.dropna(subset=['IDUSUARIO'])

#         # Ensure PLATAFORMA is always "genesis_vivo"
#         df['PLATAFORMA'] = 'genesis_vivo'

#         # Convert DATA_REFERENCIA to date (without time zone), keep invalid as None
#         df['DATA_REFERENCIA'] = pd.to_datetime(df['DATA_REFERENCIA'], errors='coerce').dt.date

#         # List to collect invalid rows for user correction
#         invalid_rows = []
#         valid_rows = []

#         # Loop over rows and validate date columns manually
#         for idx, row in df.iterrows():
#             invalid_dates = []
#             cleaned_row = row.copy()

#             # Check and parse date columns
#             for date_column in ['LOGIN', 'LOGOUT', 'ATUALIZACAO']:
#                 date_value = row[date_column]

#                 if pd.isnull(date_value):  # Empty cells are invalid
#                     invalid_dates.append(date_column)
#                     continue

#                 try:
#                     # Attempt to parse the date
#                     if not isinstance(date_value, datetime):
#                         # If it's a string, attempt parsing
#                         date_value = pd.to_datetime(date_value, format="%Y-%m-%d %H:%M:%S.%f", errors='raise')

#                     # If parsed successfully, make timezone aware
#                     aware_date = timezone.make_aware(date_value, timezone.get_current_timezone())
#                     cleaned_row[date_column] = aware_date
#                 except Exception:
#                     # If parsing failed, mark as invalid and keep original string
#                     invalid_dates.append(date_column)
#                     cleaned_row[date_column] = row[date_column]  # Keep original value

#             if invalid_dates:
#                 # If any invalid dates found, add row to invalid_rows for reporting
#                 invalid_rows.append({
#                     'row_index': idx + 2,  # +2 to match Excel row numbers (header + 1-indexed)
#                     'invalid_dates': invalid_dates,
#                     'data': row.to_dict()  # Keep original data to show user
#                 })
#             else:
#                 # All dates valid, prepare cleaned row for DB insertion
#                 valid_rows.append(cleaned_row)

#         # 🚨 If there are invalid rows, return them to user without inserting anything
#         if invalid_rows:
#             return {'status': 'error', 'invalid_rows': invalid_rows}

#         # ✅ If all rows are valid, proceed to insert
#         objs = [
#             TotalViewApiDB(
#                 IDUSUARIO=int(row['IDUSUARIO']),
#                 DATA_REFERENCIA=row['DATA_REFERENCIA'],
#                 LOGIN=row['LOGIN'],
#                 LOGOUT=row['LOGOUT'],
#                 PLATAFORMA=row['PLATAFORMA'],
#                 ATUALIZACAO=row['ATUALIZACAO']
#             )
#             for row in valid_rows
#         ]

#         # Bulk insert
#         TotalViewApiDB.objects.bulk_create(objs, batch_size=2000)

#         return {'status': 'success', 'inserted_rows': len(objs)}

#     except KeyError as e:
#         # Catch missing columns
#         return {'status': 'error', 'message': f"File format error: {str(e)}"}
#     except Exception as e:
#         # Catch any other exceptions (e.g., parsing errors, file read issues)
#         return {'status': 'error', 'message': f"An error occurred: {str(e)}"}

