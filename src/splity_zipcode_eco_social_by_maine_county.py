import geopandas as gpd


def read_zipcode_geojson():
    import geopandas as gpd
    url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/me_maine_zip_codes_geo.min.json'
    gdf = gpd.read_file(url)
    gdf['ZCTA5CE10'] = gdf['ZCTA5CE10'].astype('int')
    gdf = gdf.sort_values(by=['ZCTA5CE10'])
    gdf = gdf.drop(index=[405])  # the data come from census don't have those
    gdf['zip code tabulation area'] = gdf['ZCTA5CE10']
    gdf.drop('ZCTA5CE10', axis=1)
    return gdf


def read_census_data(social, zipcode_start, zipcode_end):  # social=B19113_001E 4992 3901
    import pandas as pd
    import requests
    res = []
    # B19113_001E stands for "MEDIAN FAMILY INCOME IN THE PAST 12 MONTHS (IN 2020 INFLATION-ADJUSTED DOLLARS)"
    url = 'https://api.census.gov/data/2020/acs/acs5?get=NAME,' + \
        social+'&for=zip%20code%20tabulation%20area:*'
    response = requests.get(url)
    res = response.json()
    columns = res[0]
    df1 = pd.DataFrame(res[1:], columns=columns)
    df1['zip code tabulation area'] = df1['zip code tabulation area'].astype(
        int)
    df1[social] = df1[social].astype(int)
    df1 = df1.loc[df1['zip code tabulation area'] <= zipcode_end]
    df1 = df1.loc[df1['zip code tabulation area'] >= zipcode_start]
    return df1


def merge_census_and_geojson(sensus, geo_data):
    Maine_zipcode_level = geo_data.merge(
        sensus, on='zip code tabulation area', how='left')
    return Maine_zipcode_level


def read_county_boundary_geojson():
    Maine_County = gpd.read_file(
        'https://raw.githubusercontent.com/ds5010/broadband/main/src/county_boundaries/Maine_County_Boundary_Polygons_Dissolved_Feature.geojson')
    # drop two useless columns that we are not gonna use
    Maine_County = Maine_County.drop(columns=['created_date'])
    Maine_County = Maine_County.drop(columns=['last_edited_date'])
    return Maine_County


def set_zipcode_geojson_to_centroid(zipcdoe_gdf):
    zipcdoe_gdf['centroid_column'] = zipcdoe_gdf.centroid
    zipcdoe_gdf = zipcdoe_gdf.set_geometry('centroid_column')
    return zipcdoe_gdf


def build_county_boundary_dist(Maine_County):
    maine_county_dict = {}
    for i, row in Maine_County.iterrows():
        maine_county_dict[row['COUNTY']] = row.geometry
    return maine_county_dict


def store_zipfile_to_file_v2(county_name, maine_counties_dict, zipcdoe_gdf):
    gdf_list = []
    for index, i in zipcdoe_gdf.iterrows():
        if i.centroid_column.within(maine_counties_dict[county_name]):
            gdf_list.append(i)
    gdf = gpd.GeoDataFrame(gdf_list)
    del gdf['centroid_column']
    gdf.set_geometry('geometry')
    gdf.to_file('../county/'+county_name+'/'+county_name+socialType+'.geojson')


def get_social_value_for_zipcode_level_data_by_main_county(socialType):
    """This function return the geodata combine with  with maine zipcode data then divide it into county
    """
    Maine_County = read_county_boundary_geojson()
    maine_counties_dict = build_county_boundary_dist(Maine_County)
    gdf = read_zipcode_geojson()
    sensus = read_census_data(socialType, 3901, 4992)
    Maine_zipcode_level = merge_census_and_geojson(sensus, gdf)
    print(Maine_zipcode_level.columns)
    zipcdoe_gdf = set_zipcode_geojson_to_centroid(Maine_zipcode_level)
    for county_name in maine_counties_dict:
        store_zipfile_to_file_v2(county_name, maine_counties_dict, zipcdoe_gdf)


socialType = 'B19113_001E'
get_social_value_for_zipcode_level_data_by_main_county(socialType)
