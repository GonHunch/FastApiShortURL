# Short code generator for any URL using FastAPI based on PostgreSQL

## Description

Allows the user to generate a short code for any given URL and store it in a database table. The short code can then be used to redirect the user to the original URL.

## Examples

`POST /links/shorten` - generates a short code for an HTTP link and creates a record. Short code can be user-generated set by `custom_alias`. Can set `expires_at` to set the time for the link to expire.

Request body:
```
{
  "url": "https://www.google.com/",
  "custom_alias": "abc",
  "expires_at": "2025-04-30T23:59"
}
```

`GET /links/{short_code}` - returns the original URL from the short code provided.

`DELETE /links/{short_code}` - deletes the table record based on the short code provided.

`PUT /links/{short_code}` - changes the short code and (optionally) its expiry date of an original URL.

Request body:
```
{
  "new_short_code": "zxc",
  "expires_at": "2025-05-31T00:00"
}
```

`GET /links/{short_code}/stats` - returns the stats of the short code provided (displays original URL, creation date, number of clicks, last clicked at date.)

`GET /links/search?original_url={url}` - returns the short code of the original URL provided.

## Start-up instructions

### Using Docker

This will run two containers, one for the database and the other for the application itself.

```
docker compose up
```

### Manually

Ensure that you have a PostgreSQL server run locally. The name of the database must be 'url_db'.

```
pip install -r requirements.txt
python app/main.py
```

Go to `0.0.0.0:8000/docs` to access HTTP methods.

