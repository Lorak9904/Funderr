from django.db import models
from django.core.validators import RegexValidator

# Model dla NGO'sów

class Projekt(models.Model):
    nazwa = models.CharField(max_length=255)
    opis = models.TextField()
    organizacja = models.ForeignKey('NGO', on_delete=models.CASCADE, related_name='projekty')
    data_rozpoczecia = models.DateField(null=True, blank=True)
    data_zakonczenia = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nazwa

class CzłonekZespolu(models.Model):
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    rola = models.CharField(max_length=100)
    doswiadczenie = models.TextField()
    organizacja = models.ForeignKey('NGO', on_delete=models.CASCADE, related_name='czlonkowie_zespolu')

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'

class NGO(models.Model):
    nazwaOrganizacji = models.CharField(max_length=100, null=True, verbose_name="Organization Name")
    adresEmail = models.EmailField(max_length=100, null=True, verbose_name="Email Address")
    
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")
    
    numerTelefonuKom = models.CharField(max_length=15, null=True, validators=[phone_validator], verbose_name="Mobile Phone Number")
    numerTelefonuSta = models.CharField(max_length=15, null=True, validators=[phone_validator], verbose_name="Landline Phone Number")
    
    branza = models.CharField(max_length=100, null=True, verbose_name="Industry")
    cel = models.TextField(null=True, verbose_name="Goal")  # TextField for more detailed text
    rozmiarOrganizacji = models.CharField(max_length=50, null=True, verbose_name="Organization Size")
    rodzajFinansowania = models.CharField(max_length=50, null=True, verbose_name="Funding Type")
    
    osobaKontaktowa = models.CharField(max_length=100, null=True, verbose_name="Contact Person")
    RankingESG = models.CharField(max_length=100, null=True, verbose_name="ESG Ranking")
    
    adres = models.CharField(max_length=150, null=True, verbose_name="Address")
    miasto = models.CharField(max_length=50, null=True, verbose_name="City")
    wojewodztwo = models.CharField(max_length=50, null=True, verbose_name="Province")
    kodPocztowy = models.CharField(max_length=10, null=True, verbose_name="Postal Code")
    kraj = models.CharField(max_length=50, null=True, verbose_name="Country")

    strategia = models.TextField()  # Strategia lub statut
    doswiadczenie = models.TextField()  # Doświadczenie w poprzednich projektach
    cele_spoleczne = models.TextField()  # Cele społeczne
    cele_biznesowe = models.TextField()  # Cele biznesowe
    zespol = models.ManyToManyField(CzłonekZespolu, related_name='organizacja_zespoly')

    def __str__(self):
        return self.nazwa

# Model dla firm

class Konkurs(models.Model):
    nazwa = models.CharField(max_length=255)
    opis = models.TextField()
    calkowita_kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data_ogloszenia = models.DateField()
    data_zakonczenia_skladania_ofert = models.DateField()
    infolinia_telefon = models.CharField(max_length=20)
    infolinia_email = models.EmailField()
    
    def __str__(self):
        return self.nazwa

class Priorytet(models.Model):
    konkurs = models.ForeignKey(Konkurs, related_name='priorytety', on_delete=models.CASCADE)
    numer = models.IntegerField()  # Priorytet 1, Priorytet 2 itd.
    nazwa = models.CharField(max_length=255)
    opis = models.TextField()
    kwota_2024 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    kwota_2025 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    kwota_2026 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Priorytet {self.numer}: {self.nazwa}"

class Zadanie(models.Model):
    priorytet = models.ForeignKey(Priorytet, related_name='zadania', on_delete=models.CASCADE)
    numer = models.IntegerField()  # Ścieżka 1, Ścieżka 2 itd.
    nazwa = models.CharField(max_length=255)
    opis = models.TextField()

    def __str__(self):
        return f"Zadanie {self.numer}: {self.nazwa}"

class Terminy(models.Model):
    konkurs = models.OneToOneField(Konkurs, related_name='terminy', on_delete=models.CASCADE)
    start_realizacji = models.DateField()
    koniec_realizacji = models.DateField()
    data_rozstrzygniecia = models.DateField()

    def __str__(self):
        return f"Terminy dla {self.konkurs.nazwa}"

class ZasadyDotacji(models.Model):
    konkurs = models.OneToOneField(Konkurs, related_name='zasady_dotacji', on_delete=models.CASCADE)
    maksymalna_dotacja = models.DecimalField(max_digits=10, decimal_places=2)
    minimalna_dotacja = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wymog_wkladu_wlasnego = models.BooleanField(default=False)

    def __str__(self):
        return f"Zasady dotacji dla {self.konkurs.nazwa}"

class Partner(models.Model):
    nazwa = models.CharField(max_length=255)
    opis = models.TextField()

    def __str__(self):
        return self.nazwa

class Firma(models.Model):
    nazwaFirmy = models.CharField(max_length=100, null=True, verbose_name="Company Name")
    adresEmail = models.EmailField(max_length=100, null=True, verbose_name="Email Address")
    
    # Phone number validator to ensure proper format (international and local)
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")
    
    numerTelefonuKom = models.CharField(max_length=15, null=True, validators=[phone_validator], verbose_name="Mobile Phone Number")
    numerTelefonuSta = models.CharField(max_length=15, null=True, validators=[phone_validator], verbose_name="Landline Phone Number")
    
    branza = models.CharField(max_length=100, null=True, verbose_name="Industry")
    cel = models.TextField(null=True, verbose_name="Purpose or Goal")  # TextField for more detailed text
    rozmiarFirmy = models.CharField(max_length=50, null=True, verbose_name="Company Size")
    rodzajFinansowania = models.CharField(max_length=50, null=True, verbose_name="Funding Type")
    
    osobaKontaktowa = models.CharField(max_length=100, null=True, verbose_name="Contact Person")
    RankingESG = models.CharField(max_length=100, null=True, verbose_name="ESG Ranking")
    
    adres = models.CharField(max_length=150, null=True, verbose_name="Address")
    miasto = models.CharField(max_length=50, null=True, verbose_name="City")
    wojewodztwo = models.CharField(max_length=50, null=True, verbose_name="Province")
    kodPocztowy = models.CharField(max_length=10, null=True, verbose_name="Postal Code")
    kraj = models.CharField(max_length=50, null=True, verbose_name="Country")
    
    strategia_spolecznego_oddzialywania = models.TextField()  # Strategia działań Social Impact
    cele_spoleczne = models.TextField()  # Cele społeczne
    cele_biznesowe = models.TextField()  # Cele biznesowe
    budzet_spoleczny = models.DecimalField(max_digits=12, decimal_places=2)  # Budżet na działania społeczne
    partnerzy = models.ManyToManyField(Partner, related_name='firmy', blank=True)  # Lista partnerów
    granty = models.ManyToManyField(Konkurs, related_name='firmy', blank=True)  # Lista konkursów

    def __str__(self):
        return self.nazwa