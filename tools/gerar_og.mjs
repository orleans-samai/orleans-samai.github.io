// Gera as imagens de compartilhamento (og/*.jpg, 1200×630) de cada página.
//
// Uso, na raiz do repositório (precisa do Playwright com o Chromium):
//   npm install --no-save playwright && npx playwright install chromium
//   node tools/gerar_og.mjs
//
// Para cada página, lê o título e a descrição do próprio <head> e usa a
// ilustração ou a tela real do topo da página. Rode depois do gerador.
import { createServer } from 'node:http';
import { readFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

async function carregarPlaywright() {
  try { return await import('playwright'); } catch {}
  const global = execSync('npm root -g').toString().trim();
  return import(join(global, 'playwright', 'index.mjs'));
}

// Servidor estático mínimo: a fonte local não carrega por file://.
const TIPOS = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.woff2': 'font/woff2',
  '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml' };
const servidor = createServer((req, res) => {
  const caminho = join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!caminho.startsWith(ROOT) || !existsSync(caminho)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TIPOS[extname(caminho)] || 'application/octet-stream' });
  res.end(readFileSync(caminho));
}).listen(0);
const BASE = `http://127.0.0.1:${servidor.address().port}`;

const meta = (html, prop) => (html.match(new RegExp(`<meta (?:property|name)="${prop}" content="([^"]*)"`)) || [])[1] || '';
const decodificar = (s) => s.replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');

function arte(html) {
  // 1º: primeira tela real da galeria; 2º: imagem do topo (páginas de segmento); 3º: ilustração SVG do topo
  const tela = html.match(/<figure class="shot[^>]*>\s*<a [^>]*>\s*<img src="([^"]+)"/)
    || html.match(/<figure class="p-art[^>]*>\s*<a [^>]*>\s*<img src="([^"]+)"/);
  if (tela) return `<img src="${tela[1].replace(/^\.\.\//, '/')}" style="width:100%;height:100%;object-fit:cover;object-position:top left">`;
  const svg = html.match(/<figure class="p-art[^>]*>\s*(<svg[\s\S]*?<\/svg>)\s*<\/figure>/);
  return svg ? svg[1] : '';
}

function cartao({ titulo, descricao, rotulo, arteHtml, redonda }) {
  return `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/fonts/manrope.css"><style>
  *{box-sizing:border-box}body{margin:0;width:1200px;height:630px;overflow:hidden;font-family:Manrope,sans-serif;color:#eaf1ff;
  background:radial-gradient(700px 420px at 85% 40%,rgba(47,123,255,.28),transparent 70%),#050b1a}
  .l{position:absolute;left:72px;top:64px;width:560px;height:502px;display:flex;flex-direction:column}
  .marca{display:flex;align-items:center;gap:14px;font-weight:800;font-size:30px;letter-spacing:-.02em}
  .rot{margin-top:auto;font-size:20px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:#8fbcff}
  h1{margin:14px 0 18px;font-size:${titulo.length > 34 ? 50 : 60}px;line-height:1.05;font-weight:800;letter-spacing:-.035em}
  p{margin:0;font-size:23px;line-height:1.45;color:#a9bbd8;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
  .r{position:absolute;right:56px;top:95px;width:470px;height:440px;border-radius:26px;overflow:hidden;border:1px solid #244478;
  box-shadow:0 0 80px -10px rgba(47,123,255,.6);background:#081328}
  .r.redonda{width:380px;height:380px;top:125px;right:100px;border-radius:50%;padding:8px;border:0;
  background:conic-gradient(from 210deg,#8fc2ff,#2f7bff 30%,#1747b8 55%,#2f7bff 80%,#8fc2ff)}
  .r.redonda img{border-radius:50%;border:8px solid #050b1a}
  .r svg{width:100%;height:100%}
  </style></head><body>
  <div class="l"><div class="marca"><svg width="40" height="40" viewBox="0 0 32 32"><defs><linearGradient id="lgo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8fc2ff"/><stop offset=".5" stop-color="#2f7bff"/><stop offset="1" stop-color="#1747b8"/></linearGradient></defs><circle cx="16" cy="16" r="11" fill="none" stroke="url(#lgo)" stroke-width="4.5"/><path d="M9 20a9 9 0 0 0 13-12" fill="none" stroke="#050b1a" stroke-width="2.4" stroke-linecap="round"/></svg>Orleans</div>
  <div class="rot">${rotulo}</div><h1>${titulo}</h1><p>${descricao}</p></div>
  <div class="r${redonda ? ' redonda' : ''}">${arteHtml}</div></body></html>`;
}

const paginas = [];
for (const pasta of ['projetos', 'solucoes']) {
  for (const f of readdirSync(join(ROOT, pasta)).filter((f) => f.endsWith('.html'))) {
    const html = readFileSync(join(ROOT, pasta, f), 'utf8');
    const slug = (pasta === 'solucoes' ? 'seg-' : '') + f.replace('.html', '');
    const titulo = decodificar((html.match(/<h1>([^<]+)<\/h1>/) || [])[1] || '');
    paginas.push({ slug, titulo, descricao: decodificar(meta(html, 'description')),
      rotulo: pasta === 'solucoes' ? 'Soluções' : 'Projeto', arteHtml: arte(html) });
  }
}
paginas.push({ slug: 'home', titulo: 'Projetos digitais com visão, estratégia e execução.',
  descricao: 'Sistemas SaaS, apps desktop e mobile e sites para operações pequenas — de oficinas a igrejas.',
  rotulo: 'Portfólio', arteHtml: '<img src="/img/orleans.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%">', redonda: true });

const { chromium } = await carregarPlaywright();
const navegador = await chromium.launch();
const pagina = await navegador.newPage({ viewport: { width: 1200, height: 630 } });
mkdirSync(join(ROOT, 'og'), { recursive: true });
for (const p of paginas) {
  await pagina.route(`${BASE}/__og`, (r) => r.fulfill({ contentType: 'text/html', body: cartao(p) }));
  await pagina.goto(`${BASE}/__og`, { waitUntil: 'networkidle' });
  await pagina.evaluate(() => document.fonts.ready);
  await pagina.screenshot({ path: join(ROOT, 'og', `${p.slug}.jpg`), type: 'jpeg', quality: 86 });
  await pagina.unroute(`${BASE}/__og`);
  console.log(`og/${p.slug}.jpg`);
}
await navegador.close();
servidor.close();
