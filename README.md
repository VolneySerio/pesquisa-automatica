# Automação de Pesquisas no Google

## Descrição

Projeto em Python que lê pesquisas de um arquivo JSON, abre cada pesquisa no Google e permite automatizar o fechamento da aba após um intervalo de tempo.

## Requisitos

- Python 3 instalado.
- Navegador instalado.
- Windows com PowerShell disponível.

## Estrutura do projeto

```text
projeto/
├── pesquisas.json
├── pesquisar.py
└── README.md
```

## Formato do arquivo JSON

O arquivo `pesquisas.json` deve conter uma lista de pesquisas:

```json
[
  {
    "pesquisa": "linguagem de programação Python"
  },
  {
    "pesquisa": "introdução à inteligência artificial"
  }
]
```

## Como executar

1. Abra o terminal na pasta do projeto.
2. Execute o comando:

```bash
python pesquisar.py
```

3. O programa percorrerá as pesquisas do arquivo JSON e abrirá cada uma no navegador.

## Observações

- O intervalo entre pesquisas pode ser alterado no código.
- O fechamento da aba depende de o navegador estar em primeiro plano.
- O programa utiliza bibliotecas nativas do Python e comandos do Windows.
