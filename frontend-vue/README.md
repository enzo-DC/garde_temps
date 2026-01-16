# 🕰️ Garde-Temps - Frontend Vue.js

Frontend moderne en Vue.js 3 + Vite pour le système de gestion de montres de luxe.

## 🚀 Démarrage Rapide

### 1. Installation des dépendances
```bash
cd frontend-vue
npm install
```

### 2. Lancer le serveur de développement
```bash
npm run dev
```

L'application sera accessible sur **http://localhost:5174/** (ou un autre port si 5173/5174 sont occupés)

### 3. Build pour la production
```bash
npm run build
```

Les fichiers statiques seront générés dans le dossier `dist/`

---

## 📋 Prérequis

- **Node.js** 16+ installé
- **Backend Django** en cours d'exécution sur http://localhost:8000

---

## 🎨 Fonctionnalités

### ✨ Page d'accueil
- Hero section avec animations
- Particules animées en arrière-plan
- Menu hamburger avec filtres
- Catalogue de montres avec pagination
- Statistiques (total montres, marques, prix moyen)
- Design premium dark/gold

### 💎 Page de détail
- Affichage complet des spécifications
- Animations au chargement
- Design 2 colonnes responsive
- Retour au catalogue

### 🔧 Filtres
- Pays de marque
- Type de mouvement
- Diamètre maximum
- Recherche textuelle
- Tri (prix, nom, date)

---

## 📁 Structure du Projet

```
frontend-vue/
├── src/
│   ├── views/
│   │   ├── Home.vue          # Page d'accueil
│   │   └── WatchDetail.vue   # Page de détail
│   ├── services/
│   │   └── api.js            # Service API
│   ├── router/
│   │   └── index.js          # Configuration des routes
│   ├── App.vue               # Composant principal
│   └── main.js               # Point d'entrée
├── vite.config.js            # Configuration Vite
└── package.json              # Dépendances
```

---

## 🔌 API

Le frontend consomme l'API Django REST sur `http://localhost:8000/api/`

### Endpoints utilisés :
- `GET /api/watches/` - Liste des montres (avec filtres et pagination)
- `GET /api/watches/:id/` - Détail d'une montre
- `GET /api/brands/` - Liste des marques
- `GET /api/complications/` - Liste des complications

---

## 🛠️ Technologies

- **Vue.js 3** - Framework JavaScript progressif
- **Vite** - Build tool ultra-rapide
- **Vue Router 4** - Navigation
- **Axios** - Client HTTP
- **CSS3** - Animations et glassmorphism

---

## 🎯 Build de Production

### 1. Générer les fichiers statiques
```bash
npm run build
```

### 2. Prévisualiser le build
```bash
npm run preview
```

### 3. Déployer
Les fichiers dans `dist/` peuvent être déployés sur :
- Netlify
- Vercel
- GitHub Pages
- Tout serveur web statique

---

## 🔧 Configuration

### Changer l'URL de l'API

Modifiez `src/services/api.js` :
```javascript
const API_BASE_URL = 'https://votre-api.com/api'
```

### Changer le port de développement

Modifiez `vite.config.js` :
```javascript
server: {
  port: 3000  // Votre port
}
```

---

## 🐛 Dépannage

### Le frontend ne charge pas les données
1. Vérifiez que Django tourne sur http://localhost:8000
2. Testez l'API directement : http://localhost:8000/api/watches/
3. Vérifiez la console du navigateur (F12) pour les erreurs CORS

### Erreur CORS
Assurez-vous que `django-cors-headers` est configuré dans Django :
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
]
```

---

## 📝 Commandes Disponibles

```bash
npm run dev      # Lancer le serveur de développement
npm run build    # Build pour la production
npm run preview  # Prévisualiser le build de production
```

---

**Profitez de votre catalogue de montres de luxe en Vue.js !** 🕰️✨
