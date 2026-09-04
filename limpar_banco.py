import os
import sys
import shutil
import sqlite3
from datetime import datetime

basedir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(basedir, 'inventario_ti.db')


def decodificar(valor):
    """Transforma bytes (BLOB) em texto legivel."""
    if isinstance(valor, bytes):
        for enc in ('utf-8', 'latin-1'):
            try:
                return valor.decode(enc)
            except Exception:
                continue
        return valor.decode('utf-8', errors='ignore')
    return valor


def main():
    if not os.path.exists(DB_PATH):
        print(f"[ERRO] Banco nao encontrado: {DB_PATH}")
        return

    # 1) Backup de seguranca antes de qualquer mudanca
    carimbo = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup = os.path.join(basedir, f'inventario_ti_BACKUP_{carimbo}.db')
    shutil.copy2(DB_PATH, backup)
    print(f"Backup criado: {os.path.basename(backup)}")

    conn = sqlite3.connect(DB_PATH)
    conn.text_factory = bytes  # le tudo como bytes para detectar BLOBs
    cur = conn.cursor()

    # 2) Converte BLOB -> texto em usuario_lista e email_no_sistema
    colunas_texto = ['usuario_lista', 'email_no_sistema', 'modelo',
                     'fabricante', 'processador', 'ram', 'armazenamento']
    convertidos = 0
    cur.execute("SELECT rowid, * FROM notebooks")
    nomes_col = [d[0] for d in cur.description]
    linhas = cur.fetchall()

    for linha in linhas:
        registro = dict(zip(nomes_col, linha))
        rowid = registro['rowid']
        for col in colunas_texto:
            if col in registro and isinstance(registro[col], bytes):
                novo = decodificar(registro[col])
                conn.execute(f"UPDATE notebooks SET {col}=? WHERE rowid=?", (novo, rowid))
                convertidos += 1

    # 3) Remove a linha de teste (serial N/A ou vazio)
    cur.execute("DELETE FROM notebooks WHERE serial IS NULL OR serial='N/A' OR trim(serial)=''")
    removidos = cur.rowcount

    conn.commit()
    conn.close()

    print(f"Campos BLOB convertidos para texto: {convertidos}")
    print(f"Linhas de teste (serial N/A) removidas: {removidos}")
    print("Concluido. Se algo der errado, restaure o arquivo de backup.")


if __name__ == '__main__':
    main()
    input("\nPressione ENTER para fechar...")
