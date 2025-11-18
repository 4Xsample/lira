from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Input, RichLog
import httpx
import json

API_BASE_URL = "http://localhost:1312"
API_ENDPOINT = "/v1/chat/completions"
MODEL_PER_DEFECTE = "Lira-gemma2:9b"

class LiraChatApp(App):
    """A TUI to chat with the LIRA agent."""
    TITLE = "LIRA TUI"

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield RichLog(id="chat_log", wrap=True, markup=True, auto_scroll=True)
            with Horizontal(id="input_box"):
                yield Input(placeholder="Escriu la teva instrucció per a LIRA...", id="chat_input")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#chat_log").write("✨ Benvingut a la TUI de LIRA.", expand=True)
        self.query_one("#chat_log").write(f"🤖 Model per defecte: {MODEL_PER_DEFECTE}", expand=True)
        self.query_one(Input).focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        input_widget = self.query_one("#chat_input", Input)
        chat_log = self.query_one("#chat_log", RichLog)
        user_message = event.value

        if not user_message:
            return

        chat_log.write(f"[bold blue]Tu:[/bold blue] {user_message}")
        input_widget.value = ""
        
        input_widget.disabled = True

        try:
            response_content = await self.call_lira_api(user_message)
            chat_log.write(f"[bold green]LIRA:[/bold green] {response_content}")
        except Exception as e:
            chat_log.write(f"[bold red]Error de connexió: {e}[/bold red]")
        finally:
            input_widget.disabled = False
            input_widget.focus()

    async def call_lira_api(self, message: str) -> str:
        """Crida a la API de LIRA i retorna la resposta."""
        headers = {"Content-Type": "application/json"}
        data = {
            "model": MODEL_PER_DEFECTE,
            "messages": [{"role": "user", "content": message}],
            "stream": False
        }
        url = f"{API_BASE_URL}{API_ENDPOINT}"
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_json = response.json()
            
            if 'choices' in response_json and len(response_json['choices']) > 0 and 'message' in response_json['choices'][0]:
                content = response_json['choices'][0]['message']['content']
                return content
            else:
                return f"Resposta inesperada de la API:\n{json.dumps(response_json, indent=2)}"

if __name__ == "__main__":
    app = LiraChatApp()
    app.run()
