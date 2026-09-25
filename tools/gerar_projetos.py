"""Gera as páginas de projeto (projetos/*.html) a partir de tools/projetos_dados.py.

Uso, na raiz do repositório:

    python3 tools/gerar_projetos.py              # regera todas
    python3 tools/gerar_projetos.py frota-lite   # regera só as páginas indicadas

Gera as 14 páginas, inclusive a do Lúmen. O CSS compartilhado fica em
projetos/projeto.css. Só usa a biblioteca padrão do Python 3.
"""
import html
import json
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'projetos')
LI = 'https://www.linkedin.com/in/orleanssamai/'

# ── ilustrações ──────────────────────────────────────────────────
F = 'font-family="Manrope,sans-serif"'
def t(x, y, s, size=10, w=700, fill='#eaf1ff', anchor='start', extra=''):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" {F} font-weight="{w}" font-size="{size}" {extra}>{html.escape(s)}</text>'
def r(x, y, w, h, rx=6, fill='#0d1d3b', stroke=None, extra=''):
    st = f' stroke="{stroke}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st} {extra}/>'
def bar(x, y, w, fill='#35507e', h=5):
    return r(x, y, w, h, h / 2, fill)
def window(x, y, w, h, title):
    return (r(x, y, w, h, 12, '#081328', '#244478') + r(x, y, w, 30, 12, '#0a1730') +
            ''.join(f'<circle cx="{x+18+14*i}" cy="{y+15}" r="4" fill="#244478"/>' for i in range(3)) +
            t(x + w / 2, y + 19, title, 10, 700, '#a9bbd8', 'middle'))
def phone(x, y, w, h, rot=0, cx=None, cy=None):
    cx = cx or x + w / 2; cy = cy or y + h / 2
    return (f'<g transform="rotate({rot} {cx} {cy})">' + r(x, y, w, h, 18, '#060d1d', '#5b9dff', 'stroke-opacity=".8" stroke-width="1.5"') +
            r(x + w / 2 - 17, y + 10, 34, 6, 3, '#16294b'))
def svg(inner, label):
    return (f'<svg viewBox="0 0 560 380" role="img" aria-label="{html.escape(label)}"><defs>'
            '<radialGradient id="bg" cx=".65" cy=".3" r=".9"><stop offset="0" stop-color="#143a78"/><stop offset="1" stop-color="#050b1a"/></radialGradient>'
            '<linearGradient id="scr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d2550"/><stop offset="1" stop-color="#040a18"/></linearGradient>'
            '<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f7bff" stop-opacity=".45"/><stop offset="1" stop-color="#2f7bff" stop-opacity="0"/></linearGradient>'
            '</defs><rect width="560" height="380" fill="url(#bg)"/>' + inner + '</svg>')
def pill(x, y, w, label, fill='#2f7bff', txt='#fff'):
    return r(x, y, w, 16, 8, fill, None, 'fill-opacity=".2"' if fill != '#1f63e8' else '') + t(x + w / 2, y + 11, label, 8, 800, txt, 'middle')

LUMEN_ART = '''<!-- janela da cabine -->
        <rect x="28" y="30" width="430" height="300" rx="12" fill="#081328" stroke="#244478"/>
        <rect x="28" y="30" width="430" height="30" rx="12" fill="#0a1730"/>
        <circle cx="46" cy="45" r="4" fill="#244478"/><circle cx="60" cy="45" r="4" fill="#244478"/><circle cx="74" cy="45" r="4" fill="#244478"/>
        <text x="243" y="49" text-anchor="middle" fill="#a9bbd8" font-family="Manrope,sans-serif" font-weight="700" font-size="10">Lúmen — Cabine</text>
        <circle cx="440" cy="45" r="5" fill="#ffb454"><animate attributeName="opacity" values="1;.35;1" dur="2.2s" repeatCount="indefinite"/></circle>
        <!-- programação do culto -->
        <text x="44" y="84" fill="#7289ad" font-family="Manrope,sans-serif" font-weight="800" font-size="8" letter-spacing="1.5">CULTO DE DOMINGO</text>
        <g font-family="Manrope,sans-serif" font-size="9" font-weight="700">
          <rect x="40" y="94" width="112" height="24" rx="6" fill="#0d1d3b"/><text x="50" y="110" fill="#a9bbd8">Abertura</text>
          <rect x="40" y="122" width="112" height="24" rx="6" fill="#1f63e8"/><text x="50" y="138" fill="#fff">Leitura · Salmo 23</text>
          <rect x="40" y="150" width="112" height="24" rx="6" fill="#0d1d3b"/><text x="50" y="166" fill="#a9bbd8">Louvor</text>
          <rect x="40" y="178" width="112" height="24" rx="6" fill="#0d1d3b"/><text x="50" y="194" fill="#a9bbd8">Avisos</text>
          <rect x="40" y="206" width="112" height="24" rx="6" fill="#0d1d3b"/><text x="50" y="222" fill="#a9bbd8">Pregação</text>
        </g>
        <!-- no ar -->
        <rect x="166" y="76" width="278" height="160" rx="8" fill="url(#scr)" stroke="#3b73d6" stroke-opacity=".8"/>
        <rect x="176" y="86" width="48" height="14" rx="7" fill="#ffb454" fill-opacity=".18" stroke="#ffb454" stroke-opacity=".7"/>
        <text x="200" y="96" text-anchor="middle" fill="#ffcf8f" font-family="Manrope,sans-serif" font-weight="800" font-size="7" letter-spacing="1">NO AR</text>
        <text x="305" y="146" text-anchor="middle" fill="#eaf1ff" font-family="Manrope,sans-serif" font-weight="800" font-size="17">O Senhor é o meu pastor;</text>
        <text x="305" y="170" text-anchor="middle" fill="#eaf1ff" font-family="Manrope,sans-serif" font-weight="800" font-size="17">nada me faltará.</text>
        <text x="305" y="204" text-anchor="middle" fill="#8fbcff" font-family="Manrope,sans-serif" font-weight="700" font-size="9" letter-spacing="2.5">SALMOS 23:1 · ALMEIDA 1819</text>
        <!-- próximos slides -->
        <g>
          <rect x="166" y="248" width="86" height="50" rx="6" fill="#0d1d3b" stroke="#2f7bff"/>
          <rect x="262" y="248" width="86" height="50" rx="6" fill="#0d1d3b" stroke="#244478"/>
          <rect x="358" y="248" width="86" height="50" rx="6" fill="#0d1d3b" stroke="#244478"/>
          <rect x="178" y="266" width="62" height="4" rx="2" fill="#5b9dff"/><rect x="186" y="276" width="46" height="4" rx="2" fill="#5b9dff" opacity=".6"/>
          <rect x="274" y="266" width="62" height="4" rx="2" fill="#35507e"/><rect x="282" y="276" width="46" height="4" rx="2" fill="#35507e"/>
          <rect x="370" y="266" width="62" height="4" rx="2" fill="#35507e"/><rect x="378" y="276" width="46" height="4" rx="2" fill="#35507e"/>
        </g>
        <text x="40" y="258" fill="#7289ad" font-family="Manrope,sans-serif" font-weight="700" font-size="8">F5 apresenta</text>
        <text x="40" y="274" fill="#7289ad" font-family="Manrope,sans-serif" font-weight="700" font-size="8">F9 emergência</text>
        <text x="40" y="290" fill="#7289ad" font-family="Manrope,sans-serif" font-weight="700" font-size="8">B apaga o telão</text>
        <!-- celular como controle -->
        <g transform="rotate(6 470 250)">
          <rect x="420" y="150" width="110" height="200" rx="18" fill="#060d1d" stroke="#5b9dff" stroke-opacity=".8" stroke-width="1.5"/>
          <rect x="458" y="160" width="34" height="6" rx="3" fill="#16294b"/>
          <text x="475" y="186" text-anchor="middle" fill="#eaf1ff" font-family="Manrope,sans-serif" font-weight="800" font-size="10">Controle</text>
          <rect x="432" y="196" width="86" height="54" rx="8" fill="url(#scr)" stroke="#244478"/>
          <rect x="442" y="216" width="66" height="4" rx="2" fill="#eaf1ff" opacity=".85"/><rect x="450" y="226" width="50" height="4" rx="2" fill="#eaf1ff" opacity=".6"/>
          <rect x="432" y="262" width="40" height="40" rx="10" fill="#0d1d3b" stroke="#244478"/>
          <rect x="478" y="262" width="40" height="40" rx="10" fill="#1f63e8"/>
          <path d="M456 274l-8 8 8 8" fill="none" stroke="#a9bbd8" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M494 274l8 8-8 8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
          <rect x="432" y="312" width="86" height="22" rx="11" fill="#0d1d3b" stroke="#244478"/>
          <text x="475" y="326.5" text-anchor="middle" fill="#8fbcff" font-family="Manrope,sans-serif" font-weight="800" font-size="8">Pedir versículo</text>
        </g>'''

def art_lumen():
    return svg(LUMEN_ART, 'Ilustração da cabine do Lúmen: programação do culto, versículo no ar e controle pelo celular')

def art_ebike():
    s = window(28, 30, 504, 316, 'EBike Suporte — Chamados')
    s += t(46, 84, 'BICICLETAS', 8, 800, '#7289ad', extra='letter-spacing="1.5"')
    for i, (n, hi) in enumerate([('Aventon Pace · #0231', 1), ('Caloi E-Vibe · #0198', 0), ('Sense Impulse · #0177', 0), ('Oggi Big Wheel · #0142', 0)]):
        s += r(40, 94 + i * 30, 150, 24, 6, '#1f63e8' if hi else '#0d1d3b') + t(50, 110 + i * 30, n, 9, 700, '#fff' if hi else '#a9bbd8')
    s += r(204, 76, 316, 256, 8, 'url(#scr)', '#3b73d6', 'stroke-opacity=".7"')
    s += t(218, 98, 'Chamado #128 · Freio traseiro', 12, 800)
    s += pill(420, 86, 88, 'EM ANDAMENTO', '#ffb454', '#ffcf8f')
    s += r(218, 112, 200, 40, 10, '#0d1d3b', '#244478') + t(230, 128, 'Cliente', 8, 800, '#8fbcff') + t(230, 143, 'O freio está fazendo barulho.', 9, 600, '#a9bbd8')
    s += r(302, 162, 204, 40, 10, '#1f63e8') + t(314, 178, 'Loja', 8, 800, '#dbe8ff') + t(314, 193, 'Pode trazer amanhã às 10h.', 9, 700, '#fff')
    s += r(218, 212, 200, 40, 10, '#0d1d3b', '#244478') + t(230, 228, 'Cliente', 8, 800, '#8fbcff') + t(230, 243, 'Combinado, obrigado!', 9, 600, '#a9bbd8')
    s += r(218, 272, 288, 44, 8, '#081328', '#244478') + t(230, 290, 'Status', 8, 800, '#7289ad')
    for i, (lab, on) in enumerate([('Aberto', 1), ('Em andamento', 1), ('Aguardando', 0), ('Resolvido', 0)]):
        s += f'<circle cx="{240 + i * 80}" cy="303" r="5" fill="{"#5b9dff" if on else "#16294b"}"/>' + t(250 + i * 80, 306, lab, 8, 700, '#a9bbd8' if on else '#7289ad')
    return svg(s, 'Ilustração do EBike Suporte: lista de bicicletas e um chamado com mensagens entre cliente e loja')

def art_qr(qr):
    s = phone(70, 36, 150, 300, -6)
    s += t(145, 80, 'Mesa 12', 13, 800, anchor='middle')
    s += r(95, 92, 100, 100, 8, '#eaf1ff') + qr
    s += r(90, 208, 110, 26, 13, '#1f63e8') + t(145, 225, 'Fazer pedido', 10, 800, '#fff', 'middle')
    s += r(90, 246, 110, 18, 6, '#0d1d3b') + t(100, 259, 'X-Burger ×2', 8, 700, '#a9bbd8') + t(190, 259, 'R$ 52', 8, 800, '#eaf1ff', 'end')
    s += r(90, 270, 110, 18, 6, '#0d1d3b') + t(100, 283, 'Suco ×2', 8, 700, '#a9bbd8') + t(190, 283, 'R$ 18', 8, 800, '#eaf1ff', 'end') + '</g>'
    s += r(262, 70, 240, 104, 12, '#081328', '#244478') + t(278, 94, 'Fila do garçom', 11, 800)
    s += f'<g><circle cx="480" cy="90" r="8" fill="#ffb454" fill-opacity=".25" stroke="#ffb454"/>' + t(480, 94, '!', 10, 800, '#ffcf8f', 'middle') + '</g>'
    for i, (m, st) in enumerate([('Mesa 12 · 4 itens', 'NOVO'), ('Mesa 5 · 2 itens', 'NA COZINHA')]):
        s += r(274, 106 + i * 30, 216, 24, 6, '#0d1d3b') + t(284, 122 + i * 30, m, 9, 700, '#a9bbd8') + t(482, 122 + i * 30, st, 7.5, 800, '#8fbcff', 'end')
    s += '<g transform="rotate(4 380 270)">'
    s += r(318, 196, 124, 18, 4, '#244478') + '<path d="M326 214 H434 V330 l-7 5 -7-5 -7 5 -7-5 -7 5 -7-5 -7 5 -7-5 -7 5 -7-5 -7 5 -7-5 -7 5 -7-5 -4 3Z" fill="#eaf1ff"/>'
    s += t(380, 236, 'COZINHA · MESA 12', 8, 800, '#050b1a', 'middle', 'letter-spacing="1"') + '<path d="M336 244 H424" stroke="#050b1a" stroke-dasharray="3 3"/>'
    for i, it in enumerate(['2× X-Burger', '2× Suco de laranja', 'Sem cebola']):
        s += t(338, 262 + i * 16, it, 9, 700, '#081328')
    s += '</g>'
    return svg(s, 'Ilustração do Autoatendimento QR: celular com QR code da mesa, fila do garçom e cupom impresso na cozinha')

def art_frota():
    s = window(28, 30, 504, 316, 'Frota Lite — Manutenção')
    s += r(28, 60, 110, 286, 0, '#0a1730')
    for i, (lab, hi) in enumerate([('Painel', 1), ('Veículos', 0), ('Agenda', 0), ('Despesas', 0), ('Equipe', 0)]):
        s += r(40, 76 + i * 30, 86, 22, 6, '#1f63e8' if hi else '#0a1730') + t(52, 91 + i * 30, lab, 9, 700, '#fff' if hi else '#a9bbd8')
    for i, (n, lab, col) in enumerate([('2', 'Atrasados', '#ffb454'), ('5', 'Próximos', '#8fbcff'), ('14', 'Em dia', '#eaf1ff')]):
        x = 154 + i * 122
        s += r(x, 76, 110, 56, 8, '#0d1d3b', '#244478') + t(x + 12, 102, n, 20, 800, col) + t(x + 12, 121, lab, 9, 700, '#a9bbd8')
    rows = [('Fiorino ABC-1D23', 'Troca de óleo', 'ATRASADO', '#ffb454'), ('Strada DEF-4G56', 'Pneus', 'PRÓXIMO', '#8fbcff'), ('Saveiro GHI-7J89', 'Revisão 40 mil', 'EM DIA', '#a9bbd8')]
    for i, (v, sv, st, c) in enumerate(rows):
        y = 146 + i * 30
        s += r(154, y, 354, 24, 6, '#0a1730') + f'<rect x="154" y="{y}" width="4" height="24" rx="2" fill="{c}"/>' + t(166, y + 16, v, 9, 800) + t(300, y + 16, sv, 9, 600, '#a9bbd8') + t(500, y + 16, st, 7.5, 800, c, 'end')
    s += t(154, 256, 'Custo por km', 9, 800, '#7289ad')
    s += '<path d="M154 330 L200 316 L246 320 L292 300 L338 306 L384 286 L430 292 L508 268 L508 334 L154 334Z" fill="url(#area)"/>'
    s += '<path d="M154 330 L200 316 L246 320 L292 300 L338 306 L384 286 L430 292 L508 268" fill="none" stroke="#5b9dff" stroke-width="2"/>'
    return svg(s, 'Ilustração do Frota Lite: painel com veículos atrasados, próximos e em dia e gráfico de custo por km')

def art_png():
    s = phone(190, 26, 180, 330, 0)
    s += t(280, 70, 'Fundo Fora', 12, 800, anchor='middle')
    s += '<defs><pattern id="chk" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#1a2b4a"/><rect width="8" height="8" fill="#2a3f66"/><rect x="8" y="8" width="8" height="8" fill="#2a3f66"/></pattern>'
    s += '<clipPath id="half"><rect x="206" y="84" width="74" height="190"/></clipPath></defs>'
    s += r(206, 84, 148, 190, 10, 'url(#chk)')
    s += f'<g clip-path="url(#half)">' + r(206, 84, 148, 190, 10, '#3a5a8f') + '<circle cx="230" cy="112" r="30" fill="#5b7fb8" opacity=".6"/></g>'
    s += '<path d="M280 84 V274" stroke="#eaf1ff" stroke-width="2" stroke-dasharray="4 4"/>'
    s += '<g><rect x="244" y="150" width="72" height="84" rx="10" fill="#eaf1ff"/><rect x="316" y="170" width="18" height="40" rx="9" fill="none" stroke="#eaf1ff" stroke-width="8"/><rect x="254" y="164" width="52" height="8" rx="4" fill="#2f7bff"/></g>'
    s += t(232, 266, 'ANTES', 8, 800, '#eaf1ff', 'middle', 'letter-spacing="1"') + t(328, 266, 'DEPOIS', 8, 800, '#eaf1ff', 'middle', 'letter-spacing="1"')
    s += r(206, 288, 148, 26, 13, '#1f63e8') + t(280, 305, 'Salvar PNG', 10, 800, '#fff', 'middle') + '</g>'
    s += r(392, 110, 138, 64, 12, '#081328', '#3b73d6', 'stroke-opacity=".7"') + t(406, 134, 'Processado no', 9, 700, '#a9bbd8') + t(406, 156, 'próprio celular', 13, 800)
    s += r(30, 214, 138, 64, 12, '#081328', '#3b73d6', 'stroke-opacity=".7"') + t(44, 238, 'Modelo de IA', 9, 700, '#a9bbd8') + t(44, 260, '~4,4 MB', 16, 800)
    return svg(s, 'Ilustração do Fundo Fora: celular mostrando uma caneca antes e depois de remover o fundo')

def art_voice():
    s = phone(200, 26, 170, 330, 0)
    s += t(285, 70, 'Voice Finance', 12, 800, anchor='middle')
    s += r(214, 86, 142, 56, 14, '#0d1d3b', '#244478') + t(226, 106, 'Você disse', 8, 800, '#8fbcff') + t(226, 124, '“Gastei 45 no', 10, 700) + t(226, 137, 'mercado hoje”', 10, 700)
    s += r(214, 154, 142, 110, 12, 'url(#scr)', '#3b73d6', 'stroke-opacity=".7"')
    for i, (k, v) in enumerate([('Valor', 'R$ 45,00'), ('Categoria', 'Mercado'), ('Data', 'Hoje')]):
        s += t(226, 180 + i * 28, k, 8, 700, '#7289ad') + t(344, 180 + i * 28, v, 10, 800, '#eaf1ff', 'end')
    s += r(214, 274, 66, 24, 12, '#0d1d3b', '#244478') + t(247, 290, 'Editar', 9, 800, '#a9bbd8', 'middle')
    s += r(290, 274, 66, 24, 12, '#1f63e8') + t(323, 290, 'Salvar', 9, 800, '#fff', 'middle')
    s += '<circle cx="285" cy="324" r="16" fill="#2f7bff" fill-opacity=".25" stroke="#5b9dff"/><rect x="280" y="314" width="10" height="14" rx="5" fill="#eaf1ff"/><path d="M276 324a9 9 0 0 0 18 0M285 333v3" stroke="#eaf1ff" stroke-width="1.8" fill="none" stroke-linecap="round"/></g>'
    for i, h in enumerate([14, 30, 46, 24, 58, 36, 20, 42, 28, 12]):
        s += r(52 + i * 12, 190 - h / 2, 6, h, 3, '#5b9dff', None, f'opacity="{.4 + (i % 3) * .2:.1f}"')
    for i, h in enumerate([12, 28, 40, 22, 50, 34, 18, 36, 24, 10]):
        s += r(392 + i * 12, 190 - h / 2, 6, h, 3, '#5b9dff', None, f'opacity="{.4 + (i % 3) * .2:.1f}"')
    return svg(s, 'Ilustração do Voice Finance: frase falada virando lançamento com valor, categoria e data')

def art_chamados():
    s = window(28, 30, 504, 316, 'Service Desk — Chamados')
    for i, (n, lab) in enumerate([('18', 'Abertos'), ('7', 'Em atendimento'), ('3', 'SLA em risco')]):
        x = 44 + i * 160
        s += r(x, 72, 148, 52, 8, '#0d1d3b', '#244478') + t(x + 12, 98, n, 20, 800, '#ffcf8f' if i == 2 else '#eaf1ff') + t(x + 12, 116, lab, 9, 700, '#a9bbd8')
    s += t(44, 148, 'Nº', 8, 800, '#7289ad') + t(96, 148, 'ASSUNTO', 8, 800, '#7289ad') + t(330, 148, 'NÍVEL', 8, 800, '#7289ad') + t(504, 148, 'SLA', 8, 800, '#7289ad', 'end')
    rows = [('#1042', 'VPN não conecta', 'N2', '1h 20m', '#ffb454'), ('#1041', 'Impressora offline', 'N1', '3h 05m', '#8fbcff'), ('#1039', 'Senha expirada', 'N1', '5h 40m', '#8fbcff'), ('#1036', 'E-mail não sincroniza', 'N2', '7h 10m', '#8fbcff')]
    for i, (n, a, lv, sla, c) in enumerate(rows):
        y = 156 + i * 30
        s += r(40, y, 480, 24, 6, '#0a1730') + t(50, y + 16, n, 9, 800, '#8fbcff') + t(96, y + 16, a, 9, 700) + t(330, y + 16, lv, 9, 800, '#a9bbd8') + t(508, y + 16, sla, 9, 800, c, 'end')
    s += r(40, 284, 480, 46, 8, '#081328', '#3b73d6', 'stroke-opacity=".6"') + t(54, 303, 'Laboratório N1/N2', 10, 800) + t(54, 319, 'Cenário: usuário sem acesso à rede — resolva e confira o gabarito.', 9, 600, '#a9bbd8')
    return svg(s, 'Ilustração do Sistema de Chamados: fila de chamados com SLA e o laboratório de treinamento')

def art_orch():
    s = window(28, 30, 504, 316, 'terminal — ai-orchestrator')
    lines = [('$ ai-orchestrator run "cadastro de clientes"', '#eaf1ff'), ('', ''), ('[1/5] Planejar ........ Antigravity  ✓', '#8fbcff'), ('      Aprovar o plano? [s/n] s', '#a9bbd8'),
             ('[2/5] Implementar ..... Codex        ✓', '#8fbcff'), ('      Aprovar a implementação? [s/n] s', '#a9bbd8'), ('[3/5] Revisar ......... Claude       ✓', '#8fbcff'),
             ('      3 achados — corrigir quais? [1,3]', '#ffcf8f'), ('[4/5] Validar achados .. aguardando você', '#a9bbd8'), ('', ''), ('Nada é commitado sem a sua decisão.', '#7289ad')]
    for i, (l, c) in enumerate(lines):
        if l:
            s += f'<text x="48" y="{86 + i * 22}" fill="{c}" font-family="ui-monospace,Menlo,monospace" font-size="11" font-weight="600" xml:space="preserve">{html.escape(l)}</text>'
    s += r(48, 318, 8, 14, 1, '#5b9dff', None, '') .replace('/>', '><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    return svg(s, 'Ilustração do AI Orchestrator: terminal com as fases planejar, implementar e revisar, cada uma pedindo aprovação')

def art_excel():
    s = window(28, 30, 504, 316, 'Insight Dashboard — vendas_2026.xlsx')
    for i, (n, lab) in enumerate([('R$ 1,2 mi', 'Receita'), ('+18%', 'vs. ano anterior'), ('4.310', 'Pedidos'), ('3', 'Anomalias')]):
        x = 44 + i * 120
        s += r(x, 72, 110, 52, 8, '#0d1d3b', '#244478') + t(x + 12, 98, n, 15, 800, '#ffcf8f' if i == 3 else '#eaf1ff') + t(x + 12, 116, lab, 8.5, 700, '#a9bbd8')
    s += r(44, 138, 290, 190, 8, '#0a1730', '#16294b') + t(58, 158, 'Receita por mês', 9, 800, '#7289ad')
    for i, h in enumerate([60, 74, 58, 90, 84, 102, 96, 120, 112, 134]):
        s += r(62 + i * 26, 314 - h, 16, h, 3, '#2f7bff' if i != 7 else '#ffb454', None, 'opacity=".9"')
    s += r(346, 138, 170, 190, 8, '#0a1730', '#16294b') + t(360, 158, 'Por categoria', 9, 800, '#7289ad')
    s += '<circle cx="431" cy="236" r="46" fill="none" stroke="#16294b" stroke-width="18"/>'
    s += '<circle cx="431" cy="236" r="46" fill="none" stroke="#2f7bff" stroke-width="18" stroke-dasharray="130 289" transform="rotate(-90 431 236)"/>'
    s += '<circle cx="431" cy="236" r="46" fill="none" stroke="#8fbcff" stroke-width="18" stroke-dasharray="80 289" stroke-dashoffset="-130" transform="rotate(-90 431 236)"/>'
    s += '<circle cx="431" cy="236" r="46" fill="none" stroke="#35507e" stroke-width="18" stroke-dasharray="50 289" stroke-dashoffset="-210" transform="rotate(-90 431 236)"/>'
    return svg(s, 'Ilustração do Excel Dashboard: indicadores, gráfico de receita por mês e gráfico por categoria gerados da planilha')

def art_fest():
    s = window(28, 30, 330, 316, 'Central da Festividade')
    s += t(46, 82, 'PROGRAMAÇÃO DE HOJE', 8, 800, '#7289ad', extra='letter-spacing="1.5"')
    for i, (h, lab, hi) in enumerate([('19:00', 'Abertura e louvor', 0), ('19:40', 'Avisos', 0), ('20:00', 'Pregação', 1), ('21:10', 'Encerramento', 0)]):
        y = 92 + i * 34
        s += r(40, y, 306, 28, 6, '#1f63e8' if hi else '#0d1d3b') + t(52, y + 18, h, 9, 800, '#fff' if hi else '#8fbcff') + t(96, y + 18, lab, 9.5, 700, '#fff' if hi else '#a9bbd8')
    s += t(46, 250, 'ESCALA', 8, 800, '#7289ad', extra='letter-spacing="1.5"')
    for i, (n, st, c) in enumerate([('Recepção · Ana', 'CONFIRMOU', '#8fbcff'), ('Som · Marcos', 'CONFIRMOU', '#8fbcff'), ('Mídia · João', 'NÃO PODE', '#ffcf8f')]):
        y = 260 + i * 26
        s += r(40, y, 306, 20, 5, '#0a1730') + t(52, y + 14, n, 9, 700, '#a9bbd8') + t(336, y + 14, st, 7.5, 800, c, 'end')
    s += phone(386, 70, 150, 280, 5)
    s += pill(420, 96, 82, '● AO VIVO', '#ffb454', '#ffcf8f')
    s += t(461, 136, 'Painel do dirigente', 9, 800, anchor='middle')
    for i, (n, lab) in enumerate([('48', 'visitantes'), ('12', 'pedidos de oração')]):
        y = 150 + i * 62
        s += r(400, y, 122, 52, 10, '#0d1d3b', '#244478') + t(412, y + 26, n, 18, 800) + t(412, y + 43, lab, 8.5, 700, '#a9bbd8')
    s += r(400, 278, 122, 26, 13, '#1f63e8') + t(461, 295, 'Próximo: Pregação', 8.5, 800, '#fff', 'middle') + '</g>'
    return svg(s, 'Ilustração da Central da Festividade: programação, escala de voluntários e painel do dirigente ao vivo no celular')

def art_slide():
    s = '<g transform="rotate(-5 130 190)">' + r(52, 60, 150, 200, 6, '#eaf1ff') + r(52, 60, 150, 22, 6, '#c9d8f2')
    s += t(64, 75, 'pregacao-domingo.pdf', 8, 800, '#081328')
    for i, w in enumerate([120, 110, 126, 90, 118, 104, 124, 80, 112, 96]):
        s += bar(64, 96 + i * 15, w, '#9fb2d0', 5)
    s += '</g>'
    s += '<path d="M226 190 H290" stroke="#5b9dff" stroke-width="2.5" stroke-dasharray="6 5"/><path d="M284 182 l10 8 -10 8" fill="none" stroke="#5b9dff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    s += r(306, 104, 224, 126, 10, 'url(#scr)', '#3b73d6', 'stroke-opacity=".8"')
    s += t(418, 158, 'Buscai primeiro', 16, 800, anchor='middle') + t(418, 180, 'o Reino de Deus', 16, 800, anchor='middle') + t(418, 204, 'MATEUS 6:33', 8, 800, '#8fbcff', 'middle', 'letter-spacing="2"')
    for i in range(3):
        s += r(306 + i * 78, 244, 68, 40, 6, '#0d1d3b', '#2f7bff' if i == 0 else '#244478') + bar(316 + i * 78, 260, 48, '#5b9dff' if i == 0 else '#35507e', 4)
    s += t(418, 312, '16:9 · tema escolhido pelo conteúdo', 9, 700, '#a9bbd8', 'middle')
    return svg(s, 'Ilustração do SlideRevive: PDF da pregação sendo convertido em slides 16:9 para o telão')

def art_netdiag():
    s = '<g fill="#8fbcff" opacity=".5"><circle cx="40" cy="40" r="1"/><circle cx="520" cy="30" r="1.2"/><circle cx="540" cy="140" r=".9"/><circle cx="60" cy="330" r="1"/></g>'
    s += '<defs><radialGradient id="gl" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#2a63c6"/><stop offset=".7" stop-color="#0b2149"/><stop offset="1" stop-color="#061129"/></radialGradient></defs>'
    s += '<circle cx="190" cy="196" r="130" fill="url(#gl)" stroke="#5b9dff" stroke-opacity=".6"/>'
    s += '<g fill="none" stroke="#5b9dff" stroke-opacity=".28"><ellipse cx="190" cy="196" rx="50" ry="130"/><ellipse cx="190" cy="196" rx="96" ry="130"/><path d="M60 196h260M72 140h236M72 252h236"/></g>'
    s += '<g stroke="#8fbcff" stroke-width="1.4" fill="none"><path d="M130 150 Q190 90 260 160"/><path d="M260 160 Q290 220 220 260"/><path d="M130 150 Q100 210 150 250"/></g>'
    s += '<g fill="#eaf1ff"><circle cx="130" cy="150" r="4"/><circle cx="260" cy="160" r="4"/><circle cx="220" cy="260" r="4"/><circle cx="150" cy="250" r="4"/></g>'
    s += r(330, 70, 200, 250, 10, '#eaf1ff') + r(330, 70, 200, 30, 10, '#c9d8f2') + t(344, 90, 'Relatório de diagnóstico', 9.5, 800, '#081328')
    for i, (k, v, ok) in enumerate([('Gateway', '2 ms', 1), ('DNS', '18 ms', 1), ('HTTPS', 'OK', 1), ('Perda de pacotes', '0%', 1), ('Porta 3389', 'fechada', 0)]):
        y = 118 + i * 26
        s += t(344, y, k, 9, 700, '#35507e') + t(516, y, v, 9, 800, '#1747b8' if ok else '#b35c00', 'end')
    s += r(344, 256, 172, 48, 6, '#dbe8ff') + t(354, 274, 'Causa provável', 8, 800, '#1747b8') + t(354, 292, 'Firewall bloqueando RDP', 9, 800, '#081328')
    return svg(s, 'Ilustração do NetDiag Pro: mapa de rede e relatório de diagnóstico com causa provável')

def art_bps():
    s = window(28, 30, 504, 316, 'Backend Python Simulator')
    s += r(40, 70, 170, 262, 8, '#0a1730', '#16294b') + t(52, 90, 'TICKET BPS-214', 8, 800, '#8fbcff', extra='letter-spacing="1"')
    s += t(52, 110, 'Endpoint de pedidos', 10, 800) + t(52, 124, 'retorna 500', 10, 800)
    for i, w in enumerate([140, 120, 132, 96]):
        s += bar(52, 140 + i * 13, w)
    s += pill(52, 202, 70, 'PRIORIDADE ALTA', '#ffb454', '#ffcf8f')
    s += r(52, 232, 146, 42, 8, '#0d1d3b', '#244478') + t(62, 250, 'Nível', 8, 700, '#7289ad') + t(62, 266, 'Pleno II · 2.340 XP', 9, 800)
    s += r(222, 70, 298, 180, 8, '#040a18', '#16294b')
    code = [('def', ' listar_pedidos(db):', '#8fbcff'), ('    ', 'itens = db.query(Pedido)', '#eaf1ff'), ('    ', '.filter(Pedido.ativo)', '#eaf1ff'), ('    ', 'return [p.to_dict()', '#eaf1ff'), ('    ', '        for p in itens]', '#eaf1ff')]
    for i, (kw, rest, c) in enumerate(code):
        s += f'<text x="236" y="{96 + i * 20}" font-family="ui-monospace,Menlo,monospace" font-size="11" font-weight="600" xml:space="preserve"><tspan fill="#ff9ad5">{kw}</tspan><tspan fill="{c}">{html.escape(rest)}</tspan></text>'
    s += r(222, 262, 298, 70, 8, '#081328', '#3b73d6', 'stroke-opacity=".6"') + t(236, 282, 'Testes', 9, 800, '#7289ad')
    s += t(236, 302, '✓ 6 de 6 passaram', 12, 800, '#8fbcff') + t(236, 320, '+120 XP · próximo nível em 160 XP', 9, 700, '#a9bbd8')
    return svg(s, 'Ilustração do Backend Python Simulator: ticket, código corrigido e testes aprovados')

def art_acc():
    s = window(28, 30, 504, 316, 'AI Control Center')
    s += t(44, 84, 'ESTA SEMANA', 8, 800, '#7289ad', extra='letter-spacing="1.5"')
    for i, (n, lab) in enumerate([('23', 'sessões'), ('41', 'commits'), ('≈ US$ 12', 'custo estimado')]):
        x = 44 + i * 118
        s += r(x, 94, 108, 50, 8, '#0d1d3b', '#244478') + t(x + 12, 118, n, 15, 800) + t(x + 12, 135, lab, 8.5, 700, '#a9bbd8')
    s += t(44, 170, 'LINHA DO TEMPO', 8, 800, '#7289ad', extra='letter-spacing="1.5"')
    for i, (d, lab, w) in enumerate([('seg', 'frota-lite', 120), ('ter', 'igreja-projetor', 200), ('qua', 'igreja-projetor', 160), ('qui', 'central-festividade', 90), ('sex', 'site', 60)]):
        y = 180 + i * 28
        s += t(44, y + 14, d, 9, 700, '#7289ad') + r(78, y + 4, w, 14, 7, '#2f7bff', None, 'opacity=".85"') + t(84 + w, y + 15, lab, 8.5, 700, '#a9bbd8')
    s += r(386, 94, 130, 234, 8, '#0a1730', '#16294b') + t(398, 114, 'Ranking', 9, 800, '#7289ad')
    for i, (n, sc) in enumerate([('Lúmen', 92), ('Frota Lite', 88), ('NetDiag', 85), ('Autoatend.', 83), ('EBike', 71)]):
        y = 128 + i * 38
        s += t(398, y + 12, f'{i + 1}. {n}', 9, 800) + r(398, y + 20, 104, 5, 2.5, '#16294b') + r(398, y + 20, sc * 1.04, 5, 2.5, '#5b9dff')
    return svg(s, 'Ilustração do AI Control Center: resumo da semana, linha do tempo por projeto e ranking do portfólio')

# QR code determinístico (mesmo desenho da página inicial, em escala maior)
import random
random.seed(7)
def qr_svg(x0, y0, size, N=21):
    c = size / N; cells = []
    finder = lambda rr, q: (rr < 7 and q < 7) or (rr < 7 and q >= N - 7) or (rr >= N - 7 and q < 7)
    for rr in range(N):
        for q in range(N):
            if not finder(rr, q) and random.random() < .47:
                cells.append(f'<rect x="{x0+q*c:.1f}" y="{y0+rr*c:.1f}" width="{c:.1f}" height="{c:.1f}"/>')
    fs = ''
    for fr, fq in [(0, 0), (0, N - 7), (N - 7, 0)]:
        X = x0 + fq * c; Y = y0 + fr * c
        fs += f'<rect x="{X+c/2:.1f}" y="{Y+c/2:.1f}" width="{6*c:.1f}" height="{6*c:.1f}" fill="none" stroke="#050b1a" stroke-width="{c:.1f}"/><rect x="{X+2*c:.1f}" y="{Y+2*c:.1f}" width="{3*c:.1f}" height="{3*c:.1f}"/>'
    return '<g fill="#050b1a">' + fs + ''.join(cells) + '</g>'

# ── modelo da página ─────────────────────────────────────────────
ICONS = {
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'arrow-up': '<path d="M7 17 17 7M8 7h9v9"/>',
 'check': '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
 'code': '<path d="m8 8-5 4 5 4M16 8l5 4-5 4M14 4l-4 16"/>',
 'download': '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
 'wifi-off': '<path d="M2 2l20 20M8.5 16.5a5 5 0 0 1 7 0M5 12.9a10 10 0 0 1 5.2-2.8M19 12.9a10 10 0 0 0-2.3-1.7M2 8.8a15 15 0 0 1 4.2-2.6M22 8.8A15 15 0 0 0 11 5M12 20h.01"/>',
 'lock': '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 'shield': '<path d="M12 3 4 6v6c0 5 3.4 8.3 8 9 4.6-.7 8-4 8-9V6l-8-3z"/><path d="m9 12 2 2 4-4"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.2a6.5 6.5 0 0 1 3.5 5.8"/>',
 'history': '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5M12 7v5l3 2"/>',
 'printer': '<path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="7"/>',
 'phone': '<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
 'send': '<path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z"/>',
 'gauge': '<path d="M12 14l4-4"/><path d="M3.3 19a10 10 0 1 1 17.4 0"/>',
 'feather': '<path d="M20 4c-6 0-12 4-14 12l-2 4M8 16h7M11 12h6"/>',
 'zap': '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
 'gift': '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M5 12v9h14v-9M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
 'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
 'moon': '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
 'cpu': '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
 'eye': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 'flask': '<path d="M9 3h6M10 3v6L4.5 18.5A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.5L14 9V3"/><path d="M7.5 15h9"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'list': '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
 'hand': '<path d="M18 11V6a2 2 0 0 0-4 0v5M14 10V4a2 2 0 0 0-4 0v6M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.9-6-2.4l-3.6-3.6a2 2 0 0 1 2.8-2.8L7 15"/>',
 'sparkles': '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 17l.8 2.2L22 20l-2.2.8L19 23l-.8-2.2L16 20l2.2-.8z"/>',
 'chart': '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
 'file': '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
 'monitor': '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
 'layers': '<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3 13 9 5 9-5"/>',
 'award': '<circle cx="12" cy="9" r="6"/><path d="M8.5 14 7 22l5-3 5 3-1.5-8"/>',
 'swap': '<path d="M4 8h13l-3-3M20 16H7l3 3"/>',
 'terminal': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3M13 15h4"/>',
 'git': '<circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="9" r="2.5"/><path d="M6 8.5v7M18 11.5c0 3-3 3.5-6 4.5"/>',
}
LOGO = '<symbol id="i-logo" viewBox="0 0 32 32"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8fc2ff"/><stop offset=".5" stop-color="#2f7bff"/><stop offset="1" stop-color="#1747b8"/></linearGradient></defs><circle cx="16" cy="16" r="11" fill="none" stroke="url(#lg)" stroke-width="4.5"/><path d="M9 20a9 9 0 0 0 13-12" fill="none" stroke="#050b1a" stroke-width="2.4" stroke-linecap="round"/></symbol>'
def ico(name): return f'<svg class="ico" aria-hidden="true"><use href="#i-{name}"/></svg>'
E = html.escape

SITE_URL = 'https://orleans-samai.github.io'
FAVICON = 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2222%22 fill=%22%23050b1a%22/><circle cx=%2250%22 cy=%2250%22 r=%2230%22 fill=%22none%22 stroke=%22%232f7bff%22 stroke-width=%2210%22/><circle cx=%2257%22 cy=%2244%22 r=%2216%22 fill=%22%23050b1a%22/></svg>'

def head_html(title, desc, og_title, path, og_slug, jsonld, css="projeto.css"):
    """<head> comum: fonte local, canônico, imagem de compartilhamento e dados estruturados."""
    url = f'{SITE_URL}/{path}'
    img = f'{SITE_URL}/og/{og_slug}.jpg'
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{E(og_title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#050b1a">
<link rel="icon" href="{FAVICON}">
<link rel="preload" href="../fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../fonts/manrope.css">
<link rel="stylesheet" href="{css}">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<script src="../assets/site.js" defer></script>
</head>
<body>
"""

PESSOA = {'@type': 'Person', 'name': 'Orleans', 'url': SITE_URL + '/',
          'sameAs': ['https://www.linkedin.com/in/orleanssamai/', 'https://github.com/orleans-samai']}

def jsonld_projeto(p):
    d = {'@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': p['name'],
         'description': p['desc'], 'url': f"{SITE_URL}/projetos/{p['slug']}.html",
         'applicationCategory': 'BusinessApplication', 'author': PESSOA,
         'image': f"{SITE_URL}/og/{p['slug']}.jpg"}
    if p.get('os'): d['operatingSystem'] = p['os']
    return d

def nav_html():
    return f"""<nav class="nav" aria-label="Principal">
  <div class="wrap nav-inner">
    <a class="brand" href="../index.html" aria-label="Orleans, página inicial"><svg aria-hidden="true"><use href="#i-logo"/></svg>Orleans</a>
    <ul class="nav-links">
      <li><a href="../index.html#projetos">Projetos</a></li>
      <li><a href="../index.html#segmentos">Soluções</a></li>
      <li><a href="../roadmap.html">Roadmap</a></li>
    </ul>
    <a class="nav-li" href="https://www.linkedin.com/in/orleanssamai/" target="_blank" rel="noopener" aria-label="LinkedIn de Orleans" title="LinkedIn" data-goatcounter-click="topo-linkedin"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4v11H3v-11zm6.5 0h3.8v1.5h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1v5.45h-4v-4.83c0-1.15-.02-2.63-1.6-2.63-1.6 0-1.85 1.25-1.85 2.55v4.91h-4v-11z"/></svg></a>
    <a class="btn btn-sm" href="#contato">Fale comigo {ico("arrow")}</a>
  </div>
</nav>"""

def cta_html(titulo, texto, assunto):
    return f"""  <section id="contato" class="cta glass" aria-labelledby="cta-title">
    <div>
      <h2 id="cta-title">{E(titulo)}</h2>
      <p>{E(texto)}</p>
    </div>
    <div class="cta-actions" data-contato data-assunto="{E(assunto)}">
      <a class="btn btn-primary" href="{LI}" target="_blank" rel="noopener" data-goatcounter-click="contato-linkedin">Fale comigo no LinkedIn {ico("arrow-up")}</a>
    </div>
  </section>"""

def footer_html():
    return f"""<footer class="foot">
  <div class="wrap foot-inner">
    <span>© <span id="year">2026</span> Orleans</span>
    <nav aria-label="Rodapé">
      <a href="../index.html">Início</a>
      <a href="../index.html#projetos">Projetos</a>
      <a href="../solucoes/igrejas.html">Igrejas</a>
      <a href="../solucoes/suporte-ti.html">Suporte de TI</a>
      <a href="../solucoes/pequenos-negocios.html">Pequenos negócios</a>
      <a href="../roadmap.html">Roadmap</a>
      <a href="https://github.com/orleans-samai" target="_blank" rel="noopener">GitHub</a>
      <a href="{LI}" target="_blank" rel="noopener">LinkedIn</a>
    </nav>
  </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>"""


def page(p):
    used = set(['arrow', 'arrow-up', 'check', 'code', 'swap'])
    used |= {w[0] for w in p['why']}
    for a in p['actions']: used.add(a.get('icon', 'arrow'))
    syms = ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{ICONS[k]}</symbol>' for k in sorted(used)) + LOGO
    chips = f'<span class="chip"><span class="dot" aria-hidden="true"></span>{E(p["status"])}</span>' + ''.join(f'<span class="chip dim">{E(c)}</span>' for c in p['chips'])
    meter = ''
    if p.get('percent') is not None:
        meter = f'<div class="meter"><div class="meter-bar" role="img" aria-label="{p["percent"]}% concluído"><i style="width:{p["percent"]}%"></i></div><span><b>{p["percent"]}%</b> até a versão vendável</span></div>'
    acts = ''
    for a in p['actions']:
        ext = ' target="_blank" rel="noopener"' if a['href'].startswith('http') else ''
        cls = 'btn btn-primary' if a.get('primary') else 'btn'
        icon = ico(a.get('icon', 'arrow'))
        acts += f'<a class="{cls}" href="{a["href"]}"{ext}>' + (f'{icon}{E(a["label"])}' if a.get('icon_first') else f'{E(a["label"])} {icon}') + '</a>'
    note = f'<p class="p-note">{E(p["hero_note"])}</p>' if p.get('hero_note') else ''
    proof = ''.join(f'<div class="proof-item"><b>{E(b)}</b><span>{E(sp)}</span></div>' for b, sp in p['proof'])
    pcols = len(p['proof'])
    done = ''.join(f'<li>{ico("check")}<span><b>{E(b)}</b>{E(rest)}</span></li>' for b, rest in p['done'])
    if p.get('timeline'):
        second = '<h3>Como chegou até aqui</h3><ol class="timeline">' + ''.join(f'<li><time datetime="{d}">{E(lab)}</time><p>{E(tx)}</p></li>' for d, lab, tx in p['timeline']) + '</ol>'
    else:
        second = '<h3>Como está construído</h3><ul class="done-list built">' + ''.join(f'<li>{ico("code")}<span><b>{E(b)}</b>{E(rest)}</span></li>' for b, rest in p['built']) + '</ul>'
    n = len(p['flow']); cols = {4: 4, 5: 5, 6: 3}[n]
    flow = ''.join(f'<li class="glass"><p><b>{E(a)}</b>{E(b)}</p></li>' for a, b in p['flow'])
    why = ''.join(f'<div class="card glass"><span class="why-ico">{ico(i)}</span><h3>{E(h)}</h3><p>{E(tx)}</p></div>' for i, h, tx in p['why'])
    vs_b, vs_rest = p['vs']
    nx = p['next']
    roadmap_link = f'<p style="margin-top:14px"><a class="link" href="../roadmap.html">Ver no roadmap {ico("arrow")}</a></p>'
    spec = ''.join(f'<div><dt>{E(k)}</dt><dd>{v}</dd></div>' for k, v in p['spec'])
    prev, nxt = p['pager']
    shots = ''
    if p.get('screens'):
        figs = ''.join(
            f'<figure class="shot glass{" phone" if k == "phone" else ""}" style="--ar:{w / h:.3f}"><a href="../img/telas/{f}" target="_blank" rel="noopener">'
            f'<img src="../img/telas/{f}" alt="{E(c)}" width="{w}" height="{h}" loading="lazy" decoding="async"></a><figcaption>{E(c)}</figcaption></figure>'
            for f, c, k, w, h in p['screens'])
        shots = f'''
  <section class="sec" aria-labelledby="telas">
    <div class="sec-head">
      <p class="eyebrow">Direto do app</p>
      <h2 class="h2" id="telas">Telas reais</h2>
    </div>
    <div class="shots">{figs}</div>
    <p class="shots-note">Capturas do app rodando com dados de exemplo, em 25 set 2026. Clique para ampliar.</p>
  </section>
'''
    return f'''{head_html(f"{p['name']} — Orleans", p['desc'], f"{p['name']} — {p['og']}", f"projetos/{p['slug']}.html", p['slug'], jsonld_projeto(p))}

<a class="skip" href="#conteudo">Pular para o conteúdo</a>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">{syms}</svg>

{nav_html()}

<main id="conteudo">

<header class="p-hero">
  <div class="wrap p-hero-grid">
    <div>
      <p class="crumbs"><a href="../index.html#projetos">Projetos</a><span aria-hidden="true">/</span><span>{E(p["sector"])}</span></p>
      <h1>{E(p["name"])}</h1>
      <p class="pitch">{p["pitch"]}</p>
      <p class="lede">{E(p["lede"])}</p>
      <div class="p-status">{chips}</div>
      {meter}
      <div class="p-actions">{acts}</div>
      {note}
    </div>

    <figure class="p-art glass" style="margin:0">
      {p["art"]}
    </figure>
  </div>
</header>

<div class="wrap">

  <section aria-label="Números do projeto">
    <div class="proof glass" style="--pcols:{pcols}">{proof}</div>
    <p class="proof-note">{E(p["proof_note"])}</p>
  </section>

{shots}
  <section class="sec" aria-labelledby="entregue">
    <div class="sec-head">
      <p class="eyebrow">Prova de entrega</p>
      <h2 class="h2" id="entregue">O que já funciona hoje</h2>
    </div>
    <div class="duo">
      <div class="card glass">
        <h3>Já entregue</h3>
        <ul class="done-list">{done}</ul>
      </div>
      <div class="card glass">
        {second}
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="como">
    <div class="sec-head">
      <p class="eyebrow">{E(p["flow_eyebrow"])}</p>
      <h2 class="h2" id="como">{E(p["flow_title"])}</h2>
    </div>
    <ol class="flow" style="--cols:{cols}">{flow}</ol>
  </section>

  <section class="sec" aria-labelledby="porque">
    <div class="sec-head">
      <p class="eyebrow">Por que o {E(p["short"])}</p>
      <h2 class="h2" id="porque">{E(p["why_title"])}</h2>
    </div>
    <div class="why">{why}</div>
    <p class="vs glass">{ico("swap")}<span><strong>{E(vs_b)}</strong> {E(vs_rest)}</span></p>
  </section>

  <section class="sec" aria-labelledby="proximo">
    <div class="sec-head">
      <p class="eyebrow">Transparência</p>
      <h2 class="h2" id="proximo">O que vem a seguir</h2>
    </div>
    <div class="next">
      <div class="next-main glass">
        <span class="label">{E(nx[0])}</span>
        <h3>{E(nx[1])}</h3>
        <p>{E(nx[2])}</p>
        {roadmap_link}
      </div>
      <div class="spec glass">
        <dl>{spec}</dl>
      </div>
    </div>
  </section>

{cta_html(p["cta"][0], p["cta"][1], p.get("assunto") or ("Olá, Orleans! Vi o " + p["name"] + " no seu site e quero saber mais."))}

  <nav class="pager" aria-label="Outros projetos">
    <a class="glass" href="{prev[0]}"><span class="dir">← Anterior</span><span class="pname">{E(prev[1])}</span></a>
    <a class="glass next-p" href="{nxt[0]}"><span class="dir">Próximo →</span><span class="pname">{E(nxt[1])}</span></a>
  </nav>

</div>
</main>

{footer_html()}
</body>
</html>
'''

exec(open(os.path.join(HERE, 'projetos_dados.py'), encoding='utf-8').read())

# Sistema em que cada produto roda (dado estruturado para buscadores).
SISTEMAS = {'lumen': 'Windows', 'netdiag-pro': 'Windows', 'autoatendimento-qr': 'Windows, Android',
            'png-foto': 'Android, Web', 'backend-python-simulator': 'Windows, Linux, macOS',
            'excel-dashboard': 'Windows, Web', 'ai-control-center': 'Windows', 'ai-orchestrator': 'Linux'}
for _slug, _p in PROJECTS.items():
    _p['slug'] = _slug
    _p['os'] = SISTEMAS.get(_slug, 'Web')

def seg_page(slug, s):
    """Página de um segmento: junta os projetos do segmento e mostra como se encaixam."""
    used = {'arrow', 'arrow-up'}
    syms = ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{ICONS[k]}</symbol>' for k in sorted(used)) + LOGO
    cards = ''
    for ps in s['projects']:
        p = PROJECTS[ps]
        if p.get('screens'):
            f, c, k, w, h = p['screens'][0]
            thumb = f'<img src="../img/telas/{f}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">'
        else:
            thumb = p['art'].replace('<svg ', '<svg aria-hidden="true" preserveAspectRatio="xMidYMid slice" ', 1).replace(' role="img"', '')
        cards += (f'<a class="seg-card glass" href="../projetos/{ps}.html"><div class="seg-thumb">{thumb}</div><div class="seg-body">'
                  f'<div class="p-status" style="margin:0"><span class="chip"><span class="dot" aria-hidden="true"></span>{E(p["status"])}</span></div>'
                  f'<h3>{E(p["name"])}</h3><p>{E(p["desc"])}</p><span class="link">Ver o projeto {ico("arrow")}</span></div></a>')
    if s.get('fit'):
        fit = f'<ol class="flow" style="--cols:{len(s["fit"])}">' + ''.join(f'<li class="glass"><p><b>{E(a)}</b>{E(b)}</p></li>' for a, b in s['fit']) + '</ol>'
    else:
        fit = '<ul class="fix">' + ''.join(
            f'<li><a class="glass" href="../projetos/{ps}.html"><span class="prob">{E(prob)}</span>{ico("arrow")}<span class="sol">{E(PROJECTS[ps]["name"])}</span></a></li>'
            for prob, ps in s['problems']) + '</ul>'
    img, alt, w, h = s['hero_img']
    jsonld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': s['title'], 'description': s['desc'],
              'url': f'{SITE_URL}/solucoes/{slug}.html', 'author': PESSOA,
              'mainEntity': {'@type': 'ItemList', 'itemListElement': [
                  {'@type': 'ListItem', 'position': i + 1, 'url': f'{SITE_URL}/projetos/{ps}.html', 'name': PROJECTS[ps]['name']}
                  for i, ps in enumerate(s['projects'])]}}
    n = len(s['projects'])
    return f"""{head_html(f"{s['title']} — Orleans", s['desc'], f"{s['title']} — {s['og']}", f"solucoes/{slug}.html", 'seg-' + slug, jsonld, css='../projetos/projeto.css')}
<a class="skip" href="#conteudo">Pular para o conteúdo</a>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">{syms}</svg>

{nav_html()}

<main id="conteudo">

<header class="p-hero">
  <div class="wrap p-hero-grid">
    <div>
      <p class="crumbs"><a href="../index.html#segmentos">Soluções</a><span aria-hidden="true">/</span><span>{E(s["name"])}</span></p>
      <h1>{E(s["title"])}</h1>
      <p class="pitch">{s["pitch"]}</p>
      <p class="lede">{E(s["lede"])}</p>
      <div class="p-status"><span class="chip"><span class="dot" aria-hidden="true"></span>{n} projetos</span></div>
      <div class="p-actions">
        <a class="btn btn-primary" href="#projetos">Ver os projetos {ico("arrow")}</a>
        <a class="btn" href="#contato">Fale comigo {ico("arrow")}</a>
      </div>
    </div>
    <figure class="p-art glass" style="margin:0">
      <a class="seg-hero-img" href="../img/telas/{img}" target="_blank" rel="noopener"><img src="../img/telas/{img}" alt="{E(alt)}" width="{w}" height="{h}" decoding="async"></a>
    </figure>
  </div>
</header>

<div class="wrap">

  <section class="sec" id="projetos" aria-labelledby="proj-title" style="padding-top:8px">
    <div class="sec-head">
      <p class="eyebrow">Projetos</p>
      <h2 class="h2" id="proj-title">Feitos para {E(s["name"].lower())}</h2>
    </div>
    <div class="seg-grid">{cards}</div>
  </section>

  <section class="sec" aria-labelledby="fit-title">
    <div class="sec-head">
      <p class="eyebrow">Na prática</p>
      <h2 class="h2" id="fit-title">{E(s["fit_title"])}</h2>
    </div>
    {fit}
  </section>

{cta_html(s["cta"][0], s["cta"][1], s["assunto"])}

</div>
</main>

{footer_html()}
</body>
</html>
"""

# ── Roadmap: fonte da verdade de status, percentual e números da página inicial ──
ROOT = os.path.join(HERE, '..')
REPOS = {'lumen': 'igreja-projetor', 'frota-lite': 'frota-lite', 'autoatendimento-qr': 'autoatendimento',
         'netdiag-pro': 'network-diagnostic', 'ebike-suporte': 'ebike-support', 'central-da-festividade': 'central-festividade',
         'sistema-chamados': 'sistema-chamados', 'png-foto': 'png-foto', 'voice-finance': 'voice-finance',
         'ai-orchestrator': 'ai-orchestrator', 'excel-dashboard': 'excel-dashboard',
         'sliderevive-church-ai': 'slide-revive-church-ai', 'backend-python-simulator': 'backend-python-simulator',
         'ai-control-center': 'ai-control-center'}
STATUS_LABEL = {'ideia': 'Ideia', 'desenvolvimento': 'Em desenvolvimento', 'mvp': 'MVP', 'teste': 'Em teste',
                'pronto': 'Pronto para venda', 'producao': 'Em produção'}

def ler_roadmap():
    import re
    src = open(os.path.join(ROOT, 'roadmap.html'), encoding='utf-8').read()
    itens = {}
    for m in re.finditer(r"repo:'([^']+)', status:'(\w+)', priority:(?:'(\w)'|null).*?percent:(\w+)", src):
        repo, status, prio, pct = m.groups()
        itens[repo] = dict(status=status, priority=prio, percent=None if pct == 'null' else int(pct))
    return itens

def conferir_com_roadmap(road):
    """Para a geração se o status ou o percentual de uma página divergir do ROADMAP."""
    erros = []
    for slug, p in PROJECTS.items():
        r = road.get(REPOS[slug])
        if not r:
            erros.append(f'{slug}: repositório {REPOS[slug]} não está no ROADMAP'); continue
        if STATUS_LABEL[r['status']] != p['status']:
            erros.append(f"{slug}: página diz '{p['status']}', roadmap diz '{STATUS_LABEL[r['status']]}'")
        if r['percent'] != p.get('percent'):
            erros.append(f"{slug}: página diz {p.get('percent')}%, roadmap diz {r['percent']}%")
    if erros:
        sys.exit('Páginas divergem do ROADMAP em roadmap.html:\n  ' + '\n  '.join(erros))

def atualizar_numeros_home(road):
    """Preenche os números da página inicial marcados com data-stat."""
    import re
    numeros = {'portfolio': len(PROJECTS),
               'mvp': sum(r['status'] in ('mvp', 'teste', 'pronto', 'producao') for r in road.values()),
               'prioridade-a': sum(r['priority'] == 'A' for r in road.values())}
    caminho = os.path.join(ROOT, 'index.html')
    html_ = open(caminho, encoding='utf-8').read()
    novo = html_
    for chave, valor in numeros.items():
        novo, n = re.subn(rf'(<b data-stat="{chave}">)\d+(</b>)', rf'\g<1>{valor}\g<2>', novo)
        if n != 1:
            sys.exit(f'index.html: marcador data-stat="{chave}" não encontrado')
    if novo != html_:
        open(caminho, 'w', encoding='utf-8').write(novo)
    print('números da página inicial: ' + ', '.join(f'{k}={v}' for k, v in numeros.items()))

def escrever_sitemap():
    """sitemap.xml e robots.txt. O roadmap tem noindex e fica de fora, assim como a 404."""
    urls = [f'{SITE_URL}/'] + [f'{SITE_URL}/solucoes/{s}.html' for s in SEGMENTS] + [f'{SITE_URL}/projetos/{p}.html' for p in PROJECTS]
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(xml)
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write(
        f'User-agent: *\nDisallow: /tools/\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    print(f'sitemap.xml com {len(urls)} endereços')

if __name__ == '__main__':
    SEG_OUT = os.path.join(HERE, '..', 'solucoes')
    roadmap = ler_roadmap()
    conferir_com_roadmap(roadmap)
    atualizar_numeros_home(roadmap)
    escrever_sitemap()
    os.makedirs(SEG_OUT, exist_ok=True)
    pedidos = sys.argv[1:] or list(PROJECTS) + list(SEGMENTS)
    desconhecidos = [s for s in pedidos if s not in PROJECTS and s not in SEGMENTS]
    if desconhecidos:
        sys.exit('Não encontrado em projetos_dados.py: ' + ', '.join(desconhecidos))
    for slug in pedidos:
        if slug in PROJECTS:
            destino, html_ = os.path.join(OUT, slug + '.html'), page(PROJECTS[slug])
        else:
            destino, html_ = os.path.join(SEG_OUT, slug + '.html'), seg_page(slug, SEGMENTS[slug])
        with open(destino, 'w', encoding='utf-8') as f:
            f.write(html_)
        print('gerado ' + os.path.relpath(destino, os.path.join(HERE, '..')))
