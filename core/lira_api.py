"""
Mòdul que implementa l'API de LIRA.
Actua com a proxy entre clients compatibles amb OpenAI i el servei d'Ollama,
gestionant la càrrega de configuració i la traducció de formats de petició/resposta.
"""
import http.server
import socketserver
import yaml
import os
import json
import requests
from http import HTTPStatus
import time

def load_config():
    """
    Carrega la configuració des del fitxer `config/lira.yaml`.
    Defineix paràmetres com el port de l'API, el model principal i la URL de l'API d'Ollama.
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'lira.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

config = load_config()
PORT = config.get('api', {}).get('port', 1312)
# Nom del model principal que LIRA exposarà per defecte.
MODEL_NAME = config.get('model', {}).get('main_model', 'gemma2:9b')
# URL base de l'API d'Ollama, utilitzada per comunicar-se amb els models.
OLLAMA_API_BASE_URL = config.get('ollama', {}).get('api_base_url', 'http://localhost:11434/v1')

class LIRAAPIHandler(http.server.BaseHTTPRequestHandler):
    """
    Handler personalitzat per a les peticions HTTP de l'API de LIRA.
    Gestiona les rutes `/v1/models` (GET) i `/v1/chat/completions` (POST).
    """
    def do_GET(self):
        """
        Gestiona les peticions GET.
        Respon a `/v1/models` per llistar models o proporciona informació bàsica.
        """
        if self.path == '/v1/models':
            self._handle_models()
        else:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(f"LIRA API està en funcionament!\n".encode('utf-8'))
            self.wfile.write(f"Utilitzant model: {MODEL_NAME}\n".encode('utf-8'))
            self.wfile.write(f"URL base de l'API d'Ollama: {OLLAMA_API_BASE_URL}".encode('utf-8'))

    def do_POST(self):
        """
        Gestiona les peticions POST.
        Respon a `/v1/chat/completions` per processar sol·licituds de xat.
        """
        if self.path == '/v1/chat/completions':
            self._handle_chat_completions()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def _handle_models(self):
        """
        Gestiona la petició GET a `/v1/models`.
        Consulta l'API d'Ollama per obtenir la llista de models i la transforma
        a un format compatible amb l'API d'OpenAI.
        # Etiqueta per a fine-tuning: model_prefixing
        S'afegeix el prefix "Lira-" als noms dels models per a una identificació clara.
        """
        try:
            ollama_models_url = f"{OLLAMA_API_BASE_URL.replace('/v1', '')}/api/tags"
            ollama_response = requests.get(ollama_models_url)
            ollama_response.raise_for_status()
            ollama_data = ollama_response.json()

            openai_models = []
            for model in ollama_data.get("models", []):
                model_id_with_prefix = f"Lira-{model['name']}"
                openai_models.append({
                    "id": model_id_with_prefix,
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "ollama",
                    "permission": [
                        {
                            "id": "model-perm-" + model["name"],
                            "object": "model_permission",
                            "created": int(time.time()),
                            "allow_create_engine": False,
                            "allow_sampling": True,
                            "allow_logprobs": False,
                            "allow_search_indices": False,
                            "allow_view": True,
                            "allow_fine_tuning": False,
                            "organization": "*",
                            "group": None,
                            "is_blocking": False
                        }
                    ],
                    "root": model_id_with_prefix,
                    "parent": None
                })

            response_payload = {
                "object": "list",
                "data": openai_models
            }

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_payload).encode('utf-8'))

        except requests.exceptions.RequestException as e:
            self.send_error(HTTPStatus.BAD_GATEWAY, f"Error connectant amb Ollama: {e}")
        except Exception as e:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"S'ha produït un error: {e}")

    def _handle_chat_completions(self):
        """
        Gestiona la petició POST a `/v1/chat/completions`.
        # Etiqueta per a fine-tuning: request_response_translation
        Tradueix la petició de format OpenAI a Ollama, l'envia a Ollama i
        retorna la resposta en format OpenAI.
        """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            request_payload = json.loads(post_data)

            messages = request_payload.get('messages')
#            model = request_payload.get('model', MODEL_NAME)
#
#            ollama_request_payload = {
#                "model": model,
#                "messages": messages,
#                "stream": False
#            }

            model = request_payload.get('model', MODEL_NAME)

            # Si el model té el prefix "Lira-", el treiem per a Ollama
            if model.startswith("Lira-"):
                ollama_model_name = model[5:]
            else:
                ollama_model_name = model

            ollama_request_payload = {
                "model": ollama_model_name, # <-- Ara enviem el nom correcte
                "messages": messages,
                "stream": False
            }

            ollama_response = requests.post(
                f"{OLLAMA_API_BASE_URL.replace('/v1', '')}/api/chat",
                json=ollama_request_payload
            )
            ollama_response.raise_for_status()

            ollama_data = ollama_response.json()

            openai_response_payload = {
                "id": ollama_data.get("id", "chatcmpl-lira"),
                "object": "chat.completion",
                "created": ollama_data.get("created_at", int(time.time())),
                "model": ollama_data.get("model", model),
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": ollama_data.get("message", {}).get("role", "assistant"),
                            "content": ollama_data.get("message", {}).get("content", "")
                        },
                        "finish_reason": ollama_data.get("done_reason", "stop")
                    }
                ],
                "usage": {
                    "prompt_tokens": ollama_data.get("prompt_eval_count", 0),
                    "completion_tokens": ollama_data.get("eval_count", 0),
                    "total_tokens": ollama_data.get("prompt_eval_count", 0) + ollama_data.get("eval_count", 0)
                }
            }

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(openai_response_payload).encode('utf-8'))

        except json.JSONDecodeError:
            self.send_error(HTTPStatus.BAD_REQUEST, "JSON invàlid")
        except requests.exceptions.RequestException as e:
            self.send_error(HTTPStatus.BAD_GATEWAY, f"Error connectant amb Ollama: {e}")
        except Exception as e:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"S'ha produït un error: {e}")

with socketserver.TCPServer(("", PORT), LIRAAPIHandler) as httpd:
    print(f"Servidor de l'API LIRA iniciat al port {PORT}")
    print(f"Model principal configurat: {MODEL_NAME}")
    print(f"URL base de l'API d'Ollama: {OLLAMA_API_BASE_URL}")
    httpd.serve_forever()