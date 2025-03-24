import streamlit as st
import random

st.set_page_config(
    page_icon="espro.png",
    page_title="QUIZ ESPRO"
)

st.logo("esproLogo.png")

# Ocultar a barra:
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("""
    <style>
        .css-1d391kg {
            background-color: #121212;
            color: #f5f5f5;
        }
        .stButton>button {
            background-color: #2A6ACE;
            color: white;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #112648;
        }
        .stRadio>div>label {
            font-size: 16px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

perguntas_espro = [
    {"pergunta": "Qual é a missão principal da Espro?", "alternativas": ["Formar jovens para o mercado de trabalho", "Oferecer cursos de culinária", "Criar projetos sociais", "Atuar como consultoria"], "resposta": "Formar jovens para o mercado de trabalho"},
    {"pergunta": "Em que ano a Espro foi fundada?", "alternativas": ["1980", "1990", "2000", "2001"], "resposta": "2001"},
    {"pergunta": "Quais são os principais programas oferecidos pela Espro?", "alternativas": ["Aprendizagem Profissional e Cursos de Qualificação", "Cursos de Artes e Música", "Cursos de Tecnologia", "Programa de Líderes"], "resposta": "Aprendizagem Profissional e Cursos de Qualificação"},
    {"pergunta": "Qual é o público-alvo da Espro?", "alternativas": ["Jovens entre 14 e 24 anos", "Idosos", "Adultos em transição de carreira", "Profissionais de TI"], "resposta": "Jovens entre 14 e 24 anos"},
    {"pergunta": "A Espro é uma organização de qual tipo?", "alternativas": ["ONG", "Instituição privada com fins lucrativos", "Instituição pública", "Fundação educativa"], "resposta": "ONG"},
    {"pergunta": "Onde a Espro oferece seus programas de aprendizagem?", "alternativas": ["Em diversas cidades do Brasil", "Somente na capital de São Paulo", "Em São Paulo e Rio de Janeiro", "Somente em escolas de ensino médio"], "resposta": "Em diversas cidades do Brasil"},
    {"pergunta": "Quais valores a Espro preza em seus programas?", "alternativas": ["Responsabilidade, ética e desenvolvimento profissional", "Diversão, lazer e competitividade", "Relações públicas e comunicação", "Criatividade e inovação"], "resposta": "Responsabilidade, ética e desenvolvimento profissional"},
    {"pergunta": "Quais áreas de atuação a Espro oferece para os aprendizes?", "alternativas": ["Administração, TI, logística e atendimento ao cliente", "Medicina, psicologia e educação", "Artes, design e produção cultural", "Arquitetura e engenharia"], "resposta": "Administração, TI, logística e atendimento ao cliente"},
    {"pergunta": "Qual é o objetivo final dos programas de aprendizagem da Espro?", "alternativas": ["Desenvolver habilidades para o mercado de trabalho", "Ensinar artes plásticas", "Prover atividades recreativas", "Ajudar na construção de carreiras acadêmicas"], "resposta": "Desenvolver habilidades para o mercado de trabalho"},
    {"pergunta": "Qual é o benefício principal para os jovens que participam da Espro?", "alternativas": ["Acesso a estágios remunerados", "Vagas em universidades públicas", "Descontos em cursos universitários", "Vagas para intercâmbio"], "resposta": "Acesso a estágios remunerados"},
    {"pergunta": "A Espro possui parcerias com empresas?", "alternativas": ["Sim, para oferecer vagas de aprendizagem e estágio", "Não, é uma instituição independente", "Sim, mas apenas com universidades", "Sim, com escolas e centros de ensino"], "resposta": "Sim, para oferecer vagas de aprendizagem e estágio"},
    {"pergunta": "Qual é a idade mínima para participar do programa de aprendizagem da Espro?", "alternativas": ["14 anos", "16 anos", "18 anos", "21 anos"], "resposta": "14 anos"},
    {"pergunta": "Quais são os objetivos da Espro além da formação profissional?", "alternativas": ["Desenvolver a cidadania e a ética profissional", "Oferecer intercâmbios internacionais", "Promover atividades culturais e sociais", "Criar startups de jovens"], "resposta": "Desenvolver a cidadania e a ética profissional"},
    {"pergunta": "A Espro oferece cursos de qualificação profissional?", "alternativas": ["Sim, para jovens de todas as idades", "Não, apenas programas de estágio", "Sim, mas apenas para empresas parceiras", "Não, oferece apenas treinamento prático"], "resposta": "Sim, para jovens de todas as idades"},
    {"pergunta": "Como os jovens podem se inscrever para participar dos programas da Espro?", "alternativas": ["Por meio do site oficial da Espro", "Pelo LinkedIn", "Enviando e-mail para a instituição", "Por meio de escolas parceiras"], "resposta": "Por meio do site oficial da Espro"},
    {"pergunta": "Qual é o papel do jovem aprendiz durante o programa da Espro?", "alternativas": ["Desenvolver habilidades práticas e realizar atividades educacionais", "Apenas assistir a aulas de formação", "Trabalhar em tempo integral em uma empresa", "Participar de atividades recreativas e culturais"], "resposta": "Desenvolver habilidades práticas e realizar atividades educacionais"},
    {"pergunta": "O que é necessário para ingressar em um programa da Espro?", "alternativas": ["Idade entre 14 e 24 anos e estar cursando ou ter concluído o ensino médio", "Ser formado em ensino superior", "Ser voluntário em algum projeto social", "Ter experiência prévia em empresas"], "resposta": "Idade entre 14 e 24 anos e estar cursando ou ter concluído o ensino médio"}
]

def selecionar_perguntas():
    perguntas_selecionadas = random.sample(perguntas_espro, 5) 
    random.shuffle(perguntas_selecionadas)
    for pergunta in perguntas_selecionadas:
        random.shuffle(pergunta["alternativas"])
    return perguntas_selecionadas

def verificar_respostas(perguntas_selecionadas):
    respostas_certas = 0
    for i, pergunta in enumerate(perguntas_selecionadas):
        resposta_usuario = st.session_state.get(f"resposta_{i}", "")
        if resposta_usuario == pergunta["resposta"]:
            respostas_certas += 1
    return respostas_certas

def exibir_quiz():
    st.title("Quiz - ESPRO")
    st.subheader("Selecione as respostas!!")
    
    if 'perguntas_selecionadas' not in st.session_state:
        st.session_state.perguntas_selecionadas = selecionar_perguntas()
    
    perguntas_selecionadas = st.session_state.perguntas_selecionadas
    
    for i, pergunta in enumerate(perguntas_selecionadas):
        st.subheader(f"{i+1}) {pergunta['pergunta']}")
        resposta = st.selectbox(
            f"Escolha uma alternativa para a pergunta {i+1}",
            ["Selecione uma resposta"] + pergunta["alternativas"],
            key=f"resposta_{i}"
        )
    
    if st.button("Verificar Respostas"):
        respostas_certas = verificar_respostas(perguntas_selecionadas)
        st.toast(f"🏆 Você acertou {respostas_certas} de 5 perguntas!")
        if respostas_certas == 5:
            st.balloons()
            st.toast(f"🏆 Parabens!! Você acertou todas as perguntas")
        
exibir_quiz()
