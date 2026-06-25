# halo_events.py — fila de eventos para o Halo Helper (Rota 1: polling no localhost)
#
# Como usar no MailPy:
#   from halo_events import halo_events_bp
#   app.register_blueprint(halo_events_bp)
#
# Endpoints:
#   POST /halo/eventos            -> MailPy enfileira  { "numero": "...", "comentario": "..." }
#   GET  /halo/eventos            -> extensão consulta (polling)
#   POST /halo/eventos/<id>/ack   -> extensão confirma que aplicou (remove da fila)

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

halo_events_bp = Blueprint("halo_events", __name__)

# Fila em memória. Pra persistir entre reinícios, troque por SQLite ou um JSON em disco.
_eventos = []


# CORS — o content script roda no domínio do Halo e busca o localhost (origem diferente),
# então o servidor precisa liberar explicitamente.
@halo_events_bp.after_request
def _cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@halo_events_bp.route("/halo/eventos", methods=["OPTIONS"])
def _preflight():
    return ("", 204)


def adicionar_evento(numero, comentario):
    """Enfileira um evento. Pode ser chamado DIRETO pelo MailPy (mesmo processo)
    ou via POST /halo/eventos. Retorna o evento criado, ou None se inválido."""
    numero = str(numero or "").strip()
    comentario = (comentario or "").strip()
    if not numero.isdigit() or not comentario:
        return None
    evento = {
        "id": uuid.uuid4().hex[:8],
        "numero": numero,
        "comentario": comentario,
        "criado_em": datetime.now().isoformat(timespec="seconds"),
    }
    _eventos.append(evento)
    return evento


@halo_events_bp.route("/halo/eventos", methods=["POST"])
def enfileirar():
    """MailPy chama aqui pra agendar um comentário num chamado (via HTTP)."""
    data = request.get_json(force=True) or {}
    evento = adicionar_evento(data.get("numero"), data.get("comentario"))
    if not evento:
        return jsonify({"erro": "campos 'numero' (dígitos) e 'comentario' são obrigatórios"}), 400
    return jsonify(evento), 201


@halo_events_bp.route("/halo/eventos", methods=["GET"])
def listar():
    """A extensão faz polling aqui."""
    return jsonify(_eventos)


@halo_events_bp.route("/halo/eventos/<evento_id>/ack", methods=["POST"])
def ack(evento_id):
    """A extensão confirma que preencheu a nota; o evento sai da fila."""
    global _eventos
    antes = len(_eventos)
    _eventos = [e for e in _eventos if e["id"] != evento_id]
    return jsonify({"removidos": antes - len(_eventos)})