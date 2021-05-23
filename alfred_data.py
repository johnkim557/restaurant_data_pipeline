

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.9254,-74.2765&radius=1500&type=restaurant&key=' + api


#####################################################################################################

link['results'][1]

name = link['results'][0]['name']
business_status = link['results'][0]['business_status']
place_id = link['results'][0]['place_id']
price_level = link['results'][0]['price_level']
rating = link['results'][0]['rating']
address = link['results'][0]['vicinity']
ratings_total = link['results'][0]['user_ratings_total']

#####################################################################################################

seconds = 1
minutes = 60*seconds
degrees = 60*minutes


first_coord_center = 41*degrees + 27*minutes + 29*seconds
first_coord_center



first_long_coord = 75*degrees + 51*minutes + 34*seconds
first_long_coord #in seconds

#discover latitude coordinates N/S 
coord_list = []
for i in range(135): #range vertically goes from 0 to 9312
    for j in range(85): #the range would go from 0 to 5794
        next_coord_center = first_coord_center - i*70.7*seconds
    
        total_coord_hours = int(next_coord_center/3600)
    
        remaining_seconds = next_coord_center%3600
    
        total_coord_min = int(remaining_seconds/60)
    
        total_coord_seconds = remaining_seconds%60
   
        lat_coord = str(total_coord_hours)+'-'+str(total_coord_min)+"-"+ str(total_coord_seconds)+'N'
            
        #Discover Longitude Coordinates E/W
        next_coord_center = first_long_coord - j*88.375*seconds
    
        total_coord_hours = int(next_coord_center/3600)
    
        remaining_seconds = next_coord_center%3600
    
        total_coord_min = int(remaining_seconds/60)
    
        total_coord_seconds = remaining_seconds%60
           #coordinates in degree,min,second format
        long_coord = str(total_coord_hours)+'-'+str(total_coord_min)+"-"+ str(total_coord_seconds)+'W'
        latitude=lat_coord
        longitude=long_coord
        latitude = sum(float(x) / 60 ** n for n, x in enumerate(latitude[:-1].split('-')))  * (1 if 'N' in latitude[-1] else -1)
        longitude = sum(float(x) / 60 ** n for n, x in enumerate(longitude[:-1].split('-'))) * (1 if 'E' in longitude[-1] else -1)
        
        
        coord_dict = {"lat_coord":latitude,
                        "long_coord":longitude}
                        
        coord_list.append(coord_dict)




#####################################################################################################

#Create a duplicate of the data as csv by turning data into pandas dataframe

#possibly use multithreading for this portion
import time
import requests
hit = 0
empty = 0
# starting time
start = time.time()

restaurant_data = []

   #order of information dict_keys(['business_status', 'geometry', 
    #'icon', 'name', 'opening_hours', 'photos', 'place_id', 'plus_code', 
    #'price_level', 'rating', 'reference', 'scope', 'types', 'user_ratings_total', 'vicinity'])
for i in range(6000): 
   
    lat = coord_list[i]['lat_coord']
   
    long = coord_list[i]['long_coord']
    
    
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(lat)+','+str(long)+'&radius=1500&type=restaurant&key='+api

   #order of information dict_keys(['business_status', 'geometry', 
    #'icon', 'name', 'opening_hours', 'photos', 'place_id', 'plus_code', 
    #'price_level', 'rating', 'reference', 'scope', 'types', 'user_ratings_total', 'vicinity'])
   
  
   
    response = requests.get(url)
    link = response.json()
    if link['results'] !=[]:
        hit = hit +1

        for j in range(len(link['results'])):
            
            restaurant_dict = {}
            for word in link['results'][j].keys():
                
               #Problem some establishments do not have certain categories of information
                if word == 'business_status':
                    restaurant_dict['business_status'] = link['results'][j]['business_status']
                elif word == 'name':
                    restaurant_dict['name'] = link['results'][j]['name']
                elif word == 'place_id':
                    place_id = link['results'][j]['place_id']
                    restaurant_dict['place_id'] = link['results'][j]['place_id']
                elif word == 'price_level':
                                        #may not exist
                    restaurant_dict['price_level'] = link['results'][j]['price_level']
            
            #may not exist
                elif word == 'rating':
                    restaurant_dict['rating'] = link['results'][j]['rating']
                
            #may not exist
                elif word == 'user_ratings_total':
                    restaurant_dict['user_ratings_total'] = link['results'][j]['user_ratings_total']
            
            restaurant_data.append(restaurant_dict)
    else:
        empty = empty + 1

end = time.time()        
print(f"Runtime of the program is {end - start}")       
        
print(hit)
print(empty)

df = pd.DataFrame(restaurant_data)
df.to_csv('/Volumes/Flashdrive/restaurant_data_7000.csv')