from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import TotalViewApiDB
from .excel_utils import load_data_from_excel
from datetime import datetime, timedelta
import logging
from django.views.decorators.csrf import csrf_exempt


# Setup logging
logger = logging.getLogger(__name__)

# Create your views here.


import logging
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import TotalViewApiDB

logger = logging.getLogger(__name__)

def queryDataBase(request):
    if request.method == 'POST':
        logger.info("Received POST request to query database.")

        # Retrieve the start and end date from the request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        inicio = start_date
        fim = end_date

        logger.debug(f"Start date: {start_date}, End date: {end_date}")

        # Ensure start_date is always provided
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                logger.debug(f"Parsed start_date: {start_date}")
            except ValueError:
                logger.error("Invalid start date format.")
                return render(request, 'homepage.html', {
                    'message': "Invalid start date format.",
                    'noData': True
                })

            if end_date:
                try:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                    logger.debug(f"Parsed and adjusted end_date: {end_date}")
                except ValueError:
                    logger.error("Invalid end date format.")
                    return render(request, 'homepage.html', {
                        'message': "Invalid end date format.",
                        'noData': True
                    })

                data = TotalViewApiDB.objects.filter(DATA_REFERENCIA__gte=start_date, DATA_REFERENCIA__lt=end_date)
                logger.info(f"Queried data from {start_date} to {end_date} (exclusive). Found: {len(data)} records.")
                message = f"Data found for the dates between {start_date.strftime('%d/%m/%Y')} and {(end_date - timedelta(days=1)).strftime('%d/%m/%Y')}. Are you sure you want to delete the data?"
            else:
                data = TotalViewApiDB.objects.filter(DATA_REFERENCIA=start_date)
                logger.info(f"Queried data for exact date {start_date}. Found: {len(data)} records.")
                message = f"Data found for the date: {start_date.strftime('%d/%m/%Y')}. Are you sure you want to delete the data?"

            noData = not data
            if noData:
                logger.info("No data found for the given date(s).")
                message = "No data was found for the date(s) provided."
        else:
            logger.warning("Start date not provided in POST request.")
            data = []
            message = "Start date is required. Please provide a valid start date."
            noData = True

        return render(request, 'homepage.html', {
            'data': data,
            'message': message,
            'noData': noData,
            'start_date': inicio,
            'end_date': fim
        })

    logger.debug("Rendering homepage without POST request.")
    return render(request, 'homepage.html')


def confirm_delete(request):
    try:
        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            print(start_date, end_date)

            logger.info("Received start_date: %s, end_date: %s", start_date, end_date)

            if start_date:
                logger.debug("Start date is provided. Converting start_date to datetime.")
                start_date = datetime.strptime(start_date, '%Y-%m-%d')

                if end_date:
                    logger.debug("End date is provided. Converting end_date to datetime.")
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    end_date_plus_one_day = end_date + timedelta(days=1)

                    logger.info("Deleting records between %s and %s", start_date, end_date_plus_one_day)
                    deleted_count, _ = TotalViewApiDB.objects.filter(
                        DATA_REFERENCIA__gte=start_date,
                        DATA_REFERENCIA__lt=end_date_plus_one_day
                    ).delete()

                    logger.debug("Deleted %d records.", deleted_count)
                    print(f"Deleted {deleted_count} records.")
                    dataRemoved = f"Deleted {deleted_count} records."
                    return render(request, 'homepage.html', {'dataRemoved': dataRemoved})
                else:
                    logger.debug("No end_date provided. Deleting records matching start_date only.")
                    deleted_count, _ = TotalViewApiDB.objects.filter(DATA_REFERENCIA=start_date).delete()

                    logger.debug("Deleted %d records based on start_date.", deleted_count)
                    print(f"Deleted {deleted_count} records based on start_date.")
                    dataRemoved = f"Deleted {deleted_count} records."
                    return render(request, 'homepage.html', {'dataRemoved': dataRemoved})
            else:
                logger.warning("Start date is missing. No records deleted.")
                print("Start date is missing.")

    except Exception as e:
        logger.error("Error occurred during delete operation: %s", str(e))
        return HttpResponse(f"An error occurred while processing your request. Please try again later. {str(e)}", status=500)

    logger.info("Delete operation completed successfully.")
    return render(request, 'homepage.html')



def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        logger.info("Received file: %s", excel_file)

        result = load_data_from_excel(excel_file)

        if result['status'] == 'error':
            # Check if it's a structural error (e.g., missing headers)
            if 'message' in result:
                return render(request, 'upLoadExcel.html', {
                    'error_message': result['message']
                })
            # Or it's a data validation error (invalid dates)
            elif 'invalid_rows' in result:
                return render(request, 'upLoadExcel.html', {
                    'invalid_rows': result['invalid_rows'],
                    'error_message': "There are invalid dates in the file. Please correct them and try again."
                })

        # If all is good
        return render(request, 'upLoadExcel.html', {
            'success_message': f"{result['inserted_rows']} rows successfully inserted."
        })

    return render(request, 'upLoadExcel.html')




def delete_data(request):
    
    TotalViewApiDB.objects.all().delete()

    return HttpResponse("All records have been deleted successfully.")


