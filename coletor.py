import os
import sys
import sqlite3
import subprocess
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

basedir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(basedir, 'inventario_ti.db')
CSV_USUARIOS = os.path.join(basedir, 'usuarios.csv')

def carregar_usuarios():
    # O CSV e UTF-8 com BOM; tenta utf-8-sig (remove o BOM) e cai para latin-1 se preciso
    df = None
    for enc in ('utf-8-sig', 'latin-1'):
        try:
            df = pd.read_csv(CSV_USUARIOS, encoding=enc, sep=';', header=None)
            break
        except Exception:
            continue
    if df is None:
        return ["Erro ao ler CSV"]
    try:
        lista = df.iloc[:, 0].dropna().astype(str).str.strip().tolist()
        # Remove BOM residual, vazios e a palavra de cabecalho "Nome"
        lista = [x.lstrip('﻿').strip() for x in lista]
        lista = [x for x in lista if x and x.lower() != 'nome']
        return sorted(set(lista))
    except Exception as e:
        return [f"Erro ao ler CSV: {e}"]

# Esconde a janela preta do console ao chamar o PowerShell (importante no .exe)
_NO_WINDOW = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

def pegar_ps(script):
    """Executa um comando PowerShell e devolve a saída limpa.
    Substitui o antigo 'wmic', que foi removido das versões recentes do Windows."""
    try:
        res = subprocess.check_output(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
            stderr=subprocess.DEVNULL,
            creationflags=_NO_WINDOW
        ).decode('utf-8', errors='ignore').strip()
        return res if res else "N/A"
    except Exception:
        return "N/A"

def pegar_ram_fisica():
    try:
        # Soma a capacidade de todos os pentes de memória instalados (RAM física real)
        gb = pegar_ps(
            "$s=(Get-CimInstance Win32_PhysicalMemory | "
            "Measure-Object -Property Capacity -Sum).Sum; "
            "[math]::Round($s/1GB)"
        )
        return f"{gb} GB" if gb.isdigit() else "N/A"
    except Exception:
        return "N/A"

def pegar_disco():
    try:
        # Soma o tamanho de todos os discos físicos
        gb = pegar_ps(
            "$s=(Get-CimInstance Win32_DiskDrive | "
            "Measure-Object -Property Size -Sum).Sum; "
            "[math]::Round($s/1GB)"
        )
        return f"{gb} GB" if gb.isdigit() else "N/A"
    except Exception:
        return "N/A"

def coletar_e_salvar():
    usuario = combo.get()
    # Garante que o nome seja gravado como TEXTO, nunca como BLOB (bytes)
    if isinstance(usuario, bytes):
        usuario = usuario.decode('utf-8', errors='ignore')
    usuario = str(usuario).strip()
    if not usuario or "Erro" in usuario:
        messagebox.showwarning("Aviso", "Selecione um usuário!")
        return

    serial = pegar_ps("(Get-CimInstance Win32_BIOS).SerialNumber")
    modelo = pegar_ps("(Get-CimInstance Win32_ComputerSystemProduct).Name")
    fabricante = pegar_ps("(Get-CimInstance Win32_ComputerSystemProduct).Vendor")
    processador = pegar_ps("(Get-CimInstance Win32_Processor | Select-Object -First 1).Name")

    # RAM CORRIGIDA (Pega o total físico, não o disponível)
    ram = pegar_ram_fisica()
    disco = pegar_disco()

    email_sys = str(os.getlogin())

    conn = sqlite3.connect(DB_PATH)
    conn.text_factory = str  # forca leitura/escrita como texto
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS notebooks
                        (serial TEXT PRIMARY KEY, modelo TEXT, fabricante TEXT,
                         processador TEXT, ram TEXT, armazenamento TEXT,
                         email_no_sistema TEXT, usuario_lista TEXT)''')

        cursor.execute('''
            INSERT OR REPLACE INTO notebooks 
            (serial, modelo, fabricante, processador, ram, armazenamento, email_no_sistema, usuario_lista) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (serial, modelo, fabricante, processador, ram, disco, email_sys, usuario))
        
        conn.commit()
        messagebox.showinfo("Sucesso", f"Cadastrado: {usuario}\nRAM: {ram} (Real)")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro no banco: {e}")
    finally:
        conn.close()

root = tk.Tk()
root.title("Coletor TI - v2.1")
root.geometry("450x250")

tk.Label(root, text="Selecione o Usuário (A-Z):", font=("Arial", 10, "bold")).pack(pady=10)
combo = ttk.Combobox(root, values=carregar_usuarios(), width=50, state="readonly")
combo.pack(pady=5)

tk.Button(root, text="RODAR COLETA AGORA", command=coletar_e_salvar, 
          bg="#28a745", fg="white", font=("Arial", 11, "bold"), height=2).pack(pady=20)

root.mainloop()