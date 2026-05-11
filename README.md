# 📧 Sistema de Liberação Técnica — Automação de E-mails com Python

Sistema web desenvolvido em **Python + Flask** para automatizar o envio de e-mails de liberação e cadastro de técnicos em bases de atendimento. Integra-se diretamente ao **Microsoft Outlook** via COM para gerar e-mails já formatados em HTML, com destinatários, cópia e assinatura automáticos.

---

## ✨ Funcionalidades

- 📋 **Formulário web** para preenchimento dos dados do chamado e do técnico
- 📨 **Envio automático de e-mail** via Outlook com corpo HTML formatado
- 🏢 **Dois tipos de solicitação:** Liberação Técnica e Cadastro de Técnico
- 📂 **Bases de atendimento carregadas dinamicamente** a partir de arquivo CSV
- 👥 **CC automático** para lista de e-mails de cópia configurável
- 👁️ **Modo visualização** — abre o e-mail no Outlook antes de enviar
- ✍️ **Assinatura automática** — captura e mantém a assinatura padrão do Outlook

---

## 🛠️ Tecnologias

- Python 3.x
- Flask
- pywin32 (`win32com.client`) — integração com Microsoft Outlook
- pythoncom — gerenciamento de threads COM
- CSV — gerenciamento das bases e listas de cópia

---

## 📁 Estrutura do Projeto

```
📦 projeto/
├── app.py                  # Aplicação principal Flask
├── Bases.csv               # Bases de atendimento com e-mails
├── emailCopia.csv          # Lista de e-mails para cópia (CC)
├── templates/
│   └── liberacao_tecnica.html  # Interface do formulário
└── README.md
```

---

## ⚙️ Configuração

### 1. Instale as dependências

```bash
pip install flask pywin32
```

### 2. Configure o arquivo `Bases.csv`

O arquivo deve conter as colunas separadas por `;`:

```
BASES ATENDIDAS;EMAIL PORTARIAS;EMAILS_CONTATO
Base Exemplo;portaria@exemplo.com;contato@exemplo.com
```

### 3. Configure o arquivo `emailCopia.csv`

Lista de pessoas que receberão cópia em todos os e-mails:

```
NOME;EMAIL
Fulano;fulano@empresa.com
Ciclano;ciclano@empresa.com
```

### 4. Execute a aplicação

```bash
python app.py
```

Acesse no navegador: [http://localhost:5000](http://localhost:5000)

---

## 🚀 Como usar

1. Selecione a **base de atendimento** no formulário
2. Escolha o tipo de solicitação: **Liberação Técnica** ou **Cadastro de Técnico**
3. Preencha o número do chamado, dados do técnico e data do atendimento
4. Clique em **Enviar** — o e-mail será gerado e enviado automaticamente via Outlook

> ⚠️ **Requisito:** Microsoft Outlook instalado e configurado na máquina.  
> ⚠️ **Compatível apenas com Windows** (uso de COM via pywin32).

---

## 📌 Observações

- O sistema captura automaticamente a assinatura padrão configurada no Outlook
- O campo "Apenas Visualizar" permite revisar o e-mail antes do envio
- Os destinatários são preenchidos automaticamente conforme a base selecionada

---

## 👨‍💻 Autor

**Lucas de Albuquerque Miranda**  
[GitHub](https://github.com/LucasMir4nd4) • [LinkedIn](https://www.linkedin.com/in/lucas-miranda-aa0430263/)
