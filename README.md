# Inventário de TI — Windows e Android

Projeto de inventário de ativos com dois clientes em **Python**: coletor Windows com interface Tkinter e aplicativo Android com Kivy. A integração móvel envia dados para um endpoint Google Apps Script que alimenta uma planilha Google Sheets. O cliente Windows grava inventário local em SQLite.

## Linguagens, formatos e ferramentas

| Tipo | Tecnologia | Evidência no repositório |
| --- | --- | --- |
| Linguagem | **Python** | `coletor.py`, `limpar_banco.py`, `app-android/main.py` |
| Scripts de compilação | **Batchfile (Windows CMD)** | `build.bat` |
| Linguagem usada pelo coletor via subprocesso | **PowerShell** | comandos `Get-CimInstance` chamados por `coletor.py`; não há arquivo `.ps1` separado |
| Linguagem de consulta de dados | **SQL (SQLite)** | instruções SQL embutidas em `coletor.py` e `limpar_banco.py` |
| Formato de configuração | **INI** | `app-android/buildozer.spec` |
| Notebook de build | **Jupyter Notebook / Google Colab** | `app-android/Build_APK_Colab.ipynb` |
| Framework Android | **Kivy** | `app-android/main.py` |
| Ponte para APIs Android | **PyJNIus** | `app-android/main.py`, `app-android/buildozer.spec` |
| Toolchain de APK | **Buildozer, Android SDK/NDK** | `app-android/buildozer.spec`, notebook de build |
| Empacotamento Windows | **PyInstaller** | `coletor.spec`, `build.bat` |
| Interface Windows / análise de dados | **Tkinter, Pandas** | `coletor.py` |
| Banco local | **SQLite** | `coletor.py`, `limpar_banco.py` |
| Integração em nuvem | **Google Apps Script / Google Sheets** | cliente HTTP em `app-android/main.py` (o código do endpoint remoto não está neste repositório) |

> **Sobre a barra “Languages” do GitHub:** ela reflete a contagem de arquivos-fonte feita pelo GitHub Linguist, não todas as tecnologias utilizadas. Frameworks como Kivy e ferramentas como Buildozer e PyInstaller não aparecem como linguagens independentes. As instruções SQL e PowerShell estão incorporadas ao código Python e, portanto, não são contabilizadas separadamente. O notebook do Colab foi marcado como auxiliar (`linguist-generated`) para evitar que o código de compilação obscureça as linguagens do aplicativo. O arquivo `buildozer.spec` foi identificado como formato INI.

## Estrutura

```text
coletor.py                       # GUI Windows, consultas de hardware via PowerShell e SQLite
limpar_banco.py                  # manutenção de registros com cópia de segurança
coletor.spec                     # configuração Python para o PyInstaller
build.bat                        # compilação do executável Windows
app-android/
  main.py                        # interface Kivy e leitura de hardware Android via PyJNIus
  buildozer.spec                 # configuração INI de compilação APK
  Build_APK_Colab.ipynb          # notebook auxiliar do Google Colab
  LEIA-ME.md                     # instruções históricas do aplicativo Android
```

## Compilação

**Windows:** disponibilize os dados locais exigidos pelo aplicativo e execute `build.bat` em um ambiente com Python e PyInstaller. O script gera `dist/coletor.exe`.

**Android:** o arquivo `app-android/buildozer.spec` define requisitos Python/Kivy/PyJNIus, permissões e parâmetros do Android. O notebook `Build_APK_Colab.ipynb` documenta o build em Google Colab. Não foram executados testes de compilação nesta atualização de documentação.

## Atenção à segurança

O código publicado inclui um endpoint de Apps Script e uma lista nominal de usuários no aplicativo Android. Antes de reutilizá-lo publicamente, revise esses dados e a autorização de acesso ao endpoint. Também é recomendável corrigir a desativação de verificação do certificado TLS na função `enviar_sheets` de `app-android/main.py` antes de uso em produção. Esta alteração de documentação **não** modifica o comportamento do aplicativo.

## Compilar Android usando o código do GitHub no Google Colab

Use [Build_APK_GitHub_Colab.ipynb](app-android/Build_APK_GitHub_Colab.ipynb) e abra-o com o Google Colab. Esse notebook baixa a branch `main` antes de compilar e executa [scripts/build_android_colab.sh](scripts/build_android_colab.sh). Assim, as alterações versionadas no repositório passam a ser a fonte do APK gerado por **esse novo notebook**.

**Importante:** o notebook antigo no Google Drive é um arquivo independente, não foi substituído nem conectado automaticamente. Para usar o novo fluxo, abra o notebook publicado no GitHub com o Colab. O repositório atualmente contém lista de usuários e URL de integração no código Android; antes de publicar ou redistribuir o APK, revise esses dados e configurações, além da validação TLS. A compilação depende do Android SDK/NDK e deve ser testada no Colab; a publicação deste arquivo não é prova de um build concluído.

**Estatísticas do GitHub:** agora existe um script Bash real, além de Python, Batchfile e da configuração INI. Os dois notebooks auxiliares continuam excluídos das porcentagens por serem artefatos de compilação. Trechos SQL e PowerShell incorporados ao Python não geram porcentagens separadas.
