#!/bin/sh

monetdbd stop db

sudo rm -rfv db

monetdbd create db
monetdbd start db

monetdb create prov
monetdb release prov

mclient -u monetdb -d prov -i script_db_admin_user_create.sql

mclient -u admin -d prov -i script_db_prov_create.sql
