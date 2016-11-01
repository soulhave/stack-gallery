# Stack API documentation

# Table of Contents
1. [Authentication](#authentication)
2. [Stacks API](#stacks-api) 
 1. [List Stacks](#list-stacks)
 2. [List Stacks](#get-stacks)
 3. [List Stacks](#add-stacks)
3. [Users API](#users-api)
4. [Trends API](#trends-api)

## Authentication
There is only one way to authentication through Stack. Request a Google OAuth Token and send it in a header, like this:

```console
curl -H "Authorization: OAUTH-TOKEN" http://stack.ciandt.com/api/version
```

## API Resources

### Stacks API

#### List Stacks
This call lists all the [available stacks] ordered by last-update field

* **URL:** /api/stacks
* **Method:** GET
* **URL Params***
* **Response**
**Code:** 200 <br />
**Content:** 
 
```js
[
	{
	"key": "unique-id",	
	"name": "name",
	"owner": "owner",
	"stack": [
		{
		"imageUrl": "https://www.googleapis.com/download/storage/v1/b/tech-gallery-prod/o/java?generation=1453060953626000&alt=media",
		"technology": "java",
		"technologyName": "Java"
		}...
	}],
	"team" : [
		{
		"email": "williamb@ciandt.com",
		"image": "https://cdn.github.com/people/photo/williamb",
		"login": "williamb"
		}...
	]
	"like_count": 0,
	"index": 0.8700000000000002
	}
	...	
]
 ```

#### Get Stacks
Get a specific stack by id

* **URL:** /api/stacks/:id
* **Method:** GET
* **Response**
**Code:** 200 <br />
**Content:** 
```js
{
	"key": "unique-id",	
	"name": "name",
	"owner": "owner",
	"stack": [
		{
		"imageUrl": "https://www.googleapis.com/download/storage/v1/b/tech-gallery-prod/o/java?alt=media",
		"technology": "java",
		"technologyName": "Java"
		}...
	}],
	"team" : [
		{
		"email": "williamb@ciandt.com",
		"image": "https://cdn.github.com/people/photo/williamb",
		"login": "williamb"
		}...
	]
	"like_count": 0,
	"index": 0.8700000000000002
}
```


#### Add Stacks
This call adds the new stack with 
* **URL:** /api/stacks
* **Method:** POST
* **Data Params:**
```js
{
	"key": "unique-id",	
	"name": "name",
	"owner": "owner",
	"stack": [
		{
		"imageUrl": "https://www.googleapis.com/download/storage/v1/b/tech-gallery-prod/o/java?alt=media",
		"technology": "java",
		"technologyName": "Java"
		}...
	}],
	"team" : [
		{
		"email": "williamb@ciandt.com",
		"image": "https://cdn.github.com/people/photo/williamb",
		"login": "williamb"
		}...
	]
	"like_count": 0,
	"index": 0.8700000000000002
}
```
* **Response**
**Code:** 201 Created <br />
**Content:** 
{
	"key": "unique-id",	
}

----
### Users API

----
### Trends API