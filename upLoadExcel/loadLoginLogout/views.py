from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .excel_utils import load_data_from_excel
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def loadData(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())
    # return HttpResponse("Hello world!")


def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        # Retrieve the date fields from the request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        num_records = load_data_from_excel(excel_file)
        return render(request, 'result.html', {'record_count': num_records})
    return render(request, 'homepage.html')


