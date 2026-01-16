from django.core.management.base import BaseCommand
from faker import Faker
from watches.models import Brand, Complication, Watch
import random


class Command(BaseCommand):
    help = 'Génère des montres de luxe réalistes avec Faker'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'count', 
            type=int, 
            help='Nombre de montres à générer'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Supprime toutes les données existantes avant de générer'
        )
    
    def handle(self, *args, **options):
        fake = Faker('fr_FR')
        count = options['count']
        
        if options['clear']:
            self.stdout.write(self.style.WARNING('Suppression des données existantes...'))
            Watch.objects.all().delete()
            Brand.objects.all().delete()
            Complication.objects.all().delete()
        
        # Marques de luxe réalistes
        brands_data = [
            {'name': 'Rolex', 'country': 'Suisse', 'year': 1905, 
             'desc': 'Manufacture horlogère suisse de prestige fondée à Londres puis établie à Genève.'},
            {'name': 'Omega', 'country': 'Suisse', 'year': 1848,
             'desc': 'Marque horlogère suisse de luxe, célèbre pour ses montres de plongée et spatiales.'},
            {'name': 'Patek Philippe', 'country': 'Suisse', 'year': 1839,
             'desc': 'Manufacture horlogère de haute horlogerie, considérée comme l\'une des plus prestigieuses.'},
            {'name': 'Audemars Piguet', 'country': 'Suisse', 'year': 1875,
             'desc': 'Manufacture horlogère suisse de luxe, créatrice de la Royal Oak.'},
            {'name': 'Seiko', 'country': 'Japon', 'year': 1881,
             'desc': 'Manufacture horlogère japonaise, pionnière du quartz et de la technologie Spring Drive.'},
            {'name': 'Grand Seiko', 'country': 'Japon', 'year': 1960,
             'desc': 'Division haute horlogerie de Seiko, reconnue pour sa précision exceptionnelle.'},
            {'name': 'Cartier', 'country': 'France', 'year': 1847,
             'desc': 'Maison de joaillerie et horlogerie française, créatrice de montres iconiques.'},
            {'name': 'IWC Schaffhausen', 'country': 'Suisse', 'year': 1868,
             'desc': 'Manufacture horlogère suisse spécialisée dans les montres d\'aviation et de plongée.'},
            {'name': 'Breitling', 'country': 'Suisse', 'year': 1884,
             'desc': 'Manufacture suisse spécialisée dans les chronographes et montres d\'aviation.'},
            {'name': 'TAG Heuer', 'country': 'Suisse', 'year': 1860,
             'desc': 'Marque horlogère suisse de luxe, pionnière du chronographe sportif.'},
            {'name': 'Jaeger-LeCoultre', 'country': 'Suisse', 'year': 1833,
             'desc': 'Manufacture horlogère suisse de haute horlogerie, créatrice de la Reverso.'},
            {'name': 'Vacheron Constantin', 'country': 'Suisse', 'year': 1755,
             'desc': 'Plus ancienne manufacture horlogère en activité continue.'},
        ]
        
        self.stdout.write('Création des marques...')
        brands = []
        for data in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=data['name'],
                defaults={
                    'country': data['country'], 
                    'founded_year': data['year'],
                    'description': data['desc']
                }
            )
            brands.append(brand)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ {brand.name}'))
        
        # Complications horlogères
        complications_data = [
            {'name': 'Chronographe', 'desc': 'Fonction de chronométrage permettant de mesurer des intervalles de temps.'},
            {'name': 'Date', 'desc': 'Affichage de la date du jour, généralement par guichet.'},
            {'name': 'Phase de Lune', 'desc': 'Indication des phases lunaires sur un cadran dédié.'},
            {'name': 'GMT / Dual Time', 'desc': 'Affichage d\'un second fuseau horaire.'},
            {'name': 'Tourbillon', 'desc': 'Mécanisme de haute précision compensant les effets de la gravité.'},
            {'name': 'Répétition Minutes', 'desc': 'Sonnerie indiquant les heures, quarts et minutes à la demande.'},
            {'name': 'Calendrier Perpétuel', 'desc': 'Calendrier automatique tenant compte des années bissextiles.'},
            {'name': 'Réserve de Marche', 'desc': 'Indication de l\'autonomie restante du mouvement.'},
            {'name': 'Jour de la Semaine', 'desc': 'Affichage du jour de la semaine.'},
            {'name': 'Équation du Temps', 'desc': 'Indication de la différence entre temps solaire et temps civil.'},
        ]
        
        self.stdout.write('Création des complications...')
        complications = []
        for data in complications_data:
            comp, created = Complication.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['desc']}
            )
            complications.append(comp)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ {comp.name}'))
        
        # Noms de modèles réalistes
        model_prefixes = [
            'Submariner', 'Speedmaster', 'Royal Oak', 'Nautilus', 'Daytona',
            'Seamaster', 'Datejust', 'Aquanaut', 'Navitimer', 'Carrera',
            'Reverso', 'Patrimony', 'Overseas', 'Aqua Terra', 'Planet Ocean',
            'Chronomat', 'Avenger', 'Pilot', 'Portugieser', 'Ingenieur',
            'Santos', 'Tank', 'Ballon Bleu', 'Calibre', 'Pasha'
        ]
        
        model_suffixes = [
            'Professional', 'Classic', 'Chronograph', 'GMT', 'Diver',
            'Heritage', 'Limited Edition', 'Automatic', 'Perpetual', 'Master',
            'Ultra Thin', 'Moonphase', 'Tourbillon', 'Skeleton', 'Complications'
        ]
        
        self.stdout.write(f'\nGénération de {count} montres...')
        created_count = 0
        
        for i in range(count):
            try:
                brand = random.choice(brands)
                
                # Nom de modèle réaliste
                if random.random() < 0.7:  # 70% avec suffixe
                    model_name = f"{random.choice(model_prefixes)} {random.choice(model_suffixes)}"
                else:
                    model_name = random.choice(model_prefixes)
                
                # Référence unique
                ref = f"{fake.bothify(text='??-####-??').upper()}"
                
                # Prix cohérent selon le matériau
                material = random.choice(['STEEL', 'GOLD', 'TITANIUM', 'CERAMIC', 'PLATINUM', 'BRONZE'])
                
                if material == 'STEEL':
                    price = random.randint(3000, 15000)
                elif material == 'TITANIUM':
                    price = random.randint(8000, 25000)
                elif material == 'CERAMIC':
                    price = random.randint(10000, 30000)
                elif material == 'BRONZE':
                    price = random.randint(5000, 18000)
                elif material == 'GOLD':
                    price = random.randint(20000, 80000)
                else:  # PLATINUM
                    price = random.randint(40000, 120000)
                
                # Mouvement cohérent avec le prix
                if price > 50000:
                    movement = random.choice(['AUTO', 'MANUAL'])  # Luxe = mécanique
                elif price > 20000:
                    movement = random.choice(['AUTO', 'AUTO', 'MANUAL', 'QUARTZ'])
                else:
                    movement = random.choice(['AUTO', 'QUARTZ', 'SOLAR'])
                
                # Description réaliste
                descriptions = [
                    f"Garde-temps d'exception alliant tradition horlogère et innovation technique. "
                    f"Ce modèle incarne l'excellence de {brand.name} avec son mouvement {dict(Watch.MOVEMENT_CHOICES)[movement].lower()}.",
                    
                    f"Montre de prestige conçue pour les amateurs d'horlogerie fine. "
                    f"Boîtier en {dict(Watch.MATERIAL_CHOICES)[material].lower()} de {random.choice([36, 38, 40, 42, 44])} mm.",
                    
                    f"Création horlogère emblématique de la maison {brand.name}. "
                    f"Design intemporel et finitions exceptionnelles pour ce modèle {model_name}.",
                    
                    f"Instrument de précision développé selon les standards les plus exigeants. "
                    f"Étanche jusqu'à {random.choice([30, 50, 100, 200, 300])} mètres.",
                ]
                
                watch = Watch.objects.create(
                    model_name=model_name,
                    reference_number=ref,
                    price=price,
                    case_diameter=random.choice([36, 38, 39, 40, 41, 42, 43, 44, 45]),
                    movement_type=movement,
                    case_material=material,
                    water_resistance=random.choice([30, 50, 100, 200, 300, 500]),
                    description=random.choice(descriptions),
                    brand=brand,
                )
                
                # Ajouter 0-4 complications aléatoires
                num_complications = random.choices([0, 1, 2, 3, 4], weights=[20, 40, 25, 10, 5])[0]
                if num_complications > 0:
                    watch.complications.set(random.sample(complications, num_complications))
                
                created_count += 1
                
                if created_count % 10 == 0:
                    self.stdout.write(f'  {created_count}/{count} montres créées...')
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Erreur: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ {created_count} montres générées avec succès!'))
        self.stdout.write(self.style.SUCCESS(f'✓ {len(brands)} marques'))
        self.stdout.write(self.style.SUCCESS(f'✓ {len(complications)} complications'))
