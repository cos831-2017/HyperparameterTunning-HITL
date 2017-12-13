
CREATE USER "admin" WITH PASSWORD 'monetdb' NAME 'Administrator' SCHEMA "sys";
CREATE SCHEMA "prov" AUTHORIZATION "admin";
ALTER USER "admin" SET SCHEMA "prov";
