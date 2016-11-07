# bikeparking
TCC - 2016

Para executar o projeto na própria máquina primeiramente fazer download do projeto em uma pasta, criar uma virtualenv (https://virtualenv.pypa.io/en/stable/) e ativar a virtualenv:

```
$ virtualenv venv
$ source venv/bin/activate
```

Instalar os requerimentos do projeto presentes no arquivo ```requirements.txt```:

```
$ (venv) pip install -r requirements.txt
```

Instalar PostgreSQL na máquina (https://www.postgresql.org) e configurar usuário e banco:

```
$ psql
$ =# CREATE USER bikeparking WITH PASSWORD 'da39a3ee5e6b4';
$ =# CREATE DATABASE bikeparking;
$ =# GRANT ALL ON DATABASE bikeparking TO bikeparking;
```

Instalar a extensão do PostGIS (http://postgis.net) e configurar no banco:

```
$ psql -U bikeparking;
$ =# CREATE EXTENSION postgis;
```

Após configurar o banco, inicializar o projeto, aplicar as migrações e criar um super-usuário:
Obs: Os comandos abaixos devem ser utilizados com a virtualenv ativa!

```
$ (venv) python src/bike_parking/manage.py migrate
$ (venv) python src/bike_parking/manage.py createsuperuser
```

Após criar o super-usuário basta rodar o projeto:

```
$ (venv) python src/bike_parking/manage.py runserver
```
