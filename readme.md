# Stack Gallery

Stack is a tool that shows technology used in your product. There is a strong integration with [Tech Gallery][techgallery] and [Knowledge Map][knowledge]

![screenshot from 2016-10-27 13-02-19](https://cloud.githubusercontent.com/assets/6742877/19829377/e83e0b94-9dbd-11e6-84d8-cbad124c8e0f.png)

## Running (local setup)
[Git][] and [Python 2.7.9 ][Python]. For Python you need to install the following modules:
* pip install flask
* pip install requests
* pip install elasticsearch

```console
$ git clone https://github.com/marcuslacerda/stack-gallery.git
$ cd stack-gallery
```

You must define these environments on your variable. 

```console
$ export GOOGLE_CLIENT_ID=set-google-client-id-here_or_export-env-vavariable>
$ export GOOGLE_CLIENT_SECRET=set-google-client-secret-here_or_export-env-vavariable>
$ export ELASTICSEARCH_URL=url-to-elasticsearch-stack
```

Running server local

```console
$ python server.py
```

## Running (by docker)

Build the image using the following command

```console
$ git clone https://github.com/marcuslacerda/stack-gallery.git
$ docker build -t stack-app:latest .
```

Run the Docker container using the command shown below.

```console
$ docker run -e ELASTICSEARCH_URL=http://localhost:9200 -p 5000:5000 stack-app
```

If you need a full local enviroment, you must start [Elasticsearch] and change elasticsearch host at ELASTICSEARCH_URL variable

```console
$ run docker -p 9200:9200 elasticsearch
```

The application will be accessible at http://localhost:5000

[techgallery]: https://github.com/ciandt-dev/tech-gallery
[knowledge]: https://github.com/marcuslacerda/tech-gallery-knowledgemap
[Git]: http://help.github.com/set-up-git-redirect
[Python]: https://www.python.org
[Pull requests]: https://help.github.com/categories/collaborating-on-projects-using-issues-and-pull-requests/
[Elasticsearch]: https://www.elastic.co/products/elasticsearch 