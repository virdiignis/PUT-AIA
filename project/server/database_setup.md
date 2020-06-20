Project is using postgresql. Here art the commands to set it up.
```
CREATE DATABASE tournament'
CREATE USER tournament WITH PASSWORD 'tournament';

ALTER ROLE tournament SET client_encoding TO 'utf8';
ALTER ROLE tournament SET default_transaction_isolation TO 'read committed';
ALTER ROLE tournament SET timezone TO 'Europe/Warsaw';

GRANT ALL PRIVILEGES ON DATABASE tournament TO tournament;
```