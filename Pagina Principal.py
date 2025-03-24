import streamlit as st
import time
import random
import re

# Configuração da página
st.set_page_config(
    page_title="ESPRO - BOT LILI",
    page_icon="espro.png"
)

st.markdown("""
    <style>
    .header {
        background-color: #6E37A6;
        padding: 10px;
        color: white;
        font-size: 34px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        border-radius: 9px;
    }
    </style>
    <div class="header">
        Desafio Espro 🏆
    </div>
    """, unsafe_allow_html=True)

st.sidebar.image("teste.gif")
st.logo("esproLogo.png")
st.subheader("Bem-vindo(a) ao jogo! Digite 'Iniciar' para começar.")

# Estado da sessão
if "fase" not in st.session_state:
    st.session_state.fase = 0
if "jogo_iniciado" not in st.session_state:
    st.session_state.jogo_iniciado = False
if "chats" not in st.session_state:
    st.session_state.chats = [("assistant", 
        "Opa, bem-vindo ao **Desafio Espro**! Eu sou a **Lili**, a jovem aprendiz mais estilosa da ESPRO.\n\n"
        "Aqui eu vou testar se você realmente sabe tudo sobre a ESPRO, ou se tá só enrolando! 😆\n\n"
        "Cada pergunta tem **alternativas**, então não tem desculpa pra errar hein! Bora jogar?\n\n"
        "Digite **'Iniciar'** e me mostra que tu manja! 😉")]
if "pontuacao" not in st.session_state:
    st.session_state.pontuacao = 0
if "perguntas_feitas" not in st.session_state:
    st.session_state.perguntas_feitas = []  # Para não repetir perguntas
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "current_mapping" not in st.session_state:
    st.session_state.current_mapping = {}  # Mapeia letras (A, B, C, D) para alternativas
if "current_correct_letter" not in st.session_state:
    st.session_state.current_correct_letter = None

if "inicio" not in st.session_state:
    st.session_state.inicio = None

# Perguntas da Espro (todas as perguntas)
perguntas_espro = [
    {"pergunta": "Qual é a missão principal da Espro? 🎯", "alternativas": ["Formar jovens para o mercado de trabalho", "Oferecer cursos de culinária", "Criar projetos sociais", "Atuar como consultoria"], "resposta": "Formar jovens para o mercado de trabalho"},
    {"pergunta": "Em que ano a Espro foi fundada? 📅", "alternativas": ["1980", "1990", "2000", "2001"], "resposta": "2001"},
    {"pergunta": "Quais são os principais programas oferecidos pela Espro? 📚", "alternativas": ["Aprendizagem Profissional e Cursos de Qualificação", "Cursos de Artes e Música", "Cursos de Tecnologia", "Programa de Líderes"], "resposta": "Aprendizagem Profissional e Cursos de Qualificação"},
    {"pergunta": "Qual é o público-alvo da Espro? 🧑‍🎓", "alternativas": ["Jovens entre 14 e 24 anos", "Idosos", "Adultos em transição de carreira", "Profissionais de TI"], "resposta": "Jovens entre 14 e 24 anos"},
    {"pergunta": "A Espro é uma organização de qual tipo? 🏢", "alternativas": ["ONG", "Instituição privada com fins lucrativos", "Instituição pública", "Fundação educativa"], "resposta": "ONG"},
    {"pergunta": "Onde a Espro oferece seus programas de aprendizagem? 🌎", "alternativas": ["Em diversas cidades do Brasil", "Somente na capital de São Paulo", "Em São Paulo e Rio de Janeiro", "Somente em escolas de ensino médio"], "resposta": "Em diversas cidades do Brasil"},
    {"pergunta": "Quais valores a Espro preza em seus programas? 💡", "alternativas": ["Responsabilidade, ética e desenvolvimento profissional", "Diversão, lazer e competitividade", "Relações públicas e comunicação", "Criatividade e inovação"], "resposta": "Responsabilidade, ética e desenvolvimento profissional"},
    {"pergunta": "Quais são as áreas de atuação da Espro para os aprendizes? 💼", "alternativas": ["Administração, TI, logística e atendimento ao cliente", "Medicina, psicologia e educação", "Artes, design e produção cultural", "Arquitetura e engenharia"], "resposta": "Administração, TI, logística e atendimento ao cliente"},
    {"pergunta": "Qual é o objetivo final dos programas de aprendizagem da Espro? 🎯", "alternativas": ["Desenvolver habilidades para o mercado de trabalho", "Ensinar artes plásticas", "Prover atividades recreativas", "Ajudar na construção de carreiras acadêmicas"], "resposta": "Desenvolver habilidades para o mercado de trabalho"},
    {"pergunta": "Qual é o benefício principal para os jovens que participam da Espro? 🎁", "alternativas": ["Vagas para intercâmbio", "Vagas em universidades públicas", "Acesso a estágios remunerados", "Descontos em cursos universitários"], "resposta": "Acesso a estágios remunerados"},
    {"pergunta": "A Espro possui parcerias com empresas? 🤝", "alternativas": ["Sim, para oferecer vagas de aprendizagem e estágio", "Não, é uma instituição independente", "Sim, mas apenas com universidades", "Sim, com escolas e centros de ensino"], "resposta": "Sim, para oferecer vagas de aprendizagem e estágio"},
    {"pergunta": "Qual é a idade mínima para participar do programa de aprendizagem da Espro? 🕒", "alternativas": ["14 anos", "16 anos", "18 anos", "21 anos"], "resposta": "14 anos"},
    {"pergunta": "Quais são os objetivos da Espro além da formação profissional? 🌍", "alternativas": ["Desenvolver a cidadania e a ética profissional", "Oferecer intercâmbios internacionais", "Promover atividades culturais e sociais", "Criar startups de jovens"], "resposta": "Desenvolver a cidadania e a ética profissional"},
    {"pergunta": "A Espro oferece cursos de qualificação profissional? 🏫", "alternativas": ["Sim, para jovens de todas as idades", "Não, apenas programas de estágio", "Sim, mas apenas para empresas parceiras", "Não, oferece apenas treinamento prático"], "resposta": "Sim, para jovens de todas as idades"},
    {"pergunta": "Como os jovens podem se inscrever para participar dos programas da Espro? 📝", "alternativas": ["Por meio do site oficial da Espro", "Pelo LinkedIn", "Enviando e-mail para a instituição", "Por meio de escolas parceiras"], "resposta": "Por meio do site oficial da Espro"},
    {"pergunta": "Qual é o papel do jovem aprendiz durante o programa da Espro? 👨‍🏫", "alternativas": ["Desenvolver habilidades práticas e realizar atividades educacionais", "Apenas assistir a aulas de formação", "Trabalhar em tempo integral em uma empresa", "Participar de atividades recreativas e culturais"], "resposta": "Desenvolver habilidades práticas e realizar atividades educacionais"},
    {"pergunta": "O que é necessário para ingressar em um programa da Espro? 🏅", "alternativas": ["Idade entre 14 e 24 anos e estar cursando ou ter concluído o ensino médio", "Ser formado em ensino superior", "Ser voluntário em algum projeto social", "Ter experiência prévia em empresas"], "resposta": "Idade entre 14 e 24 anos e estar cursando ou ter concluído o ensino médio"}
]

def formatar_resposta(resposta):
    """Normaliza a resposta para aceitar, por exemplo, 'a', 'A', 'a)' ou 'A)'."""
    resposta = resposta.strip()
    resposta = re.sub(r"[^A-Da-d]", "", resposta)
    return resposta.upper()

def exibir_pergunta(pergunta):
    """
    Embaralha as alternativas da pergunta, gera o mapeamento letra->alternativa e determina
    qual letra corresponde à resposta correta.
    """
    alternativas = pergunta["alternativas"].copy()  # Copia para não alterar a original
    random.shuffle(alternativas)
    mapping = {}
    mensagem = f"**{pergunta['pergunta']}**\n\n"
    for i, alt in enumerate(alternativas):
        letra = chr(65 + i)  # 'A', 'B', 'C', 'D'
        mapping[letra] = alt
        mensagem += f"{letra}) {alt}\n\n"
    # Determinar qual letra corresponde à resposta correta:
    letra_correta = None
    for letra, alt in mapping.items():
        if alt == pergunta["resposta"]:
            letra_correta = letra
            break
    return mensagem, mapping, letra_correta

prompt = st.chat_input("Digite sua resposta...")

if prompt:
    st.session_state.chats.append(("user", prompt))
    
    if not st.session_state.jogo_iniciado:
        if prompt.lower() == "iniciar":
            st.session_state.jogo_iniciado = True
            st.session_state.fase = 0
            st.session_state.pontuacao = 0
            st.session_state.inicio = time.time()  # Início do jogo
            st.session_state.chats.append(("assistant", "🎯 Beleza, bora pro jogo! Aqui vai a primeira pergunta:"))
            
            # Seleciona uma pergunta aleatória que ainda não foi feita
            perguntas_restantes = [p for p in perguntas_espro if p not in st.session_state.perguntas_feitas]
            pergunta_atual = random.choice(perguntas_restantes)
            st.session_state.current_question = pergunta_atual
            mensagem_pergunta, mapping, letra_correta = exibir_pergunta(pergunta_atual)
            st.session_state.current_mapping = mapping
            st.session_state.current_correct_letter = letra_correta
            
            st.session_state.chats.append(("assistant", mensagem_pergunta))
        else:
            st.session_state.chats.append(("assistant", "😤 Bora começar logo! Digita **'Iniciar'** e me mostra que tu sabe!"))
    else:
        # O usuário já iniciou o jogo e está respondendo à pergunta atual.
        resposta_usuario = formatar_resposta(prompt)
        # Verifica se o usuário já tem uma pergunta atual armazenada
        if st.session_state.current_question is None:
            st.session_state.chats.append(("assistant", "Ops! Algo deu errado, vamos reiniciar o jogo. Digite **'Iniciar'** novamente."))
        else:
            if resposta_usuario == st.session_state.current_correct_letter:
                st.session_state.pontuacao += 1
                st.session_state.chats.append(("assistant", "🎉 EITA, ACERTOU! Tá mandando bem! Bora pra próxima! 🚀"))
                # Adiciona a pergunta atual à lista de feitas
                st.session_state.perguntas_feitas.append(st.session_state.current_question)
                st.session_state.fase += 1
                st.session_state.current_question = None  # Limpa a pergunta atual
            else:
                st.session_state.chats.append(("assistant", 
                    "❌ Ihhh, errou! Será que você estudou mesmo? 🤔💀 Vou fingir que não vi, tenta de novo! 😆"))
            
        # Se ainda não completou 7 perguntas, exibe a mesma pergunta novamente se não foi acertada,
        # ou uma nova pergunta se a anterior foi acertada.
        if st.session_state.fase < 7:
            # Se a pergunta não foi acertada, reexibe a mesma
            if st.session_state.current_question is not None:
                mensagem_pergunta, mapping, letra_correta = exibir_pergunta(st.session_state.current_question)
                st.session_state.current_mapping = mapping
                st.session_state.current_correct_letter = letra_correta
                st.session_state.chats.append(("assistant", mensagem_pergunta))
            else:
                # Seleciona uma nova pergunta que ainda não foi feita
                perguntas_restantes = [p for p in perguntas_espro if p not in st.session_state.perguntas_feitas]
                if perguntas_restantes:  # Se ainda houver perguntas disponíveis
                    pergunta_atual = random.choice(perguntas_restantes)
                    st.session_state.current_question = pergunta_atual
                    mensagem_pergunta, mapping, letra_correta = exibir_pergunta(pergunta_atual)
                    st.session_state.current_mapping = mapping
                    st.session_state.current_correct_letter = letra_correta
                    st.session_state.chats.append(("assistant", mensagem_pergunta))
                else:
                    # Se não houver perguntas restantes, finaliza o jogo
                    st.session_state.fase = 7
        else:
            # Finaliza o jogo e exibe os resultados
            tempo_total = time.time() - st.session_state.inicio
            tempo_formatado = time.strftime("%M:%S", time.gmtime(tempo_total))
            st.balloons()
            st.session_state.chats.append(("assistant", 
                f"🏆 **FIM DO JOGO!**\n\n"
                f"🔥 Ufa, foram 7 perguntas! Agora me diz, foi habilidade ou foi sorte? 😆\n\n"
                f"⏰ O tempo total foi de **{tempo_formatado}**.\n\n"
                "Se quiser tentar de novo e ver se consegue um **desempenho digno**, é só reiniciar! 😉"))
            if tempo_formatado <= "00:30":
                st.toast("Parabéns! Terminou antes do tempo", icon="🎉")
            else:
                st.toast("Tempo esgotado! Terminou depois do tempo haha!!", icon="⏰")

for remetente, mensagem in st.session_state.chats:
    st.chat_message(remetente).markdown(mensagem)

if st.sidebar.button("Reiniciar Jogo"):
    st.session_state.fase = 0
    st.session_state.jogo_iniciado = False
    st.session_state.pontuacao = 0
    st.session_state.perguntas_feitas = []
    st.session_state.current_question = None
    st.session_state.current_mapping = {}
    st.session_state.current_correct_letter = None
    st.session_state.chats = [("assistant", "🔥 Bora jogar de novo? Digita **'Iniciar'** e vamos ver se aprendeu algo! 😏")]
    st.toast("Reiniciando o jogo...", icon="⌛")
    time.sleep(2)
    st.rerun()
