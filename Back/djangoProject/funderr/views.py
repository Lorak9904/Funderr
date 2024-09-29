from django.shortcuts import render
from django.http import JsonResponse
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

def browse(request):
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
    
    if request.method == 'POST':
        print(request.POST)
    print(request)
    
    events = Event.objects.all()
    
    # Create a list of dictionaries for each event
    events_list = []
    for event in events:
        event_dict = model_to_dict(event)

        # Format the date, time, and created_at fields
        event_dict['date'] = event.date.isoformat() if event.date else None
        event_dict['time'] = event.time.isoformat() if event.time else None
        event_dict['created_at'] = event.created_at.isoformat()

        # Handle the image field
        event_dict['image'] = event.image.url if event.image else None
        
        # Append the formatted event dictionary to the list
        events_list.append(event_dict)

    # Prepare the response data with the key "carousel"
    response_data = {
        'carousel': events_list
    }

    
    return JsonResponse(response_data)

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


def handle():
    companies_data = [
        {
            "nazwaFirmy": "PKN Orlen",
            "adresEmail": "kontakt@orlen.pl",
            "numerTelefonuKom": "+48123456789",
            "numerTelefonuSta": "+48123456788",
            "branza": "Energia",
            "cel": "Wsparcie lokalnych społeczności",
            "rozmiarFirmy": "Duża",
            "rodzajFinansowania": "Własne",
            "osobaKontaktowa": "Jan Kowalski",
            "RankingESG": "A",
            "adres": "ul. Chemików 7",
            "miasto": "Płock",
            "wojewodztwo": "Mazowieckie",
            "kodPocztowy": "09-400",
            "kraj": "Polska",
            "strategia_spolecznego_oddzialywania": "Szeroko zakrojone działania proekologiczne.",
            "cele_spoleczne": "Zrównoważony rozwój.",
            "cele_biznesowe": "Zwiększenie efektywności operacyjnej.",
            "budzet_spoleczny": 50000000.00,
            "partnerzy": [
                {"nazwa": "Caritas Polska", "opis": "Wsparcie dla osób potrzebujących."},
                {"nazwa": "Fundacja WOŚP", "opis": "Wsparcie dla służby zdrowia."},
            ]
        },
        {
            "nazwaFirmy": "Polsat",
            "adresEmail": "kontakt@polsat.pl",
            "numerTelefonuKom": "+48123456790",
            "numerTelefonuSta": "+48123456789",
            "branza": "Media",
            "cel": "Edukacja młodzieży",
            "rozmiarFirmy": "Duża",
            "rodzajFinansowania": "Własne",
            "osobaKontaktowa": "Anna Nowak",
            "RankingESG": "B",
            "adres": "ul. Nowy Świat 18",
            "miasto": "Warszawa",
            "wojewodztwo": "Mazowieckie",
            "kodPocztowy": "00-001",
            "kraj": "Polska",
            "strategia_spolecznego_oddzialywania": "Promowanie aktywności społecznej.",
            "cele_spoleczne": "Wsparcie dla organizacji pozarządowych.",
            "cele_biznesowe": "Zwiększenie świadomości marki.",
            "budzet_spoleczny": 20000000.00,
            "partnerzy": [
                {"nazwa": "Fundacja PCK", "opis": "Wsparcie dla osób w potrzebie."},
                {"nazwa": "Fundacja Dziecięca Fantazja", "opis": "Pomoc dzieciom w trudnej sytuacji."},
            ]
        },
        {
            "nazwaFirmy": "KGHM Polska Miedź",
            "adresEmail": "kontakt@kghm.pl",
            "numerTelefonuKom": "+48123456791",
            "numerTelefonuSta": "+48123456790",
            "branza": "Przemysł",
            "cel": "Inwestycje w lokalne społeczności",
            "rozmiarFirmy": "Duża",
            "rodzajFinansowania": "Własne",
            "osobaKontaktowa": "Tomasz Wysocki",
            "RankingESG": "A",
            "adres": "ul. Miedziowa 1",
            "miasto": "Lubin",
            "wojewodztwo": "Dolnośląskie",
            "kodPocztowy": "59-300",
            "kraj": "Polska",
            "strategia_spolecznego_oddzialywania": "Edukacja i pomoc społeczna.",
            "cele_spoleczne": "Zwiększenie jakości życia lokalnych społeczności.",
            "cele_biznesowe": "Zrównoważony rozwój.",
            "budzet_spoleczny": 30000000.00,
            "partnerzy": [
                {"nazwa": "Fundacja Anny Dymnej", "opis": "Wsparcie osób z niepełnosprawnościami."},
                {"nazwa": "Fundacja Wspólna Ziemia", "opis": "Ochrona środowiska."},
            ]
        },
        {
            "nazwaFirmy": "Allegro",
            "adresEmail": "kontakt@allegro.pl",
            "numerTelefonuKom": "+48123456792",
            "numerTelefonuSta": "+48123456791",
            "branza": "E-commerce",
            "cel": "Wsparcie lokalnych rzemieślników",
            "rozmiarFirmy": "Duża",
            "rodzajFinansowania": "Własne",
            "osobaKontaktowa": "Michał Wiśniewski",
            "RankingESG": "B",
            "adres": "ul. Grunwaldzka 123",
            "miasto": "Poznań",
            "wojewodztwo": "Wielkopolskie",
            "kodPocztowy": "60-000",
            "kraj": "Polska",
            "strategia_spolecznego_oddzialywania": "Wsparcie lokalnych inicjatyw.",
            "cele_spoleczne": "Zwiększenie dostępności dla lokalnych sprzedawców.",
            "cele_biznesowe": "Zwiększenie liczby transakcji.",
            "budzet_spoleczny": 15000000.00,
            "partnerzy": [
                {"nazwa": "Fundacja Kiva", "opis": "Wsparcie mikroprzedsiębiorstw."},
                {"nazwa": "Fundacja EkoWawel", "opis": "Edukacja ekologiczna."},
            ]
        },
        {
            "nazwaFirmy": "LPP S.A.",
            "adresEmail": "kontakt@lpp.com.pl",
            "numerTelefonuKom": "+48123456793",
            "numerTelefonuSta": "+48123456792",
            "branza": "Odzież",
            "cel": "Zrównoważona moda",
            "rozmiarFirmy": "Duża",
            "rodzajFinansowania": "Własne",
            "osobaKontaktowa": "Ewa Jankowska",
            "RankingESG": "A",
            "adres": "ul. Gdańska 123",
            "miasto": "Gdańsk",
            "wojewodztwo": "Pomorskie",
            "kodPocztowy": "80-000",
            "kraj": "Polska",
            "strategia_spolecznego_oddzialywania": "Edukacja i wspieranie lokalnych projektów.",
            "cele_spoleczne": "Zrównoważony rozwój.",
            "cele_biznesowe": "Wzrost sprzedaży.",
            "budzet_spoleczny": 25000000.00,
            "partnerzy": [
                {"nazwa": "Fundacja Nagle Sami", "opis": "Wsparcie osób starszych."},
                {"nazwa": "Fundacja Dzieciom", "opis": "Wsparcie dla dzieci z ubogich rodzin."},
            ]
        },
        {
            "nazwaFirmy": "Tauron",
            "adresEmail": "kontakt@tauron.pl",
            "numerTelefonuKom": "+48123456794",
            "numerTelefonuSta": "+48123456793",
            "branza": "Energia",
            "cel": "Zielona energia",
            "rozmiarFirmy": "Duża",
            "rodzajFinansowania": "Własne",
            "osobaKontaktowa": "Jakub Mały",
            "RankingESG": "A",
            "adres": "ul. Energetyków 2",
            "miasto": "Katowice",
            "wojewodztwo": "Śląskie",
            "kodPocztowy": "40-003",
            "kraj": "Polska",
            "strategia_spolecznego_oddzialywania": "Ochrona środowiska.",
            "cele_spoleczne": "Zwiększenie dostępu do energii odnawialnej.",
            "cele_biznesowe": "Wzrost efektywności operacyjnej.",
            "budzet_spoleczny": 40000000.00,
            "partnerzy": [
                {"nazwa": "Fundacja EkoZiemia", "opis": "Ochrona środowiska."},
                {"nazwa": "Fundacja My w Europie", "opis": "Wspieranie kultury."},
            ]
        },
        {
            "nazwaFirmy": "Złote Tarasy",
            "adresEmail": "kontakt@zlotetarasy.pl",
            "numerTelefonuKom": "+48123456795",
            "numerTelefonuSta": "+48123456794",
            "branza": "Handel",
            "cel": "Promowanie lokalnych producentów",
            "rozmiarFirmy": "Duża",
            "rodzajFinansowania": "Własne",
            "osobaKontaktowa": "Katarzyna Kowalczyk",
            "RankingESG": "B",
            "adres": "ul. Złota 1",
            "miasto": "Warszawa",
            "wojewodztwo": "Mazowieckie",
            "kodPocztowy": "00-020",
            "kraj": "Polska",
            "strategia_spolecznego_oddzialywania": "Wsparcie lokalnych rzemieślników.",
            "cele_spoleczne": "Zwiększenie dostępu do rynku lokalnego.",
            "cele_biznesowe": "Zwiększenie sprzedaży.",
            "budzet_spoleczny": 20000000.00,
            "partnerzy": [
                {"nazwa": "Fundacja Lokalna", "opis": "Wsparcie dla lokalnych inicjatyw."},
                {"nazwa": "Fundacja Będę Mamą", "opis": "Wsparcie dla kobiet w ciąży."},
            ]
        },
        {
            "nazwaFirmy": "Coca-Cola HBC Polska",
            "adresEmail": "kontakt@cokecola.pl",
            "numerTelefonuKom": "+48123456796",
            "numerTelefonuSta": "+48123456795",
            "branza": "Napojowa",
            "cel": "Ochrona środowiska",
            "rozmiarFirmy": "Duża",
            "rodzajFinansowania": "Własne",
            "osobaKontaktowa": "Julia Nowicka",
            "RankingESG": "A",
            "adres": "ul. Coca-Cola 5",
            "miasto": "Warszawa",
            "wojewodztwo": "Mazowieckie",
            "kodPocztowy": "00-000",
            "kraj": "Polska",
            "strategia_spolecznego_oddzialywania": "Edukacja ekologiczna.",
            "cele_spoleczne": "Ochrona zasobów wodnych.",
            "cele_biznesowe": "Zwiększenie efektywności operacyjnej.",
            "budzet_spoleczny": 30000000.00,
            "partnerzy": [
                {"nazwa": "Fundacja WWF Polska", "opis": "Ochrona środowiska."},
                {"nazwa": "Fundacja Nasza Ziemia", "opis": "Edukacja ekologiczna."},
            ]
        },
        {
            "nazwaFirmy": "Nestlé Polska",
            "adresEmail": "kontakt@nestle.pl",
            "numerTelefonuKom": "+48123456797",
            "numerTelefonuSta": "+48123456796",
            "branza": "Spożywcza",
            "cel": "Zrównoważona produkcja",
            "rozmiarFirmy": "Duża",
            "rodzajFinansowania": "Własne",
            "osobaKontaktowa": "Marta Zielińska",
            "RankingESG": "A",
            "adres": "ul. Karmelowa 2",
            "miasto": "Warszawa",
            "wojewodztwo": "Mazowieckie",
            "kodPocztowy": "00-001",
            "kraj": "Polska",
            "strategia_spolecznego_oddzialywania": "Edukacja na temat zdrowego żywienia.",
            "cele_spoleczne": "Wspieranie zdrowego stylu życia.",
            "cele_biznesowe": "Zwiększenie udziału w rynku.",
            "budzet_spoleczny": 35000000.00,
            "partnerzy": [
                {"nazwa": "Fundacja Smaki Życia", "opis": "Wsparcie zdrowego stylu życia."},
                {"nazwa": "Fundacja Dzieciom", "opis": "Wsparcie dzieci w trudnej sytuacji."},
            ]
        },
    ]

    for company in companies_data:
        # Create Firma instance
        firma = Firma.objects.create(
            nazwaFirmy=company["nazwaFirmy"],
            adresEmail=company["adresEmail"],
            numerTelefonuKom=company["numerTelefonuKom"],
            numerTelefonuSta=company["numerTelefonuSta"],
            branza=company["branza"],
            cel=company["cel"],
            rozmiarFirmy=company["rozmiarFirmy"],
            rodzajFinansowania=company["rodzajFinansowania"],
            osobaKontaktowa=company["osobaKontaktowa"],
            RankingESG=company["RankingESG"],
            adres=company["adres"],
            miasto=company["miasto"],
            wojewodztwo=company["wojewodztwo"],
            kodPocztowy=company["kodPocztowy"],
            kraj=company["kraj"],
            strategia_spolecznego_oddzialywania=company["strategia_spolecznego_oddzialywania"],
            cele_spoleczne=company["cele_spoleczne"],
            cele_biznesowe=company["cele_biznesowe"],
            budzet_spoleczny=company["budzet_spoleczny"]
        )

        # Create Partner instances
        for partner_data in company["partnerzy"]:
            Partner.objects.create(
                firma=firma,
                nazwa=partner_data["nazwa"],
                opis=partner_data["opis"]
            )


def handle1():
    ngos_data = [
    {
        "nazwaOrganizacji": "Fundacja Dziecięca Przyszłość",
        "adresEmail": "kontakt@dziecieceprzyszlosci.pl",
        "numerTelefonuKom": "+48123456780",
        "numerTelefonuSta": "+48123456781",
        "branza": "Edukacja",
        "cel": "Wsparcie dzieci z rodzin ubogich",
        "rozmiarOrganizacji": "Duża",
        "rodzajFinansowania": "Dotacje",
        "osobaKontaktowa": "Anna Kowalska",
        "RankingESG": "A",
        "adres": "ul. Szkolna 5",
        "miasto": "Warszawa",
        "wojewodztwo": "Mazowieckie",
        "kodPocztowy": "00-001",
        "kraj": "Polska",
        "strategia": "Organizacja zajęć pozalekcyjnych dla dzieci.",
        "doswiadczenie": "Ponad 10-letnie doświadczenie w edukacji.",
        "cele_spoleczne": "Wspieranie równości w edukacji.",
        "cele_biznesowe": "Rozwój programów stypendialnych.",
        "czlonkowie_zespolu": [
            {
                "imie": "Marek",
                "nazwisko": "Jankowski",
                "rola": "Dyrektor",
                "doswiadczenie": "15 lat w edukacji."
            },
            {
                "imie": "Katarzyna",
                "nazwisko": "Nowak",
                "rola": "Koordynator",
                "doswiadczenie": "8 lat w pracy z dziećmi."
            }
        ],
        "tagi": [
            "edukacja", "dzieci", "wsparcie", "fundacja", "stypendia",
            "Mazowieckie", "projekty", "społeczność", "rozwój", "działalność"
        ]
    },
    {
        "nazwaOrganizacji": "Fundacja Na Rzecz Zwierząt",
        "adresEmail": "kontakt@zwierzeta.pl",
        "numerTelefonuKom": "+48123456782",
        "numerTelefonuSta": "+48123456783",
        "branza": "Ochrona zwierząt",
        "cel": "Pomoc bezdomnym zwierzętom",
        "rozmiarOrganizacji": "Średnia",
        "rodzajFinansowania": "Darowizny",
        "osobaKontaktowa": "Marta Zielińska",
        "RankingESG": "A",
        "adres": "ul. Leśna 12",
        "miasto": "Wrocław",
        "wojewodztwo": "Dolnośląskie",
        "kodPocztowy": "50-001",
        "kraj": "Polska",
        "strategia": "Akcje adopcyjne i edukacyjne o odpowiedzialnej opiece.",
        "doswiadczenie": "8 lat doświadczenia w ochronie zwierząt.",
        "cele_spoleczne": "Poprawa warunków życia zwierząt.",
        "cele_biznesowe": "Zwiększenie liczby adopcji.",
        "czlonkowie_zespolu": [
            {
                "imie": "Jan",
                "nazwisko": "Kowalczyk",
                "rola": "Wolontariusz",
                "doswiadczenie": "5 lat w opiece nad zwierzętami."
            },
            {
                "imie": "Anita",
                "nazwisko": "Krawczyk",
                "rola": "Menadżer",
                "doswiadczenie": "3 lata w zarządzaniu fundacjami."
            }
        ],
        "tagi": [
            "zwierzęta", "opieka", "fundacja", "Wrocław", "adopcja",
            "edukacja", "darowizny", "szkolenia", "społeczność", "pomoc"
        ]
    },
    {
        "nazwaOrganizacji": "Fundacja Wolność i Prawa",
        "adresEmail": "kontakt@wolnosciiprawa.pl",
        "numerTelefonuKom": "+48123456784",
        "numerTelefonuSta": "+48123456785",
        "branza": "Prawa człowieka",
        "cel": "Edukacja i pomoc w zakresie praw człowieka",
        "rozmiarOrganizacji": "Mała",
        "rodzajFinansowania": "Darowizny",
        "osobaKontaktowa": "Piotr Głowacki",
        "RankingESG": "B",
        "adres": "ul. Prawa 8",
        "miasto": "Gdańsk",
        "wojewodztwo": "Pomorskie",
        "kodPocztowy": "80-001",
        "kraj": "Polska",
        "strategia": "Warsztaty i seminaria na temat praw człowieka.",
        "doswiadczenie": "10 lat pracy w NGO.",
        "cele_spoleczne": "Edukacja społeczeństwa o prawach człowieka.",
        "cele_biznesowe": "Budowanie sieci współpracy.",
        "czlonkowie_zespolu": [
            {
                "imie": "Kinga",
                "nazwisko": "Bąk",
                "rola": "Edukator",
                "doswiadczenie": "6 lat w edukacji prawnej."
            },
            {
                "imie": "Tomasz",
                "nazwisko": "Szymański",
                "rola": "Koordynator",
                "doswiadczenie": "4 lata w organizacjach pozarządowych."
            }
        ],
        "tagi": [
            "prawa_człowieka", "edukacja", "fundacja", "Gdańsk", "pomoc",
            "darowizny", "społeczność", "warsztaty", "seminaria", "współpraca"
        ]
    },
    {
        "nazwaOrganizacji": "Fundacja Młodzieżowa Akcja",
        "adresEmail": "kontakt@mlodziezowaakcja.pl",
        "numerTelefonuKom": "+48123456786",
        "numerTelefonuSta": "+48123456787",
        "branza": "Edukacja",
        "cel": "Wspieranie aktywności młodzieży",
        "rozmiarOrganizacji": "Średnia",
        "rodzajFinansowania": "Dotacje",
        "osobaKontaktowa": "Katarzyna Lis",
        "RankingESG": "A",
        "adres": "ul. Młodzieżowa 3",
        "miasto": "Poznań",
        "wojewodztwo": "Wielkopolskie",
        "kodPocztowy": "60-001",
        "kraj": "Polska",
        "strategia": "Projekty aktywizujące młodzież.",
        "doswiadczenie": "5 lat w pracy z młodzieżą.",
        "cele_spoleczne": "Wspieranie młodych liderów.",
        "cele_biznesowe": "Zwiększenie aktywności młodzieży w społeczności.",
        "czlonkowie_zespolu": [
            {
                "imie": "Michał",
                "nazwisko": "Pawlak",
                "rola": "Trener",
                "doswiadczenie": "7 lat w szkoleniach młodzieżowych."
            },
            {
                "imie": "Justyna",
                "nazwisko": "Dąbrowska",
                "rola": "Koordynator projektów",
                "doswiadczenie": "3 lata w NGO."
            }
        ],
        "tagi": [
            "młodzież", "edukacja", "wsparcie", "fundacja", "aktywność",
            "Poznań", "projekty", "liderzy", "społeczność", "rozwój"
        ]
    },
    {
        "nazwaOrganizacji": "Fundacja Pomocy Rodzinie",
        "adresEmail": "kontakt@pomocrodzinie.pl",
        "numerTelefonuKom": "+48123456788",
        "numerTelefonuSta": "+48123456789",
        "branza": "Wsparcie społeczne",
        "cel": "Pomoc rodzinom w trudnej sytuacji",
        "rozmiarOrganizacji": "Duża",
        "rodzajFinansowania": "Darowizny",
        "osobaKontaktowa": "Maria Piekarska",
        "RankingESG": "B",
        "adres": "ul. Rodzinna 15",
        "miasto": "Lublin",
        "wojewodztwo": "Lubelskie",
        "kodPocztowy": "20-001",
        "kraj": "Polska",
        "strategia": "Wsparcie finansowe i doradcze dla rodzin.",
        "doswiadczenie": "12 lat w pomocy społecznej.",
        "cele_spoleczne": "Poprawa sytuacji życiowej rodzin.",
        "cele_biznesowe": "Zwiększenie zasięgu działalności.",
        "czlonkowie_zespolu": [
            {
                "imie": "Tadeusz",
                "nazwisko": "Kowalczyk",
                "rola": "Konsultant",
                "doswiadczenie": "10 lat w pomocy rodzinnej."
            },
            {
                "imie": "Natalia",
                "nazwisko": "Kowal",
                "rola": "Koordynator",
                "doswiadczenie": "5 lat w NGO."
            }
        ],
        "tagi": [
            "rodzina", "wsparcie", "pomoc", "Lublin", "darowizny",
            "sytuacja", "społeczność", "fundacja", "działalność", "strategia"
        ]
    },
    {
        "nazwaOrganizacji": "Fundacja Ochrony Środowiska",
        "adresEmail": "kontakt@ochronasrodowiska.pl",
        "numerTelefonuKom": "+48123456790",
        "numerTelefonuSta": "+48123456791",
        "branza": "Ochrona środowiska",
        "cel": "Promowanie ekologii i ochrony przyrody",
        "rozmiarOrganizacji": "Duża",
        "rodzajFinansowania": "Dotacje",
        "osobaKontaktowa": "Zofia Nowakowska",
        "RankingESG": "A",
        "adres": "ul. Ekologiczna 4",
        "miasto": "Kraków",
        "wojewodztwo": "Małopolskie",
        "kodPocztowy": "30-002",
        "kraj": "Polska",
        "strategia": "Edukacja ekologiczna i projekty ochrony przyrody.",
        "doswiadczenie": "9 lat w ochronie środowiska.",
        "cele_spoleczne": "Zwiększenie świadomości ekologicznej.",
        "cele_biznesowe": "Rozwój projektów ekologicznych.",
        "czlonkowie_zespolu": [
            {
                "imie": "Artur",
                "nazwisko": "Witkowski",
                "rola": "Ekolog",
                "doswiadczenie": "7 lat w projektach ekologicznych."
            },
            {
                "imie": "Barbara",
                "nazwisko": "Wojciechowska",
                "rola": "Koordynator",
                "doswiadczenie": "4 lata w NGO."
            }
        ],
        "tagi": [
            "ekologia", "ochrona", "środowisko", "Kraków", "projekty",
            "edukacja", "fundacja", "przyroda", "świadomość", "dotacje"
        ]
    },
    {
        "nazwaOrganizacji": "Fundacja Wspierania Kulturalnego",
        "adresEmail": "kontakt@wspieraniekultury.pl",
        "numerTelefonuKom": "+48123456792",
        "numerTelefonuSta": "+48123456793",
        "branza": "Kultura",
        "cel": "Wsparcie lokalnych inicjatyw kulturalnych",
        "rozmiarOrganizacji": "Średnia",
        "rodzajFinansowania": "Dotacje",
        "osobaKontaktowa": "Krystyna Górska",
        "RankingESG": "B",
        "adres": "ul. Kulturalna 9",
        "miasto": "Warszawa",
        "wojewodztwo": "Mazowieckie",
        "kodPocztowy": "00-002",
        "kraj": "Polska",
        "strategia": "Organizacja wydarzeń kulturalnych i artystycznych.",
        "doswiadczenie": "6 lat w promocji kultury.",
        "cele_spoleczne": "Zwiększenie dostępu do kultury.",
        "cele_biznesowe": "Rozwój współpracy z lokalnymi artystami.",
        "czlonkowie_zespolu": [
            {
                "imie": "Adam",
                "nazwisko": "Sienkiewicz",
                "rola": "Kurator",
                "doswiadczenie": "5 lat w organizacji wydarzeń."
            },
            {
                "imie": "Monika",
                "nazwisko": "Kozłowska",
                "rola": "Koordynator",
                "doswiadczenie": "3 lata w fundacjach kulturalnych."
            }
        ],
        "tagi": [
            "kultura", "wsparcie", "fundacja", "Warszawa", "wydarzenia",
            "lokalne", "inicjatywy", "artystyczne", "społeczność", "edukacja"
        ]
    },
    {
        "nazwaOrganizacji": "Fundacja Aktywności Społecznej",
        "adresEmail": "kontakt@aktywnosc.pl",
        "numerTelefonuKom": "+48123456794",
        "numerTelefonuSta": "+48123456795",
        "branza": "Aktywność społeczna",
        "cel": "Promowanie aktywności obywatelskiej",
        "rozmiarOrganizacji": "Mała",
        "rodzajFinansowania": "Darowizny",
        "osobaKontaktowa": "Tadeusz Król",
        "RankingESG": "C",
        "adres": "ul. Społeczna 1",
        "miasto": "Bydgoszcz",
        "wojewodztwo": "Kujawsko-Pomorskie",
        "kodPocztowy": "85-001",
        "kraj": "Polska",
        "strategia": "Organizacja warsztatów obywatelskich.",
        "doswiadczenie": "4 lata w pracy na rzecz społeczności.",
        "cele_spoleczne": "Zwiększenie udziału obywateli w życiu społecznym.",
        "cele_biznesowe": "Budowanie zaufania w społeczności.",
        "czlonkowie_zespolu": [
            {
                "imie": "Marta",
                "nazwisko": "Nowicka",
                "rola": "Koordynator",
                "doswiadczenie": "3 lata w NGO."
            },
            {
                "imie": "Krzysztof",
                "nazwisko": "Jasiński",
                "rola": "Wolontariusz",
                "doswiadczenie": "2 lata w pracy społecznej."
            }
        ],
        "tagi": [
            "aktywność", "obywatelska", "wsparcie", "Bydgoszcz", "darowizny",
            "społeczność", "fundacja", "warsztaty", "edukacja", "współpraca"
        ]
    },
    {
        "nazwaOrganizacji": "Fundacja Zdrowego Życia",
        "adresEmail": "kontakt@zdrowezycie.pl",
        "numerTelefonuKom": "+48123456796",
        "numerTelefonuSta": "+48123456797",
        "branza": "Zdrowie",
        "cel": "Promowanie zdrowego stylu życia",
        "rozmiarOrganizacji": "Mała",
        "rodzajFinansowania": "Dotacje",
        "osobaKontaktowa": "Julia Smolińska",
        "RankingESG": "A",
        "adres": "ul. Zdrowa 6",
        "miasto": "Szczecin",
        "wojewodztwo": "Zachodniopomorskie",
        "kodPocztowy": "70-001",
        "kraj": "Polska",
        "strategia": "Edukacja na temat zdrowego stylu życia.",
        "doswiadczenie": "6 lat w promocji zdrowia.",
        "cele_spoleczne": "Zwiększenie świadomości zdrowotnej.",
        "cele_biznesowe": "Rozwój programów zdrowotnych.",
        "czlonkowie_zespolu": [
            {
                "imie": "Krzysztof",
                "nazwisko": "Maciąg",
                "rola": "Trener",
                "doswiadczenie": "4 lata w prowadzeniu szkoleń."
            },
            {
                "imie": "Oliwia",
                "nazwisko": "Białek",
                "rola": "Koordynator",
                "doswiadczenie": "2 lata w NGO."
            }
        ],
        "tagi": [
            "zdrowie", "styl_życia", "edukacja", "Szczecin", "fundacja",
            "promocja", "społeczność", "programy", "świadomość", "wsparcie"
        ]
    }
]


    for ngo_data in ngos_data:
        # Tworzenie instancji NGO
        ngo = NGO.objects.create(
            nazwaOrganizacji=ngo_data["nazwaOrganizacji"],
            adresEmail=ngo_data["adresEmail"],
            numerTelefonuKom=ngo_data["numerTelefonuKom"],
            numerTelefonuSta=ngo_data["numerTelefonuSta"],
            branza=ngo_data["branza"],
            cel=ngo_data["cel"],
            rozmiarOrganizacji=ngo_data["rozmiarOrganizacji"],
            rodzajFinansowania=ngo_data["rodzajFinansowania"],
            osobaKontaktowa=ngo_data["osobaKontaktowa"],
            RankingESG=ngo_data["RankingESG"],
            adres=ngo_data["adres"],
            miasto=ngo_data["miasto"],
            wojewodztwo=ngo_data["wojewodztwo"],
            kodPocztowy=ngo_data["kodPocztowy"],
            kraj=ngo_data["kraj"],
            strategia=ngo_data["strategia"],
            doswiadczenie=ngo_data["doswiadczenie"],
            cele_spoleczne=ngo_data["cele_spoleczne"],
            cele_biznesowe=ngo_data["cele_biznesowe"],
            tags=", ".join(ngo_data["tagi"])
        )

        # Tworzenie instancji CzłonekZespolu
        for czlonek_data in ngo_data["czlonkowie_zespolu"]:
            czlonek = CzłonekZespolu.objects.create(
                imie=czlonek_data["imie"],
                nazwisko=czlonek_data["nazwisko"],
                rola=czlonek_data["rola"],
                doswiadczenie=czlonek_data["doswiadczenie"],
                organizacja=ngo
            )


def funkcja(request):


    # handle()
    handle1()
    #    events_data = [
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

    
    return JsonResponse({"status": "success", "message": "Data created successfully!"})



