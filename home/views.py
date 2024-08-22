


from django.shortcuts import render, HttpResponse, redirect
from .forms import UserDetailForm
from .models import UserDetail, Quote
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .pdf_utils import render_to_pdf  # Import the PDF utility function




def userdetail(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']

        # Create and save the user detail
        user_detail = UserDetail(name=name, email=email, number=number)
        user_detail.save()


        # Store the user detail ID in the session
        request.session['user_detail_id'] = user_detail.id

        return redirect('index')  # Redirect to the index page after form submission

    return render(request, 'userdetail.html')

def index(request):
    return render(request, 'index1.html')

def result(request):
    if request.method == 'GET':
        global required_wattage
        required_wattage = float(request.GET.get('required_watt'))

        global panel_wattage
        if '350_watt' in request.GET:
            panel_wattage = 350
        elif '450_watt' in request.GET:
            panel_wattage = 450
        elif '500_watt' in request.GET:
            panel_wattage = 500
        elif '550_watt' in request.GET:
            panel_wattage = 550
        else:
            panel_wattage = 0 

        global panels_required
        panels_required = required_wattage / panel_wattage
        panels_required = int(panels_required + 1.5)

        global battries_required
        battries_required = required_wattage / (290 * 12) 
        battries_required = int(battries_required + 1.5)

        global required_inverter
        required_inverter = int((required_wattage / 1000) + 2 ) 

        user_detail_id = request.session.get('user_detail_id')
        user_detail = UserDetail.objects.get(id=user_detail_id)

        if 'generate_pdf' in request.GET:
            context = {
                'panels_required': panels_required,
                'house_consumption': required_wattage,
                'battries_required': battries_required,
                'required_inverter': required_inverter,
                'user_details': user_detail
            }
            pdf = render_to_pdf('result_pdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

    return render(request, 'result.html', {'panels_required': panels_required, 'house_consumption': required_wattage, 'battries_required': battries_required, 'required_inverter': required_inverter})

def day_scrape_website(url):
    global extracted_data
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        target_td_elements = soup.find_all('td', class_='c tr sep-l')
        extracted_data = [td_element.text.strip() for td_element in target_td_elements]
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        extracted_data = []

    return extracted_data

def process_data(extracted_data):
    total_hours = 0
    for time_str in extracted_data:
        try:
            hours, minutes, seconds = map(int, time_str.split(':'))
            total_seconds = hours * 3600 + minutes * 60 + seconds
            total_hours += total_seconds / 3600
            total_hours = int(total_hours)
        except ValueError:
            print(f"Invalid time format: {time_str}")

    return total_hours

def production(request):
    length = 0 
    current_date = datetime.now()
    current_month = current_date.month

    if '2024' in request.GET:
        current_year = 2024
    elif '2025' in request.GET:
        current_year = 2025
    else:
        current_year = 2023

    all_data = []
    start_month = current_month if current_year == current_date.year else 1

    for month in range(start_month, 13):
        url = f"https://www.timeanddate.com/sun/pakistan/karachi?month={month}&year={current_year}"
        data = day_scrape_website(url)
        all_data.extend(data)
        length += len(data)


    length = (length * 24)
    sum_of_hours = process_data(all_data)
    total_night_hour = length - sum_of_hours
    sun_hours = sum_of_hours
    night_hour = total_night_hour
    panel_production = panel_wattage * sun_hours * panels_required
    panel_production -= panel_production * 0.20

    global solar_kw_production
    solar_kw_production = panel_production / 1000

    global battery_kw_production
    battery_url = f'https://solarpanelprices.pk/product/exide-tr-2000-210-ah-tubular-battery-price-in-pakistan/#google_vignette'
    battery_kw_production = ((290 * 12) * night_hour) / 1000

    # PRICING CODE

    panel_pricing = panel_wattage * panels_required * 40
    battery_pricing = battries_required * 54000
    inverter_pricing = required_inverter * 45000
    total_cost = panel_pricing + battery_pricing + inverter_pricing

    # Requirement

    panels_required_pdf = panels_required
    required_wattage_pdf = required_wattage
    battries_required_pdf = battries_required
    required_inverter_pdf = required_inverter

    global user_detail
    user_detail_id = request.session.get('user_detail_id')
    user_detail = UserDetail.objects.get(id=user_detail_id)

    quote = Quote(
            user=user_detail,
            solar_kw_production=solar_kw_production,
            battery_kw_production=battery_kw_production,
            panel_pricing=panel_pricing,
            battery_pricing=battery_pricing,
            inverter_pricing=inverter_pricing,
            panels_required_pdf=panels_required,
            house_consumption_pdf=required_wattage,
            battries_required_pdf=battries_required,
            required_inverter_pdf=required_inverter,
            total_cost=total_cost
        )
    quote.save()

    if 'generate_pdf' in request.GET:
        context = {
            'solar_kw_production': solar_kw_production,
            'battery_kw_production': battery_kw_production,
            'panel_pricing': panel_pricing,
            'battery_pricing': battery_pricing,
            'inverter_pricing': inverter_pricing,
            'panels_required_pdf': panels_required_pdf,
            'house_consumption_pdf': required_wattage_pdf,
            'battries_required_pdf': battries_required_pdf,
            'required_inverter_pdf': required_inverter_pdf,
            'total_cost': total_cost,
            'user_details': user_detail
        }
        pdf = render_to_pdf('pricing_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


    return render(request, 'production.html', {'solar_kw_production': solar_kw_production, 'battery_kw_production': battery_kw_production, 'panel_pricing': panel_pricing, 'battery_pricing': battery_pricing, 'inverter_pricing': inverter_pricing})

def report(request):
    panel_pricing = panel_wattage * panels_required * 40
    battery_pricing = battries_required * 60000
    inverter_pricing = required_inverter * 45000
    total_cost = panel_pricing + battery_pricing + inverter_pricing

    # Requirement

    panels_required_pdf = panels_required
    required_wattage_pdf = required_wattage
    battries_required_pdf = battries_required
    required_inverter_pdf = required_inverter

    return render(request,'report.html',{ 'solar_kw_production': solar_kw_production,'battery_kw_production': battery_kw_production,'panel_pricing': panel_pricing,'battery_pricing': battery_pricing,'inverter_pricing': inverter_pricing,'panels_required_pdf': panels_required_pdf,'house_consumption_pdf': required_wattage_pdf,'battries_required_pdf': battries_required_pdf,'required_inverter_pdf': required_inverter_pdf,'total_cost': total_cost,'user_details': user_detail})