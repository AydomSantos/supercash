# Supercash - Sistema de Gestão para Pet Shop

Supercash é um sistema de gestão completo desenvolvido especialmente para Pet Shops, oferecendo funcionalidades para controle de vendas, estoque, clientes e relatórios gerenciais.

## Características Principais

- **Gestão de Produtos**
  - Cadastro e atualização de produtos
  - Controle de estoque com alertas de estoque baixo
  - Gerenciamento de preços de custo e venda
  - Busca rápida por nome, código ou fornecedor

- **Gestão de Clientes**
  - Cadastro completo de clientes e seus pets
  - Registro de informações de contato
  - Histórico de compras
  - Busca por nome ou CPF/CNPJ

- **Controle de Vendas**
  - Interface intuitiva para registro de vendas
  - Múltiplas formas de pagamento
  - Aplicação de descontos
  - Busca rápida de produtos por código de barras

- **Relatórios Gerenciais**
  - Vendas por período
  - Produtos mais vendidos
  - Clientes mais ativos
  - Análise de estoque
  - Relatórios de lucratividade

## Requisitos do Sistema

- Python 3.11 ou superior
- PostgreSQL 15.5 ou superior
- PySide6

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/supercash.git
cd supercash
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados:
- Crie um banco de dados PostgreSQL
- Copie o arquivo `.env.example` para `.env` e configure as variáveis de ambiente
- Execute o script de criação das tabelas:
```bash
psql -U seu_usuario -d seu_banco -f scripts/create_tables.sql
```

4. Inicialize o administrador do sistema:
```bash
python scripts/init_admin.py
```

## Uso

1. Inicie o sistema:
```bash
python main.py
```

2. Faça login com as credenciais de administrador

3. Navegue pelo menu principal para acessar as diferentes funcionalidades

## Interface

O sistema possui uma interface moderna e intuitiva com tema escuro, proporcionando melhor experiência visual e usabilidade.

### Telas Principais

- **Login**: Autenticação segura com diferentes níveis de acesso
- **Dashboard**: Visão geral do sistema com acesso rápido às funcionalidades
- **Produtos**: Gerenciamento completo do catálogo e estoque
- **Clientes**: Cadastro e gestão de clientes e seus pets
- **Vendas**: PDV intuitivo para registro de vendas
- **Relatórios**: Análises e relatórios gerenciais

## Segurança

- Autenticação de usuários com diferentes níveis de acesso
- Senhas criptografadas
- Validação de dados em todas as operações
- Logs de atividades importantes

## Suporte

Para suporte ou dúvidas, entre em contato através do email: suporte@supercash.com

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contribuição

Contribuições são bem-vindas! Por favor, leia o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre nosso código de conduta e o processo para enviar pull requests.