# tools

Scripts de apoio ao site. Nada aqui é necessário para o site funcionar: o
GitHub Pages serve o HTML que já está commitado.

## Gerador das páginas de projeto

`gerar_projetos.py` monta as páginas `projetos/*.html` a partir dos dados em
`projetos_dados.py`. Só usa a biblioteca padrão do Python 3.

```bash
python3 tools/gerar_projetos.py                 # regera as 14 páginas
python3 tools/gerar_projetos.py frota-lite      # regera só uma (ou várias)
```

Para mudar o texto de uma página, edite o projeto em `projetos_dados.py` e
rode o gerador. Para mudar o layout de todas, edite o modelo `page()` em
`gerar_projetos.py` ou o CSS compartilhado em `projetos/projeto.css`.

- **Todas as 14 páginas** saem do gerador, inclusive a do Lúmen. Não edite
  `projetos/*.html` à mão: a próxima execução sobrescreve.
- **Status, percentual e próxima tarefa** precisam bater com o array
  `ROADMAP` em `roadmap.html`. Ao mudar um, mude o outro.
- **Números** na faixa de prova são só os conferidos no repositório de cada
  projeto (testes, migrações, commits, versões). Não entram depoimentos,
  clientes nem métricas de uso que não existam.
