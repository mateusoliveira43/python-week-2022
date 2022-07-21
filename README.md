# Python Week 2022

Minha versão do projeto desenvolvido durante a [Python Week 2022 - 25 a 29 de Abril na Linux Tips](https://www.youtube.com/watch?v=NqUC-G_Pu-o&list=PLf-O3X2-mxDlfAv8IOfic1sHArdwrrkgh)

## Obtendo seu repositório

1. Faça login no github (cadastre-se gratuitamente caso ainda não tenha uma conta)
1. Crie um **fork** (cópia) do repositório da Python Week 2022 clicando em [fork](https://github.com/rochacbruno/python-week-2022/fork)
1. O seu repositório estará em `https://github.com/<SEU_USUARIO>/python-week-2022`
1. Para rodar localmente faça o clone com `git clone https://github.com/<SEU_USUARIO>/python-week-2022`
1. Para acessar a pasta, execute `cd python-week-2022`

## Requisitos

Para rodar o projeto, as seguintes ferramentas são necessárias:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

ou

- Python 3.8
- [Poetry](https://python-poetry.org/docs/#installation)

## Iniciando o ambiente

### Docker

TODO

### Poetry

O comando a seguir instala as dependências do projeto
```bash
poetry install
```

O comando a seguir ativa o ambiente virtual do `Poetry`
```bash
poetry shell
```

Ou execute `source scripts/start_poetry.sh` que é um script que automatiza todos os comandos acima.

O comando a seguir executa o serviço de interface de linha de comando
```bash
beerlog_cli
```

O comando a seguir executa o serviço de API
```
beerlog_api
```

Para desativar o ambiente virtual do `Poetry`, execute `CTRL+D` ou `exit`.

## Qualidade

Para rodar as métricas de qualidade do projeto, é necessário instalar as dependências do projeto e ter o ambiente virtual ativo.

As métricas de qualidade do modelo são reproduzidas pelas etapas de integração contínua do projeto. Configurações das etapas de integração contínua descritas no arquivo `.github/workflows/ci.yml`.

### Testes

Para rodar os testes e relatório de cobertura, execute
```
pytest
```

Para ver o relatório html, confira `tests/coverage-results/htmlcov/index.html`.

Configurações dos testes e relatório de cobertura descritas no arquivo `pyproject.toml`.

### Checagem de tipo

Para rodar o checador de tipo do Python, execute
```
mypy .
```

Configurações do checador de tipo do Python descritas no arquivo `pyproject.toml`.

### Linter

Para rodar o linter de código Python, execute
```
prospector
```

Configurações do linter de Python descritas no arquivo `.prospector.yaml`.

### Formatadores de código

Para checar o formato das importações no código Python, execute
```
isort --check --diff .
```

Para formatar as importações no código Python, execute
```
isort .
```

Para checar o formato do código Python, execute
```
black --check --diff .
```

Para formatar o código Python, execute
```
black .
```

Configurações do isort e black descritas no arquivo `pyproject.toml`.

Para checar o formato de todos os arquivos do repositório, execute
```
ec -verbose
```

Configurações do formato dos arquivos descritas no arquivo `.editorconfig`.

### Varredura de vulnerabilidades de segurança

Para checar problemas de segurança comuns no código Python, execute
```
bandit --recursive beerlog
```

Para checar vulnerabilidades de segurança conhecidas nas dependências Python, execute
```
safety check --file requirements/prod.txt --full-report
safety check --file requirements/dev.txt --full-report
```

## Pre-commit

Para configurar o pre-commit automaticamente ao clonar o repositório, execute
```
pip install pre-commit
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir --hook-type commit-msg --hook-type pre-commit ~/.git-template
```
Precisa ser instalado de forma global. Mais informações em https://pre-commit.com/#automatically-enabling-pre-commit-on-repositories

Para configurar o pre-commit localmente, execute
```
pip install pre-commit
pre-commit install --hook-type commit-msg --hook-type pre-commit
```
com seu ambiente virtual ativo.

Para testá-lo, execute
```
pre-commit run --all-files
```

## Licença

Esse repositório é licenciado sob os termos da [Licença](LICENSE).
