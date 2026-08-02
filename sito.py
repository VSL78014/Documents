import streamlit as st
import streamlit_authenticator as stauth
import sympy as sp
utenti = {
    "usernames": {
        "Francescopizzichemi13@gmail.com": {
            "name": "P.dldd7",
            "password": "JessaSolina89"
        },
        "bonarrigovasyl@gmail.com": {
            "name": "Vasyl",
            "password": "JessaSolina89"
        },
        "claudiocalanna88@gmail.com": {
            "name": "Claudio",
            "password": "JessaSolina89"
        }
    }
}

authenticator = stauth.Authenticate(
    utenti,
    cookie_name="simulatore_moti_cookie",
    key="chiave_segreta_univoca",
    cookie_expiry_days=30
)

# RIGA MODIFICATA: Usiamo il parametro esplicito location='main'
# Mostra il form di login e recupera lo stato in modo corretto
authenticator.login(location='main')

authentication_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")
username = st.session_state.get("username")
if authentication_status == False:
    st.error("Email o Password errati. Riprova.")
elif authentication_status == None:
    st.warning("Inserisci le tue credenziali per accedere al simulatore.")
elif authentication_status == True:
    
    # Questo aggiunge il tasto logout nella barra laterale
    authenticator.logout('Disconnetti', 'sidebar')
    
    # ----------------------------------------------------------------
    # DA QUI IN POI INIZIA IL TUO VECCHIO CODICE!
    # (Tutto il resto del file deve stare dentro questo "if", quindi 
    # ricordati di selezionarlo tutto e premere il tasto TAB una volta)
    # ----------------------------------------------------------------
    st.title("🦿 Risolvitore Guidato di Cinematica")
        # ... tutto il resto del tuo codice ...
    import re
    # --- MENU LATERALE ---
    st.sidebar.title("📚 Centro di Studio")
    sezione = st.sidebar.selectbox(
        "Scegli dove andare:",
        ["Home", "Algebra", "Geometria", "Fisica"]
    )

    # =================================================================
    # 🏠 PAGINA PRINCIPALE: HOME
    # =================================================================
    if sezione == "Home":
        # Spostiamo QUI il titolo principale che si vedeva nello screenshot!
        st.title("🧮 Risolutore e Formulario Matematico/Fisico")
        st.subheader("Benvenuto nel tuo hub di studio personale!")
        st.write("""
        Usa il menu a tendina nella barra laterale a sinistra per navigare tra le sezioni:
        * **Algebra:** Risolvi equazioni/disequazioni con passaggi completi stile Google e studia retta e parabola.
        * **Geometria:** Ripassa i teoremi di Pitagora, Euclide e le proprietà dei poligoni.
        * **Fisica:** Consulta le formule dei moti cinematici e i principi della dinamica.
        """)

   # =================================================================
    # 🧮 SEZIONE 1: ALGEBRA
    # =================================================================
    elif sezione == "Algebra":
        st.title("Strumenti e Formule di Algebra")
        
        # Sotto-menu per l'Algebra
        sub_algebra = st.selectbox("Scegli l'argomento:", ["Risolutore Equazioni/Disequazioni", "La Parabola", "La Retta"])
        
        if sub_algebra == "Risolutore Equazioni/Disequazioni":
            st.subheader("Risolutore Automatico di 2° Grado")

            stringa_utente = st.text_input("Inserisci l'equazione o disequazione:")
            
            if stringa_utente:
                stringa_spaziata = re.sub(r'([><=])', r' \1 ', stringa_utente)
                pezzi = re.findall(r'[+-]?\d*x\^2|[+-]?\d*x|[+-]?\d+|[><=]', stringa_spaziata)
                
                simbolo = ""
                if ">" in stringa_utente:
                    simbolo = ">"
                elif "<" in stringa_utente:
                    simbolo = "<"
                elif "=" in stringa_utente:
                    simbolo = "="
                else:
                    simbolo = "="
                
                st.write(f"Operazione inserita: `{stringa_utente}`")
                
                a = 0.0
                b = 0.0
                c = 0.0
        def estrai_coefficienti(testo_membro):
            testo_spaziato = re.sub(r'([<>=])', r' \1 ', testo_membro)
            blocchi = re.findall(r'([+-]?\d*x\^2|[+-]?\d*x|[+-]?\d+)', testo_spaziato)
            coeff_a, coeff_b, coeff_c = 0.0, 0.0, 0.0
            for p in blocchi:
                p = p.strip()
                if "x^2" in p:
                    val = p.replace("x^2", "")
                    coeff_a += 1.0 if val in ["", "+"] else (-1.0 if val == "-" else float(val))
                elif "x" in p:
                    val = p.replace("x", "")
                    coeff_b += 1.0 if val in ["", "+"] else (-1.0 if val == "-" else float(val))
                elif p not in ["", "+", "-", "="]:
                    coeff_c += float(p)
            return coeff_a, coeff_b, coeff_c

        passaggi_algebra = "### 🛠️ Passaggi Algebrici (Forma Normale):\n"

        if "=" in stringa_utente:
            parti = stringa_utente.split("=")
            sinistro = parti[0].strip()
            destro = parti[1].strip()

            a_sin, b_sin, c_sin = estrai_coefficienti(sinistro)
            a_des, b_des, c_des = estrai_coefficienti(destro)

            passaggi_algebra += f"1. **Equazione originale:** \n$({sinistro}) = {destro}$\n\n"
            
            if c_des != 0 or a_des != 0 or b_des != 0:
                forma_des_pulita = f"{f'{a_des}x^2' if a_des else ''}{f' {b_des:+}x' if b_des else ''}{f' {c_des:+}' if c_des else ''}".strip()
                passaggi_algebra += f"2. **Semplifichiamo il membro destro:** \n${sinistro} = {forma_des_pulita}$\n\n"

            a = a_sin - a_des
            b = b_sin - b_des
            c = c_sin - c_des

            passaggi_algebra += f"3. **Spostiamo tutti i termini a sinistra cambiando il segno:** \n$({sinistro}) - ({destro}) = 0$\n\n"
            passaggi_algebra += f"4. **Sommiamo i termini simili:** \n${a}x^2 {b:+}x {c:+} = 0$\n\n"
            passaggi_algebra += f"5. **Identifichiamo i coefficienti definitivi:** \n$a = {a}$, $b = {b}$, $c = {c}$\n---"
        else:
            a, b, c = estrai_coefficienti(stringa_utente)
            passaggi_algebra += f"1. **Espressione in forma normale:** \n${a}x^2 {b:+}x {c:+} = 0$\n\n"
            passaggi_algebra += f"2. **Coefficienti estratti:** \n$a = {a}$, $b = {b}$, $c = {c}$\n---"
        delta = b**2 - 4 * a * c
        if delta > 0:
            if delta > 0:
             st.markdown(passaggi_algebra)
            
            # Calcolo esatto con SymPy
            a_sym = sp.Rational(str(a))
            b_sym = sp.Rational(str(b))
            c_sym = sp.Rational(str(c))
            delta_sym = b_sym**2 - 4 * a_sym * c_sym
            
            x1_exact = (-b_sym - sp.sqrt(delta_sym)) / (2 * a_sym)
            x2_exact = (-b_sym + sp.sqrt(delta_sym)) / (2 * a_sym)
            
            # Ordinamento basato sul valore decimale reale
            if float(x1_exact.evalf()) > float(x2_exact.evalf()):
                x1_exact, x2_exact = x2_exact, x1_exact
                
            # Generazione stringhe LaTeX per il sito
            x1_latex = sp.latex(x1_exact)
            x2_latex = sp.latex(x2_exact)

            # --- GRAFICA DI STREAMLIT (TUTTA INDENTATA DENTRO IL DELTA > 0) ---
            st.success("✅ Calcolo completato con successo!")
            
            with st.expander("📁 Mostra Formule e Procedimento Passo dopo Passo"):
                st.markdown("#### Formule applicate:")
                st.latex(r"\Delta = b^2 - 4ac")
                st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{\Delta}}{2a}")
                
                st.markdown("#### Passaggi numerici:")
                st.write(f"1. **Calcolo del Delta:** $({b})^2 - 4 \\cdot ({a}) \\cdot ({c}) = {delta}$")
                
                st.write("2. **Radici dell'equazione associata:**")
                st.latex(r"x_1 = " + x1_latex)
                st.latex(r"x_2 = " + x2_latex)
                
                if simbolo in [">", "<"]:
                    st.write(f"3. **Studio del segno:** Poiché $a = {a}$ e cerchiamo i valori con il simbolo di `{simbolo}`...")
                else:
                    st.write("3. **Determinazione delle radici:** Abbiamo trovato i punti di intersezione con l'asse x.")

            # Mostra i risultati finali nei box colorati
            if simbolo == "=":
                st.markdown("### 🎯 Risultato dell'Equazione:")
                st.info(f"**Soluzione dell'equazione:** \n\n $x_1 = {x1_latex}$ \n\n $x_2 = {x2_latex}$")
            else:
                st.markdown("### 🎯 Risultato della Disequazione:")
                if simbolo == ">":
                    st.info(f"**Soluzione (Valori Esterni):** \n\n $x < {x1_latex}$ oppure $x > {x2_latex}$")
                elif simbolo == "<":
                    st.info(f"**Soluzione (Valori Interni):** \n\n ${x1_latex} < x < {x2_latex}$")
        elif delta == 0:
           if a != 0:
             x = -b / (2 * a)
             st.write(f"Sostituisco i valori nella formula: x = -({b}) / (2 * ({a}))")
             st.success(f"L'equazione associata ha una sola soluzione: x = {x}")
        
        # Ora il controllo del simbolo è DENTRO l'if, quindi al sicuro!
             if simbolo == ">":
                 st.info(f"x != {x}")
             elif simbolo == "<":
                 st.info("Soluzione: Impossibile (Nessuna soluzione reale)")
            
        else:
            st.warning("Inserisci un'equazione valida per calcolare il risultato.") 
        elif delta < 0:
                st.success("✅ Calcolo completato con successo!")
            
            with st.expander("📂 Mostra Formule e Procedimento Passo dopo Passo"):
             with st.expander("📂 Mostra Formule e Procedimento Passo dopo Passo"):
                # STAMPIAMO I PASSAGGI ALGEBRICI QUI!
                st.markdown(passaggi_algebra)
                st.markdown("#### 2. Calcolo del Delta:")
                st.latex(r"\Delta = b^2 - 4ac")
                st.write(f"**Sostituzione:** $({b})^2 - 4 \\cdot ({a}) \\cdot ({c}) = {delta}$")
                st.write(f"**Analisi del risultato:** Poiché il Delta è negativo ($\Delta < 0$), l'equazione associata non ha soluzioni reali.")

            # Titolo dinamico del risultato
            if simbolo == "=":
                st.markdown("### 🎯 Risultato dell'Equazione:")
                st.info("**Soluzione dell'equazione:** \n\nNessuna soluzione reale ($\Delta < 0$)")
            else:
                st.markdown("### 🎯 Risultato della Disequazione:")
                if simbolo == ">":
                    st.info("**Soluzione:** \n\nQualsiasi valore di $x$ ($x \\in \\mathbb{R}$)")
                elif simbolo == "<":
                    st.info("**Soluzione:** \n\nImpossibile ($x \\in \\emptyset$)") 


    # =================================================================
    # 📐 SEZIONE 2: GEOMETRIA
    # =================================================================
    elif sezione == "Geometria":
        st.title("📐 Formulario di Geometria")
        sub_geometria = st.selectbox("Scegli l'argomento:", ["Pitagora ed Euclide", "Poligoni Inscritti/Circoscritti", "Similitudine"])
        
        if sub_geometria == "Pitagora ed Euclide":
            st.subheader("Teoremi sui Triangoli Rettangoli")


    # =================================================================
    # ⚡ SEZIONE 3: FISICA
    # =================================================================
    elif sezione == "Fisica":
            st.title("⚡ Formulario di Fisica")
            sub_fisica = st.selectbox("Scegli l'argomento:", ["Studio dei Moti (Cinematica)", "I Principi della Dinamica", "Il Pendolo"])
            
            if sub_fisica == "Studio dei Moti (Cinematica)":
                st.subheader("🏃‍♂️ Formulario di Cinematica (I Moti)")
                st.write("Consulta le formule principali per lo studio del movimento dei corpi.")
                
                # --- MOTO RETTILINEO UNIFORME ---
                with st.expander("🔹 Moto Rettilineo Uniforme (MRU)"):
                    st.markdown("**Caratteristica:** Velocità costante ($v = \\text{costante}$) e accelerazione nulla ($a = 0$).")
                    
                    st.markdown("**Formula Principale (Legge Oraria):**")
                    st.latex(r"s = s_0 + v \cdot t")
                    
                    st.markdown("**Formule Inverse:**")
                    st.latex(r"v = \frac{\Delta s}{\Delta t} \quad | \quad t = \frac{\Delta s}{v}")
                    
                    st.info("💡 *Legenda:* $s$ = posizione finale, $s_0$ = posizione iniziale, $v$ = velocità, $t$ = tempo.")
    
                # --- MOTO RETTILINEO UNIFORMEMENTE ACCELERATO ---
                with st.expander("🔸 Moto Rettilineo Uniformemente Accelerato (MRUA)"):
                    st.markdown("**Caratteristica:** Accelerazione costante ($a = \\text{costante}$) e velocità che varia linearmente.")
                    
                    st.markdown("**Legge Oraria della Posizione:**")
                    st.latex(r"s = s_0 + v_0 \cdot t + \frac{1}{2} a \cdot t^2")
                    
                    st.markdown("**Legge della Velocità:**")
                    st.latex(r"v = v_0 + a \cdot t")
                    st.markdown("**Relazione che lega la velocità con il tempo:")
                    st.latex(r"v^2 = 2 a s + v^2_0")
                    st.markdown("**Accelerazione**")
                    st.latex(r"a_m = \frac {\Delta_v}{\Delta_t}")
                    st.info("💡 *Legenda:* $a$ = accelerazione, $v_0$ = velocità iniziale, $v$ = velocità finale.")
                with st.expander("🔸La caduta dei gravi"):
                    st.latex(r"s = \frac{1}{2} g t^2")
                    st.latex(r"v = g t")
                    st.info("Nota: l'accelerazione di gravità(g) è sempre costante, che equivale a 9.81 m/s^2")
    
                with st.expander("🔹 Moto Circolare Uniforme (MCU)"):
                    st.markdown("**Velocità Angolare:**")
                    st.latex(r"\omega = \frac{2\pi}{T}")
                    st.latex(r"\omega = \frac{v}{r}")
                    st.latex(r"\omega = \frac {2\pi}{T}")
                    st.markdown("**Velocità Tangenziale**")
                    st.latex(r"v = \frac{2\pi r}{T}")
                    st.latex(r"v = 2\pi r f")
                    st.latex(r"v = \omega r")
                    st.markdown("**Accelerazione Centripeda**")
                    st.latex(r"a_c = \frac {\Delta_\alpha}{\Delta_t}")
                    st.latex(r"a_c = \frac {v^2}{r}")
                    st.latex(r"a_c = \omega^2 r")
                    st.markdown("**Frequenza**")
                    st.latex(r"f = \frac {1}{T}")
                    st.info("Nota: La frequenza (f) è sempre l'inverso del periodo(T)")
                    st.latex(r"f = \frac{\text{numero di giri}}{\text{tempo impiegato (s)}}")
                with st.expander("🔹Moto Armonico"):
                    st.markdown("**Caratteristica:** Il moto armonico è un particolare tipo di moto oscillatorio e periodico. Si verifica quando un punto si sposta avanti e indietro lungo una linea retta, oscillando tra due estremi attorno a un punto centrale detto centro di oscillazione.")
                    st.info("Al centro:  la velocità è massima e l'accelerazione è nulla")
                    st.info("Agli estremi: : la velocità è nulla e l'accelerazione è massima.")
                    st.markdown("**Formule**")
                    st.latex(r"s = A \cdot \cos(\omega \cdot t)")
                    st.latex(r"a = -\omega^2 \cdot A")
                with st.expander("🔸Il pendolo semplice"):
                    st.markdown("**Caratteristica:** Il pendolo semplice è un sistema ideale costituito da una massa puntiforme m sospesa a un filo inestensibile e privo di massa")
                    st.latex(r"T = 2\pi \cdot \sqrt{\frac{L}{g}}")
                    st.markdown("**Pendolo Semplice (Formule Inverse):**")
                
                    st.markdown("Per trovare la **lunghezza del filo ($l$):**")
                    st.latex(r"l = g \cdot \left(\frac {T}{2\pi}\right)^2")
                    
                    st.markdown("Per trovare l'**accelerazione di gravità ($g$):**")
                    st.latex(r"g = \frac{4\pi^2 \cdot l}{T^2}")
                    
                    st.info("💡 *Legenda:* $T$ = periodo (s), $l$ = lunghezza del filo (m), $g$ = accelerazione di gravità ($9.81 \\text{ m/s}^2$).")
                with st.expander("🔹 Il moto parabolico"):
                    st.markdown("**Caratteristica:** Il moto parabolico (o moto del proiettile) è un movimento bidimensionale in cui un oggetto segue una traiettoria a forma di parabola. Si ottiene lanciando un corpo con una certa velocità iniziale e trascurando la resistenza dell'aria.")
                    st.markdown("Formule:")
                    st.latex(r"y = \frac {g \cdot x^2}{2 \cdot v^2_0}")
                    st.latex(r"""
                    \begin{cases} 
                    x = v_{0x} \cdot t \\ 
                    y = y_0 + v_{0y} \cdot t - \frac{1}{2}g \cdot t^2 
                    \end{cases}
                    """)
                with st.expander("🔹I tre princìpi della dinamica"):
                    st.markdown("**Il primo principio della dinamica**")
                    st.markdown("**Caratteristica:** Il primo principio della dinamica, noto anche come principio d'inerzia, stabilisce che un corpo mantiene il proprio stato di quiete o di moto rettilineo uniforme finché non interviene una forza esterna a modificarlo. Di conseguenza, un oggetto su cui non agisce alcuna forza (o la cui risultante è nulla) non accelera.")
                    st.markdown("**Il secondo principio della dinamica**")
                    st.markdown("**Caratteristica:**Il secondo principio della dinamica (o legge fondamentale della dinamica) stabilisce che l'accelerazione subita da un corpo è direttamente proporzionale alla forza totale (o risultante delle forze) applicata ed è inversamente proporzionale alla sua massa")
                    st.markdown("**Formule:**")
                    st.latex(r"F = m \cdot a")
                    st.markdown("**Formule inverse:**")
                    st.latex(r"m = \frac {F}{a}")
                    st.latex(r"a = \frac {F}{m}")
                    st.latex(r"P = m \cdot g")
                    st.markdown("**Il terzo principio della dinamica**")
                    st.markdown("**Caratteristica:** Il terzo principio della dinamica, o principio di azione e reazione, afferma che quando un corpo \(A\) esercita una forza su un corpo \(B\), il corpo \(B\) esercita sul corpo \(A\) una forza uguale per intensità e direzione, ma di verso opposto")
                    st.markdown("**Forza centripeda e forza centrifuga**")
                    st.latex(r"a_c = \frac {v^2}{r}")
                    st.latex(r"F_c = m \cdot \frac {v^2}{r}")
                    st.info("La **forza centripeda** è una **grandezza vettoriale** che ha la stessa direzione e lo stesso verso dell'accelerazione centripeda")
                    with st.expander("Forze applicate al movimento"):
                        st.markdown("**Caratteristiche:** Nel piano iclinato sono presente molte forze come:Forza parallela($F_\\parallel$) e la forza perpendicolare($F_\\perp$)")
                        st.markdown("**Formule:**")
                        st.latex(r"P_\parallel = P \cdot \frac {h}{l} ")
                        st.latex(r"P_\parallel = P \cdot \sin \alpha")
