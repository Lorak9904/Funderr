from django.shortcuts import render
from django.http import JsonResponse
from register.models import Firma, NGO
from difflib import SequenceMatcher

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
    response_data = {
        "status": "success",
        "message": "Welcome to the API!",
        "data": {
            "name": "Django-Vue/Angular Integration",
            "version": "1.0",
            "description": "This is a sample JSON response from the Django server.",
            "features": [
                "REST API",
                "CORS Enabled",
                "Frontend Integration with Vue/Angular"
            ],
            "contact": {
                "email": "admin@example.com",
                "support": "http://example.com/support"
            }
        }
    }
    return JsonResponse(response_data)