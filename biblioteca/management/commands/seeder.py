from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, randint
from biblioteca.models import Llengua, Pais, Llibre, Exemplar, Usuari

faker = Faker(["es_CA", "es_ES", "en_US", "fr_FR"])

class Command(BaseCommand):
    help = "Seeder per omplir la base de dades amb llibres i usuaris"

    def handle(self, *args, **kwargs):
        self.stdout.write("Esborrant dades antigues...")
        Exemplar.objects.all().delete()
        Llibre.objects.all().delete()
        Usuari.objects.filter(username__startswith="fake_user").delete()
        
        # Idiomes
        llengues = {
            "Català": Llengua.objects.get_or_create(nom="Català")[0],
            "Español": Llengua.objects.get_or_create(nom="Español")[0],
            "English": Llengua.objects.get_or_create(nom="English")[0],
            "Français": Llengua.objects.get_or_create(nom="Français")[0],
        }
        
        # Països
        paisos = [Pais.objects.get_or_create(nom=faker.country())[0] for _ in range(4)]
        
        # Creació de llibres
        self.stdout.write("Creant 40 llibres...")
        llibres = []
        
        for idioma, llengua in llengues.items():
            for _ in range(10):
                llibre = Llibre.objects.create(
                    titol=faker.sentence(nb_words=3),
                    autor=faker.name(),
                    CDU=faker.word(),
                    signatura=faker.lexify(text="???-???"),
                    data_edicio=faker.date_between(start_date="-10y", end_date="today"),
                    resum=faker.paragraph(),
                    anotacions=faker.sentence(),
                    mides=faker.word(),
                    ISBN=faker.numerify(text="#############"),
                    editorial=faker.company(),
                    colleccio=faker.word(),
                    lloc=faker.city(),
                    pais=choice(paisos),
                    llengua=llengua,
                    numero=randint(1, 5),
                    volums=randint(1, 3),
                    pagines=randint(50, 500),
                    info_url=faker.url(),
                    preview_url=faker.url(),
                    thumbnail_url=faker.url()
                )
                llibres.append(llibre)
        
        # Creació de 2 exemplars per llibre
        self.stdout.write("Creant exemplars per a cada llibre...")
        for llibre in llibres:
            for _ in range(2):
                Exemplar.objects.create(
                    cataleg=llibre,
                    registre=faker.lexify(text="????-????"),
                    exclos_prestec=faker.boolean(chance_of_getting_true=25),
                    baixa=faker.boolean(chance_of_getting_true=10)
                )
        
        # Creació de 50 usuaris
        self.stdout.write("Creant 50 usuaris...")
        for i in range(50):
            Usuari.objects.create_user(
                username=f"fake_user{i}",
                password="password123",
                email=faker.email(),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
            )
        
        self.stdout.write(self.style.SUCCESS("Seeder completat amb èxit! 🎉"))