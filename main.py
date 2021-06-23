import os
import time
import vk
import requests

publish_date = None

print("ID группы")
group_id = input(">>> ")
print("ID альбома")
album_id = input(">>> ")
print("Токен доступа")
access_token = input(">>> ")
print("Частота публикации (в секундах)")
frequency = input(">>> ")

def finder():
    global publish_date
    names = os.listdir(os.getcwd() + '\downloads')
    for name in names:
        url_photo = os.path.join(os.getcwd() + '\downloads', name)
        if os.path.isfile(url_photo):
            print(url_photo)
            postArticle(url_photo)
            time.sleep(1)
    print('Последняя запись будет')
    print(datetime.utcfromtimestamp(publish_date).strftime('%Y-%m-%d %H:%M:%S'))
    print('Не забудь подготовить материал для новой публикации')
 

def postArticle(url_photo):
    global publish_date
    global group_id
    global album_id
    global access_token
    if publish_date:
        publish_date = int(publish_date) + frequency
    else:
        publish_date = int(time.time()) + frequency
        
    filename = url_photo
    #caption = 'Some text'
    

    # Авторизуемся в VK
    session = vk.Session(access_token=access_token)
    vk_api = vk.API(session)

    # Получаем адрес сервера для загрузки картинки
    params = {
            'album_id': album_id,
            'group_id': group_id,
            'v': '5.131'}
    upload_url = vk_api.photos.getUploadServer(**params)['upload_url']

    # Формируем данные параметров для сохранения картинки на сервере
    request = requests.post(upload_url, files={'photo': open(filename, "rb")})
    
    params = {'server': request.json()['server'],
              'photos_list': request.json()['photos_list'],
              'hash': request.json()['hash'],
              'group_id': group_id,
              'album_id': album_id,
              'v': '5.131'}
              
    request = vk_api.photos.save(**params)
    owner_id = request[0]['owner_id']
    photo_id = request[0]['id']
    print('photo' + str(owner_id) + '_' + str(photo_id))
    # Формируем параметры для размещения картинки в группе и публикуем её
    params = {'attachments': 'photo' + str(owner_id) + '_' + str(photo_id),
              'owner_id': '-' + group_id,
             'from_group': '1',
              'v': '5.131',
              'publish_date': publish_date}
    vk_api.wall.post(**params)
    
if __name__ == '__main__':
    finder()