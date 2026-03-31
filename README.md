# dbt-spotify-analytics
Projeto de Engenharia de Dados para aprendizado de dbt, construindo um data warehouse analítico com dados da Spotify API.

## Python
Para desenvolver os módulos Python do projeto, use sempre a virtualenv local:

```powershell
.\.venv\Scripts\python.exe -m spotify_dbt.source.main
```

O arquivo `spotify_dbt/source/main.py` também pode ser executado diretamente no VS Code sem quebrar os imports, desde que o interpretador selecionado seja o da `.venv` do projeto.
