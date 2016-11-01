# Stack API documentation

# Table of Contents
1. [Authentication](#authentication)
2. [Stacks API](#stacks-api) 
 1. [List Stacks](#list-stacks)
 2. [Search Stacks](#search-stacks)
 3. [Get Stack's Team](#team-stacks) 
 4. [Get Stacks](#get-stacks) 
 5. [Add Stacks](#add-stacks)
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

#### Search Stacks
Search stack by query param. Query is passed by 'q' URL param

* **URL:** /api/stacks/search
* **Method:** GET
* **URL Params**
**Required:** <br />
   `q=[string]`
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

#### Team Stack
Get a team for stack id. A team is a list of users with email, login, image-url and name

* **URL:** /api/stacks/team/<id>
* **Method:** GET
* **Response**
**Code:** 200 <br />
**Content:** 
```js
[
	{
	"email": "williamb@ciandt.com",
	"image": "https://cdn.github.com/people/photo/williamb",
	"login": "williamb"
	},
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
This call adds the new stack.

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
```js
{
	"key": "unique-id",	
}
``

----
### Users API

----
### Trends API