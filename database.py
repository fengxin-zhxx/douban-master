import pymysql


db = pymysql.connect(host='localhost',
                     user='root',
                     password='root',
                     database='douban')

cursor = db.cursor()


def db_store(movie_data):
    name1, name2, score, comment, quote_str, page_url, director, actor, place, lang, year, length = movie_data
    
    # 插入movie表
    sql = 'insert into movie(name, global_name, score, comment, quote, url, year, length) values("%s", "%s", %s, %s, "%s", "%s", %s, %s)' % (
        name1, name2, score, comment, quote_str, page_url, year, length)
    
    cursor.execute(sql)
    
    sql = 'select last_insert_id()'
    cursor.execute(sql)
    movie_id = cursor.fetchone()[0]
    
    # director表
    for i in director:
        sql = 'select id from director where name="%s"' % i
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) == 0:
            sql = 'insert into director(name) values ("%s")' % i
            cursor.execute(sql)
            sql = 'select last_insert_id()' # 插入的导演id
            cursor.execute(sql)
            director_id = cursor.fetchone()[0]
        else:
            director_id = res[0][0]
            
        # direct表
        sql = 'insert into movie_director(director_id, movie_id) values(%s, %s)' % (director_id, movie_id)
        cursor.execute(sql)
        
    # actor
    for i in actor:
        sql = 'select id from actor where name="%s"' % i
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) == 0:
            sql = 'insert into actor(name) values ("%s")' % i
            cursor.execute(sql)
            sql = 'select last_insert_id()' # 插入的演员id
            cursor.execute(sql)
            actor_id = cursor.fetchone()[0]
        else:
            actor_id = res[0][0]
            
        # actor_movie
        try:
            sql = 'insert into movie_actor(actor_id, movie_id) values(%s, %s)' % (actor_id, movie_id)
            cursor.execute(sql)        
        except:
            # TO DO 一部电影两个同名演员....(SB?)
            print("error:" + sql)
            # print(name1, actor_id, movie_id, i, sql)
            # print(actor)
            
    # place
    for i in place:
        sql = 'select id from place where name="%s"' % i
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) == 0:
            sql = 'insert into place(name) values ("%s")' % i
            cursor.execute(sql)
            sql = 'select last_insert_id()' # 插入的演员id
            cursor.execute(sql)
            place_id = cursor.fetchone()[0]
        else:
            place_id = res[0][0]
            
        # actor_movie
        
        try:
            sql = 'insert into movie_place(place_id, movie_id) values(%s, %s)' % (place_id, movie_id)
            cursor.execute(sql)        
        except:
            print("error:" + sql)
    
    # lang
    for i in lang:
        sql = 'select id from lang where name="%s"' % i
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) == 0:
            sql = 'insert into lang(name) values ("%s")' % i
            cursor.execute(sql)
            sql = 'select last_insert_id()' # 插入的演员id
            cursor.execute(sql)
            lang_id = cursor.fetchone()[0]
        else:
            lang_id = res[0][0]
            
        # actor_movie
        
        try:
            sql = 'insert into movie_lang(lang_id, movie_id) values(%s, %s)' % (lang_id, movie_id)
            cursor.execute(sql)        
        except:
            print("error:" + sql)
    
    
    db.commit() # 提交
