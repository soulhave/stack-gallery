# Stack Gallery

Stack is a tool that shows technology used in your product. There is a strong integration with [Tech Gallery][techgallery] and [Knowledge Map][knowledge]

![screenshot from 2016-10-27 13-02-19](https://cloud.githubusercontent.com/assets/6742877/19829377/e83e0b94-9dbd-11e6-84d8-cbad124c8e0f.png)

## Before start is necessary have previously installed:
- [Git][Git]
- [Python 2.7.9](https://www.python.org/)
- [Pip](https://packaging.python.org/installing/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts)
- [Elasticsearch][Elasticsearch]
### Optional:
- [Docker][Docker]

### Google App Engine Account
- Create new [google account](https://console.cloud.google.com/)
- Create a new OAUTH account.
- Use this account in JS file:
```
$ app/client/app/app.js
```
- Find by **clientId** and put that key on there.

### Clone this repository:
```
$ git clone https://github.com/marcuslacerda/stack-gallery.git
$ cd stack-gallery
```

### You must define these environments on your .env file on app directory

```
GOOGLE_CLIENT_ID=set-google-client-id-here_or_export-env-vavariable>
GOOGLE_CLIENT_SECRET=set-google-client-secret-here_or_export-env-vavariable>
ELASTICSEARCH_URL=url-to-elasticsearch-stack
MODE=<development-production>
```

## Running server local
### Into the project access the 'app' directory:
```
$ cd app
```

### Install requirements
```
pip install -r ../requirements.txt -t lib
```

### Run the command bellow:
```
$ dev_appserver.py .
```

If you need a full local enviroment, you must start [Elasticsearch] and change elasticsearch host at ELASTICSEARCH_URL variable.

You must configure these GOOGLE values from [Google APIs console]

```console
$ run docker -p 9200:9200 elasticsearch
```

The application will be accessible at http://localhost:8080

[Docker]: https://docs.docker.com/engine/installation
[Google APIs console]: https://code.google.com/apis/console
[techgallery]: https://github.com/ciandt-dev/tech-gallery
[knowledge]: https://github.com/marcuslacerda/tech-gallery-knowledgemap
[Git]: http://help.github.com/set-up-git-redirect
[Python]: https://www.python.org
[Pull requests]: https://help.github.com/categories/collaborating-on-projects-using-issues-and-pull-requests/
[Elasticsearch]: https://www.elastic.co/products/elasticsearch
