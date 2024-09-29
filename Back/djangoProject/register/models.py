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



class Grant(models.Model):
    nazwa_grantu = models.CharField(max_length=150, null=True, verbose_name="Nazwa Grantu")
    maksymalna_kwota = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name="Maksymalna Kwota")  # Maximum amount of funding
    data_rozpoczecia = models.DateField(null=True, verbose_name="Data Rozpoczęcia")  # Start date of the grant
    data_zakonczenia = models.DateField(null=True, verbose_name="Data Zakończenia")  # End date of the grant
    opis = models.TextField(null=True, verbose_name="Opis Grantu")  # Description of the grant
    priorytet = models.ForeignKey('Priorytet', on_delete=models.CASCADE, related_name='grants_s', verbose_name="Priorytet")  # Link to priority

    def __str__(self):
        return f"{self.nazwa_grantu} - Maksymalna Kwota: {self.maksymalna_kwota} zł"


class Priorytet(models.Model):
    nazwa_priorytetu = models.CharField(max_length=100, null=True, verbose_name="Nazwa Priorytetu")
    opis = models.TextField(null=True, verbose_name="Opis Priorytetu")  # Description of the priority
    grants = models.ManyToManyField(Grant, related_name='priorytety', verbose_name="Grants")  # Many-to-many relation with grants

    def __str__(self):
        return self.nazwa_priorytetu


class Competition(models.Model):
    nazwa_konkursu = models.CharField(max_length=150, null=True, verbose_name="Nazwa Konkursu")
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE, related_name='competitions', verbose_name="Grant")  # Link to the grant
    data_rozpoczecia = models.DateField(null=True, verbose_name="Data Rozpoczęcia")  # Start date of the competition
    data_zakonczenia = models.DateField(null=True, verbose_name="Data Zakończenia")  # End date of the competition
    opis = models.TextField(null=True, verbose_name="Opis Konkursu")  # Description of the competition
    status = models.CharField(max_length=50, null=True, verbose_name="Status Konkursu")  # Status of the competition (e.g., "otwarty", "zamknięty")

    def __str__(self):
        return f"{self.nazwa_konkursu} - Status: {self.status}"


class Partner(models.Model):
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE, related_name='partnerzy', null=True)
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
    tags = models.CharField(max_length=255, null=True, verbose_name="Tags")  # Tags for searching

    def __str__(self):
        return self.nazwaFirmy


