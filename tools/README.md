# tools

Scripts de apoio ao site. Nada aqui é necessário para o site funcionar: o
GitHub Pages serve o HTML que já está commitado.

## Gerador das páginas

`gerar_projetos.py` gera as 14 páginas de projeto (`projetos/*.html`), as 3
páginas por segmento (`solucoes/*.html`), o `sitemap.xml` e o `robots.txt`, e
preenche os números da página inicial (`data-stat` em `index.html`) a partir
dos dados dos projetos.

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
- **Status, percentual e próxima tarefa** de cada projeto ficam em
  `projetos_dados.py`, e os números da página inicial saem deles.
- **Números** na faixa de prova são só os conferidos no repositório de cada
  projeto (testes, migrações, commits, versões). Não entram depoimentos,
  clientes nem métricas de uso que não existam.

## Imagens de compartilhamento

`gerar_og.mjs` cria `og/*.jpg` (1200×630), a imagem que aparece ao colar o link
no WhatsApp, no LinkedIn ou em outra rede. Rode depois do gerador:

```bash
npm install --no-save playwright && npx playwright install chromium
node tools/gerar_og.mjs
```

## Verificação

`verificar_site.mjs` abre todas as páginas em 320, 390, 768, 1280 e 1440 px e
confere erros, rolagem horizontal, links internos e imagens de compartilhamento.
A GitHub Action `.github/workflows/verificar.yml` roda o gerador e essa
verificação a cada push.

```bash
node tools/verificar_site.mjs
```

## Contato e estatística de visitas

Os botões de WhatsApp, e-mail e agenda e o contador de visitas (GoatCounter,
sem cookies) ficam em `assets/site.js`. Preencha o objeto `SITE` no topo do
arquivo; campo vazio não aparece.
