import mimetypes
import os
import sys
import urllib
import zipfile

from channels.db import database_sync_to_async
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from selenium import webdriver


async def find_all_images_and_save(request):
    browser = webdriver.Firefox()
    browser.get(request.url)
    imgs = browser.find_elements_by_tag_name('img')
    await set_progress(request, 10)
    files_dir = os.path.join(os.getcwd(), 'files')
    req_dir = os.path.join(files_dir, str(request.req_id))
    caches_dir = os.path.join(req_dir, '.cache')
    if not os.path.isdir(caches_dir):
        os.mkdir(caches_dir)
    for idx, img in enumerate(imgs):
        src = img.get_attribute('src')
        # sys.stdout.write(src + '\n')
        if check_url(src):
            hostname = urllib.parse.urlparse(src).netloc
            name = src.split('/')[-1].split('?')[0]
            if name.find('.') == -1:
                res = urllib.request.urlopen(src)
                info = res.info()
                ext = mimetypes.guess_extension(info['Content-Type'])
                name += ext
            host_dir = os.path.join(caches_dir, hostname)
            if not os.path.isdir(host_dir):
                os.mkdir(host_dir)
            # sys.stdout.write(name + '\n')
            urllib.request.urlretrieve(src, os.path.join(host_dir, name))
        await set_progress(request, 10 + int((idx / len(imgs)) * 70))
    browser.close()
    zf = zipfile.ZipFile(os.path.join(req_dir, 'images.zip'), 'w')
    for dirname, subdirs, files in os.walk(caches_dir):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    await set_progress(request, 100)


async def set_progress(request, progress):
    request.progress = progress
    await database_sync_to_async(request.save)()


def check_url(url):
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError as e:
        return False
    return True
