# Stack API documentation

## Authentication
There is only one way to authentication through Stack. Request a Google OAuth Token and send it in a header, like this:

```console
curl -H "Authorization: OAUTH-TOKEN" http://stack.ciandt.com/version
```

## API Resources

### Stacks API

**List Stacks**
----
This call lists all the [available stacks] ordered by last-update field

* **URL**
* **Method: GET**
* **URL Params***
* **Success Response**
* **Code:** 200 <br />
* **Content:** 
 
```js
[
	{
	"index": 0.8700000000000002,
	"key": "1LDOG-vha5Tei2ME4WWd1pmyMpt2japmt-qKBNRiRNMM",
	"like_count": 0,
	"name": "BR/CPS - WebSites Imkt",
	"owner": "Coca-Cola",
	"stack": [
		{
		"imageUrl": "https://www.googleapis.com/download/storage/v1/b/tech-gallery-prod/o/java?generation=1453060953626000&alt=media",
		"technology": "java",
		"technologyName": "Java"
		},
		{
		"imageUrl": "https://www.googleapis.com/download/storage/v1/b/tech-gallery-prod/o/javascript?generation=1453211966798000&alt=media",
		"technology": "javascript",
		"technologyName": "Javascript"
		}
	}
]
 ```

### Users API

### Trends API