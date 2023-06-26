# camera_projeto

Esse é um projeto de estudos que tem como foco a criação de uma página que tira foto com a webcam e salva na pasta do servidor.

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```bash
git clone https://github.com/jeannefernanda/camera_projeto.git
cd estoque
python -m venv .venv
./venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
