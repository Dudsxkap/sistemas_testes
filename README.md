# Agendamento de Testes

## Descrição
Sistema desenvolvido para o processo seletivo EDITAL Nº 028/2023 – LAIS/UFRN, Fase 2, pelo participante Eduardo Amorim dos Santos Araujo.

O sistema tem por objetivo permitir ao cidadão realizar agendamentos de testes para COVID-19, caso esteja apto para isso.

## Configuração do projeto

### Tecnologias

O sistema foi desenvolvido usando Python 3.9, com o framework Django 3.2.3. O banco de dados escolhido foi o PostgreSQL 13.3.

### Instruções de execução

Primeiramente, após clonar o repositório, é preciso criar o ambiente virtual e instalar as dependências do projeto Python:
> python -m venv venv
> 
> pip install -r requirements.txt

Após isso, na raiz do [projeto Django](sistema_testes) crie um novo arquivo chamado local_settings.py e faça as configurações do banco de dados nesse arquivo criado. É possível encontrar um arquivo de exemplo em [sistema_testes/local_settings_sample.py](sistema_testes/local_settings_sample.py). A SECRET_KEY necessária para o projeto pode ser tanto adicionada nesse arquivo quanto nas variáveis de ambiente.

Então, efetue a migração dos models e das importações necessárias:
> python manage.py migrate

Para iniciar o projeto, utilize o seguinte comando:
> python manage.py runserver

Após iniciar o projeto, é possível acessar a página inicial através do link:
> http://localhost:8000

### Admin 

Primeiramente, para acessar o admin do projeto, é necessário ter uma conta do tipo superusuário. Para isso, faça o cadastro normalmente no sistema e rode o seguinte comando:
> python manage.py tornar_superusuario cpf

Sendo "cpf" substituído pelo CPF utilizado no seu cadastro.

Após isso, é possível acessar o admin do projeto através do link:
> http://localhost:8000/admin

### Importações

Caso deseje, é possível fazer a importação dos estabelecimentos de saúde utilizando o seguinte comando:
> python manage.py importar_estabelecimentos

Além disso, é possível realizer a criação em massa de agendamentos disponíveis, seguindo as regras descritas no edital, utilizando o seguinte comando:
> python manage.py criar_agendamentos data_inicial data_final

Sendo "data_inicial" e "data_final" substituídos por datas em string no formato Y-m-d.

### Docker

O projeto possui configurações para criar o container do banco de dados! Caso deseje utilizá-lo, na raiz do projeto crie um arquivo chamado .env e adicione as variáveis necessárias. É possível encontrar um arquivo de exemplo em [.env_example](.env_example). Após a criação desse arquivo, rode o seguinte comando:
> docker-compose up -d db

Após criação do container, lembre de configurar o banco de dados criado ao projeto, como explicado no passo "Instruções de execução".
