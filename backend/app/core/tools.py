from typing import Dict, List, Any, Optional
from app.core.mcp_client import MCPClient
from app.core.rapidapi_client import RapidAPIClient
from app.core.telegram_client import TelegramClient
from app.config import settings

class ToolOrchestrator:
    def __init__(self):
        self.mcp_client = MCPClient() if settings.BROWSERLESS_API_KEY else None
        self.rapidapi_client = RapidAPIClient() if settings.RAPIDAPI_KEY else None
        self.telegram_client = TelegramClient() if settings.TELEGRAM_BOT_TOKEN else None
        self.available_tools = self._get_available_tools()

    def _get_available_tools(self) -> List[Dict[str, Any]]:
        tools = [
            {
                "name": "web_search",
                "description": "Search the web for information",
                "enabled": True
            },
            {
                "name": "calculator",
                "description": "Perform mathematical calculations",
                "enabled": True
            },
            {
                "name": "code_executor",
                "description": "Execute code snippets",
                "enabled": True
            }
        ]

        if self.mcp_client:
            tools.append({
                "name": "browser_automation",
                "description": "Control a headless browser for web interactions",
                "enabled": True
            })

        if self.rapidapi_client:
            tools.append({
                "name": "rapidapi",
                "description": "Access various APIs through RapidAPI",
                "enabled": True
            })

        if self.telegram_client:
            tools.append({
                "name": "telegram",
                "description": "Send messages via Telegram",
                "enabled": True
            })

        return tools

    async def execute_tool(
        self, 
        tool_name: str, 
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        if tool_name == "web_search":
            return await self._web_search(parameters.get("query", ""))
        elif tool_name == "calculator":
            return self._calculate(parameters.get("expression", ""))
        elif tool_name == "code_executor":
            return await self._execute_code(
                parameters.get("code", ""),
                parameters.get("language", "python")
            )
        elif tool_name == "browser_automation":
            return await self._browser_action(parameters)
        elif tool_name == "rapidapi":
            return await self._rapidapi_call(
                parameters.get("endpoint", ""),
                parameters.get("params", {})
            )
        elif tool_name == "telegram":
            return await self._send_telegram(
                parameters.get("chat_id", ""),
                parameters.get("message", "")
            )
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    async def _web_search(self, query: str) -> Dict[str, Any]:
        if self.rapidapi_client:
            return await self.rapidapi_client.search_web(query)
        return {
            "query": query,
            "results": [],
            "message": "Web search not configured. Please set RAPIDAPI_KEY."
        }

    def _calculate(self, expression: str) -> Dict[str, Any]:
        try:
            # Safe evaluation for basic math
            allowed_chars = set("0123456789+-*/.() ")
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return {"expression": expression, "result": result}
            else:
                return {"error": "Invalid characters in expression"}
        except Exception as e:
            return {"error": str(e)}

    async def _execute_code(self, code: str, language: str) -> Dict[str, Any]:
        if language.lower() == "python":
            try:
                import io
                import sys
                
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                
                exec(code)
                
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout
                
                return {"language": language, "output": output, "success": True}
            except Exception as e:
                sys.stdout = old_stdout
                return {"language": language, "error": str(e), "success": False}
        else:
            return {"error": f"Language '{language}' not supported"}

    async def _browser_action(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if not self.mcp_client:
            return {"error": "Browser automation not configured"}
        
        action = params.get("action", "navigate")
        url = params.get("url", "")
        
        if action == "navigate":
            return await self.mcp_client.navigate(url)
        elif action == "screenshot":
            return await self.mcp_client.screenshot()
        else:
            return {"error": f"Unknown action: {action}"}

    async def _rapidapi_call(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if not self.rapidapi_client:
            return {"error": "RapidAPI not configured"}
        
        return await self.rapidapi_client.call_endpoint(endpoint, params)

    async def _send_telegram(self, chat_id: str, message: str) -> Dict[str, Any]:
        if not self.telegram_client:
            return {"error": "Telegram not configured"}
        
        return await self.telegram_client.send_message(chat_id, message)

    def get_tools(self) -> List[Dict[str, Any]]:
        return self.available_tools

    def get_tool_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        for tool in self.available_tools:
            if tool["name"] == name:
                return tool
        return None
