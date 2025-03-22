from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import TotalViewApiDB
from .excel_utils import load_data_from_excel
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt




# Create your views here.


def queryDataBase(request):
    if request.method == 'POST':
        # Retrieve the start and end date from the request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

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
                print(data)
                
                # Message for both start and end dates
                message = f"Data found for the dates between {start_date.strftime('%d/%m/%Y')} and {end_date.strftime('%d/%m/%Y')}. Are you sure you want to delete the data?"
                noData = False
            else:
                # If only start_date is provided, query for records that match start_date
                data = TotalViewApiDB.objects.filter(DATA_REFERENCIA=start_date)
                print(f"Querying for records with start_date: {start_date}")
                print(data)
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
        return render(request, 'homepage.html', {'data': data, 'message': message, 'noData': noData})
    
    # Default rendering if the request is not a POST
    return render(request, 'homepage.html')



def confirm_delete(request):
    if request.method == 'POST':
        print('Action from modal to delete data')
    return render(request,'homepage.html')

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


