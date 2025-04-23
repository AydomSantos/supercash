from config.database import Database
from datetime import datetime

class Cliente:
    def __init__(self, id=None, nome=None, cpf_cnpj=None, telefone=None,
                 endereco=None, pet_nome=None, pet_nascimento=None):
        self.id = id
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.telefone = telefone
        self.endereco = endereco
        self.pet_nome = pet_nome
        self.pet_nascimento = pet_nascimento
        self.db = Database()
    
    def save(self):
        conn = self.db.get_connection()
        cur = conn.cursor()
        
        if self.id is None:
            # Insert new client
            cur.execute("""
                INSERT INTO clientes (
                    nome, cpf_cnpj, telefone, endereco,
                    pet_nome, pet_nascimento
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                self.nome, self.cpf_cnpj, self.telefone,
                self.endereco, self.pet_nome, self.pet_nascimento
            ))
            self.id = cur.fetchone()[0]
        else:
            # Update existing client
            cur.execute("""
                UPDATE clientes
                SET nome = %s, cpf_cnpj = %s, telefone = %s,
                    endereco = %s, pet_nome = %s, pet_nascimento = %s
                WHERE id = %s
            """, (
                self.nome, self.cpf_cnpj, self.telefone,
                self.endereco, self.pet_nome, self.pet_nascimento,
                self.id
            ))
        
        cur.close()
        return self.id

    @classmethod
    def get_by_id(cls, cliente_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
        cliente_data = cur.fetchone()
        
        cur.close()
        
        if cliente_data:
            return cls(
                id=cliente_data[0],
                nome=cliente_data[1],
                cpf_cnpj=cliente_data[2],
                telefone=cliente_data[3],
                endereco=cliente_data[4],
                pet_nome=cliente_data[5],
                pet_nascimento=cliente_data[6]
            )
        return None

    @classmethod
    def get_by_cpf_cnpj(cls, cpf_cnpj):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM clientes WHERE cpf_cnpj = %s", (cpf_cnpj,))
        cliente_data = cur.fetchone()
        
        cur.close()
        
        if cliente_data:
            return cls(
                id=cliente_data[0],
                nome=cliente_data[1],
                cpf_cnpj=cliente_data[2],
                telefone=cliente_data[3],
                endereco=cliente_data[4],
                pet_nome=cliente_data[5],
                pet_nascimento=cliente_data[6]
            )
        return None

    @classmethod
    def get_all(cls):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM clientes ORDER BY nome")
        clientes = []
        
        for cliente_data in cur.fetchall():
            clientes.append(cls(
                id=cliente_data[0],
                nome=cliente_data[1],
                cpf_cnpj=cliente_data[2],
                telefone=cliente_data[3],
                endereco=cliente_data[4],
                pet_nome=cliente_data[5],
                pet_nascimento=cliente_data[6]
            ))
        
        cur.close()
        return clientes

    def get_purchase_history(self):
        conn = self.db.get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT v.id, v.data_venda, v.valor_total, v.forma_pagamento,
                   p.nome as produto_nome, iv.quantidade, iv.preco_unitario
            FROM vendas v
            JOIN itens_venda iv ON v.id = iv.venda_id
            JOIN produtos p ON iv.produto_id = p.id
            WHERE v.cliente_id = %s
            ORDER BY v.data_venda DESC
        """, (self.id,))
        
        purchases = []
        for row in cur.fetchall():
            purchases.append({
                'venda_id': row[0],
                'data': row[1],
                'valor_total': row[2],
                'forma_pagamento': row[3],
                'produto': row[4],
                'quantidade': row[5],
                'preco_unitario': row[6]
            })
        
        cur.close()
        return purchases

    def delete(self):
        if self.id is None:
            return False
            
        conn = self.db.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("DELETE FROM clientes WHERE id = %s", (self.id,))
            success = cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting client: {e}")
            success = False
        finally:
            cur.close()
            
        return success