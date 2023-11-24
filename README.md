# bidb / buildinfo.debian.net

## Local database setup

* Create PostgreSQL user with id matching your UNIX username:

    `$ sudo -u postgres createuser $(whoami) -SDR`

* Create a database owned by this user:

    `$ sudo -u postgres createdb -E UTF-8 -O $(whoami) bidb`

* Run any initial migrations:

    `$ ./manage.py migrate`
