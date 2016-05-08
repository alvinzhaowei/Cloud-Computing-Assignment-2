import json

inner_east="/Users/Sunjingjing/Desktop/poverty_rate/inner_east.csv"
inner_melbourne="/Users/Sunjingjing/Desktop/poverty_rate/inner_melbourne.csv"
inner_south= "/Users/Sunjingjing/Desktop/poverty_rate/inner_south.csv"
north_east="/Users/Sunjingjing/Desktop/poverty_rate/north_east.csv"
north_west="/Users/Sunjingjing/Desktop/poverty_rate/north_west.csv"
outer_east="/Users/Sunjingjing/Desktop/poverty_rate/outer_east.csv"
south_east="/Users/Sunjingjing/Desktop/poverty_rate/south_east.csv"
west="/Users/Sunjingjing/Desktop/poverty_rate/west.csv"
mornington_Peninsula="/Users/Sunjingjing/Desktop/poverty_rate/mornington_penunsula.csv"


def preprocess_file(filename):
    poverty_rate_list=[]
    f = open(filename, 'r')
    for line in f:
        number,suburb,poverty_rate,standardised_poverty_rate,feature_code,feature_name= line.split(',')
        if poverty_rate!='null' and poverty_rate!=' poverty_rate_synthetic_estimates':
            poverty_rate_list.append(poverty_rate)
    return poverty_rate_list

def average_poverty_rate(poverty_rate_list):
    sum=0
    for item in poverty_rate_list:
        sum+=float(item)
    return sum/len(poverty_rate_list)

poverty_dict={}

poverty_rate_inner_east=preprocess_file(inner_east)
ave_inner_east=average_poverty_rate(poverty_rate_inner_east)
poverty_dict.setdefault('inner_east',ave_inner_east)

poverty_rate_inner_melbourne=preprocess_file(inner_melbourne)
ave_inner_melbourne=average_poverty_rate(poverty_rate_inner_melbourne)
poverty_dict.setdefault('inner_melbourne',ave_inner_melbourne)

poverty_rate_inner_south=preprocess_file(inner_south)
ave_inner_south=average_poverty_rate(poverty_rate_inner_south)
poverty_dict.setdefault('inner_south',ave_inner_south)

poverty_rate_north_east=preprocess_file(north_east)
ave_north_east=average_poverty_rate(poverty_rate_north_east)
poverty_dict.setdefault('north_east',ave_north_east)

poverty_rate_north_west=preprocess_file(north_west)
ave_north_west=average_poverty_rate(poverty_rate_north_west)
poverty_dict.setdefault('north_west',ave_north_west)

poverty_rate_outer_east=preprocess_file(outer_east)
ave_outer_east=average_poverty_rate(poverty_rate_outer_east)
poverty_dict.setdefault('outer_east',ave_outer_east)

poverty_rate_south_east=preprocess_file(south_east)
ave_outer_south_east=average_poverty_rate(poverty_rate_south_east)
poverty_dict.setdefault('outer_south_east',ave_outer_south_east)

poverty_rate_west=preprocess_file(west)
ave_outer_west=average_poverty_rate(poverty_rate_west)
poverty_dict.setdefault('west',ave_outer_west)

poverty_rate_mornington_Peninsula=preprocess_file(mornington_Peninsula)
ave_outer_mornington_Peninsula=average_poverty_rate(poverty_rate_mornington_Peninsula)
poverty_dict.setdefault('mornington_Peninsula',ave_outer_mornington_Peninsula)

poverty_dict= sorted(poverty_dict.iteritems(), key=lambda d:d[1], reverse = True)
print poverty_dict