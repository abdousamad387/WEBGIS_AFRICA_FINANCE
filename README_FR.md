# Observatoire Financier Africain -- Plateforme WebGIS

## Table des matieres

1. [Introduction](#1-introduction)
2. [Contexte](#2-contexte)
3. [Justification](#3-justification)
4. [Objectifs de l'etude](#4-objectifs-de-letude)
5. [Methodologie](#5-methodologie)
6. [Architecture technique](#6-architecture-technique)
7. [Description des donnees](#7-description-des-donnees)
8. [Fonctionnalites](#8-fonctionnalites)
9. [Resultats](#9-resultats)
10. [Discussion](#10-discussion)
11. [Limites et perspectives](#11-limites-et-perspectives)
12. [Conclusion](#12-conclusion)
13. [Installation et deploiement](#13-installation-et-deploiement)
14. [References](#14-references)

---

## 1. Introduction

Le WebGIS de l'Observatoire Financier Africain est une plateforme geospatiale interactive d'aide a la decision concue pour visualiser, analyser et explorer le paysage financier et macroeconomique du continent africain. Couvrant 54 pays sur une periode de 25 ans (2000--2024), la plateforme integre des donnees financieres multidimensionnelles avec des systemes d'information geographique pour produire un outil d'analyse spatiale complet.

Ce projet comble le fossee entre le reporting statistique traditionnel et la geovisualisation moderne, permettant aux decideurs politiques, chercheurs, analystes financiers et praticiens du developpement d'examiner les configurations spatiales, les dynamiques temporelles et les disparites entre pays dans le developpement financier africain. La plateforme fonctionne entierement dans un navigateur web, ne necessite aucun traitement cote serveur pour les utilisateurs finaux et est deployee comme site statique via GitHub Pages.

---

## 2. Contexte

L'Afrique subsaharienne et l'Afrique du Nord constituent un espace financier heterogene ou la penetration bancaire, la profondeur des marches de capitaux, l'adoption du mobile money et la stabilite macroeconomique varient enormement d'un pays a l'autre. Au cours des deux dernieres decennies, le continent a connu des transformations rapides : la revolution du mobile money nee en Afrique de l'Est, des ameliorations significatives de la reglementation bancaire en Afrique de l'Ouest, des defis de dette souveraine dans plusieurs economies et l'emergence d'ecosystemes fintech dans des pays comme le Nigeria, le Kenya, l'Afrique du Sud et l'Egypte.

Malgre ces evolutions, les outils analytiques disponibles pour le suivi des systemes financiers africains restent fragmentes. Les donnees des institutions internationales (Banque mondiale, FMI, Banque africaine de developpement) sont generalement presentees sous forme tabulaire ou via des tableaux de bord generiques depourvus de contexte spatial. Les systemes d'information geographique, largement utilises en sciences de l'environnement et en amenagement urbain, restent sous-exploites dans le domaine de l'analyse financiere sur le continent africain.

Ce projet repond au besoin d'une plateforme spatialement explicite, temporellement dynamique et analytiquement riche qui synthetise les multiples dimensions du developpement financier dans une interface interactive unique.

---

## 3. Justification

Le developpement de cette plateforme WebGIS se justifie par les considerations suivantes :

**Lacune analytique.** Les outils existants de suivi financier pour l'Afrique integrent rarement l'analyse geospatiale. Les donnees nationales sont generalement presentees dans des tableaux ou des graphiques statiques, qui masquent les configurations spatiales telles que le regroupement regional, les effets de voisinage et les corridors geographiques de developpement financier.

**Besoins d'aide a la decision.** Les organisations internationales, les banques centrales, les ministeres des finances et les agences de developpement necessitent des outils permettant une comparaison visuelle rapide entre pays et dans le temps. Un WebGIS repond a ce besoin en offrant la cartographie choroplethe interactive, l'animation temporelle et les requetes spatiales a la volee.

**Complexite de l'integration des donnees.** Les donnees financieres africaines couvrent plusieurs domaines (macroeconomie, secteur bancaire, fintech, microfinance) avec des sources, des unites et des couvertures differentes. Cette plateforme realise l'harmonisation necessaire, croisant 53 pays sur 6 jeux de donnees thematiques et 16 indicateurs fondamentaux.

**Accessibilite.** En deployant la plateforme comme site web statique, elle devient accessible a tout utilisateur disposant d'un navigateur web, sans installation de logiciel, connexion a une base de donnees ou formation SIG specialisee. L'interface bilingue (anglais et francais) etend encore l'accessibilite aux deux principales langues de travail de l'Union africaine.

**Reproductibilite.** L'ensemble du pipeline de donnees, du fichier Excel brut aux charges utiles GeoJSON et JSON, est implemente dans un seul script Python. Cela garantit que l'analyse peut etre reproduite, mise a jour et auditee.

---

## 4. Objectifs de l'etude

### 4.1 Objectif general

Concevoir et implementer une plateforme WebGIS de niveau professionnel pour l'analyse spatiale et la visualisation interactive des indicateurs financiers et macroeconomiques sur le continent africain pour la periode 2000--2024.

### 4.2 Objectifs specifiques

1. Construire une base de donnees geospatiale structuree reliant les indicateurs financiers au niveau national aux limites geographiques derivees des donnees Natural Earth.
2. Developper un pipeline de donnees automatise (ETL) qui extrait, transforme et charge des donnees financieres multidimensionnelles d'un classeur Excel structure dans des charges utiles JSON optimisees pour la cartographie web.
3. Implementer une application WebGIS riche en fonctionnalites supportant la cartographie thematique (choroplethe, cercles proportionnels, cartes de chaleur), l'animation temporelle, les requetes spatiales, l'exploration de tables attributaires et l'analytique statistique.
4. Permettre l'analyse comparative a travers des systemes de classement interactifs, des graphiques Top 10, des series temporelles continentales et des panneaux de detail par pays.
5. Deployer la plateforme comme site web statique publiquement accessible ne necessitant aucune infrastructure backend.
6. Fournir une interface bilingue (anglais et francais) pour repondre aux besoins linguistiques divers des parties prenantes africaines.

---

## 5. Methodologie

### 5.1 Collecte des donnees

La source de donnees principale est la **Base de donnees AfricaFinance 2000--2024**, un classeur Excel structure contenant six feuilles thematiques :

| Feuille | Domaine | Variables cles |
|---|---|---|
| Macroeconomie (Annuel) | Comptabilite nationale, commerce, demographie | PIB, PIB/habitant, taux de croissance, inflation, dette publique, IDE, chomage, IDH, balance courante, envois de fonds, reserves, taux directeur |
| Secteur Bancaire (Annuel) | Performance du systeme bancaire | Taux de bancarisation, ratio NPL, CAR, ROE, ROA, NIM, credit/PIB, spread de taux, nombre de banques, depots/PIB, agences et DAB pour 100k habitants |
| Fintech et Mobile Money | Services financiers numeriques | Comptes mobile money, volumes de transactions, couverture de la population, startups fintech, investissements fintech, part des paiements numeriques, penetration des smartphones |
| Microfinance et Inclusion | Inclusion financiere | PAR30, autosuffisance operationnelle, score d'inclusion financiere, clients actifs des IMF, nombre d'IMF, portefeuille de microcredit, part des clientes femmes |
| Profils Pays | Informations structurelles | Monnaie, nom de la banque centrale, bourse, population, coordonnees geographiques |
| Crises et Chocs | Perturbations financieres | Type de crise, indice de severite (1--5), impact sur le PIB, pays et annees concernes |

Les limites geographiques proviennent de **Natural Earth** (vecteurs culturels au 1:50 000 000), fournissant des geometries MultiPolygon a haute resolution pour l'ensemble des 55 entites africaines (54 Etats souverains plus Bir Tawil).

### 5.2 Pipeline de traitement des donnees

Le pipeline ETL est implemente dans `build_webgis.py` (Python 3, pandas, numpy, openpyxl) et realise les operations suivantes :

1. **Pretraitement GeoJSON.** Le GeoJSON brut de Natural Earth (2,6 Mo, environ 160 proprietes par entite) est reduit pour ne conserver que 16 proprietes essentielles (ISO_A3, NAME, ADMIN, REGION_WB, SUBREGION, POP_EST, GDP_MD, LABEL_X, LABEL_Y, etc.), reduisant la taille du fichier a environ 2,3 Mo.

2. **Ingestion Excel.** Six feuilles thematiques sont lues avec des dictionnaires de correspondance de colonnes explicites (MACRO_MAP, BANK_MAP, FINT_MAP, MFI_MAP) qui traduisent les en-tetes de colonnes en francais de la base de donnees originale en cles internes standardisees.

3. **Harmonisation des pays.** Un dictionnaire complet ISO3_MAP fait correspondre 53 noms de pays en francais aux codes ISO 3166-1 alpha-3, permettant des jointures fiables entre les donnees tabulaires et les entites geographiques.

4. **Construction de la matrice d'indicateurs.** Pour chaque annee (2000--2024) et chaque pays, le pipeline fusionne les donnees macroeconomiques, bancaires, fintech et de microfinance en un seul enregistrement contenant jusqu'a 40 variables.

5. **Calculs derives.** Les KPI continentaux (totaux, moyennes), les series temporelles par pays, les classements (top et bottom 10 pour 10 variables) et les agregations regionales sont calcules de maniere programmatique.

6. **Securite des types.** Un encodeur JSON personnalise (NpEncoder) gere les types de donnees numpy (int64, float64, bool_) pour assurer la compatibilite de serialisation.

7. **Sortie.** Deux fichiers sont produits : `africa.geojson` (couche geographique) et `indicators.json` (charge utile analytique contenant indicateurs, KPI, series temporelles, classements, profils pays et enregistrements de crises).

### 5.3 Conception cartographique

Le WebGIS suit les principes etablis de cartographie thematique :

- **Cartographie choroplethe** avec trois methodes de classification (quantile, intervalle egal, approximation des seuils naturels) et nombre de classes configurable (3 a 7). Les palettes de couleurs sont adaptees a la direction semantique de chaque indicateur : vert pour les indicateurs positifs (PIB/habitant, taux de bancarisation), rouge pour les indicateurs negatifs (NPL, inflation, dette), bleu pour les indicateurs neutres (credit/PIB, IDE), et une palette divergente pour les taux de croissance.
- **Cercles proportionnels** mis a l'echelle par la racine carree des valeurs de l'indicateur, positionnes aux coordonnees d'etiquettes des donnees Natural Earth.
- **Couche de carte de chaleur** utilisant l'estimation de densite par noyau pour reveler les concentrations spatiales.
- **Couche d'etiquettes** avec les noms de pays rendus en icones div HTML avec ombre de texte pour la lisibilite.
- **Couche des capitales** avec des marqueurs geolocalises provenant des donnees de profil pays.

### 5.4 Conception de l'interface

L'interface utilisateur adopte un theme sombre optimise pour le travail analytique, avec les principes de conception suivants :

- Effets de glassmorphisme pour les elements flottants (affichage de l'annee, info-bulles).
- Un panneau lateral gauche avec quatre onglets contextuels (Couches, Indicateurs, Analytique, Donnees).
- Un panneau de detail droit pour l'examen approfondi par pays.
- Des controles reactifs utilisant des curseurs, des menus de selection, des cases a cocher et des boutons d'action.
- Typographie basee sur Inter (texte d'interface) et JetBrains Mono (valeurs numeriques).

### 5.5 Pile technologique

| Composant | Technologie | Version |
|---|---|---|
| Cartographie de base | Leaflet.js | 1.9.4 |
| Outils de dessin | Leaflet.draw | 1.0.4 |
| Carte d'ensemble | Leaflet-minimap | 3.6.1 |
| Rendu de carte de chaleur | Leaflet.heat | 0.2.0 |
| Graphiques | Chart.js | 4.4.7 |
| Analyse spatiale | Turf.js | 7.x |
| Icones | Font Awesome | 6.5.1 |
| Pipeline de donnees | Python, pandas, numpy | 3.x |
| Deploiement | GitHub Pages | -- |

---

## 6. Architecture technique

```
WEBGIS_AFRICA_FINANCE/
  build_webgis.py          Pipeline ETL Python (traitement des donnees)
  index.html               Application WebGIS autonome
  server.py                Serveur de developpement local (port 9999)
  data/
    africa.geojson          Limites geographiques (55 entites, ~2,3 Mo)
    indicators.json         Charge utile des indicateurs financiers (~1,2 Mo)
```

L'application est entierement autonome dans un seul fichier HTML qui charge toutes les dependances depuis des CDN. Aucune etape de compilation, aucun gestionnaire de paquets et aucun code cote serveur n'est requis pour le deploiement. Les fichiers de donnees sont recuperes via des requetes HTTP GET standard a l'initialisation.

### Flux de donnees

```
Classeur Excel (6 feuilles, 15 000+ lignes)
        |
        v
  build_webgis.py (ETL pandas)
        |
        +---> africa.geojson (couche geographique)
        +---> indicators.json (charge utile analytique)
                    |
                    v
            index.html (Leaflet + Chart.js)
                    |
                    v
            Navigateur (WebGIS interactif)
```

---

## 7. Description des donnees

### 7.1 Couverture spatiale

- **54 Etats africains souverains** avec identification ISO 3166-1 alpha-3
- **5 sous-regions** : Afrique australe, Afrique centrale, Afrique du Nord, Afrique occidentale, Afrique orientale
- **Systeme de coordonnees de reference** : EPSG:4326 (WGS 84)
- **Type de geometrie** : MultiPolygon (Natural Earth 1:50m)

### 7.2 Couverture temporelle

- **Periode** : 2000--2024 (25 observations annuelles par pays)
- **Observations maximales** : 53 pays x 25 ans = 1 325 enregistrements pays-annee

### 7.3 Indicateurs thematiques (16 variables fondamentales)

| Indicateur | Unite | Direction | Description |
|---|---|---|---|
| PIB par habitant | USD | Plus eleve = mieux | Produit interieur brut divise par la population |
| Croissance du PIB | % | Plus eleve = mieux | Taux de croissance annuel du PIB reel |
| PIB | Milliards USD | Plus eleve = mieux | Produit interieur brut total |
| Inflation | % | Plus bas = mieux | Variation annuelle de l'indice des prix a la consommation |
| Dette publique / PIB | % | Plus bas = mieux | Dette publique en part du PIB |
| Taux de bancarisation | % | Plus eleve = mieux | Part de la population disposant d'un compte bancaire |
| Ratio NPL | % | Plus bas = mieux | Prets non performants en part du total des prets |
| Ratio d'adequation du capital | % | Plus eleve = mieux | Capital bancaire rapporte aux actifs ponderes par les risques |
| Rentabilite des fonds propres | % | Plus eleve = mieux | Mesure de rentabilite bancaire |
| Credit au PIB | % | Plus eleve = mieux | Credit interieur au secteur prive en part du PIB |
| Adoption du mobile money | % | Plus eleve = mieux | Part de la population disposant d'un compte mobile money |
| Score d'inclusion financiere | 0--10 | Plus eleve = mieux | Indice composite d'inclusion |
| IDE entrants | Milliards USD | Plus eleve = mieux | Investissements directs etrangers entrants |
| Chomage | % | Plus bas = mieux | Part de la population active sans emploi |
| PAR30 | % | Plus bas = mieux | Portefeuille a risque a plus de 30 jours (microfinance) |
| IDH | 0--1 | Plus eleve = mieux | Indice de developpement humain |

---

## 8. Fonctionnalites

### 8.1 Cartographie thematique

- Choroplethe interactif avec 16 indicateurs selectionnables
- Trois methodes de classification : quantile, intervalle egal, seuils naturels
- Nombre de classes configurable (3 a 7)
- Opacite de couche ajustable (0--100 %)
- Palettes de couleurs semantiques adaptees a la direction de l'indicateur
- Legende dynamique avec limites de classes et unites

### 8.2 Couches supplementaires

- Frontieres des pays (activation/desactivation)
- Etiquettes de noms de pays (positionnees aux coordonnees Natural Earth)
- Marqueurs des capitales avec info-bulles
- Cercles proportionnels (mise a l'echelle en racine carree par rapport aux valeurs de l'indicateur)
- Carte de chaleur (estimation de densite par noyau pour l'analyse des concentrations spatiales)

### 8.3 Fonds de carte

Quatre options de fond de carte : Sombre (CartoDB Dark Matter), OpenStreetMap, Clair (CartoDB Positron), Satellite (Esri World Imagery). Une minicarte d'ensemble est affichee dans le coin inferieur gauche.

### 8.4 Navigation temporelle

- Curseur d'annee (2000--2024)
- Navigation pas a pas (boutons precedent/suivant)
- Lecture animee avec progression automatique des annees
- Indicateur d'annee flottant sur la carte

### 8.5 Outils de mesure et de dessin

- Mesure de distance le long de polylignes (kilometres, via Turf.js)
- Mesure de surface de polygones (kilometres carres, via Turf.js)
- Outils de dessin libre : polygone, polyligne, marqueur ponctuel (Leaflet.draw)
- Calcul automatique de surface/distance pour les entites dessinees

### 8.6 Panneau analytique

- Grille d'indicateurs cles de performance (KPI) : PIB total, croissance moyenne, taux de bancarisation, NPL, inflation, IDE total, score d'inclusion, adoption du mobile money
- Graphique de series temporelles continentales (croissance, inflation, bancarisation sur 25 ans)
- Graphique en barres des Top 10 pays (mise a jour dynamique avec la selection d'indicateur et d'annee)
- Moteur de requete spatiale : filtrer les pays par valeur d'indicateur avec operateurs de comparaison (>, <, >=, <=)

### 8.7 Panneau de detail pays

- Nom du pays, region et annee selectionnee
- Huit indicateurs statistiques affiches dans une grille compacte
- Deux graphiques de series temporelles : (1) PIB et croissance, (2) bancarisation, mobile money et NPL
- Tableau de profil pays (monnaie, banque centrale, bourse, population)

### 8.8 Table attributaire

- Table modale affichant tous les pays et 12 indicateurs pour l'annee selectionnee
- Tri des colonnes (ascendant/descendant) par clic sur les en-tetes
- Fonctionnalite d'export CSV et GeoJSON

### 8.9 Recherche et classements

- Recherche de pays avec auto-completion et affichage de la region
- Clic pour zoomer et ouverture automatique du panneau de detail
- Classements pour 10 variables avec top 10 et bottom 10 pays

### 8.10 Internationalisation

- Support bilingue complet : anglais (par defaut) et francais
- Bouton de basculement de langue commutant l'ensemble des libelles de l'interface, noms d'indicateurs, etiquettes de graphiques et titres de sections
- Dictionnaire i18n avec plus de 40 elements d'interface traduits

---

## 9. Resultats

### 9.1 Sortie du pipeline de donnees

Le pipeline ETL traite avec succes :
- **55 entites geographiques** (54 pays + Bir Tawil) dans la couche GeoJSON (2 298 Ko)
- **1 325 enregistrements pays-annee** avec jusqu'a 40 variables chacun dans la charge utile d'indicateurs (1 190 Ko)
- **16 KPI continentaux** calcules pour l'annee de reference 2024
- **25 ans de series temporelles continentales** avec 9 variables agregees par annee
- **53 series temporelles individuelles par pays** avec 7 variables par pays
- **10 variables de classement** avec top 10 et bottom 10 pour chacune
- **53 profils pays** avec metadonnees institutionnelles et geographiques

### 9.2 Principaux constats (annee de reference 2024)

La cartographie choroplethe revele plusieurs configurations spatiales :

**PIB par habitant.** Un gradient Nord-Sud net est visible, avec les pays nord-africains (Libye, Algerie, Egypte, Tunisie) et les economies d'Afrique australe (Botswana, Afrique du Sud, Namibie) affichant un PIB par habitant plus eleve que la ceinture sahelienne (Niger, Tchad, Centrafrique, Burundi).

**Penetration bancaire.** Le taux de bancarisation montre un fort regroupement regional : l'Afrique du Nord et l'Afrique australe depassent 50 %, tandis que l'Afrique de l'Ouest et l'Afrique centrale restent en dessous de 30 % dans de nombreux pays, avec des exceptions notables (Ghana, Senegal, Cameroun).

**Adoption du mobile money.** L'Afrique de l'Est domine, avec le Kenya, la Tanzanie et l'Ouganda affichant des taux de penetration superieurs a 50 %. Cela confirme le corridor de mobile money bien documente s'etendant depuis la region du Rift.

**Inclusion financiere.** Le score composite d'inclusion revele un continent a plusieurs vitesses : les pays disposant d'ecosystemes fintech solides (Kenya, Ghana, Rwanda) obtiennent des scores significativement plus eleves que les economies dependantes des ressources avec une infrastructure financiere sous-developpee.

**Prets non performants.** Les ratios NPL eleves se concentrent dans les pays confrontes a l'instabilite politique ou aux chocs des prix des matieres premieres, avec des concentrations spatiales visibles en Afrique centrale et dans certaines parties de l'Afrique de l'Ouest.

### 9.3 Dynamiques temporelles

L'analyse des series temporelles continentales revele :
- Une tendance generale a la hausse de la penetration bancaire sur le continent de 2000 a 2024.
- L'adoption du mobile money montrant une croissance exponentielle a partir de 2010.
- La volatilite de la croissance du PIB correlee aux cycles mondiaux des matieres premieres et au choc du COVID-19 (2020).
- L'amelioration progressive des indicateurs de stabilite financiere (CAR, NPL) dans les pays mettant en oeuvre des reglementations alignees sur Bale.

---

## 10. Discussion

### 10.1 Configurations spatiales et disparites regionales

Le WebGIS revele que le developpement financier africain se caracterise par une forte heterogeneite spatiale. Plutot qu'une trajectoire continentale uniforme, les donnees montrent cinq profils regionaux distincts :

- **Afrique du Nord** : systemes bancaires matures, forte penetration bancaire, adoption limitee du mobile money, niveaux d'endettement moderes.
- **Afrique de l'Ouest** : croissance rapide de la fintech, amelioration des taux de bancarisation, defis persistants de NPL dans certaines economies, corridors de transferts de fonds importants.
- **Afrique de l'Est** : leadership mondial dans le mobile money, modeles innovants d'inclusion financiere, investissements fintech croissants.
- **Afrique centrale** : penetration bancaire plus faible, ratios NPL plus eleves, economies dependantes des ressources avec vulnerabilite aux chocs des matieres premieres.
- **Afrique australe** : systemes financiers diversifies (Afrique du Sud, Maurice), disparites intra-regionales significatives (Botswana vs. Lesotho).

### 10.2 Contributions methodologiques

Ce projet demontre la valeur de la technologie WebGIS pour l'analyse financiere, un domaine qui s'est traditionnellement appuye sur les tableaux et les graphiques statiques. La representation spatiale des indicateurs financiers ajoute une dimension analytique qui permet :

- L'identification visuelle des regroupements spatiaux et des valeurs aberrantes.
- L'exploration des effets de voisinage et des corridors financiers transfrontaliers.
- La comparaison temporelle rapide par la cartographie animee.
- L'analyse multi-indicateurs par la commutation et la superposition de couches.

### 10.3 Considerations techniques

Le choix d'une architecture entierement cote client (sans serveur backend) assure la simplicite de deploiement et elimine les couts d'infrastructure. Cependant, il impose des contraintes sur le volume de donnees : la charge utile actuelle (environ 3,5 Mo au total) est adaptee aux donnees annuelles au niveau national mais necessiterait une optimisation (tuiles vectorielles, rendu cote serveur) pour une granularite spatiale ou temporelle plus fine.

L'utilisation de la classification par quantiles comme methode par defaut assure une representation visuelle equilibree sur l'echelle de couleurs, ce qui est particulierement important pour les distributions asymetriques courantes dans les donnees financieres africaines (ou quelques grandes economies dominent les indicateurs agreges).

---

## 11. Limites et perspectives

### 11.1 Limites

- Les donnees pour certains pays et certaines annees peuvent etre incompletes ou estimees, refletant les lacunes dans les rapports des sources originales.
- La classification par seuils naturels utilise une approximation basee sur les quantiles plutot que l'algorithme complet d'optimisation de Jenks.
- L'analyse infranationale n'est pas supportee dans la version actuelle (les donnees sont agregees au niveau national).
- Le modele de deploiement statique limite la capacite d'integrer des sources de donnees en temps reel ou frequemment mises a jour.

### 11.2 Directions de developpement futures

- Integration de donnees financieres infranationales la ou elles sont disponibles (statistiques bancaires regionales, cartes de couverture mobile money).
- Ajout de modeles de prevision de series temporelles (ARIMA, Prophet) pour projeter les indicateurs cles.
- Implementation d'analyses d'autocorrelation spatiale (I de Moran, LISA) pour quantifier statistiquement les regroupements.
- Developpement d'un mode tableau de bord comparatif pour l'analyse cote a cote de pays.
- Connexion a des API de donnees en direct (Banque mondiale, FMI WEO) pour les mises a jour automatiques des donnees.

---

## 12. Conclusion

Le WebGIS de l'Observatoire Financier Africain represente une plateforme geospatiale complete pour comprendre le developpement financier sur le continent africain. En combinant 25 ans de donnees financieres multidimensionnelles avec des outils cartographiques interactifs, la plateforme permet des flux de travail analytiques qui n'etaient auparavant accessibles que par des logiciels SIG de bureau ou des environnements de recherche personnalises.

Le projet demontre que les technologies modernes de cartographie web (Leaflet, Chart.js, Turf.js) sont suffisamment matures pour supporter une analyse spatiale de niveau professionnel dans des contextes specifiques a un domaine. L'architecture entierement statique garantit que la plateforme reste accessible, peu couteuse a maintenir et facilement reproductible.

Avec 54 pays, 16 indicateurs fondamentaux, 25 ans de profondeur temporelle et un riche ensemble d'outils analytiques, ce WebGIS fournit une base solide pour l'analyse factuelle des systemes financiers africains.

---

## 13. Installation et deploiement

### Prerequis

- Python 3.8+ avec pandas, numpy et openpyxl
- Un navigateur web moderne (Chrome, Firefox, Edge, Safari)

### Developpement local

```bash
# Cloner le depot
git clone https://github.com/abdousamad387/WEBGIS_AFRICA_FINANCE.git
cd WEBGIS_AFRICA_FINANCE

# (Optionnel) Reconstruire les donnees depuis la source Excel
python build_webgis.py

# Demarrer le serveur local
python server.py
# S'ouvre automatiquement a http://localhost:9999
```

### Deploiement

L'application est deployee via GitHub Pages a :
**https://abdousamad387.github.io/WEBGIS_AFRICA_FINANCE/**

Aucune etape de compilation ou configuration serveur n'est requise. Le fichier `index.html` et le repertoire `data/` sont servis directement comme fichiers statiques.

---

## 14. References

- Natural Earth. "Admin 0 -- Countries." Version 5.x. https://www.naturalearthdata.com/
- Banque mondiale. "World Development Indicators." https://databank.worldbank.org/
- Fonds monetaire international. "World Economic Outlook Database." https://www.imf.org/
- Banque africaine de developpement. "African Economic Outlook." https://www.afdb.org/
- GSMA. "State of the Industry Report on Mobile Money." https://www.gsma.com/
- Leaflet. "An open-source JavaScript library for interactive maps." https://leafletjs.com/
- Turf.js. "Advanced geospatial analysis for browsers and Node.js." https://turfjs.org/
- Chart.js. "Simple yet flexible JavaScript charting." https://www.chartjs.org/

---

**Auteur** : Abdou Samad

**Licence** : MIT

**Demo en ligne** : https://abdousamad387.github.io/WEBGIS_AFRICA_FINANCE/
