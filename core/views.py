from django.shortcuts import render
import requests
import json
import os

# Create View
def currency_data():
    """ All countries' currency data """
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'currencies.json')
    with open(file_path, "r") as f:
        currency_data = json.loads(f.read())
    return currency_data

def currency(request):
    if request.method == "POST":

        # Get data from the html form
        amount = float(request.POST.get('amount'))
        currency_from = request.POST.get("currency_from")
        currency_to = request.POST.get("currency_to")

        # Get currency exchange rates
        url = f"https://open.er-api.com/v6/latest/{currency_from}"
        d = requests.get(url).json()

        # Converter
        if d["result"] == "success":
            
            # Get currency exchange of the target
            ex_target =  d["rates"][currency_to]

            # Mltiply by the amount
            result = ex_target * amount

            # Set 2 decimal places
            result = "{:.2f}".format(result)

            context = {
            "result":result, 
            "currency_to":currency_to, 
            "currency_data":currency_data()
            }

            return render(request, "index.html", context)
    return render(request, "index.html", {"currency_data":currency_data()})