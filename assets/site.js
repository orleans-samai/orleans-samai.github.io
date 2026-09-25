/* ═══════════════════════════════════════════════════════════════
   Configuração do site — preencha e publique.

   Cada campo vazio simplesmente não aparece: sem número de WhatsApp,
   não há botão de WhatsApp; sem código do GoatCounter, nenhuma
   estatística é coletada. O botão do LinkedIn está sempre no HTML.
   ═══════════════════════════════════════════════════════════════ */
const SITE = {
  // Só dígitos, com DDI e DDD. Ex.: '5511999998888'
  whatsapp: '5527988255629',
  // Ex.: 'contato@seudominio.com'
  email: '',
  // Link de agendamento de conversa (Cal.com, Calendly, Google Agenda…)
  agenda: '',
  // Código da conta no GoatCounter (https://www.goatcounter.com), sem cookies.
  // Ex.: 'orleans' para https://orleans.goatcounter.com
  goatcounter: '',
};

/* ── Botões de contato ──────────────────────────────────────────
   Qualquer elemento com data-contato recebe os botões configurados.
   data-assunto vira a mensagem pronta do WhatsApp e o assunto do e-mail. */
(function contato() {
  const alvos = document.querySelectorAll('[data-contato]');
  if (!alvos.length) return;
  const icone = {
    whatsapp: '<path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.3z"/><path d="M9 9.5c.2 2.2 2.5 4.6 5 5l1.2-1.3 2 1-.4 1.6c-3.6.5-8.6-4.1-8.4-7.9L10 7.5l1 2z"/>',
    email: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    agenda: '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M16 3v3M8 3v3M3 10h18"/>',
  };
  const svg = (k) => `<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" style="fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round">${icone[k]}</svg>`;
  alvos.forEach((el) => {
    const assunto = el.dataset.assunto || 'Olá, Orleans! Vi seu portfólio e quero conversar.';
    const pagina = (location.pathname.split('/').pop() || 'inicio').replace('.html', '');
    const botoes = [];
    if (SITE.whatsapp) botoes.push(['whatsapp', 'WhatsApp', `https://wa.me/${SITE.whatsapp}?text=${encodeURIComponent(assunto)}`]);
    if (SITE.email) botoes.push(['email', 'E-mail', `mailto:${SITE.email}?subject=${encodeURIComponent(assunto)}`]);
    if (SITE.agenda) botoes.push(['agenda', 'Agendar conversa', SITE.agenda]);
    botoes.forEach(([k, rotulo, href]) => {
      const a = document.createElement('a');
      a.className = 'btn';
      a.href = href;
      if (!href.startsWith('mailto:')) { a.target = '_blank'; a.rel = 'noopener'; }
      a.dataset.goatcounterClick = `contato-${k}-${pagina}`;
      a.innerHTML = `${svg(k)}${rotulo}`;
      el.appendChild(a);
    });
  });
})();

/* ── Estatística de visitas (GoatCounter, sem cookies) ──────────── */
(function estatistica() {
  if (!SITE.goatcounter || location.protocol === 'file:') return;
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://gc.zgo.at/count.js';
  s.dataset.goatcounter = `https://${SITE.goatcounter}.goatcounter.com/count`;
  document.head.appendChild(s);
})();
