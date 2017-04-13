
import sys
import os

from imgurpython import ImgurClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from secret.secret import imgur_client_id, imgur_client_secret

imgur = ImgurClient(imgur_client_id, imgur_client_secret)

def get_first_album_image(url):
    album_id = get_imgur_id(url, 'album') or get_imgur_id(url, 'gallery')
    try:
        album_images = imgur.get_album_images(album_id)
        return album_images[0].link
    except Exception as e:
        print('Could not get album images for url: {0}'.format(url))
        return False

def get_gallery_image_id(url):
    gallery_id = get_imgur_id(url, 'gallery')
    try:
        item = imgur.gallery_item(gallery_id)
        print(item.link)
        return item.id
    except Exception as e:
        print('Could not get gallery item')
        return False

def get_imgur_id(url, imgur_type='image'):
    result = False
    if imgur_type == 'image':
        pos = url.find('.com/')
        if pos != -1:
            result = url[pos+5:]
    if imgur_type == 'album':
        pos = url.find('/a/')
        if pos != -1:
            result = url[pos+3:]
    if imgur_type == 'gallery':
        pos = url.find('/gallery/')
        if pos != -1:
            result = url[pos+9:]
    return result

def get_image_link(url):
    imgur_type = get_imgur_type(url)

    # handle differently if album or gallery
    if imgur_type == 'album' or imgur_type == 'gallery':
        return get_first_album_image(url)
    
    image_id = get_imgur_id(url, imgur_type)
    if not image_id:
        return False

    try:
        image = imgur.get_image(image_id)
        return image.link
    except Exception as e:
        print('Could not get the image')
        return False

def get_imgur_type(url):
    if '.com/a/' in url or '/album/' in url:
        return 'album'
    if '.com/gallery/' in url or '/g/' in url:
        return 'gallery'
    else:
        return 'image'

# testing from command line
if __name__ == '__main__':
    url = 'http://imgur.com/Swz7F8B'
    raw_url = get_image_link(url)
    print('Found raw url: {0}'.format(raw_url))

    url = 'http://imgur.com/a/diA2p'
    raw_url = get_image_link(url)
    print('Found raw url: {0}'.format(raw_url))

    url = 'https://imgur.com/gallery/2h9Z8'
    raw_url = get_image_link(url)
    print('Found raw url: {0}'.format(raw_url))