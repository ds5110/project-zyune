import pandas as pd
import geopandas as gpd

B16010_041E = gpd.read_file(
    '../county/Cumberland/CumberlandB16010_041E.geojson')
B19019_001E = gpd.read_file(
    '../county/Cumberland/CumberlandB19019_001E.geojson')
B28003_004E = gpd.read_file(
    '../county/Cumberland/CumberlandB28003_004E.geojson')
B01001_001E = gpd.read_file(
    '../county/Cumberland/CumberlandB01001_001E.geojson')
df = pd.DataFrame()
df['ZCTA5CE10'] = B01001_001E['ZCTA5CE10']
df['total_population'] = B01001_001E['B01001_001E']
df['num_of_bachelor_degree_higer'] = B16010_041E['B16010_041E']
df['num_of_internet_subscribe'] = B28003_004E['B28003_004E']
df['median_household_income'] = B19019_001E['B19019_001E']


def find_number_of_tiers_according_to_zipcode(county_name, zipcode, tier_num):
    try:
        directory = '../Zipcode/'+county_name+'_zip/'+tier_num+'/'+zipcode+'.geojson'
        print(directory)
        gdf = gpd.read_file(directory)
        return len(gdf)
    except:
        return 0


find_number_of_tiers_according_to_zipcode('Cumberland', '04101', 'tier_4')
tier_list = ['tier_0', 'tier_1', 'tier_2', 'tier_3', 'tier_4', 'tier_5']
for tiers in tier_list:
    tier_list = []
    for zipcode in df['ZCTA5CE10']:

        tier_list.append(find_number_of_tiers_according_to_zipcode(
            'Cumberland', '0'+str(zipcode), tiers))
    new_column_name = 'num_'+tiers
    df[new_column_name] = pd.DataFrame(tier_list)
df.to_csv('../Zipcode/number_of_tiers_cumberlamd_zipcode.csv', index=False)
