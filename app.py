import csv
import io
import pandas as pd
import plotly.express as px
import urllib.request

# ==========================================
# 1. CHARGEMENT DES DONNÉES DEPUIS L'URL (SANS REQUESTS)
# ==========================================
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv'

# Chargement pour Pandas directement depuis l'URL
données = pd.read_csv(url)

# Calcul de la colonne Chiffre d'Affaires (CA)
données['ca'] = données['prix'] * données['qte']

# ==========================================
# 2. ANALYSE STATISTIQUE AVEC PANDAS
# ==========================================
print('--- 1. STATISTIQUES PAR PRODUIT (PANDAS) ---')
stats_par_produit = données.groupby('produit').agg(
    ca_moyenne=('ca', 'mean'),
    ca_mediane=('ca', 'median'),
    qte_moyenne=('qte', 'mean'),
    qte_mediane=('qte', 'median'),
    qte_ecart_type=('qte', 'std'),
    qte_variance=('qte', 'var'),
)
print(stats_par_produit)
print('\n' + '=' * 50 + '\n')

# ==========================================
# 3. PRODUIT LE PLUS / MOINS VENDU (PYTHON NATIF)
# ==========================================
print('--- 2. PRODUITS LE PLUS ET MOINS VENDUS (PYTHON NATIF) ---')
ventes_par_produit_natif = {}

# Téléchargement natif avec urllib (sans dépendance externe)
with urllib.request.urlopen(url) as reponse:
  contenu_texte = reponse.read().decode('utf-8')

# Lecture native du CSV
contenu_ficher = io.StringIO(contenu_texte)
lecteur = csv.DictReader(contenu_ficher)

for ligne in lecteur:
  prod = ligne['produit']
  quantite = int(ligne['qte'])
  ventes_par_produit_natif[prod] = (
      ventes_par_produit_natif.get(prod, 0) + quantite
  )

produit_plus_vendu = max(
    ventes_par_produit_natif, key=ventes_par_produit_natif.get
)
produit_moins_vendu = min(
    ventes_par_produit_natif, key=ventes_par_produit_natif.get
)

print(
    f'Produit le plus vendu : {produit_plus_vendu} avec'
    f' {ventes_par_produit_natif[produit_plus_vendu]} unités.'
)
print(
    f'Produit le moins vendu : {produit_moins_vendu} avec'
    f' {ventes_par_produit_natif[produit_moins_vendu]} unités.'
)
print('\n' + '=' * 50 + '\n')

# ==========================================
# 4. GÉNÉRATION des GRAPHIQUES PLOTLY
# ==========================================
print('--- 3. GÉNÉRATION DES GRAPHIQUES HTML ---')

# a. Graphique 1 : Quantité vendue par région (Camembert)
fig_region = px.pie(
    données, values='qte', names='region', title='Quantité vendue par région'
)
fig_region.write_html('ventes-par-region.html')
print("-> Fichier 'ventes-par-region.html' généré.")

# Agrégrations globales par produit pour les graphiques suivants
df_produits = (
    données.groupby('produit')
    .agg({'qte': 'sum', 'ca': 'sum'})
    .reset_index()
)

# b. Graphique 2 : Ventes par produit (Barres)
fig_ventes = px.bar(
    df_produits,
    x='produit',
    y='qte',
    title='Quantité totale vendue par produit',
    labels={'produit': 'Produit', 'qte': 'Quantité totale'},
    color='produit',
)
fig_ventes.write_html('ventes-par-produit.html')
print("-> Fichier 'ventes-par-produit.html' généré.")

# c. Graphique 3 : Chiffre d'affaires par produit (Barres)
fig_ca = px.bar(
    df_produits,
    x='produit',
    y='ca',
    title="Chiffre d'affaires total par produit (€)",
    labels={'produit': 'Produit', 'ca': "Chiffre d'affaires (€)"},
    color='produit',
)
fig_ca.write_html('ca-par-produit.html')
print("-> Fichier 'ca-par-produit.html' généré.")