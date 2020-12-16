import pandas as pd
import folium
import json

#NYC COVID-19 cases data retrieved from live github
github_url = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/data-by-modzcta.csv'

dc = pd.read_csv(github_url)

dc['MODIFIED_ZCTA'].fillna(0, inplace=True)
dc['MODIFIED_ZCTA'] = dc['MODIFIED_ZCTA'].astype(int)

dc['COVID_CASE_COUNT'].fillna(0, inplace=True)
dc['COVID_CASE_COUNT'] = dc['COVID_CASE_COUNT'].astype(int)

impcols = [dc['MODIFIED_ZCTA'], dc['COVID_CASE_COUNT']]
headers = ['postal_code', 'counts']
dc_zip = pd.concat(impcols, axis=1, keys=headers)

dc_zip['postal_code'] = dc_zip['postal_code'].astype(str)

##bins = list(dc_zip['counts'].quantile([0, 0.15, 0.5, 0.6, 0.95, 1]))

nycMap = folium.Map(location=[40.693943, -73.985880], zoom_start=10)
mapLines = '/Users/Dr. Maryam Vulis/Desktop/zipMap.geojson.json'
                                                              
choropleth = folium.Choropleth(geo_data = mapLines,
                               data = dc_zip,
                               columns = ['postal_code', 'counts'],
                               key_on = 'feature.properties.postalCode',
                               fill_color = 'PuBuGn',
                               fill_opacity=0.7,
                               line_opacity=1.0,
                               highlight = True,
                               legend_name = 'COVID-19 Cases by Zip Code',
                               ##bins=bins
                               #threshold_scale = [0,0.1,0.75,0.9,0.98,1]
                               ).add_to(nycMap)

 
folium.LayerControl().add_to(nycMap)                       
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['PO_NAME'], 
    labels=False)
    )

nycMap.save(outfile='index.html')
