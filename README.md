# DDownloader | Direct downloader

* Download files through http to your home server
* Manage and monitor downloads through a web UI

## Usage case
Let's say you're on you phone/tablet/laptop and you find out a file that want
to download into your server (Linux distro, Wallpaper, Photo album, Movie, etc),
instead of going to your server and do a `wget` manually you just paste the url
into the **DDownloader** UI and it will take care for you.

## Deployment

### Database setup

Ddownloader requires a running Postgres database. Use the [schema.sql](./db/schema.sql) file to create the tables.

### Env variables and config file

Use [template.env](./template.env) as a base to prepare your own env file with appropriate values for your deployment

```shell
wget ...
vim .env
```

Then, prepare the config file for `gallery-dl`. If you're going to download private galleries or galleries that require some kind of authentication, make sure to enter your cookie values here.

```shell
wget ...
vim 
```





## Development

See [Development section](./docs/development.md)