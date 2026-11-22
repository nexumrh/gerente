#!/usr/bin/env python3
"""Gera as páginas por cidade do site de vendas (crediario-celular-<cidade>.html), o sitemap.xml e o robots.txt
a partir do site.html. Roda sozinho pelo GitHub Actions quando o site.html muda (.github/workflows/cidades.yml).
Para incluir ou tirar cidades, edite a lista CIDADES abaixo."""
import json, re, pathlib
BASE = 'https://nexumrh.github.io/gerente/'
CIDADES = [  # (slug, nome, UF)
    ('foz-do-iguacu', 'Foz do Iguaçu', 'PR'), ('cascavel', 'Cascavel', 'PR'), ('toledo', 'Toledo', 'PR'), ('medianeira', 'Medianeira', 'PR'),
    ('santa-terezinha-de-itaipu', 'Santa Terezinha de Itaipu', 'PR'), ('sao-miguel-do-iguacu', 'São Miguel do Iguaçu', 'PR'),
    ('marechal-candido-rondon', 'Marechal Cândido Rondon', 'PR'), ('guaira', 'Guaíra', 'PR'), ('matelandia', 'Matelândia', 'PR'),
    ('curitiba', 'Curitiba', 'PR'), ('londrina', 'Londrina', 'PR'), ('maringa', 'Maringá', 'PR'), ('ponta-grossa', 'Ponta Grossa', 'PR'),
]
raiz = pathlib.Path(__file__).parent
site = (raiz / 'site.html').read_text(encoding='utf-8')
lista = json.dumps([[s, n] for s, n, _ in CIDADES], ensure_ascii=False)
marca = re.compile(r'<script id="nxCidades">.*?</script>', re.S)
tag = f'<script id="nxCidades">window.NX_CIDADES={lista};</script>'
site = marca.sub(tag, site) if marca.search(site) else site.replace('<script src="marketing.js"></script>', '<script src="marketing.js"></script>\n' + tag, 1)
(raiz / 'site.html').write_text(site, encoding='utf-8')
for slug, nome, uf in CIDADES:
    p = site
    p = re.sub(r'<title>.*?</title>', f'<title>Crediário de celular em {nome} ({uf}) para lojas — NexumCell</title>', p, count=1)
    p = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="Loja de celular em {nome}? Venda parcelado no crediário até para negativado, com análise própria sem SPC/Serasa e trava do aparelho. Cadastre sua loja na NexumCell.">\n<link rel="canonical" href="{BASE}crediario-celular-{slug}.html">', p, count=1)
    p = p.replace('<span class="tag">Crediário de celular para lojas</span>', f'<span class="tag">Crediário de celular para lojas de {nome} ({uf})</span>', 1)
    p = p.replace('<h1>Venda celular parcelado <em>até para negativado.</em></h1>', f'<h1>Venda celular parcelado em {nome} <em>até para negativado.</em></h1>', 1)
    p = p.replace(tag, tag + f'<script>window.NX_CIDADE={json.dumps(nome + " / " + uf, ensure_ascii=False)};</script>', 1)
    bloco = (f'<section class="alt"><div class="wrap"><div class="sec-h"><small>{nome} ({uf})</small><h2>Crediário de celular para lojas de {nome}</h2>'
             f'<p>Lojas de {nome} e região usam a NexumCell para vender celular parcelado no boleto e no Pix para quem não tem cartão ou está com o nome negativado. '
             f'A análise é feita na hora, pelo sistema, e o aparelho fica protegido pela trava até a última parcela. Agende uma demonstração ou cadastre a sua loja abaixo.</p></div></div></section>\n\n<section id="como">')
    p = p.replace('<section id="como">', bloco, 1)
    (raiz / f'crediario-celular-{slug}.html').write_text(p, encoding='utf-8')
urls = ['site.html'] + [f'crediario-celular-{s}.html' for s, _, _ in CIDADES]
(raiz / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{u}</loc></url>\n' for u in urls) + '</urlset>\n', encoding='utf-8')
(raiz / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n', encoding='utf-8')
print(len(CIDADES), 'páginas geradas')
