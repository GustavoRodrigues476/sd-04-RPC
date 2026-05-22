from flask import Flask, jsonify, request
from datetime import datetime
import requests

app = Flask(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3"

def coingecko_get(endpoint, params={}):
    """Faz requisição à API do CoinGecko."""
    try:
        r = requests.get(f"{COINGECKO_URL}/{endpoint}", params=params, timeout=10)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Sem conexão com a API CoinGecko"
    except requests.exceptions.Timeout:
        return None, "Timeout ao consultar CoinGecko"
    except requests.exceptions.HTTPError as e:
        return None, f"Erro HTTP: {e}"

# ── GET /moedas ───────────────────────────────────────────────
@app.route("/moedas", methods=["GET"])
def listar_moedas():
    limit = request.args.get("limit", 10)
    dados, erro = coingecko_get("coins/markets", params={
        "vs_currency": "brl",
        "order":       "market_cap_desc",
        "per_page":    limit,
        "page":        1,
        "sparkline":   False
    })
    if erro:
        return jsonify({"erro": erro}), 503

    moedas = []
    for m in dados:
        moedas.append({
            "id":             m["id"],
            "simbolo":        m["symbol"].upper(),
            "nome":           m["name"],
            "preco_brl":      m["current_price"],
            "variacao_24h":   round(m["price_change_percentage_24h"] or 0, 2),
            "market_cap_brl": m["market_cap"],
            "volume_24h":     m["total_volume"],
        })

    print(f"[Servidor] GET /moedas — {len(moedas)} moedas")
    return jsonify({"total": len(moedas), "moedas": moedas}), 200

# ── GET /moedas/<id> ──────────────────────────────────────────
@app.route("/moedas/<moeda_id>", methods=["GET"])
def obter_moeda(moeda_id):
    dados, erro = coingecko_get(f"coins/{moeda_id}", params={
        "localization":   False,
        "tickers":        False,
        "market_data":    True,
        "community_data": False,
        "developer_data": False,
    })
    if erro:
        return jsonify({"erro": erro}), 503
    if "error" in dados:
        return jsonify({"erro": f"Moeda '{moeda_id}' não encontrada"}), 404

    md = dados["market_data"]
    resultado = {
        "id":              dados["id"],
        "simbolo":         dados["symbol"].upper(),
        "nome":            dados["name"],
        "descricao":       dados["description"].get("en", "")[:300],
        "preco_brl":       md["current_price"].get("brl"),
        "preco_usd":       md["current_price"].get("usd"),
        "variacao_24h":    round(md["price_change_percentage_24h"] or 0, 2),
        "variacao_7d":     round(md["price_change_percentage_7d"]  or 0, 2),
        "maxima_24h_brl":  md["high_24h"].get("brl"),
        "minima_24h_brl":  md["low_24h"].get("brl"),
        "market_cap_brl":  md["market_cap"].get("brl"),
        "volume_24h_brl":  md["total_volume"].get("brl"),
        "rank":            dados["market_cap_rank"],
    }

    print(f"[Servidor] GET /moedas/{moeda_id}")
    return jsonify(resultado), 200

# ── GET /moedas/<id>/preco ────────────────────────────────────
@app.route("/moedas/<moeda_id>/preco", methods=["GET"])
def preco_moeda(moeda_id):
    dados, erro = coingecko_get("simple/price", params={
        "ids":              moeda_id,
        "vs_currencies":    "brl,usd",
        "include_24hr_change": True,
    })
    if erro:
        return jsonify({"erro": erro}), 503
    if moeda_id not in dados:
        return jsonify({"erro": f"Moeda '{moeda_id}' não encontrada"}), 404

    preco = dados[moeda_id]
    resultado = {
        "moeda":        moeda_id,
        "preco_brl":    preco.get("brl"),
        "preco_usd":    preco.get("usd"),
        "variacao_brl": round(preco.get("brl_24h_change") or 0, 2),
        "variacao_usd": round(preco.get("usd_24h_change") or 0, 2),
        "hora":         datetime.now().strftime("%H:%M:%S"),
    }

    print(f"[Servidor] GET /moedas/{moeda_id}/preco")
    return jsonify(resultado), 200

# ── GET /mercado ──────────────────────────────────────────────
@app.route("/mercado", methods=["GET"])
def mercado():
    dados, erro = coingecko_get("global")
    if erro:
        return jsonify({"erro": erro}), 503

    d = dados["data"]
    resultado = {
        "total_moedas":         d["active_cryptocurrencies"],
        "total_mercados":       d["markets"],
        "market_cap_usd":       d["total_market_cap"].get("usd"),
        "volume_24h_usd":       d["total_volume"].get("usd"),
        "dominancia_bitcoin":   round(d["market_cap_percentage"].get("btc", 0), 2),
        "dominancia_ethereum":  round(d["market_cap_percentage"].get("eth", 0), 2),
        "hora":                 datetime.now().strftime("%H:%M:%S"),
    }

    print(f"[Servidor] GET /mercado")
    return jsonify(resultado), 200

# ── GET /health ───────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    _, erro = coingecko_get("ping")
    return jsonify({
        "status":     "ok",
        "coingecko":  "online" if not erro else "offline",
        "hora":       datetime.now().strftime("%H:%M:%S"),
    }), 200

if __name__ == "__main__":
    print("[Servidor] API Gateway CoinGecko rodando em 0.0.0.0:5000")
    print("Endpoints:")
    print("  GET /moedas")
    print("  GET /moedas/<id>")
    print("  GET /moedas/<id>/preco")
    print("  GET /mercado")
    print("  GET /health")
    app.run(host="0.0.0.0", port=5000, debug=False)