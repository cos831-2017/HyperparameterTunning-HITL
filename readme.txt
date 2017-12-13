- Usar o python >= 3.4

- Fazer cd para a pasta labbd

- Executar:

	python3 -m venv flask;

	flask/bin/pip install -r requirements.txt;

	chmod a+x run.py

	sudo apt install redis-server


- Para subir o servidor em modo debug:

	./run.py


- Para instalar o monetdb no linux:

	https://www.monetdb.org/downloads/deb/


- Para configurar o banco de proveniência (INICIAL. O script apaga o atual, se existir):

	./erase_and_first_config_monet_db.sh (caso a senha do banco seja solicitada está é 'monetdb')


- Para iniciar o servidor do monetdb, caso este não esteja rodando:

	monetdbd start db
