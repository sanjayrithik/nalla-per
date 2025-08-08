# Utility functions for tool management
import os
import subprocess

def get_available_tools():
    """Return a list of available tools in categories"""
    tools = {}
    categories_path = "/app/categories"
    
    for category in os.listdir(categories_path):
        category_path = os.path.join(categories_path, category)
        if os.path.isdir(category_path):
            tools[category] = []
            for tool in os.listdir(category_path):
                tool_path = os.path.join(category_path, tool)
                if os.path.isdir(tool_path):
                    tools[category].append(tool)
    
    return tools

def check_tool_installed(tool_name):
    """Check if a tool is installed and available in PATH"""
    try:
        subprocess.check_output(['which', tool_name], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False