
from config.database import Database
from datetime import datetime
import sqlite3

class Venda:
    def __init__(self, id=None, cliente_id=None, usuario_id=None, data_venda=None,
                 valor_total=0, desconto=0, forma_pagamento=None):
        self.id = id
        self.cliente_id = cliente_id
        self.usuario_id = usuario_id
        self.data_venda = data_venda or datetime.now()
        self.valor_total = valor_total
        self.desconto = desconto
        self.forma_pagamento = forma_pagamento
        self.itens = []
        self.db = Database()
    
    def add_item(self, produto_id, quantidade, preco_unitario):
        """Add an item to the sale"""
        subtotal = quantidade * preco_unitario
        self.itens.append({
            'produto_id': produto_id,
            'quantidade': quantidade,
            'preco_unitario': preco_unitario,
            'subtotal': subtotal
        })
        self.valor_total += subtotal
    
    def apply_discount(self, discount_value):
        """Apply discount to the total value"""
        if discount_value > self.valor_total:
            return False
        self.desconto = discount_value
        return True
    
    def save(self):
        conn = self.db.get_connection()
        
        try:
            cur = conn.cursor()
            # Start transaction
            conn.execute("BEGIN")
            
            if self.id is None:
                # Insert new sale
                cur.execute("""
                    INSERT INTO vendas (
                        cliente_id, usuario_id, data_venda,
                        valor_total, desconto, forma_pagamento
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    self.cliente_id, self.usuario_id, self.data_venda,
                    self.valor_total, self.desconto, self.forma_pagamento
                ))
                self.id = cur.lastrowid
                
                # Insert sale items
                for item in self.itens:
                    cur.execute("""
                        INSERT INTO itens_venda (
                            venda_id, produto_id, quantidade,
                            preco_unitario, subtotal
                        )
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        self.id, item['produto_id'], item['quantidade'],
                        item['preco_unitario'], item['subtotal']
                    ))
                    
                    # Update product stock
                    cur.execute("""
                        UPDATE produtos
                        SET estoque_atual = estoque_atual - ?
                        WHERE id = ?
                    """, (item['quantidade'], item['produto_id']))
            
            # Commit transaction
            conn.commit()
            success = True
        except Exception as e:
            conn.rollback()
            print(f"Error saving sale: {e}")
            success = False
        finally:
            self.db.return_connection(conn)
        
        return success

    @classmethod
    def get_by_id(cls, venda_id):
        db = Database()
        conn = db.get_connection()
        
        try:
            cur = conn.cursor()
            # Get sale data
            cur.execute("SELECT * FROM vendas WHERE id = ?", (venda_id,))
            venda_data = cur.fetchone()
            
            if not venda_data:
                return None
            
            # Create sale object
            venda = cls(
                id=venda_data[0],
                cliente_id=venda_data[1],
                usuario_id=venda_data[2],
                data_venda=venda_data[3],
                valor_total=venda_data[4],
                desconto=venda_data[5],
                forma_pagamento=venda_data[6]
            )
            
            # Get sale items
            cur.execute("""
                SELECT produto_id, quantidade, preco_unitario, subtotal
                FROM itens_venda
                WHERE venda_id = ?
            """, (venda_id,))
            
            for item_data in cur.fetchall():
                venda.itens.append({
                    'produto_id': item_data[0],
                    'quantidade': item_data[1],
                    'preco_unitario': item_data[2],
                    'subtotal': item_data[3]
                })
            
            return venda
        finally:
            db.return_connection(conn)

    @classmethod
    def get_sales_by_period(cls, start_date, end_date):
        db = Database()
        conn = db.get_connection()
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT v.*, c.nome as cliente_nome, u.nome as usuario_nome
                FROM vendas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                LEFT JOIN usuarios u ON v.usuario_id = u.id
                WHERE DATE(v.data_venda) BETWEEN ? AND ?
                ORDER BY v.data_venda DESC
            """, (start_date, end_date))
            
            sales = []
            for row in cur.fetchall():
                sales.append({
                    'id': row[0],
                    'cliente_nome': row[7],
                    'usuario_nome': row[8],
                    'data_venda': row[3],
                    'valor_total': row[4],
                    'desconto': row[5],
                    'forma_pagamento': row[6]
                })
            
            return sales
        finally:
            db.return_connection(conn)

    def delete(self):
        if self.id is None:
            return False
            
        conn = self.db.get_connection()
        
        try:
            cur = conn.cursor()
            # Start transaction
            conn.execute("BEGIN")
            
            # Get items to restore stock
            cur.execute("""
                SELECT produto_id, quantidade
                FROM itens_venda
                WHERE venda_id = ?
            """, (self.id,))
            
            # Restore stock for each item
            for item in cur.fetchall():
                cur.execute("""
                    UPDATE produtos
                    SET estoque_atual = estoque_atual + ?
                    WHERE id = ?
                """, (item[1], item[0]))
            
            # Delete sale items
            cur.execute("DELETE FROM itens_venda WHERE venda_id = ?", (self.id,))
            
            # Delete sale
            cur.execute("DELETE FROM vendas WHERE id = ?", (self.id,))
            
            # Commit transaction
            conn.commit()
            success = True
        except Exception as e:
            conn.rollback()
            print(f"Error deleting sale: {e}")
            success = False
        finally:
            self.db.return_connection(conn)
            
        return success
