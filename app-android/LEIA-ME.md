# Inventario TI — tudo que você precisa

Esta pasta tem o app pronto com a lista nova de usuários + o projeto completo.

## ✅ APK PRONTO PARA INSTALAR (com os 56 nomes novos)

**`inventarioti-0.2-NOVO-56usuarios.apk`** — é este que você quer.

Gerei a partir do seu APK original, trocando a lista de usuários por dentro e
re-assinando (v1+v2+v3, chave debug). Já vem com os **56 nomes novos** do seu
CSV. É só passar pro celular e instalar (ative "Fontes desconhecidas").

> Os outros arquivos (`inventarioti-0.1-ORIGINAL.apk`, notebook, `main.py` etc.)
> são o histórico/projeto. Para instalar, use só o `...0.2-NOVO-56usuarios.apk`.

## 🔧 Quando quiser mudar de novo / rebuild completo — Google Colab

Se um dia precisar alterar mais coisas (não só a lista), use o Colab:

1. Abra https://colab.research.google.com
2. `Arquivo` → `Fazer upload de notebook` → **`Build_APK_Colab.ipynb`**
3. Menu `Ambiente de execução` → **`Executar tudo`**
4. No fim, o `.apk` baixa sozinho (1ª vez demora ~20-40 min).

O notebook já traz código, config, lista e ícone embutidos.

## Conteúdo da pasta

| Arquivo | Para que serve |
|---|---|
| `Build_APK_Colab.ipynb` | Notebook pronto pra gerar o APK novo no Colab. |
| `inventarioti-0.1-ORIGINAL.apk` | Seu APK que já funciona (backup / uso imediato). |
| `main.py` | Código do app (Kivy). A lista de nomes está na variável `USUARIOS`. |
| `buildozer.spec` | Configuração de build (pacote, permissões, bibliotecas). |
| `icon.png` | Ícone do app. |
| `usuarios.csv` | Lista de nomes de referência (a fonte da lista). |

## O que o app faz

1. Ao abrir, lê o hardware do aparelho: **fabricante, modelo, serial, versão do
   Android e Android ID**.
2. O usuário escolhe o nome dele numa lista (menu suspenso).
3. Ao tocar em **ENVIAR INVENTÁRIO**, os dados vão para uma planilha Google
   (via Apps Script Web App).

## Mudar a lista de usuários no futuro

Edite a variável `USUARIOS` no `main.py` (ou troque o `usuarios.csv` e me peça
pra regenerar) e gere o APK de novo pelo notebook.

## Pontos de atenção

- **URL da planilha:** está em `SHEETS_URL` no topo do `main.py`. É o mesmo
  endereço do Apps Script que estava no app original. Se a planilha/Apps Script
  mudou, atualize essa URL.
- A lista atual tem **56 nomes** (removi duplicados e o cabeçalho "Nome" do CSV).
  Um nome veio com palavra repetida no seu CSV ("Claudio Claudio José Pontello
  Junior") — mantive igual ao arquivo; me avise se quiser corrigir.
