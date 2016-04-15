import random
import sys
import math
from xlrd import open_workbook
import operator
from haversine import haversine

FACT = "factory"
LONG = "Longitute"
LAT = "Latitud"
OCC = 'occurence'
CITY = "City"
COUNTRY = "Country"
FACT_LIST = []
FIX_NAMES = [CITY,COUNTRY,FACT,LONG,LAT]
used_Factory_List = []

def readcsv(path,sheet_index):
    """
    Used to read a csv file
    input:
        path - path to the file in the machine
        sheet_index = sheet no in a excel file
    Output:
        List of Dictionary of each row in excel  
    """
    book = open_workbook(path)
    sheet = book.sheet_by_index(sheet_index)

    # read header values into the list    
    keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

    dict_list = []
    for row_index in range(1, sheet.nrows):
        d = {keys[col_index]: sheet.cell(row_index, col_index).value 
             for col_index in range(sheet.ncols)}
        dict_list.append(d)

    return dict_list

def dist(p1,p2):
    """
    calculate the distance, move to a funtion
    """
    _p1 = (float(p1[LONG]),float(p1[LAT]))
    _p2 = (float(p2[LONG]),float(p2[LAT]))
    return haversine(_p1, _p2)

def city_factory_distance(city,factory_dict):
    """
    returns dictionary of
    factory and distance from the city for a given city
    and list of all factories
    """
    d = {}
    for factory in factory_dict:
        d[factory[CITY]] = dist(city,factory)
    return d        

def sort_dic(d,n):
    """
    Sorts the dictionary in ascending order by value and returns
    list of the top n iems as tuples
    """
    #
    #lisKey = list(set(d.keys()) - set(FIX_NAMES))
    #d = {k:d[k] for k in d if k in lisKey}
    count = 1
    dic = sorted(d.items(), key=operator.itemgetter(1))
    lisDic = []
    for k in dic:
        lisDic.append(k)
        if(count>n-1):
            break
        count+=1
    return lisDic

def getunusedFactory(factories):
    lst = [fact[CITY] for fact in factories]
    lst = [elem for elem in lst if elem not in used_Factory_List]
    return lst

def main(cities,factory):
    """
    This following code takes list of city, and
    a) adds a keys for each factory and its distance from the city to each city
    b) sorts the city in ascending order of distance of factory
    c) populates used_Factory_List
    d) returns closest two factories for two cities
    
    """
    for city in cities:
        city_factory_dist = city_factory_distance(city,factory)
        city.update(city_factory_dist)
        near_fac = sort_dic(city_factory_dist,2)
        #factory city names stored
        [used_Factory_List.append(tup[0]) for tup in near_fac]     
        city[FACT] = near_fac
    unused_fact = getunusedFactory(factory)

    #calculating city for factories which have not been used yet
    #curr-city will find the closest city for this factory
    for f in factories:
        name = f[CITY]
        if name in unused_fact and unused_fact:
            prev,curr = 0,0
            prev_city,curr_city = None,None
            for city in cities:
                curr,prev = city[name],curr
                prev_city,curr_city = curr_city,city
                if prev < curr and prev:
                    curr = prev
                    curr_city = prev_city

            count = 0
            #checking if curr_city is closer to this factory than previous factory as story in city dictionary as FACT key
            for key in curr_city[FACT]:
                curr_city[FACT] = [key,(name,dist(f,curr_city))]
                used_Factory_List.append(name)
                break
                
cities = readcsv('FINALDATA.xlsx',1)
factories = readcsv('FINALDATA.xlsx',0)
main(cities,factories)
print({city[CITY]:city[FACT] for city in cities})
getunusedFactory(factories)
