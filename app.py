import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
import random
import os

# Firebase Configuration
firebase_config_path = os.path.join(os.getcwd(), "firebase_config.json")

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
# Custom Styling
st.markdown(
    """
    <style>
    .main {background-color:rgb(131, 159, 216);}
    .stButton >button {background-color:#4CAF50; color: white;}
    .stRadio div{ background-color: #ffffff; padding: 10px; border-radius: 5px;}
    .stTable{font-size: 16px;}
    </style>
    """, unsafe_allow_html=True
)

# Authentication Functions
def register_user(email, password, username):
    try:
        user = auth.create_user(email=email, password=password, display_name=username)
        db.collection("users").document(user.uid).set({"username": username, "score": 0})
        st.sidebar.success("✅ Account Created! Please log in.")
    except Exception as e:
        st.sidebar.error(f"⚠️ Error: {e}")

def login_user(email):
    try:
        user = auth.get_user_by_email(email)
        return user
    except Exception:
        return None

# Fetch Leaderboard Data
def get_leaderboard():
    try:
        users_ref = db.collection("users").order_by("score", direction=firestore.Query.DESCENDING).limit(5).stream()
        return [{"username": user.get("username"), "score": user.get("score")} for user in users_ref]
    except Exception as e:
        st.error(f"Error fetching leaderboard: {e}")
        return []

# Streamlit App
st.title("🧬 BioHack Gamified Biotech Learning App 🎮")
st.write("**Learn Genetics & Biotechnology through fun challenges!**")

# User Authentication

st.sidebar.subheader("🔑 User Authentication")
user_email = st.sidebar.text_input("📧 Email:")
user_password = st.sidebar.text_input("🔑 Password:", type="password")
username = st.sidebar.text_input("🆔 Username (for Signup)")

if st.sidebar.button("Sign Up"):
    if user_email and user_password and username:
        register_user(user_email, user_password, username)
    else:
        st.sidebar.warning("⚠️ Please fill in all fields.")



user = None

if st.sidebar.button("Login"):
    user = login_user(user_email)
    if user:
        st.sidebar.success(f"🎉 Welcome back, {user.display_name if user.display_name else 'User'}!")
    else:
        st.sidebar.error("⚠️ Login Failed! Check your email or register.")


# Tabs for Games
tab1, tab2, tab3, tab4 = st.tabs(["🎓 Quiz Mode", "🧬 DNA Matching Game", "🧪 PCR Simulator", "🏆 Leaderboard"])

# **Quiz Mode**
with tab1:
    st.subheader("🔬 Biotech Quiz Challenge")

    quiz_questions = [
         {"question": "Which molecule carries genetic instructions?", "options": ["Protein", "DNA", "RNA", "Lipid"], "correct_answer": "DNA"},
    {"question": "What is the full form of PCR?", "options": ["Polymerase Chain Reaction", "Protein Cloning Reaction", "Polymer Coding Reaction", "Primary Cell Replication"], "correct_answer": "Polymerase Chain Reaction"},
    {"question": "Which base pairs with Adenine in DNA?", "options": ["Guanine", "Thymine", "Cytosine", "Uracil"], "correct_answer": "Thymine"},
    {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Ribosome", "Mitochondria", "Golgi Apparatus"], "correct_answer": "Mitochondria"},
    {"question": "Which nitrogenous base is found in RNA but not in DNA?", "options": ["Thymine", "Cytosine", "Uracil", "Adenine"], "correct_answer": "Uracil"},
    {"question": "Which enzyme unzips DNA during replication?", "options": ["Helicase", "Ligase", "Polymerase", "Topoisomerase"], "correct_answer": "Helicase"},
    {"question": "What is the basic unit of proteins?", "options": ["Nucleotides", "Amino acids", "Fatty acids", "Monosaccharides"], "correct_answer": "Amino acids"},
    {"question": "Which type of RNA carries amino acids?", "options": ["mRNA", "tRNA", "rRNA", "siRNA"], "correct_answer": "tRNA"},
    {"question": "What does CRISPR technology enable?", "options": ["Gene editing", "Protein synthesis", "RNA translation", "Cell division"], "correct_answer": "Gene editing"},
    {"question": "Which organelle is responsible for protein synthesis?", "options": ["Lysosome", "Ribosome", "Mitochondria", "Nucleus"], "correct_answer": "Ribosome"},
    {"question": "What does 'GMO' stand for?", "options": ["Genetically Modified Organism", "Genetic Modification Operation", "General Molecular Organization", "Gene Mutation Output"], "correct_answer": "Genetically Modified Organism"},
    {"question": "Which sugar is present in DNA?", "options": ["Ribose", "Deoxyribose", "Glucose", "Fructose"], "correct_answer": "Deoxyribose"},
    {"question": "Which enzyme synthesizes RNA from a DNA template?", "options": ["DNA polymerase", "RNA polymerase", "Ligase", "Helicase"], "correct_answer": "RNA polymerase"},
    {"question": "What is the function of ribosomes?", "options": ["Lipid synthesis", "DNA replication", "Protein synthesis", "Energy production"], "correct_answer": "Protein synthesis"},
    {"question": "Which genetic disorder is caused by an extra chromosome 21?", "options": ["Turner syndrome", "Down syndrome", "Klinefelter syndrome", "Cystic fibrosis"], "correct_answer": "Down syndrome"},
    {"question": "Which process converts DNA into mRNA?", "options": ["Replication", "Translation", "Transcription", "Mutation"], "correct_answer": "Transcription"},
    {"question": "Which molecule carries amino acids to the ribosome?", "options": ["mRNA", "tRNA", "rRNA", "DNA"], "correct_answer": "tRNA"},
    {"question": "Which type of bond holds base pairs together in DNA?", "options": ["Covalent bond", "Ionic bond", "Hydrogen bond", "Peptide bond"], "correct_answer": "Hydrogen bond"},
    {"question": "Which part of the cell contains genetic material?", "options": ["Cytoplasm", "Mitochondria", "Nucleus", "Golgi apparatus"], "correct_answer": "Nucleus"},
    {"question": "What is the function of lysosomes?", "options": ["Protein synthesis", "Digestion of waste", "Energy production", "DNA replication"], "correct_answer": "Digestion of waste"},
    ]

    question = random.choice(quiz_questions)
    st.subheader(question["question"])

    user_answers = {option: st.checkbox(option) for option in question["options"]}

    if st.button("Submit Answer"):
        selected_answers = [option for option, checked in user_answers.items() if checked]

        if len(selected_answers) == 1 and selected_answers[0] == question["correct_answer"]:
            st.success("✅ Correct! You earned points! 🎉")
            if user:
                user_ref = db.collection("users").document(user.uid)
                user_data = user_ref.get().to_dict()
                if user_data:
                    new_score = user_data["score"] + 10
                    user_ref.update({"score": new_score})
                    st.sidebar.info(f"🎉 Your new score: {new_score}")
        elif len(selected_answers) > 1:
            st.warning("⚠️ You selected multiple answers. Please select only one!")
        else:
            st.error(f"❌ Wrong answer! The correct answer is: {question['correct_answer']}")

# **DNA Matching Game**
with tab2:
    st.subheader("🔗 DNA Base Pair Matching")
    dna_sequence ="ACCGTGTA"
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}

    shuffled = list(dna_sequence)
    random.shuffle(shuffled)

    st.info(f"🔄 Unscramble the sequence: {''.join(shuffled)}")

    user_sequence = st.text_input ("Enter the correct complementary DNA sequence:")


    if st.button("Check DNA Match"):
        correct_sequence = "".json([complement[base] for base in dna_sequence])
        if user_sequence.upper()  == correct_sequence:
            st.success("✅ Correct DNA sequence! 🎉")
        else:
            st.error (f"❌ Wrong! The correct sequence is: {correct_sequence}")

# **PCR Simulator**
with tab3:
    st.subheader("🔥 PCR Reaction Simulator")
    pcr_stages =[
        {"name": "Denaturation", "temp": 95},
        {"name": "Annealing", "temp": 55},
        {"name": "Extension", "temp": 72}
    ]


    stage = random.choice(pcr_stages)
    st.subheader(f"🔬 Set the correct temperature for: {stage['name']}")

    user_temp = st.slider ("🌡 Choose Temperature (°C)", 30, 100, 50)



    if st.button("Submit Temperature"):
        if user_temp == stage["temp"]:
            st.success("✅ Correct! You mastered this step! 🎉")
        else:
            st.error(f"❌ Incorrect! The correct temperature for {stage['name']} is {stage['temp']}°C.")



# 🏆 **LEADERBOARD**
with tab4:
    st.subheader("🏆 Top 5 Players")
    leaderboard = get_leaderboard()
    if leaderboard:
        st.table(leaderboard)
    else:
        st.warning("No leaderboard data available.")
