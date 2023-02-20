from movie_detail import get_detail_data 

with open('./html/7号房的礼物.html', 'r') as f:
    print(get_detail_data(f.read()))



