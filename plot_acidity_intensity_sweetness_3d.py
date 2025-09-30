import pandas as pd
import plotly.express as px

# Load the Excel file
df = pd.read_excel('data/all_wines.xlsx')

# ...existing code...

# Filter by country = 'Portugal'
df_portugal = df[(df['country_name'] == 'Portugal')]

# Map wine_type_id to names
wine_type_map = {
    1: 'Red',
    2: 'White',
    3: 'Sparkling',
    4: 'Rosé',
    7: 'Dessert',
    24: 'Fortified'
}
df_portugal['wine_type'] = df_portugal['wine_type_id'].map(wine_type_map)

# Filter for only red and white wines and specific regions
allowed_types = ['Red', 'White']
allowed_regions = ['Douro', 'Alentejo', 'Lisboa', 'Dão']
df_filtered = df_portugal[
    (df_portugal['wine_type'].isin(allowed_types)) &
    (df_portugal['region_name'].isin(allowed_regions))
]

# Create interactive 3D scatter plot
fig = px.scatter_3d(
    df_filtered,
    x='acidity',
    y='intensity',
    z='sweetness',
    color='region_name',
    title='Acidity vs Intensity vs Sweetness (Colored by Region)',
    labels={
        'acidity': 'Acidity',
        'intensity': 'Intensity',
        'sweetness': 'Sweetness',
        'region_name': 'Region'
    }
)
# ...existing code...
fig.update_traces(marker=dict(size=3))
fig.show()
