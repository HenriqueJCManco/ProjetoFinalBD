import mariadb
import sys
import tkinter as tk
from tkinter import ttk

# Estabelecendo a conexão com o banco de dados
def conectar_ao_banco():
    try:
        conexao = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="ods3_hospital"
        )
        print("Conexão estabelecida com sucesso!")
    except mariadb.Error as e:
        print(f"Erro ao conectar ao MariaDB: {e}")
        sys.exit(1)
    return conexao




# Função para buscar e exibir os dados da tabela selecionada
def exibir_dados():
    tabela_selecionada = combobox_tabelas.get()
    
    if not tabela_selecionada:
        print("Nenhuma tabela selecionada.")
        return

    print(f"Tabela Selecionada: {tabela_selecionada}")

    conexao = conectar_ao_banco()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM {tabela_selecionada}")
    dados = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    
    if colunas:
        tree.delete(*tree.get_children())  # Limpar dados anteriores
        tree["columns"] = colunas
        tree["show"] = "headings"  # Esconde a primeira coluna vazia

        for col in colunas:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=150)

        # Adiciona os dados ao Treeview
        for row in dados:
                tree.insert("", "end", values=row)

    
conexao = conectar_ao_banco()


root = tk.Tk()
root.title("Selecionar Tabela")

# Lista de tabelas disponíveis
tabelas = ["bloco", "consulta", "departamento", "doenca", "exame",
           "funcionario", "grupo_de_risco", "medicamento", "paciente", "receita"]

#Combobox para selecionar a tabela
combobox_tabelas = ttk.Combobox(root, values=tabelas, state="readonly")
combobox_tabelas.pack(pady=10)

#botão para carregar os dados da tabela selecionada
botao_carregar = tk.Button(root, text="Carregar Dados", command=exibir_dados)
botao_carregar.pack(pady=5)

#tabela para exibir os dados
tree = ttk.Treeview(root)
tree.pack(expand=True, fill="both")

# Inicia o loop do Tkinter
root.mainloop()
