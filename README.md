# Inventário de Ativos de TI — Coletor Windows

Coletor em Python para inventariar computadores Windows, associar os equipamentos a usuários e armazenar os registros localmente em SQLite.

O aplicativo Android agora está no repositório independente [Coletor de Dispositivos Android](https://github.com/hiagoac7/coletor-dispositivos-android).

## Tecnologias

- Python e Tkinter: interface.
- Pandas: leitura da lista de usuários.
- PowerShell / Get-CimInstance: consulta de fabricante, modelo, serial, processador, memória física e armazenamento.
- SQLite: armazenamento local.
- PyInstaller e Batch: geração do executável.

## Estrutura

- `coletor.py`: interface, coleta e gravação.
- `limpar_banco.py`: manutenção do banco com cópia de segurança.
- `coletor.spec` e `build.bat`: empacotamento Windows.
- `usuarios.exemplo.csv`: modelo da lista local.

## Uso e compilação

1. Instale Python com Tkinter, Pandas e PyInstaller no Windows.
2. Prepare `usuarios.csv` com os usuários autorizados, usando o exemplo como referência.
3. Execute `python coletor.py` ou use `build.bat` para gerar `dist/coletor.exe`.
4. Distribua a pasta de saída com a lista local necessária. O banco `inventario_ti.db` é criado durante a coleta.

O script `limpar_banco.py` altera registros existentes e cria uma cópia de segurança antes da manutenção. Preserve os backups.

## Separação dos projetos

A pasta Android foi retirada da versão atual após a publicação do cliente independente. Os arquivos de execução e compilação Windows foram preservados. A revisão não identificou dependências desses arquivos em relação à pasta Android. A compilação Windows não foi executada nesta atualização.

Os commits antigos continuam no histórico Git e podem conter a lista nominal e o endpoint anteriormente publicados. Retirar arquivos da versão atual não apaga o histórico. Revise o acesso ao Apps Script original.
