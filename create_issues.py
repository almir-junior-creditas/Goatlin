import os
import json
import requests

# Carregar o token do GitHub e o nome do repositório
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")

# URL da API para criar issues
url = f"https://api.github.com/repos/{REPO}/issues"

# Carregar resultados do Semgrep
with open("semgrep_results.json") as f:
    results = json.load(f)

# Processar cada alerta do Semgrep
for result in results.get("results", []):
    title = result["check_id"]
    message = f"""
    **Descrição:** {result["extra"]["message"]}

    **Arquivo:** {result["path"]}
    **Linha:** {result["start"]["line"]}

    **Código vulnerável:**
    ```kotlin
    {result["extra"]["lines"]}
    ```
    """

    issue_data = {
        "title": title,
        "body": message,
        "labels": ["security", "semgrep"],
    }

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.post(url, headers=headers, json=issue_data)

    if response.status_code == 201:
        print(f"Issue created: {title}")
    else:
        print(f"Failed to create issue: {title}")
        print(response.json())
