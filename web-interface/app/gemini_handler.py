import google.generativeai as genai
import requests
from typing import List, Dict, Optional
import time

class GeminiHandler:
    def __init__(self):
        self.api_keys: List[str] = []
        self.key_status: Dict[str, bool] = {}
        self.current_key_index = 0
        
    def add_keys(self, keys: List[str]) -> Dict[str, bool]:
        """Add and validate API keys"""
        self.api_keys = [key.strip() for key in keys if key.strip()]
        self.key_status = {}
        
        # Validate each key
        for key in self.api_keys:
            self.key_status[key] = self._validate_key(key)
            
        return self.key_status
    
    def _validate_key(self, api_key: str) -> bool:
        """Test if an API key is valid"""
        try:
            print(f"Validating key: {api_key[:8]}...")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Simple test prompt
            response = model.generate_content("Hello")
            result = response.text is not None
            print(f"Key validation result: {result}")
            return result
        except Exception as e:
            print(f"Key validation failed for {api_key[:8]}...: {e}")
            return False
    
    def _get_working_key(self) -> Optional[str]:
        """Get the next working API key"""
        attempts = 0
        while attempts < len(self.api_keys):
            key = self.api_keys[self.current_key_index]
            if self.key_status.get(key, False):
                return key
            
            # Try next key
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            attempts += 1
            
        return None
    
    def convert_task_to_command(self, task: str) -> str:
        """Convert natural language task to CLI command"""
        working_key = self._get_working_key()
        if not working_key:
            raise Exception("No working API keys available")
        
        try:
            genai.configure(api_key=working_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            Convert this task to a CLI command. Return ONLY the command, nothing else.
            
            Available tools in /app/categories:
            - nmap: Network scanning
            - sqlmap: SQL injection testing
            - peframe: PE file analysis
            - ghidra: Reverse engineering
            
            Task: {task}
            
            Examples:
            - "scan example.com" → "nmap -v example.com"
            - "check for SQL injection on example.com" → "sqlmap -u http://example.com"
            """
            
            response = model.generate_content(prompt)
            command = response.text.strip()
            
            # Basic safety check - only allow certain commands
            allowed_prefixes = ['nmap', 'sqlmap', 'peframe', 'ghidra', 'ls', 'cat', 'head', 'tail']
            if not any(command.startswith(prefix) for prefix in allowed_prefixes):
                raise Exception("Command not allowed for security reasons")
                
            return command
            
        except Exception as e:
            # Mark current key as failed and retry
            self.key_status[working_key] = False
            return self.convert_task_to_command(task)
    
    def summarize_output(self, output: str, original_task: str) -> str:
        """Summarize CLI output using Gemini"""
        working_key = self._get_working_key()
        if not working_key:
            raise Exception("No working API keys available")
        
        try:
            genai.configure(api_key=working_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            Summarize this CLI output in a clear, concise way. Focus on important findings and actionable information.
            
            Original task: {original_task}
            CLI Output:
            {output}
            
            Provide a structured summary with key findings, open ports, vulnerabilities, or other important information.
            """
            
            response = model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            # Mark current key as failed and retry
            self.key_status[working_key] = False
            return self.summarize_output(output, original_task)
    
    def get_key_status(self) -> Dict[str, bool]:
        """Get current status of all keys"""
        return self.key_status.copy() 