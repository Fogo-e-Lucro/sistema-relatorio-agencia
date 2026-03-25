"""
claude_feedback.py — Integração com a API da Anthropic.
- gerar_feedback(): feedback por cliente (WhatsApp-style)
- gerar_relatorio_dia(): relatório executivo completo do dia
"""

import os
import sys
from typing import Optional

SYSTEM_PROMPT = (
    "Você é um especialista em gestão e comunicação para agências de marketing digital. "
    "Escreva sempre em português brasileiro profissional e claro."
)

_FEEDBACK_TEMPLATE = """Com base nas atividades realizadas hoje para o cliente abaixo, \
escreva um feedback informal, animado e motivador que o gestor da agência pode enviar para o cliente.

O texto deve:
- Ser escrito em português brasileiro informal (como uma conversa de WhatsApp profissional)
- Ter no máximo 5 linhas
- Destacar os principais resultados e entregas do dia
- Terminar com uma frase de incentivo ou próximos passos
- NÃO usar bullet points, só texto corrido

Cliente: {nome_cliente}
Atividades do dia:
{lista_atividades}"""

_RELATORIO_TEMPLATE = """Você é um consultor sênior de marketing digital. Com base nas atividades \
realizadas hoje pela equipe, escreva um relatório executivo profissional do dia.

O relatório deve:
- Ser em português brasileiro formal e profissional
- Ter um parágrafo de introdução resumindo o dia
- Para cada cliente, um parágrafo destacando o que foi feito e os resultados
- Finalizar com uma conclusão e perspectivas para os próximos dias
- Tom: confiante, proativo e orientado a resultados

Data: {data}
Atividades do dia:
{resumo_atividades}"""


def _cliente_anthropic():
    """Instancia o cliente Anthropic. Retorna None se a chave não estiver configurada."""
    api_key = os.environ.get('ANTHROPIC_API_KEY', '').strip()
    if not api_key:
        return None
    try:
        import anthropic
        return anthropic.Anthropic(api_key=api_key)
    except ImportError:
        print("AVISO: biblioteca 'anthropic' não instalada.", file=sys.stderr)
        return None


def _chamar_claude(prompt: str, max_tokens: int = 600) -> Optional[str]:
    """Chama a API do Claude e retorna o texto, ou None se não disponível."""
    client = _cliente_anthropic()
    if not client:
        return None
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        print(f"Erro ao chamar API do Claude: {e}", file=sys.stderr)
        return f"[Erro ao gerar conteúdo: verifique sua chave de API e conexão.]"


def gerar_feedback(registros_cliente: list, nome_cliente: str) -> Optional[str]:
    """
    Gera um feedback motivacional (WhatsApp-style) para um cliente específico.
    Retorna None se ANTHROPIC_API_KEY não estiver configurada.
    """
    linhas = []
    for r in registros_cliente:
        linha = f"- {r['funcionario']} ({r['servico_nome']}): {r['descricao']}"
        if r.get('resultado'):
            linha += f" → Resultado: {r['resultado']}"
        linhas.append(linha)

    prompt = _FEEDBACK_TEMPLATE.format(
        nome_cliente=nome_cliente,
        lista_atividades='\n'.join(linhas)
    )
    return _chamar_claude(prompt, max_tokens=400)


def gerar_relatorio_dia(data: str, registros_por_cliente: dict) -> Optional[str]:
    """
    Gera um relatório executivo completo do dia para todos os clientes.

    Parâmetros:
        data:                  data no formato 'YYYY-MM-DD'
        registros_por_cliente: dict { cliente_id: {'nome': str, 'registros': list} }

    Retorna texto do relatório ou None se API não disponível.
    """
    if not registros_por_cliente:
        return None

    # Formata a data para exibição
    try:
        from datetime import date
        d = date.fromisoformat(data)
        data_display = d.strftime('%d/%m/%Y')
    except ValueError:
        data_display = data

    # Monta o resumo de atividades por cliente
    secoes = []
    for dados in sorted(registros_por_cliente.values(), key=lambda x: x['nome']):
        nome_cliente = dados['nome']
        linhas_cliente = [f"Cliente: {nome_cliente}"]
        for r in dados['registros']:
            linha = f"  • {r['funcionario']} ({r['servico_nome']}): {r['descricao']}"
            if r.get('resultado'):
                linha += f"\n    Resultado: {r['resultado']}"
            linhas_cliente.append(linha)
        secoes.append('\n'.join(linhas_cliente))

    resumo = '\n\n'.join(secoes)
    total_tarefas = sum(len(d['registros']) for d in registros_por_cliente.values())
    total_clientes = len(registros_por_cliente)

    cabecalho = (
        f"Total de clientes atendidos: {total_clientes}\n"
        f"Total de tarefas realizadas: {total_tarefas}\n\n"
        f"Detalhamento:\n{resumo}"
    )

    prompt = _RELATORIO_TEMPLATE.format(
        data=data_display,
        resumo_atividades=cabecalho
    )
    return _chamar_claude(prompt, max_tokens=1200)
