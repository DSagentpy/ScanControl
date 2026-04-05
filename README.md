# ScanControl

**Controle e auditoria de recebimento logístico** — um sistema pensado para o dia a dia do armazém: registrar o que chegou, conferir com o que deveria chegar e gerar evidências para auditoria, tudo em uma interface que funciona bem no **computador e no celular**.

---

## Por que existe

Em operações de estoque, pequenas divergências entre **nota, pedido e físico** viram retrabalho, perda de tempo e risco na auditoria. Este projeto mostra como dá para **organizar esse fluxo em um só lugar**: coleta rápida no chão de fábrica ou doca, visão consolidada para quem precisa auditar, e relatórios exportáveis para quem precisa **provar** o que foi feito.

---

## O que você pode fazer com a aplicação

- **Coletar** leituras e registros de recebimento de forma simples, inclusive em dispositivos móveis na rede local.
- **Acompanhar sessões** de trabalho e o histórico do que foi conferido.
- **Auditar** e **conciliar** informações para reduzir erro humano e facilitar o controle interno.
- **Gerar saídas** úteis para gestão (por exemplo planilhas e PDFs), para arquivo ou compartilhamento.

Em resumo: menos planilha solta, menos “foi no papel de um, sumiu no bolso do outro”, mais **rastreabilidade**.

---

## Exemplo de saída: relatório de conferência

O sistema produz documentos prontos para arquivo e compartilhamento — como um **relatório de conferência** por sessão (itens, códigos e quantidades conferidas). É o tipo de material que operações usam para **fechar o ciclo** com tranquilidade na auditoria interna ou externa.

**[Abrir o exemplo em PDF](docs/exemplo-relatorio-conferencia.pdf)** *(gerado pelo próprio ScanControl; arquivo incluído neste repositório)*

---

## O que isso diz sobre quem desenvolveu

- **Visão de produto**: não é só código — é resolver um problema real de operação e compliance.
- **Ponta a ponta**: interface para o usuário final, regras de negócio, dados e preparação para ambiente de produção.
- **Cuidado com deploy**: aplicação containerizada, com suporte a banco relacional em nuvem, pronta para serviços como o Render.

---

## Tecnologias (em uma frase)

Backend em **Python** com **FastAPI**, banco **SQLAlchemy** (SQLite no dia a dia local ou **PostgreSQL** em produção), leitura e geração de documentos (PDF, Excel), e **Docker** para o ambiente de hospedagem ficar repetível e confiável.

---

## Rodar no seu computador

Na pasta do projeto, com [uv](https://github.com/astral-sh/uv) instalado:

```bash
uv sync
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Abra o navegador em `http://127.0.0.1:8000`. Para acessar de outro aparelho na mesma rede, use `--host 0.0.0.0` e o endereço IP da sua máquina.

Hospedagem na nuvem: o repositório inclui **`Dockerfile`** e **`render.yaml`** para publicação no [Render](https://render.com) (ou outro provedor compatível com Docker).

---

## Contato

Se quiser conversar sobre o projeto, desafios de logística ou oportunidades, use os canais do meu perfil aqui no GitHub.
