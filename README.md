# 🔥 Fogo e Lucro — Sistema de Relatório Diário

Sistema web local para registro de tarefas diárias e geração de relatórios PDF para agências de marketing digital.

---

## Instalação

### 1. Instale as dependências

```bash
cd agencia
pip install -r requirements.txt
```

### 2. Configure a API do Claude (opcional)

Para gerar feedbacks automáticos com IA:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da Anthropic:

```
ANTHROPIC_API_KEY=sk-ant-SUA_CHAVE_AQUI
```

> Sem a chave, o sistema funciona normalmente — apenas o botão "Gerar Feedback Claude" ficará indisponível.

### 3. Inicie o servidor

```bash
python app.py
```

### 4. Acesse no navegador

```
http://localhost:5000
```

---

## Primeiros passos

1. Acesse **Equipe** (`/funcionarios`) e cadastre os membros da sua equipe
2. Acesse **Clientes** (`/clientes`) e cadastre seus clientes
3. Use o formulário principal (`/`) para registrar as tarefas do dia
4. Acesse o **Painel** (`/admin`) para visualizar os registros e gerar o PDF

---

## Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| 📝 Registro de tarefas | Formulário com data, funcionário, cliente, área, descrição, resultado, horas e upload de mídia |
| 📊 Painel do gestor | Filtros por data/funcionário/cliente, estatísticas e tabela de registros |
| 📄 Relatório PDF | PDF profissional organizado por cliente com cabeçalho, tarefas, imagens e rodapé |
| 🤖 Feedback Claude | Texto motivacional gerado por IA para cada cliente, incluído no PDF |
| 👥 Clientes | Cadastro, ativação/desativação e exclusão de clientes |
| ⚙️ Serviços | Gerenciamento das áreas de trabalho |
| 👤 Equipe | Cadastro dos funcionários |

---

## Estrutura de pastas

```
agencia/
├── app.py              ← Servidor Flask principal
├── database.py          ← Camada de dados (SQLite)
├── pdf_generator.py     ← Geração de PDF (ReportLab)
├── claude_feedback.py  ← Integração com API da Anthropic
├── agencia.db           ← Banco de dados (criado automaticamente)
├── uploads/             ← Fotos e vídeos enviados
├── relatorios/          ← PDFs gerados
└── templates/           ← Páginas HTML
```

---

## Tipos de arquivo aceitos

- **Imagens:** JPG, JPEG, PNG, GIF (máx. 50MB cada)
- **Vídeos:** MP4, MOV, AVI (máx. 50MB cada)

---

## Requisitos

- Python 3.10 ou superior
- Conexão com internet apenas para o feedback do Claude (opcional)
