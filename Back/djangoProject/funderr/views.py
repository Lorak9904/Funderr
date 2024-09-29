from django.shortcuts import render
from django.http import JsonResponse
from register.models import Firma, NGO, Partner, Priorytet, Competition, Grant
from register.models import Firma, NGO, Partner, CzłonekZespolu
from .models import Event
from difflib import SequenceMatcher
from datetime import date
import html.parser
from time import sleep
from django.http import HttpResponse, JsonResponse
from datetime import date, time
from django.http import JsonResponse
from django.core import serializers
import random

from django.forms import formset_factory, modelformset_factory
from django.forms.models import model_to_dict
from openai import APIConnectionError
from traceback import format_exc
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import QueryDict
from django.http import HttpResponse, QueryDict
from django.urls import reverse 
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage as DjangoCoreEmailMessage, EmailMultiAlternatives, send_mass_mail, get_connection, send_mail
from django.utils.html import format_html
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import json
import requests
from django.contrib import messages
from django.forms.models import model_to_dict



from email.message import EmailMessage
from email.parser import BytesParser
from email.mime.image import MIMEImage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import message_from_string, policy


import re
import html2text
from base64 import b64decode, b64encode
import os



def ngo_to_json(ngo_instance):
    return {
        "nazwaOrganizacji": ngo_instance.nazwaOrganizacji,
        "adresEmail": ngo_instance.adresEmail,
        "numerTelefonuKom": ngo_instance.numerTelefonuKom,
        "numerTelefonuSta": ngo_instance.numerTelefonuSta,
        "branza": ngo_instance.branza,
        "cel": ngo_instance.cel,
        "rozmiarOrganizacji": ngo_instance.rozmiarOrganizacji,
        "rodzajFinansowania": ngo_instance.rodzajFinansowania,
        "osobaKontaktowa": ngo_instance.osobaKontaktowa,
        "RankingESG": ngo_instance.RankingESG,
        "adres": ngo_instance.adres,
        "miasto": ngo_instance.miasto,
        "wojewodztwo": ngo_instance.wojewodztwo,
        "kodPocztowy": ngo_instance.kodPocztowy,
        "kraj": ngo_instance.kraj,
        "strategia": ngo_instance.strategia,
        "doswiadczenie": ngo_instance.doswiadczenie,
        "cele_spoleczne": ngo_instance.cele_spoleczne,
        "cele_biznesowe": ngo_instance.cele_biznesowe,
        "zespol": [{"id": czlon.id, "imie": czlon.imie, "nazwisko": czlon.nazwisko} for czlon in ngo_instance.zespol.all()],
        "tags": ngo_instance.tags,
    }

def ngo_detail_view(request, ngo_id):
    ngo_instance = NGO.objects.get(id=ngo_id)
    data = ngo_to_json(ngo_instance)
    return JsonResponse(data)

def firma_to_json(firma_instance):
    return {
        "nazwaFirmy": firma_instance.nazwaFirmy,
        "adresEmail": firma_instance.adresEmail,
        "numerTelefonuKom": firma_instance.numerTelefonuKom,
        "numerTelefonuSta": firma_instance.numerTelefonuSta,
        "branza": firma_instance.branza,
        "cel": firma_instance.cel,
        "rozmiarFirmy": firma_instance.rozmiarFirmy,
        "rodzajFinansowania": firma_instance.rodzajFinansowania,
        "osobaKontaktowa": firma_instance.osobaKontaktowa,
        "RankingESG": firma_instance.RankingESG,
        "adres": firma_instance.adres,
        "miasto": firma_instance.miasto,
        "wojewodztwo": firma_instance.wojewodztwo,
        "kodPocztowy": firma_instance.kodPocztowy,
        "kraj": firma_instance.kraj,
        "strategia_spolecznego_oddzialywania": firma_instance.strategia_spolecznego_oddzialywania,
        "cele_spoleczne": firma_instance.cele_spoleczne,
        "cele_biznesowe": firma_instance.cele_biznesowe,
        "budzet_spoleczny": str(firma_instance.budzet_spoleczny),  # Decimal as string
        "tags": firma_instance.tags,
    }

def firma_detail_view(request, firma_id):
    firma_instance = Firma.objects.get(id=firma_id)
    data = firma_to_json(firma_instance)
    return JsonResponse(data)

def dopasowanie(obiekt1, obiekt2):
    """Obliczanie dopasowania pomiędzy dwoma obiektami (firma lub NGO) na podstawie kilku kryteriów"""
        
    # Wagi dla poszczególnych kryteriów
    waga_branza = 0.4
    waga_rozmiar = 0.3
    waga_miasto = 0.2
    waga_kraj = 0.1

    # Inicjalizacja wyniku dopasowania
    wynik = 0

    # Dopasowanie branży
    if hasattr(obiekt1, 'branza') and hasattr(obiekt2, 'branza'):
        podobienstwo_branza = SequenceMatcher(None, obiekt1.branza, obiekt2.branza).ratio()
        wynik += podobienstwo_branza * waga_branza

    # Dopasowanie rozmiaru (firmy/organizacji)
    rozmiar_obiekt1 = getattr(obiekt1, 'rozmiarFirmy', getattr(obiekt1, 'rozmiarOrganizacji', None))
    rozmiar_obiekt2 = getattr(obiekt2, 'rozmiarFirmy', getattr(obiekt2, 'rozmiarOrganizacji', None))

    if rozmiar_obiekt1 and rozmiar_obiekt2:
        if rozmiar_obiekt1 == rozmiar_obiekt2:
            wynik += 1 * waga_rozmiar
        else:
            wynik += 0.5 * waga_rozmiar  # Przykładowo, mniejsze dopasowanie

    # Dopasowanie miasta
    if hasattr(obiekt1, 'miasto') and hasattr(obiekt2, 'miasto'):
        if obiekt1.miasto == obiekt2.miasto:
            wynik += 1 * waga_miasto

    # Dopasowanie kraju
    if hasattr(obiekt1, 'kraj') and hasattr(obiekt2, 'kraj'):
        if obiekt1.kraj == obiekt2.kraj:
            wynik += 1 * waga_kraj

    # Zwracamy wynik dopasowania jako procent (od 0 do 100)
    return round(wynik * 100, 2)





def matching(request):
    # Tworzenie przykładowych obiektów firm
    firma1 = Firma.objects.create(
        nazwaFirmy="TechCorp",
        adresEmail="contact@techcorp.com",
        numerTelefonuKom="+48123456789",
        numerTelefonuSta="+48222333444",
        branza="IT",
        cel="Innowacja w IT",
        rozmiarFirmy="Średnia",
        rodzajFinansowania="Prywatne",
        osobaKontaktowa="Jan Kowalski",
        RankingESG="A+",
        adres="Marszałkowska 123",
        miasto="Warszawa",
        wojewodztwo="Mazowieckie",
        kodPocztowy="00-123",
        kraj="Polska",
        strategia_spolecznego_oddzialywania="Promowanie zrównoważonego rozwoju",
        cele_spoleczne="Redukcja CO2",
        cele_biznesowe="Wzrost udziału w rynku",
        budzet_spoleczny=1000000.00
    )
    firma2 = Firma.objects.create(
        nazwaFirmy="InnovateTech",
        adresEmail="contact@innovatetech.com",
        numerTelefonuKom="+48600999888",
        numerTelefonuSta="+48222999666",
        branza="Finanse",
        cel="Automatyzacja procesów finansowych",
        rozmiarFirmy="Duża",
        rodzajFinansowania="Inwestycje",
        osobaKontaktowa="Anna Nowak",
        RankingESG="B",
        adres="Nowogrodzka 50",
        miasto="Kraków",
        wojewodztwo="Małopolskie",
        kodPocztowy="30-001",
        kraj="Polska",
        strategia_spolecznego_oddzialywania="Zrównoważone inwestycje",
        cele_spoleczne="Zwiększenie świadomości ekologicznej",
        cele_biznesowe="Ekspansja międzynarodowa",
        budzet_spoleczny=2000000.00
    )
    
    # Tworzenie przykładowych obiektów NGO
    NGO1 = NGO.objects.create(
        nazwaOrganizacji="Fundacja Edukacja Dla Wszystkich",
        adresEmail="kontakt@edukacjadlawszystkich.org",
        numerTelefonuKom="+48123123123",
        numerTelefonuSta="+48123456789",
        branza="Edukacja",
        cel="Zapewnienie dostępu do edukacji dla dzieci z ubogich regionów.",
        rozmiarOrganizacji="Mała",
        rodzajFinansowania="Donacje indywidualne",
        osobaKontaktowa="Anna Kowalska",
        RankingESG="A",
        adres="ul. Miodowa 5",
        miasto="Warszawa",
        wojewodztwo="Mazowieckie",
        kodPocztowy="00-001",
        kraj="Polska",
        strategia="Rozwój programów edukacyjnych, organizacja warsztatów oraz szkoleń dla nauczycieli.",
        doswiadczenie="5 lat doświadczenia w organizacji wydarzeń edukacyjnych.",
        cele_spoleczne="Zwiększenie dostępu do edukacji w małych miejscowościach.",
        cele_biznesowe="Zwiększenie liczby darczyńców o 20% rocznie."
    )
    
    NGO2 = NGO.objects.create(
        nazwaOrganizacji="Tech Innovators Sp. z o.o.",
        adresEmail="kontakt@techinnovators.pl",
        numerTelefonuKom="+48777777777",
        numerTelefonuSta="+48765432109",
        branza="Technologie informacyjne",
        cel="Tworzenie innowacyjnych rozwiązań w obszarze sztucznej inteligencji.",
        rozmiarOrganizacji="Średnia",
        rodzajFinansowania="Inwestycje venture capital",
        osobaKontaktowa="Jan Nowak",
        RankingESG="B",
        adres="ul. Wrocławska 10",
        miasto="Kraków",
        wojewodztwo="Małopolskie",
        kodPocztowy="30-001",
        kraj="Polska",
        strategia="Wprowadzanie innowacyjnych technologii AI na rynek oraz rozwój nowych platform SaaS.",
        doswiadczenie="Zespół złożony z ekspertów z branży technologicznej z ponad 10-letnim doświadczeniem.",
        cele_spoleczne="Tworzenie rozwiązań wspierających walkę z wykluczeniem cyfrowym.",
        cele_biznesowe="Zwiększenie udziału rynkowego w Europie Środkowo-Wschodniej."
    )

    firmy = [firma1, firma2]
    NGOs = [NGO1, NGO2]

    # Przechowywanie wyników w formie listy słowników
    result = []

    # Iterowanie po wszystkich firmach i NGO (porównujemy każdy obiekt z każdym)
    for firma in firmy:
        for ngo in NGOs:
            # Zakładamy, że metoda dopasowanie istnieje i zwraca wynik dopasowania
            dopasowanie_firma_ngo = dopasowanie(firma, ngo)
            result.append({
                'firma': firma.nazwaFirmy,
                'ngo': ngo.nazwaOrganizacji,
                'dopasowanie': dopasowanie_firma_ngo
            })

        # Porównanie firma-firma, bez duplikatów
        for inna_firma in firmy:
            if firma != inna_firma and firma.nazwaFirmy < inna_firma.nazwaFirmy:  # Porównanie alfabetyczne, aby uniknąć duplikatów
                dopasowanie_firma_firma = dopasowanie(firma, inna_firma)
                result.append({
                    'firma1': firma.nazwaFirmy,
                    'firma2': inna_firma.nazwaFirmy,
                    'dopasowanie': dopasowanie_firma_firma
                })

    # Iterowanie po wszystkich NGO i porównywanie ich między sobą, bez duplikatów
    for ngo in NGOs:
        for inne_ngo in NGOs:
            if ngo != inne_ngo and ngo.nazwaOrganizacji < inne_ngo.nazwaOrganizacji:  # Porównanie alfabetyczne, aby uniknąć duplikatów
                dopasowanie_ngo_ngo = dopasowanie(ngo, inne_ngo)
                result.append({
                    'ngo1': ngo.nazwaOrganizacji,
                    'ngo2': inne_ngo.nazwaOrganizacji,
                    'dopasowanie': dopasowanie_ngo_ngo
                })

    # Sortowanie wyników według dopasowania malejąco
    result_sorted = sorted(result, key=lambda x: x['dopasowanie'], reverse=True)

    # Przygotowanie danych do zwrócenia w formacie JSON
    response_data = {
        'dopasowania': result_sorted
    }

    return JsonResponse(response_data)

def home(request):
    
    response_data = {}
    dopasowanie(Firma.objects.last(), NGO.objects.last())
    
    return JsonResponse(dopasowanie(Firma.objects.last(), NGO.objects.last()), safe=False)


@csrf_exempt  # Temporarily disable CSRF for testing, use token in production
def search_view(request):
    if request.method == 'POST':
        # Load JSON data from the request body
        data = json.loads(request.body)

        keywords = data.get('keywords', '')
        selected_types = data.get('selectedTypes', [])  # Expecting a list like ["NGO", "Grants", "Companies"]

        results = {
            'NGOs': [],
            'Grants': [],
            'Companies': []
        }

        # Split keywords into a list
        keyword_list = keywords.split() if keywords else []

        # Querying NGOs
        if 'NGO' in selected_types:
            ngos = NGO.objects.filter(name__icontains=keywords)
            results['NGOs'] = [{'name': ngo.name, 'mission': ngo.mission_statement} for ngo in ngos]

        # Querying Grants
        if 'Grants' in selected_types:
            grants = Konkurs.objects.filter(title__icontains=keywords)
            results['Grants'] = [{'title': grant.title, 'description': grant.description} for grant in grants]

        # Querying Companies
        if 'Companies' in selected_types:
            companies = Firma.objects.filter(name__icontains=keywords)
            results['Companies'] = [{'name': company.name, 'description': company.description} for company in companies]

        return JsonResponse(results)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def serialize_all_grants_to_json():
    # Fetch all Grant objects
    grants = Grant.objects.all()
    
    # Serialize each grant into a dictionary
    grants_data = []
    for grant in grants:
        grant_data = {
            'nazwa_grantu': grant.nazwa_grantu,
            'maksymalna_kwota': str(grant.maksymalna_kwota),  # Ensure Decimal fields are properly serialized
            'data_rozpoczecia': grant.data_rozpoczecia.isoformat() if grant.data_rozpoczecia else None,
            'data_zakonczenia': grant.data_zakonczenia.isoformat() if grant.data_zakonczenia else None,
            'opis': grant.opis,
            'priorytety': [
                {
                    'nazwa_priorytetu': priorytet.nazwa_priorytetu,
                    'opis': priorytet.opis
                }
                for priorytet in grant.priorytety.all()  # Priorytety is a ManyToMany field
            ],
            'competitions': [
                {
                    'nazwa_konkursu': competition.nazwa_konkursu,
                    'status': competition.status,
                    'data_rozpoczecia': competition.data_rozpoczecia.isoformat() if competition.data_rozpoczecia else None,
                    'data_zakonczenia': competition.data_zakonczenia.isoformat() if competition.data_zakonczenia else None,
                    'opis': competition.opis
                }
                for competition in grant.competitions.all()  # Competitions linked to the grant
            ]
        }
        # Append each serialized grant to the list
        grants_data.append(grant_data)
    
    return grants_data


def funkcja(request):

    # save_competition_data()    #    events_data = [
    #     {
    #         'name': 'Wielka Orkiestra Świątecznej Pomocy',
    #         'description': 'Annual charity event supporting healthcare in Poland.',
    #         'date': date(2024, 1, 14),
    #         'time': time(12, 0),
    #         'location': 'Warsaw, Poland',
    #         'organizer': 'WOŚP Foundation',
    #         'contact': 'contact@wosp.org.pl',
    #         'image': None,
    #         'partners': 'TVN, Allegro, Siepomaga'
    #     },
    #     {
    #         'name': 'Poland Business Run',
    #         'description': 'Charity relay race supporting people with mobility impairments.',
    #         'date': date(2024, 9, 3),
    #         'time': time(9, 30),
    #         'location': 'Krakow, Poland',
    #         'organizer': 'Poland Business Run Foundation',
    #         'contact': 'info@polandbusinessrun.pl',
    #         'image': None,
    #         'partners': 'PwC, UBS, ABB'
    #     },
    #     {
    #         'name': 'Bieg Wegański',
    #         'description': 'Charity run promoting veganism and animal rights.',
    #         'date': date(2024, 4, 21),
    #         'time': time(10, 0),
    #         'location': 'Warsaw, Poland',
    #         'organizer': 'Viva Foundation',
    #         'contact': 'contact@viva.org.pl',
    #         'image': None,
    #         'partners': 'Vegan Fair, BioBazar'
    #     },
    #     {
    #         'name': 'Runmageddon',
    #         'description': 'Extreme obstacle course race with a charity component.',
    #         'date': date(2024, 6, 10),
    #         'time': time(8, 0),
    #         'location': 'Gdańsk, Poland',
    #         'organizer': 'Runmageddon Foundation',
    #         'contact': 'info@runmageddon.pl',
    #         'image': None,
    #         'partners': 'PKO Bank Polski, 4F, T-Mobile'
    #     },
    #     {
    #         'name': 'Pomoc Dla Ukrainy',
    #         'description': 'Fundraising event to support Ukraine during the ongoing conflict.',
    #         'date': date(2024, 3, 15),
    #         'time': time(18, 0),
    #         'location': 'Poznań, Poland',
    #         'organizer': 'Help for Ukraine Foundation',
    #         'contact': 'contact@helpforukraine.org',
    #         'image': None,
    #         'partners': 'UNICEF, Caritas, Polish Red Cross'
    #     }
    # ]

    # for event_data in events_data:
    #     Event.objects.create(**event_data)

    # print("Fundraising events created successfully!")
    
    # # 1. Create a Konkurs record
    # konkurs = Konkurs.objects.create(
    #     nazwa="Konkurs Fundusz Młodzieżowy 2024",
    #     opis="Otwarte konkursy ofert na realizację zadań publicznych dofinansowanych w 2024 r. ze środków Rządowego Programu Fundusz Młodzieżowy.",
    #     calkowita_kwota=47_000_000,  # Total amount as mentioned in the text
    #     data_ogloszenia=date(2023, 9, 15),  # Replace with the actual announcement date if available
    #     data_zakonczenia_skladania_ofert=date(2023, 9, 25),
    #     infolinia_telefon="601-901-327",
    #     infolinia_email="fm@niw.gov.pl"
    # )

    # # 2. Create Priorytet records related to the Konkurs
    # priorytet1 = Priorytet.objects.create(
    #     konkurs=konkurs,
    #     numer=1,
    #     nazwa="Aktywizacja młodzieży w samorządach",
    #     opis="Realizacja projektów w ramach Priorytetu 1 odbywać się będzie poprzez wyłonienie Operatorów.",
    #     kwota_2024=7_000_000,
    #     kwota_2025=7_000_000,
    #     kwota_2026=7_000_000
    # )

    # priorytet2 = Priorytet.objects.create(
    #     konkurs=konkurs,
    #     numer=2,
    #     nazwa="Organizacje młodzieżowe w życiu publicznym",
    #     opis="Projekty powinny przyczyniać się do zwiększenia obecności organizacji młodzieżowych w życiu publicznym.",
    #     kwota_2024=7_000_000,
    #     kwota_2025=7_000_000,
    #     kwota_2026=None  # Not applicable in 2026
    # )

    # priorytet3 = Priorytet.objects.create(
    #     konkurs=konkurs,
    #     numer=3,
    #     nazwa="Wzmocnienie kompetencji organizacji młodzieżowych",
    #     opis="Projekty mają na celu budowę i wzmocnienie potencjału organizacji młodzieżowych.",
    #     kwota_2024=5_200_000,
    #     kwota_2025=5_200_000,
    #     kwota_2026=None
    # )

    # # 3. Create Zadanie (task) records related to Priorytety
    # zadanie1_1 = Zadanie.objects.create(
    #     priorytet=priorytet1,
    #     numer=1,
    #     nazwa="Tworzenie i aktywizacja rad młodzieżowych",
    #     opis="Tworzenie i aktywizacja rad młodzieżowych w jednostkach samorządu terytorialnego."
    # )

    # zadanie1_2 = Zadanie.objects.create(
    #     priorytet=priorytet1,
    #     numer=2,
    #     nazwa="Aktywizacja samorządów uczniowskich i studenckich",
    #     opis="Aktywizacja samorządów uczniowskich i studenckich w jednostkach edukacyjnych."
    # )

    # zadanie2_1 = Zadanie.objects.create(
    #     priorytet=priorytet2,
    #     numer=1,
    #     nazwa="Edukacja obywatelska i dialog obywatelski",
    #     opis="Zwiększanie udziału młodzieży w dialogu obywatelskim i procesach konsultacji."
    # )

    # # 4. Create Terminy (dates) related to the Konkurs
    # terminy = Terminy.objects.create(
    #     konkurs=konkurs,
    #     start_realizacji=date(2024, 1, 1),
    #     koniec_realizacji=date(2026, 12, 31),  # End date as per text
    #     data_rozstrzygniecia=date(2023, 11, 30)
    # )

    # # 5. Create ZasadyDotacji (funding rules) related to the Konkurs
    # zasady_dotacji = ZasadyDotacji.objects.create(
    #     konkurs=konkurs,
    #     maksymalna_dotacja=6_300_000,  # Maximum possible dotation mentioned for Priorytet 1
    #     minimalna_dotacja=50_000,
    #     wymog_wkladu_wlasnego=False  # Wkład własny not required as per text
    # )


    # events_data = [
    #     {
    #         "name": "Gala Charytatywna Polsat",
    #         "description": "Coroczna gala organizowana przez Polsat, aby zbierać fundusze na różne cele charytatywne.",
    #         "date": "2024-05-20",
    #         "time": "18:00:00",
    #         "location": "Warszawa, Polska",
    #         "organizer": "Polsat",
    #         "contact": "kontakt@polsat.pl",
    #         "partners": "PKO Bank Polski, Grupa Lotos, Coca-Cola"
    #     },
    #     {
    #         "name": "Akcja Charytatywna PCK",
    #         "description": "Wydarzenie charytatywne organizowane przez PCK w celu wsparcia lokalnych organizacji.",
    #         "date": "2024-06-15",
    #         "time": "10:00:00",
    #         "location": "Kraków, Polska",
    #         "organizer": "PCK",
    #         "contact": "info@pck.pl",
    #         "partners": "Nestlé Polska, Lidl, PZU"
    #     },
    #     {
    #         "name": "Bieg Charytatywny Siepomaga",
    #         "description": "Bieg charytatywny organizowany przez Siepomaga, aby zwiększyć świadomość i zbierać fundusze dla chorych dzieci.",
    #         "date": "2024-07-10",
    #         "time": "09:00:00",
    #         "location": "Wrocław, Polska",
    #         "organizer": "Siepomaga",
    #         "contact": "info@siepomaga.pl",
    #         "partners": "Allegro, Decathlon, MediaMarkt"
    #     },
    #     {
    #         "name": "Coroczny Fundraiser Caritas",
    #         "description": "Caritas organizuje coroczny fundraiser, aby wspierać potrzebujących w Polsce.",
    #         "date": "2024-08-05",
    #         "time": "17:00:00",
    #         "location": "Gdańsk, Polska",
    #         "organizer": "Caritas",
    #         "contact": "kontakt@caritas.pl",
    #         "partners": "KGHM, Energa, Orange"
    #     },
    #     {
    #         "name": "Wielka Orkiestra Świątecznej Pomocy",
    #         "description": "Największe wydarzenie charytatywne w Polsce, zbierające fundusze na zdrowie dzieci.",
    #         "date": "2024-01-14",
    #         "time": "12:00:00",
    #         "location": "Ogólnokrajowo",
    #         "organizer": "WOSP",
    #         "contact": "info@wosp.pl",
    #         "partners": "Carrefour, Lotos, Polpharma"
    #     }
    # ]

    # # Create and save Event objects
    # for event_data in events_data:
    #     event = Event(
    #         name=event_data["name"],
    #         description=event_data["description"],
    #         date=event_data["date"],
    #         time=event_data["time"],
    #         location=event_data["location"],
    #         organizer=event_data["organizer"],
    #         contact=event_data["contact"],
    #         partners=event_data["partners"]
    #     )
    #     event.save()  # Save the event to the database

    
    return JsonResponse(serialize_grant_to_json(0), safe=False)


def serialize_all_firma_to_json():
    # Fetch all Firma objects
    firms = Firma.objects.all()
    
    # Create an empty list to store the serialized data
    firms_data = []
    
    # Loop through each Firma and convert it to a dictionary
    for firm in firms:
        firm_data = model_to_dict(firm)  # Convert the model instance to a dictionary
        firm_data['budzet_spoleczny'] = str(firm_data['budzet_spoleczny'])  # Ensure Decimal fields are serialized
        
        # Include related Partner records
        firm_data['partnerzy'] = [
            {
                'nazwa': partner.nazwa,
                'opis': partner.opis
            }
            for partner in firm.partnerzy.all()  # Fetch related Partner objects
        ]
        
        firms_data.append(firm_data)  # Append the dictionary to the list
    
    return firms_data




from django.forms.models import model_to_dict
from django.http import JsonResponse
# from .models import NGO

def serialize_all_ngo_to_json():
    # Fetch all NGO objects
    ngos = NGO.objects.all()
    
    # Create an empty list to store the serialized data
    ngos_data = []
    
    # Loop through each NGO and convert it to a dictionary
    for ngo in ngos:
        ngo_data = model_to_dict(ngo)  # Convert the model instance to a dictionary
        
        # Include related Projekt records
        ngo_data['projekty'] = [
            {
                'nazwa': projekt.nazwa,
                'opis': projekt.opis,
                'data_rozpoczecia': projekt.data_rozpoczecia.isoformat() if projekt.data_rozpoczecia else None,
                'data_zakonczenia': projekt.data_zakonczenia.isoformat() if projekt.data_zakonczenia else None,
            }
            for projekt in ngo.projekty.all()  # Fetch related Projekt objects
        ]
        
        # Include related CzłonekZespolu records
        ngo_data['czlonkowie_zespolu'] = [
            {
                'imie': czlonek.imie,
                'nazwisko': czlonek.nazwisko,
                'rola': czlonek.rola,
                'doswiadczenie': czlonek.doswiadczenie,
            }
            for czlonek in ngo.czlonkowie_zespolu.all()  # Fetch related CzłonekZespolu objects
        ]
        
        ngos_data.append(ngo_data)  # Append the dictionary to the list
    
    return ngos_data


def browse(request):
    print(request.GET)

    result = {}
    result['companies'] = list(Firma.objects.all().values())

    result = {'grants': serialize_all_grants_to_json(),
              'companies': serialize_all_firma_to_json(),
              'ngo': serialize_all_ngo_to_json()}



    return JsonResponse(result, safe=False)