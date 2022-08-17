import geopandas as gpd
import pandas as pd
tierNumber = 'tier_4'
countyname = 'Cumberland'
B16010_041E = gpd.read_file(
    '../county/'+countyname+'/'+countyname+'B16010_041E.geojson')
tier = gpd.read_file('../county/'+countyname+'/' +
                     countyname+'_'+tierNumber+'.geojson')


def set_zipcode_geojson_to_centroid(zipcdoe_gdf):
    zipcdoe_gdf['centroid_column'] = zipcdoe_gdf.centroid
    zipcdoe_gdf = zipcdoe_gdf.set_geometry('centroid_column')
    return zipcdoe_gdf


def build_zipcode_boundary_dict(Maine_County):
    zipcode_dict = {}
    for i, row in Maine_County.iterrows():
        zipcode_dict[row['ZCTA5CE10']] = row.geometry
    return zipcode_dict


zipcode_dict = build_zipcode_boundary_dict(B16010_041E)

tier = set_zipcode_geojson_to_centroid(tier)


def divide_county_by_zipcode(countyname, zipcode):
    gdf_list = []
    for index, i in tier.iterrows():
        if i.centroid_column.within(zipcode_dict[zipcode]):
            gdf_list.append(i)
    if gdf_list:
        gdf = gpd.GeoDataFrame(gdf_list)
        gdf = gdf.drop(columns=['centroid_column'])
#         print(gdf.head())
        gdf.set_geometry('geometry')
        gdf.to_file('../Zipcode/'+countyname+'_zip/' +
                    tierNumber+'/0'+str(zipcode)+'.geojson')
    else:
        df = pd.DataFrame(gdf_list)
        df.to_csv('../Zipcode/'+countyname+'_zip/' +
                  tierNumber+'/0'+str(zipcode)+'.csv')


zipcode_name = zipcode_dict.keys()
for i in zipcode_name:
    print(i)
    divide_county_by_zipcode(countyname, i)
