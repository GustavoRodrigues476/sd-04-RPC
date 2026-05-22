import requests

BASE_URL = "http://192.168.56.10:5000"

def separador(titulo):
    print(f"\n{'='*55}")
    print(f" {titulo}")
    print(f"{'='*55}")

def main():

    separador("HEALTH CHECK")
    r = requests.get(f"{BASE_URL}/health")
    d = r.json()
    print(f"  Status:    {d['status']}")
    print(f"  CoinGecko: {d['coingecko']}")
    print(f"  Hora:      {d['hora']}")

    separador("TOP 10 CRIPTOMOEDAS (em BRL)")
    r = requests.get(f"{BASE_URL}/moedas")
    dados = r.json()
    print(f"  {'#':<4} {'Símbolo':<8} {'Nome':<20} {'Preço BRL':>15} {'24h':>8}")
    print(f"  {'-'*60}")
    for i, m in enumerate(dados["moedas"], 1):
        sinal = "▲" if m["variacao_24h"] >= 0 else "▼"
        print(f"  {i:<4} {m['simbolo']:<8} {m['nome']:<20} R${m['preco_brl']:>12,.2f} {sinal}{abs(m['variacao_24h']):>6.2f}%")

    separador("DETALHES — BITCOIN")
    r = requests.get(f"{BASE_URL}/moedas/bitcoin")
    m = r.json()
    print(f"  Nome:          {m['nome']} ({m['simbolo']})")
    print(f"  Rank:          #{m['rank']}")
    print(f"  Preço BRL:     R${m['preco_brl']:,.2f}")
    print(f"  Preço USD:     ${m['preco_usd']:,.2f}")
    print(f"  Variação 24h:  {m['variacao_24h']:+.2f}%")
    print(f"  Variação 7d:   {m['variacao_7d']:+.2f}%")
    print(f"  Máxima 24h:    R${m['maxima_24h_brl']:,.2f}")
    print(f"  Mínima 24h:    R${m['minima_24h_brl']:,.2f}")
    print(f"  Market Cap:    R${m['market_cap_brl']:,.2f}")

    separador("PREÇO RÁPIDO — ETHEREUM")
    r = requests.get(f"{BASE_URL}/moedas/ethereum/preco")
    p = r.json()
    print(f"  Moeda:        {p['moeda']}")
    print(f"  Preço BRL:    R${p['preco_brl']:,.2f}")
    print(f"  Preço USD:    ${p['preco_usd']:,.2f}")
    print(f"  Variação BRL: {p['variacao_brl']:+.2f}%")
    print(f"  Hora:         {p['hora']}")

    separador("VISÃO GERAL DO MERCADO")
    r = requests.get(f"{BASE_URL}/mercado")
    m = r.json()
    print(f"  Total de moedas:      {m['total_moedas']:,}")
    print(f"  Total de mercados:    {m['total_mercados']:,}")
    print(f"  Market Cap USD:       ${m['market_cap_usd']:,.0f}")
    print(f"  Volume 24h USD:       ${m['volume_24h_usd']:,.0f}")
    print(f"  Dominância Bitcoin:   {m['dominancia_bitcoin']}%")
    print(f"  Dominância Ethereum:  {m['dominancia_ethereum']}%")

    separador("TESTE DE ERRO — MOEDA INEXISTENTE")
    r = requests.get(f"{BASE_URL}/moedas/moeda-falsa-xyz")
    print(f"  {r.status_code} — {r.json()}")

if __name__ == "__main__":
    main()