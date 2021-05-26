import re
import shutil
import requests
import threading
from django.conf import settings
from mimetypes import guess_extension

from PIL import Image
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand, CommandError
from api.models import Albums, Photos
from django.db import connection


def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = threading.Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator


class Command(BaseCommand):
    args = ""
    api_url = "http://jsonplaceholder.typicode.com"
    albums_path = "/albums/"
    photos_path = "/photos/"
    users_path = "/users/"

    def add_arguments(self, parser):
        pass

    def get_users(self):
        try:
            users_response = requests.get(self.api_url + self.users_path)
        except requests.exceptions.Timeout as e:
            print(e)
        except requests.exceptions.TooManyRedirects as e:
            print(e)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        try:
            users = users_response.json()
        except ValueError as e:
            print(e)
            return False

        if len(users) > 0:
            for user in users:
                u, created = User.objects.get_or_create(
                    username=user.get('username'),
                    first_name=user.get('name').split(' ')[0],
                    last_name=user.get('name').split(' ')[1],
                    email=user.get('email'),
                )
                if created:
                    try:
                        u.save()
                    except ValidationError:
                        print(ValidationError)

    def get_albums(self):
        try:
            albums_response = requests.get(self.api_url + self.albums_path)
        except requests.exceptions.Timeout as e:
            print(e)
        except requests.exceptions.TooManyRedirects as e:
            print(e)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        try:
            albums = albums_response.json()
        except ValueError as e:
            print(e)
            return False

        if len(albums) > 0:
            for album in albums:
                u, created = User.objects.get_or_create(pk=album.get('userId'))
                album_object = Albums(
                    id=album.get('id', ''),
                    title=album.get('title', ''),
                    userId=u
                )
                try:
                    album_object.save()
                except ValidationError:
                    print(ValidationError)

    def get_photos(self):
        try:
            photos_response = requests.get(self.api_url + self.photos_path)
        except requests.exceptions.Timeout as e:
            print(e)
        except requests.exceptions.TooManyRedirects as e:
            print(e)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        try:
            photos = photos_response.json()
        except ValueError as e:
            print(e)
            return False

        if len(photos) > 0:
            for photo in photos:
                album, created = Albums.objects.get_or_create(pk=photo.get('albumId'))

                photo_object = Photos(
                    albumId=album,
                    title=photo.get('title', ''),
                    url=photo.get('url', ''),
                    thumbnailUrl=photo.get('thumbnailUrl', ''),
                )

                try:
                    photo_object.save()
                except ValidationError:
                    print(ValidationError)

    def load_photos(self):
        photos = Photos.objects.all()
        size = 500
        # The `iterator()` method ensures only a few rows are fetched from
        # the database at a time, saving memory.
        for photo in photos.iterator():
            filename = photo.url.split("/")[-1]
            response = requests.get(photo.url, stream=True)
            ext = guess_extension(response.headers['content-type'].partition(';')[0].strip())

            if response.status_code == 200:
                response.raw.decode_content = True
                saved_url = settings.MEDIA_ROOT + '/' + filename + ext
                thumb_url = settings.MEDIA_URL + str(size) + '-' + filename + ext
                resized_url = settings.MEDIA_ROOT + '/' + str(size) + '-' + filename + ext

                with open(saved_url, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)

                try:
                    image = Image.open(saved_url)
                    image = image.resize((size, size))
                    image.save(resized_url, ext.upper()[1:])
                except OSError as e:
                    print('open() or file.__enter__() failed', e)

                Photos.objects.filter(pk=photo.id).update(localUrl=thumb_url)

    def handle(self, *args, **options):
        self.get_users()
        self.get_albums()
        self.get_photos()
        # self.load_photos()
