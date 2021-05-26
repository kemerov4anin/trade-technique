# XWay test task

## You must have Git, Docker and Docker-compose!

Pull project from repo

Run `docker-compose up -d --build`

Open `http://localhost:8888/` with browser

Urls:

Django templates view:
    albums/ [name='albums-list']
    album/<pk>/ [name='album-details']

DRF api:
    api-token-auth/
    api/v1/

Static files:
    ^staticfiles/(?P<path>.*)$