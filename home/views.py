from django.shortcuts import render, HttpResponse
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


  
# Create your views here.
def index(request):
    return render(request, 'index1.html')


    



# Result function that uses the extracted and calculated data
def result(request):
    # Get parameters from the request
    required_wattage = float(request.GET.get('required_watt'))
    #WATTAGE SAVE IN DICTIONARY
    house_consumption = {'house_consumption': required_wattage}

    global panel_wattage
    # panel_wattage REQUIRED SECTION
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

    # Calculate the number of solar panels required
        global panels_required
    panels_required = required_wattage / panel_wattage
    panels_required = int(panels_required + 1.5)

    global battries_required
    battries_required = required_wattage  / (290 * 12) 
    battries_required = int(battries_required + 0.8)
    # Pass the results to the template
    return render(request, 'result.html', {'panels_required': panels_required, 'house_consumption': required_wattage,'battries_required': battries_required})






def day_scrape_website(url):
    global extracted_data  # Use the global variable
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and extract the text content inside <td> tags with class="c tr sep-l"
        target_td_elements = soup.find_all('td', class_='c tr sep-l')

        # Store extracted text in a list
        extracted_data = [td_element.text.strip() for td_element in target_td_elements]

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        extracted_data = []

    return extracted_data  # Return the extracted data





# Another function that uses the extracted data and calculates the sum of hours
def process_data(extracted_data):
    # global extracted_data  # Use the global variable
    # Process the extracted data
    print("Extracted Data:")
    for data in extracted_data:
        print(data)

    # Calculate the sum of hours
    total_hours = 0

    for time_str in extracted_data:
        try:
            hours, minutes, seconds = map(int, time_str.split(':'))
            total_seconds = hours * 3600 + minutes * 60 + seconds
            total_hours += total_seconds / 3600  # Convert total seconds to hours and add to sum
            total_hours = int(total_hours )
            # panels_required = int(panels_required + 1.5)
        except ValueError:
            print(f"Invalid time format: {time_str}")

    print("Total sum of hours:", total_hours)

    return total_hours  # Return the calculated sum of hours








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

    
    # List to store all extracted data
    all_data = []

    start_month = current_month if current_year == current_date.year else 1

    # Loop through the months from the current month till the end
    for month in range(start_month, 13):  # assuming 1 to 12 for months
    # Construct the URL with the current month and year
        url = f"https://www.timeanddate.com/sun/pakistan/karachi?month={month}&year={current_year}"

    # Call the scrape_website function with the constructed URL
        data = day_scrape_website(url)

    # Append the extracted data to the list
        all_data.extend(data)

    # LENGTH IS TOTAL DAYS = TOTAL HOURS 24    
        length += len(data)
    print(length)
    length = (length * 24)


   

# Call the process_data function to calculate and print the sum of hours for all data
    sum_of_hours = process_data(all_data)

    total_night_hour = length - sum_of_hours
    
    # Use the calculated sum_of_hours in sun_hours
    sun_hours = sum_of_hours  # You can adjust this value as needed

    night_hour = total_night_hour
    
# Calculate daily energy production in kilowatt-hours
    # panel required missing
    panel_production =  panel_wattage * sun_hours * panels_required
    #efficiency of solar Panel
    panel_production -= panel_production * 0.20
    solar_kw_production = panel_production / 1000
    battery_kw_production = ((290*12)* night_hour)/1000
   

    return render(request, 'production.html', {'solar_kw_production': solar_kw_production , 'battery_kw_production':battery_kw_production})




def pricing(request):

    panel_pricing = panel_wattage * panels_required * 40


    # return panel_pricing  # Return the extracted data
    return render(request, 'pricing.html', {'panel_pricing': panel_pricing})