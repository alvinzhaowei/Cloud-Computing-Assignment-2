import json

inner_east="/Users/Sunjingjing/Desktop/teenage_rate/inner_east.csv"
inner_melbourne="/Users/Sunjingjing/Desktop/teenage_rate/inner_melbourne.csv"
inner_south= "/Users/Sunjingjing/Desktop/teenage_rate/inner_south.csv"
north_east="/Users/Sunjingjing/Desktop/teenage_rate/north_east.csv"
north_west="/Users/Sunjingjing/Desktop/teenage_rate/north_west.csv"
outer_east="/Users/Sunjingjing/Desktop/teenage_rate/outer_east.csv"
south_east="/Users/Sunjingjing/Desktop/teenage_rate/south_east.csv"
west="/Users/Sunjingjing/Desktop/teenage_rate/west.csv"
mornington_Peninsula="/Users/Sunjingjing/Desktop/teenage_rate/west.csv"


def preprocess_file(filename):
    teenager_rate_list=[]
    f = open(filename, 'r')
    for line in f:
        level_code,level_name,teenager_rate,teenager_count,feature_code,feature_name= line.split(',')
        if teenager_rate!='0' and teenager_rate!=' x15_19_p_3_percent_6_13_6_13' and teenager_rate!='null':
           teenager_rate_list.append(teenager_rate)
    return teenager_rate_list

def preprocess_file2(filename):
    teenager_rate_list=[]
    f = open(filename, 'r')
    for line in f:
        level_code,level_name,teenager_count,teenager_rate,feature_code,feature_name= line.split(',')
        if teenager_rate!='0' and teenager_rate!=' x15_19_p_3_percent_6_13_6_13'and teenager_rate!='null':
           teenager_rate_list.append(teenager_rate)
    return teenager_rate_list

def average_teenager_rate(teenager_rate_list):
    sum=0
    for item in teenager_rate_list:
        sum+=float(item)
    return sum/len(teenager_rate_list)

teenager_dict={}

teenager_rate_inner_east=preprocess_file(inner_east)
ave_inner_east=average_teenager_rate(teenager_rate_inner_east)
teenager_dict.setdefault('inner_east',ave_inner_east)

teenager_rate_inner_melbourne=preprocess_file(inner_melbourne)
ave_inner_melbourne=average_teenager_rate(teenager_rate_inner_melbourne)
teenager_dict.setdefault('inner_melbourne',ave_inner_melbourne)

teenager_rate_inner_south=preprocess_file(inner_south)
ave_inner_south=average_teenager_rate(teenager_rate_inner_south)
teenager_dict.setdefault('inner_south',ave_inner_south)

teenager_rate_north_east=preprocess_file2(north_east)
ave_north_east=average_teenager_rate(teenager_rate_north_east)
teenager_dict.setdefault('north_east',ave_north_east)

teenager_rate_north_west=preprocess_file(north_west)
ave_north_west=average_teenager_rate(teenager_rate_north_west)
teenager_dict.setdefault('north_west',ave_north_west)

teenager_rate_outer_east=preprocess_file(outer_east)
ave_outer_east=average_teenager_rate(teenager_rate_outer_east)
teenager_dict.setdefault('outer_east',ave_outer_east)

teenager_rate_south_east=preprocess_file(south_east)
ave_outer_south_east=average_teenager_rate(teenager_rate_south_east)
teenager_dict.setdefault('outer_south_east',ave_outer_south_east)

teenager_rate_west=preprocess_file(west)
ave_outer_west=average_teenager_rate(teenager_rate_west)
teenager_dict.setdefault('west',ave_outer_west)

teenager_rate_mornington_Peninsula=preprocess_file(mornington_Peninsula)
ave_outer_mornington_Peninsula=average_teenager_rate(teenager_rate_mornington_Peninsula)
teenager_dict.setdefault('mornington_Peninsula',ave_outer_mornington_Peninsula)

teenager_dict= sorted(teenager_dict.iteritems(), key=lambda d:d[1], reverse = True)
print teenager_dict