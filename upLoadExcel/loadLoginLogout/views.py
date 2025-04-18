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


def queryDataBase(request):
    if request.method == 'POST':
        # Retrieve the start and end date from the request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        inicio = request.POST.get('start_date')
        fim= request.POST.get('end_date')
        print(start_date, end_date)

        # Ensure start_date is always provided
        if start_date:
            # Convert start_date to datetime object
            start_date = datetime.strptime(start_date, '%Y-%m-%d')  # Adjust the format if needed

            if end_date:
                # If end_date is provided, convert it to datetime and adjust to exclusive range
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                end_date = end_date + timedelta(days=1)  # Add 1 day to make the end date exclusive
                
                # Query the database for date range >= start_date and < end_date
                data = TotalViewApiDB.objects.filter(DATA_REFERENCIA__gte=start_date, DATA_REFERENCIA__lt=end_date)
                print(f"Querying from {start_date} to {end_date}")
                # print(data)
                
                # Message for both start and end dates
                message = f"Data found for the dates between {start_date.strftime('%d/%m/%Y')} and {end_date.strftime('%d/%m/%Y')}. Are you sure you want to delete the data?"
                noData = False
            else:
                # If only start_date is provided, query for records that match start_date
                data = TotalViewApiDB.objects.filter(DATA_REFERENCIA=start_date)
                print(f"Querying for records with start_date: {start_date}")
                # print(data)
                # Message for only start date
                message = f"Data found for the date: {start_date.strftime('%d/%m/%Y')}. Are you sure you want to delete the data?"
                noData = False
        else:
            # If no start_date is provided (shouldn't happen as it's a must), handle the case
            data = []  # Or you could raise an error or return an empty result

            # No valid message for missing start date
            message = "Start date is required. Please provide a valid start date."
            noData = False

        # Check if no data was found
        if not data:
            message = "No data was found for the date(s) provided."
            noData = True

        # Render the results to the template with the message
        return render(request, 'homepage.html', {'data': data, 'message': message, 'noData': noData, 'start_date': inicio, 'end_date': fim})
    
    # Default rendering if the request is not a POST
    return render(request, 'homepage.html')


def confirm_delete(request):
    try:
        if request.method == 'POST':
            # Retrieve start_date and end_date from the POST request
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            print(start_date, end_date)

            # logging.info("Received start_date: %s, end_date: %s", start_date, end_date)

            # Step 2: Check if start_date is provided (it should always be provided)
            if start_date:
                # logging.debug("Start date is provided. Converting start_date to datetime.")
                start_date = datetime.strptime(start_date, '%Y-%m-%d')

                # Step 3: Check if end_date is provided
                if end_date:
                    # logging.debug("End date is provided. Converting end_date to datetime.")
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')

                    # Add one day to the end_date to include the whole next day
                    end_date_plus_one_day = end_date + timedelta(days=1)
                    # logging.info("Deleting records between start_date: %s and end_date: %s", start_date, end_date_plus_one_day)

                    deleted_count, _ = TotalViewApiDB.objects.filter(
                        DATA_REFERENCIA__gte=start_date,
                        DATA_REFERENCIA__lt=end_date_plus_one_day
                    ).delete()

                    # logging.debug("Deleted %d records.", deleted_count)
                    print(f"Deleted {deleted_count} records.")
                    dataRemoved = f"Deleted {deleted_count} records."
                    return render(request, 'homepage.html', {'dataRemoved': dataRemoved})
                else:
                    # logging.debug("No end_date provided. Deleting records matching start_date only.")
                    deleted_count, _ = TotalViewApiDB.objects.filter(DATA_REFERENCIA=start_date).delete()

                    # logging.debug("Deleted %d records based on start_date.", deleted_count)
                    print(f"Deleted {deleted_count} records based on start_date.")
                    dataRemoved = f"Deleted {deleted_count} records."
                    return render(request, 'homepage.html', {'dataRemoved': dataRemoved})
            else:
                # logging.warning("Start date is missing. No records deleted.")
                print("Start date is missing.")

    except Exception as e:
        # Log the exception if it occurs
        # logging.error("Error occurred during delete operation: %s", str(e))
        return HttpResponse(f"An error occurred while processing your request. Please try again later. {str(e)}", status=500)

    # Step 4: Finalize and return response
    # logging.info("Delete operation completed successfully.")
    return render(request, 'homepage.html')

def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        
        # Call the function to load the data and check for invalid dates
        result = load_data_from_excel(excel_file)
        
        if result['status'] == 'error':  # There were invalid rows
            print(result['invalid_rows'])
            return render(request, 'upLoadExcel.html', {
                'invalid_rows': result['invalid_rows'],
                'error_message': "There are invalid dates in the file. Please correct them and try again."
            })
        else:
            # Success case, show how many rows were inserted
            return render(request, 'upLoadExcel.html', {
                'success_message': f"{result['inserted_rows']} rows successfully inserted."
            })

    return render(request, 'upLoadExcel.html')



def delete_data(request):
    
    TotalViewApiDB.objects.all().delete()

    return HttpResponse("All records have been deleted successfully.")


