# 🕰️ Garde-Temps - Chrono-Collections

> Système complet de gestion de montres de luxe avec Django REST API + Frontend Vue.js

---

## 🚀 Démarrage Ultra-Rapide

### Option 1 : Script automatique (Windows)
```bash
start_all.bat
```

### Option 2 : Manuel

#### 1. Backend Django
```bash
python manage.py runserver
```

#### 2. Frontend Vue.js
```bash
cd frontend-vue
npm run dev
```

---

## 🌐 Accès aux Applications

- **Frontend Vue.js** : http://localhost:5173/ (ou 5174)
- **Admin Django** : http://localhost:8000/admin
  - Username: `admin`
  - Password: `admin123`
- **API REST** : http://localhost:8000/api/watches/

---

## 📋 Fonctionnalités

### 🎨 Frontend Vue.js (Moderne)

#### Design Premium
- ✅ Hero section avec animations spectaculaires
- ✅ Particules animées (30 particules flottantes)
- ✅ Menu hamburger élégant avec filtres
- ✅ Glassmorphism et effets visuels avancés
- ✅ Typographie premium (Cormorant Garamond + Montserrat)
- ✅ Palette or/rose ultra-luxe
- ✅ Responsive (mobile, tablette, desktop)

#### Fonctionnalités
- **Catalogue** : Grille élégante de montres avec pagination
- **Filtres** :
  - Pays de marque (Suisse, Japon, France)
  - Type de mouvement (Automatique, Manuel, Quartz, Solaire)
  - Diamètre maximum (pour petits poignets)
  - Recherche textuelle
  - Tri (prix, nom, date)
- **Page de détail** : Informations complètes avec animations
- **Statistiques** : Total montres, marques, prix moyen

### 🔧 Backend Django

#### Modèles de données
- **Brand** (Marque) : nom, pays, année de fondation, logo, description
- **Complication** : nom, description technique
- **Watch** (Montre) : 
  - Champs : model_name, reference_number, price, case_diameter, movement_type, case_material, water_resistance, description
  - Relations : 1-N avec Brand, N-N avec Complication
  - Génération automatique du numéro de série

#### Admin personnalisé
- **Export PDF** : Certificat d'authenticité élégant pour chaque montre
- **Graphiques Matplotlib** :
  - Camembert : Répartition des types de mouvements
  - Histogramme : Prix moyen par marque
- **Export JSON** : Export complet de la base de données
- **Filtres** : Par mouvement, matériau, marque
- **Recherche** : Par nom, référence, marque

#### API REST (Django REST Framework)
- **Endpoints** :
  - `/api/watches/` - Liste des montres (pagination 12/page)
  - `/api/watches/:id/` - Détail d'une montre
  - `/api/brands/` - Liste des marques
  - `/api/complications/` - Liste des complications
- **Filtres disponibles** :
  - `brand__country` : Filtrer par pays
  - `case_diameter__lte` : Diamètre maximum
  - `movement_type` : Type de mouvement
  - `case_material` : Matériau du boîtier
  - `price__gte` / `price__lte` : Fourchette de prix
- **Recherche** : Par nom, référence, marque
- **Tri** : Par prix, diamètre, date, nom

---

## 📊 Exemples d'utilisation de l'API

```bash
# Toutes les montres
http://localhost:8000/api/watches/

# Montres suisses uniquement
http://localhost:8000/api/watches/?brand__country=Suisse

# Montres automatiques de moins de 40mm
http://localhost:8000/api/watches/?movement_type=AUTO&case_diameter__lte=40

# Montres entre 5000€ et 20000€
http://localhost:8000/api/watches/?price__gte=5000&price__lte=20000

# Recherche "Omega"
http://localhost:8000/api/watches/?search=Omega

# Tri par prix décroissant
http://localhost:8000/api/watches/?ordering=-price
```

---

## 🛠️ Commandes Django utiles

```bash
# Générer plus de montres
python manage.py generate_watches 100 --clear

# Créer un nouveau superuser
python manage.py createsuperuser

# Shell Django
python manage.py shell

# Migrations
python manage.py makemigrations
python manage.py migrate
```

---

## 📁 Structure du projet

```
garde_temps/
├── start_all.bat               # Script de démarrage complet
├── .env                        # Variables d'environnement
├── .gitignore                  # Fichiers à ignorer
├── requirements.txt            # Dépendances Python
├── README.md                   # Ce fichier
├── db.sqlite3                  # Base de données SQLite
│
├── config/
│   ├── settings.py            # Configuration Django
│   ├── urls.py                # Routes API
│   └── ...
│
├── watches/
│   ├── models.py              # Brand, Watch, Complication
│   ├── admin.py               # Admin personnalisé (PDF, graphiques)
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # API ViewSets
│   ├── templates/             # Templates Django (legacy)
│   └── management/
│       └── commands/
│           └── generate_watches.py  # Script Faker
│
└── frontend-vue/              # Frontend Vue.js
    ├── src/
    │   ├── views/
    │   │   ├── Home.vue       # Page d'accueil
    │   │   └── WatchDetail.vue # Page de détail
    │   ├── services/
    │   │   └── api.js         # Service API
    │   ├── router/
    │   │   └── index.js       # Routes Vue
    │   ├── App.vue            # Composant principal
    │   └── main.js            # Point d'entrée
    ├── vite.config.js         # Configuration Vite
    └── package.json           # Dépendances npm
```

---

## 🔧 Technologies utilisées

### Backend
- **Django 6.0** - Framework web Python
- **Django REST Framework 3.16** - API REST
- **SQLite 3** - Base de données
- **ReportLab 4.2** - Génération PDF
- **Matplotlib 3.9** - Graphiques
- **Faker 33.4** - Données de test

### Frontend
- **Vue.js 3** - Framework JavaScript progressif
- **Vite** - Build tool ultra-rapide
- **Vue Router 4** - Navigation
- **Axios** - Client HTTP
- **CSS3** - Animations et glassmorphism

---

## 📝 Données de test

Le projet est livré avec **50 montres de luxe** déjà générées :
- 12 marques prestigieuses (Rolex, Omega, Patek Philippe, etc.)
- 10 complications horlogères
- Prix réalistes selon les matériaux
- Descriptions en français

### Compte administrateur
- **Username** : `admin`
- **Password** : `admin123`

---

## 🎉 Résultat

Vous avez un système complet de gestion de montres de luxe avec :

✅ **Frontend Vue.js moderne** avec design ultra-premium  
✅ **Backend Django professionnel** avec API REST  
✅ **Base de données SQLite** (simple et rapide)  
✅ **Admin Django** avec export PDF, graphiques, JSON  
✅ **50 montres de luxe** déjà générées  
✅ **Filtres avancés** et recherche  
✅ **Responsive design** mobile/tablette/desktop  

**Le projet est prêt à être utilisé immédiatement !** 🕰️✨

---

## 📝 Licence

Projet éducatif - 2026
