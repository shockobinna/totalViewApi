from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import TotalViewApiDB
from .excel_utils import load_data_from_excel
from django.views.decorators.csrf import csrf_exempt




# Create your views here.

def queryDataBase(request):
    if request.method == 'POST':
        
    # template = loader.get_template('homepage.html')
    
        # Retrieve the date fields from the request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        print(f"start date: {start_date}, end date: {end_date}")
    return render(request, 'homepage.html')
    # return HttpResponse("Hello world!")


# def upload_excel(request):
#     if request.method == 'POST' and request.FILES.get('excel_file'):
#         excel_file = request.FILES['excel_file']
#         if excel_file:
#             print(excel_file)


#         num_records = load_data_from_excel(excel_file)
#         print(f'record_count: {num_records}')
#         # return render(request, 'result.html', {'record_count': num_records})
#     return render(request, 'upLoadExcel.html')
# from django.shortcuts import render
# from .forms import ExcelUploadForm
# from .excel_utils import load_data_from_excel

# def upload_excel(request):
#     if request.method == 'POST' and request.FILES['excel_file']:
#         excel_file = request.FILES['excel_file']
        
#         # Call the function to load the data and check for invalid dates
#         invalid_rows = load_data_from_excel(excel_file)
        
#         if isinstance(invalid_rows, list):  # There were invalid rows
#             print(invalid_rows)
#             return render(request, 'upLoadExcel.html', {
#                 'invalid_rows': invalid_rows,
#                 'error_message': "There are invalid dates in the file. Please correct them and try again."
#             })
#         else:
#             # Success case, show how many rows were inserted
#             return render(request, 'upLoadExcel.html', {
#                 'success_message': f"{invalid_rows['inserted_rows']} rows successfully inserted."
#             })

#     return render(request, 'upLoadExcel.html')

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


