# DataMining

Trabalho realizado para a disciplina: MR36O - MINERAÇÃO DE REPOSITÓRIO DE SOFTWARE

### Pré Requisitos
Para o desenvolvimento foi utilizado a linguagem [Python](https://www.python.org/) com as bibliotecas:
* [Requests](https://requests.readthedocs.io/en/master/);
* [json](https://docs.python.org/3/library/json.html);
* [pandas](https://pandas.pydata.org/docs/);

### Começando
Primeiramente, abra o terminal no diretório do teste e instale as dependências:
* `$ pip install requests`
* `$ pip install json`
* `$ pip install pandas`

### Configurando
Dentro do diretório tem o arquivo **./config.json/**, onde estão contidos os arquivo de configuração:

```
{
  "github_token": [
    {token_github}
  ],
  "users_list": [
    {lista_usuarios - entre aspas e separados por virgula}
  ],
  "filenameGist": "{nome_desejado}.csv",
  "filenameUsers": "{nome_desejado2}.csv"
}
```
Altere para as suas configurações.

### Executando

Para rodar a aplicação use o comando:
`$ python new-mining.py`
