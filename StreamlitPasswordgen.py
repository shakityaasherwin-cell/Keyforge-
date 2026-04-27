import streamlit as st
import pandas as pd
import secrets, string, json, os

# --- STUDENT BRANDING & CSS ---
st.set_page_config(page_title="KeyForge Vault", page_icon="🔑", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0a0a0f; color: #e8e8f0; }
    .stButton>button { width: 100%; border-radius: 10px; background: linear-gradient(135deg, #7c3aed, #06b6d4); color: white; border: none; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #16161f; color: white; border: 1px solid #2a2a3a; }
    .css-1r6slb0 { background-color: #111118; border: 1px solid #2a2a3a; border-radius: 15px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION ---
def check_password():
    """Returns `True` if the user had not the password."""
    def password_entered():
        if st.session_state["password"] == "keyforge2024":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.warning("🔐 Enter password to access KeyForge")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.error("❌ Incorrect password")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- APP STATE & LOGIC ---
if 'vault' not in st.session_state:
    if os.path.exists('vault.json'):
        with open('vault.json', 'r') as f: st.session_state.vault = json.load(f)
    else: st.session_state.vault = []

def save_v():
    with open('vault.json', 'w') as f: json.dump(st.session_state.vault, f)

# --- UI HEADER ---
st.title("🔑 KeyForge")
st.caption("Secure Password Generator & Vault Manager")

tab1, tab2, tab3, tab4 = st.tabs(["⚡ Generator", "🔒 Vault", "⚙️ Settings", "🛡️ Security Tips"])

# --- TAB 1: GENERATOR ---
with tab1:
    with st.container():
        length = st.slider("Password Length", 8, 64, 16)
        col1, col2 = st.columns(2)
        use_lower = col1.checkbox("abc (Lowercase)", True)
        use_upper = col2.checkbox("ABC (Uppercase)", True)
        use_nums = col1.checkbox("123 (Numbers)", True)
        use_syms = col2.checkbox("!@# (Symbols)", True)
        
        charset = ""
        if use_lower: charset += string.ascii_lowercase
        if use_upper: charset += string.ascii_uppercase
        if use_nums: charset += string.digits
        if use_syms: charset += string.punctuation
        
        if charset:
            pw = "".join(secrets.choice(charset) for _ in range(length))
        else:
            pw = "Select at least one character type"
        
        st.code(pw, language=None)
        
        st.subheader("Save to Vault")
        site_name = st.text_input("Site/Service Name", placeholder="e.g., Gmail, GitHub, Netflix")
        username = st.text_input("Username/Email", placeholder="e.g., user@example.com")
        
        if st.button("Save Password"):
            if site_name and username and pw != "Select at least one character type":
                st.session_state.vault.append({"Site": site_name, "User": username, "Pass": pw})
                save_v()
                st.success(f"✅ Saved '{site_name}' to Vault!")
            else:
                st.error("Please fill in all fields and generate a password")

# --- TAB 2: VAULT ---
with tab2:
    search = st.text_input("🔍 Search entries...")
    for i, entry in enumerate(st.session_state.vault):
        site = entry.get('Site', entry.get('site', 'Unknown'))
        user = entry.get('User', entry.get('user', 'Unknown'))
        passwd = entry.get('Pass', entry.get('pass', 'Unknown'))
        if not search or search.lower() in site.lower():
            with st.expander(f"🌐 {site} ({user})"):
                st.text(f"Password: {passwd}")
                if st.button(f"🗑 Delete {i}", key=f"del_{i}"):
                    st.session_state.vault.pop(i)
                    save_v()
                    st.rerun()

# --- TAB 3: SETTINGS ---
with tab3:
    st.subheader("Data Management")
    if st.button("🗑 Wipe All Data"):
        st.session_state.vault = []
        save_v()
        st.warning("Vault cleared.")
    
    st.download_button("📤 Export Vault (JSON)", 
                       data=json.dumps(st.session_state.vault), 
                       file_name="keyforge_export.json")

    st.info("Project by: Team KeyForge (Local storage mode active)")

# --- TAB 4: SECURITY TIPS ---
with tab4:
    st.title("🛡️ Password Security Tips")
    st.markdown("---")
    
    # Tip 1
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("🔐 Use 16+ Characters")
        st.write("Strong protection against brute-force attacks. The longer your password, the harder it is to crack.")
    with col2:
        st.metric("", "16+")
    st.markdown("---")
    
    # Tip 2
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("🎲 Mix All Character Types")
        st.write("Uppercase, lowercase, numbers, and symbols create exponentially stronger passwords.")
    with col2:
        st.write("✓ ABC ✓ abc ✓ 123 ✓ !@#")
    st.markdown("---")
    
    # Tip 3
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("🔄 Never Reuse Passwords")
        st.write("Each account deserves a unique password. If one service gets breached, your other accounts remain safe.")
    with col2:
        st.write("🚨 One breach = All accounts at risk")
    st.markdown("---")
    
    # Tip 4
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("🛡️ Enable 2FA Everywhere")
        st.write("Two-factor authentication adds a second layer of defense, even if your password is compromised.")
    with col2:
        st.write("Extra layer of protection")
    st.markdown("---")
    
    # Tip 5
    st.subheader("⚠️ Never Share Passwords")
    st.error("❌ NEVER share passwords via email, chat, SMS, or any unencrypted method.")
    st.success("✅ Keep passwords private. Use password managers (like this one!) to store them securely.")
    
    st.markdown("---")
    st.info("💡 Pro Tip: Use this KeyForge tool to generate unique, strong passwords for all your accounts!")   
