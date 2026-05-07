#!/usr/bin/env python
"""Script para corrigir os arquivos do projeto."""

from pathlib import Path

project_root = Path(__file__).parent

# Dicionário de arquivos e conteúdo
files_content = { }

# Escrever todos os arquivos
for file_path, content in files_content.items():
    file_path.write_text(content, encoding="utf-8")
    print(f"✓ {file_path.relative_to(project_root)}")

print("\nArquivos corrigidos com sucesso!")
