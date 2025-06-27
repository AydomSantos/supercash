from config.database import Database
import sqlite3

class Produto:
    def __init__(self, id=None, nome=None, codigo_barras=None, categoria_id=None,
                 preco_custo=None, preco_venda=None, estoque_atual=None,
                 estoque_minimo=None, fornecedor=None):
        self.id = id
        self.nome = nome
        self.codigo_barras = codigo_barras
        self.categoria_id = categoria_id
        self.preco_custo = preco_custo
        self.preco_venda = preco_venda
        self.estoque_atual = estoque_atual
        self.estoque_minimo = estoque_minimo
        self.fornecedor = fornecedor
        self.db = Database()
    
    def save(self):
        conn = self.db.get_connection()
        cur = conn.cursor()
        
        try:
            if self.id is None:
                # Insert new product
                cur.execute("""
                    INSERT INTO produtos (
                        nome, codigo_barras, categoria_id, preco_custo,
                        preco_venda, estoque_atual, estoque_minimo, fornecedor
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.nome, self.codigo_barras, self.categoria_id,
                    self.preco_custo, self.preco_venda, self.estoque_atual,
                    self.estoque_minimo, self.fornecedor
                ))
                self.id = cur.lastrowid
            else:
                # Update existing product
                cur.execute("""
                    UPDATE produtos
                    SET nome = ?, codigo_barras = ?, categoria_id = ?,
                        preco_custo = ?, preco_venda = ?, estoque_atual = ?,
                        estoque_minimo = ?, fornecedor = ?
                    WHERE id = ?
                """, (
                    self.nome, self.codigo_barras, self.categoria_id,
                    self.preco_custo, self.preco_venda, self.estoque_atual,
                    self.estoque_minimo, self.fornecedor, self.id
                ))
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error saving product: {e}")
            success = False
        finally:
            self.db.return_connection(conn)
        
        return success

    @classmethod
    def get_by_id(cls, produto_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
            produto_data = cur.fetchone()
            
            if produto_data:
                return cls(
                    id=produto_data[0],
                    nome=produto_data[1],
                    codigo_barras=produto_data[2],
                    categoria_id=produto_data[3],
                    preco_custo=produto_data[4],
                    preco_venda=produto_data[5],
                    estoque_atual=produto_data[6],
                    estoque_minimo=produto_data[7],
                    fornecedor=produto_data[8]
                )
            return None
        finally:
            db.return_connection(conn)

    @classmethod
    def get_by_barcode(cls, codigo_barras):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT * FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
            produto_data = cur.fetchone()
            
            if produto_data:
                return cls(
                    id=produto_data[0],
                    nome=produto_data[1],
                    codigo_barras=produto_data[2],
                    categoria_id=produto_data[3],
                    preco_custo=produto_data[4],
                    preco_venda=produto_data[5],
                    estoque_atual=produto_data[6],
                    estoque_minimo=produto_data[7],
                    fornecedor=produto_data[8]
                )
            return None
        finally:
            db.return_connection(conn)

    @classmethod
    def get_all(cls):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                SELECT p.*, c.nome as categoria_nome
                FROM produtos p
                LEFT JOIN categorias c ON p.categoria_id = c.id
                ORDER BY p.nome
            """)
            produtos = []
            
            for produto_data in cur.fetchall():
                produtos.append(cls(
                    id=produto_data[0],
                    nome=produto_data[1],
                    codigo_barras=produto_data[2],
                    categoria_id=produto_data[3],
                    preco_custo=produto_data[4],
                    preco_venda=produto_data[5],
                    estoque_atual=produto_data[6],
                    estoque_minimo=produto_data[7],
                    fornecedor=produto_data[8]
                ))
            
            return produtos
        finally:
            db.return_connection(conn)

    def update_stock(self, quantidade):
        """Update stock quantity (positive for additions, negative for subtractions)"""
        conn = self.db.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                UPDATE produtos
                SET estoque_atual = estoque_atual + ?
                WHERE id = ?
            """, (quantidade, self.id))
            
            # Get updated stock value
            cur.execute("SELECT estoque_atual FROM produtos WHERE id = ?", (self.id,))
            result = cur.fetchone()
            if result:
                self.estoque_atual = result[0]
            
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error updating stock: {e}")
            success = False
        finally:
            self.db.return_connection(conn)
            
        return success

    def delete(self):
        if self.id is None:
            return False
            
        conn = self.db.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("DELETE FROM produtos WHERE id = ?", (self.id,))
            conn.commit()
            success = cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting product: {e}")
            success = False
        finally:
            self.db.return_connection(conn)
            
        return success