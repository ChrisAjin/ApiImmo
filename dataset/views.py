from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DataSet
from .serializers import DataSetSerializers
import os
from django.conf import settings
from django.shortcuts import render
import numpy as np 
#Load Data import
import pandas
from django.db.models import Avg, Min, Max, FloatField

class LoadDatasetView(APIView):
    def post(self, request):
        print("POST request received for /dataset/load-dataset/")
        dataset_path = os.path.join(settings.BASE_DIR, 'dataset_annonces.csv')

        try:
            df = pandas.read_csv(dataset_path)

            for _, row in df.iterrows():
                dept_code = row.get('DEPT_CODE')
                if pandas.isna(dept_code):
                    dept_code = None
                else:
                    dept_code = str(int(float(dept_code)))  
                price = row.get('PRICE')
                if pandas.isna(price):
                    price = None

                DataSet.objects.get_or_create(
                    url=row['AD_URLS'],
                    defaults={
                        'price': price,
                        'department': dept_code,
                        'city': row.get('CITY'),
                        'postal_code': row.get('ZIP_CODE'),
                    }
                )
            return Response({"message": "Dataset loaded successfully."}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

class StatsView(APIView):
    def get(self, request):
        department = request.query_params.get('department')
        city = request.query_params.get('city')
        postal_code = request.query_params.get('postal_code')

        queryset = DataSet.objects.all()
        if department:
            queryset = queryset.filter(department=department)
        if city:
            queryset = queryset.filter(city=city)
        if postal_code:
            queryset = queryset.filter(postal_code=postal_code)

        if not queryset.exists():
            return Response({"error": "No data available for the ici given filters."}, status=404)

        stats = queryset.aggregate(
            average_charges=Avg('price', output_field=FloatField()),
            min_charges=Min('price', output_field=FloatField()),
            max_charges=Max('price', output_field=FloatField())
        )

        return Response(stats)

def stats_form(request):
    stats = None
    error = None

    if request.method == "POST":
        department = request.POST.get("department")
        city = request.POST.get("city")
        postal_code = request.POST.get("postal_code")

        queryset = DataSet.objects.all()
        if department:
            queryset = queryset.filter(department=department)
        if city:
            queryset = queryset.filter(city=city)
        if postal_code:
            queryset = queryset.filter(postal_code=postal_code)

        if not queryset.exists():
            error = "No data available for the given filters."
        else:
            prices = list(queryset.values_list('price', flat=True))
            if prices:
                stats = {
                    "average_charges": queryset.aggregate(Avg("price", output_field=FloatField()))["price__avg"],
                    "quantile_10": np.percentile(prices, 10),  
                    "quantile_90": np.percentile(prices, 90),  
                }

    return render(request, "stats_form.html", {"stats": stats, "error": error})

def add_bienici_announcement(request):
    if request.method == "POST":
        url = request.POST.get("url")
        if not url:
            return render(request, "add_announcement.html", {"error": "URL is required"})

        try:
            ad_id = url.split('/')[-1]
            api_url = f"https://www.bienici.com/realEstateAd.json?id={ad_id}"

            response = requests.get(api_url)
            if response.status_code != 200:
                return render(request, "add_announcement.html", {"error": "Failed to fetch data from BienIci API"})

            ad_data = response.json()
            data_set_ad, created = DataSet.objects.get_or_create(
                url=url,
                defaults={
                    'price': ad_data.get('price'),
                    'charges': ad_data.get('charges'),
                    'department': ad_data.get('department'),
                    'city': ad_data.get('city'),
                    'postal_code': ad_data.get('postal_code'),
                }
            )

            if created:
                message = "Announcement added successfully!"
            else:
                message = "This announcement already exists in the database."

            return render(request, "add_announcement.html", {"message": message})

        except Exception as e:
            return render(request, "add_announcement.html", {"error": str(e)})

    return render(request, "add_announcement.html")