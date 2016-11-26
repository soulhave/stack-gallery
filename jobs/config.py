import yaml
import os.path

def load():
	resource_path = os.path.join(os.path.split(__file__)[0], "resources/config.yaml")
	with open(resource_path, 'r') as stream:
	    try:
	        return yaml.load(stream)
	    except yaml.YAMLError as exc:
	        print(exc)


# es_host = os.environ.get('ELASTICSEARCH_URL')
# if not es_host:
# 	sys.exit('Error: You must define ELASTICSEARCH_URL environment variable')
	        

