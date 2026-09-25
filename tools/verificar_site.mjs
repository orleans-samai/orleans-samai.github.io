// Verifica o site inteiro antes de publicar.
//
// Uso, na raiz do repositório (precisa do Playwright com o Chromium):
//   npm install --no-save playwright && npx playwright install chromium
//   node tools/verificar_site.mjs
//
// Para cada página HTML, em 320, 390, 768, 1280 e 1440 px de largura:
//   - nenhum erro de JavaScript nem de carregamento de recurso local;
//   - nenhuma rolagem horizontal;
// e, uma vez por página:
//   - todo link interno aponta para um arquivo que existe (e para uma âncora que existe);
//   - a imagem de compartilhamento (og:image) existe em og/.
// Sai com código 1 se encontrar qualquer problema.
import { createServer } from 'node:http';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, extname, dirname, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const LARGURAS = [320, 390, 768, 1280, 1440];

async function carregarPlaywright() {
  try { return await import('playwright'); } catch {}
  const global = execSync('npm root -g').toString().trim();
  return import(join(global, 'playwright', 'index.mjs'));
}

const TIPOS = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.woff2': 'font/woff2',
  '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml', '.xml': 'application/xml', '.txt': 'text/plain' };
const servidor = createServer((req, res) => {
  let caminho = join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (caminho.endsWith('/')) caminho = join(caminho, 'index.html');
  if (!caminho.startsWith(ROOT) || !existsSync(caminho)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TIPOS[extname(caminho)] || 'application/octet-stream' });
  res.end(readFileSync(caminho));
}).listen(0);
const BASE = `http://127.0.0.1:${servidor.address().port}`;

const paginas = ['index.html', '404.html']
  .concat(readdirSync(join(ROOT, 'projetos')).filter((f) => f.endsWith('.html')).map((f) => 'projetos/' + f))
  .concat(readdirSync(join(ROOT, 'solucoes')).filter((f) => f.endsWith('.html')).map((f) => 'solucoes/' + f));

const problemas = [];
const { chromium } = await carregarPlaywright();
const navegador = await chromium.launch();

for (const pg of paginas) {
  const html = readFileSync(join(ROOT, pg), 'utf8');

  // links internos e âncoras
  for (const [, href] of html.matchAll(/<a [^>]*href="([^"]+)"/g)) {
    if (/^(https?:|mailto:|tel:|data:)/.test(href)) continue;
    const [arquivo, ancora] = href.split('#');
    const alvo = arquivo === '' ? pg
      : arquivo.startsWith('/') ? (arquivo === '/' ? 'index.html' : arquivo.slice(1))
      : normalize(join(dirname(pg), arquivo));
    if (!existsSync(join(ROOT, alvo))) { problemas.push(`${pg}: link quebrado → ${href}`); continue; }
    if (ancora && !readFileSync(join(ROOT, alvo), 'utf8').includes(`id="${ancora}"`)) problemas.push(`${pg}: âncora inexistente → ${href}`);
  }

  // imagem de compartilhamento
  const og = (html.match(/<meta property="og:image" content="https:\/\/orleans-samai\.github\.io\/([^"]+)"/) || [])[1];
  if (og && !existsSync(join(ROOT, og))) problemas.push(`${pg}: og:image não existe → ${og}`);

  for (const largura of LARGURAS) {
    const ctx = await navegador.newContext({ viewport: { width: largura, height: 900 }, reducedMotion: 'reduce' });
    const p = await ctx.newPage();
    const erros = [];
    p.on('pageerror', (e) => erros.push(e.message));
    p.on('requestfailed', (r) => { if (r.url().startsWith(BASE)) erros.push('falhou ' + r.url().replace(BASE, '')); });
    p.on('response', (r) => { if (r.url().startsWith(BASE) && r.status() >= 400 && !pg.startsWith('404')) erros.push(`${r.status()} ${r.url().replace(BASE, '')}`); });
    await p.goto(`${BASE}/${pg}`, { waitUntil: 'networkidle' });
    const larguraTotal = await p.evaluate(() => document.documentElement.scrollWidth);
    if (larguraTotal > largura) problemas.push(`${pg} @${largura}px: rolagem horizontal (${larguraTotal}px)`);
    for (const e of erros) problemas.push(`${pg} @${largura}px: ${e}`);
    await ctx.close();
  }
}

await navegador.close();
servidor.close();
if (problemas.length) {
  console.error(`${problemas.length} problema(s):\n  ` + problemas.join('\n  '));
  process.exit(1);
}
console.log(`${paginas.length} páginas × ${LARGURAS.length} larguras: nenhum problema.`);
