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
        "Nderi": {
            "name": "Dario",
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
    tipo_moto = None
    
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
        sub_algebra = st.selectbox("Scegli l'argomento:", ["Risolutore Equazioni/Disequazioni"])
        
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

        passaggi_algebra = "###  Passaggi Algebrici (Forma Normale):\n"

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
            xv = -b_sym / (2 * a_sym)
            yv = -delta_sym / (4 * a_sym)
            
            x1_exact = (-b_sym - sp.sqrt(delta_sym)) / (2 * a_sym)
            x2_exact = (-b_sym + sp.sqrt(delta_sym)) / (2 * a_sym)
            
            # Ordinamento basato sul valore decimale reale
            if float(x1_exact.evalf()) > float(x2_exact.evalf()):
                x1_exact, x2_exact = x2_exact, x1_exact
                
            # Generazione stringhe LaTeX per il sito
            x1_latex = sp.latex(x1_exact)
            x2_latex = sp.latex(x2_exact)
            st.markdown("###  Coordinate del Vertice:")
            st.latex(f"V = \\left( {sp.latex(xv)}, {sp.latex(yv)} \\right)")

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
                st.write(f"Sostituisco i valori nella formula: x = -({b}) / (2 * {a})")
                st.success(f"L'equazione associata ha una sola soluzione: x = {x}")
        else:
            st.warning("Inserisci un'equazione valida per calcolare il risultato.")
        if simbolo == ">":
            st.info(f"x ∈ ℝ con x ≠ {x}")
        elif simbolo == "<":
                st.info("**Soluzione:** Impossibile (Nessuna soluzione reale, x ∈ ∅)")
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

        elif sub_algebra == "La Parabola":
            st.subheader("Formule della Parabola")
            
        elif sub_algebra == "La Retta":
            st.subheader("Geometria Analitica: La Retta")


    # =================================================================
    # 📐 SEZIONE 2: GEOMETRIA
    # =================================================================
    elif sezione == "Geometria":
        st.title("📐 Formulario di Geometria")
        with st.expander("🔸Circonferenze In Relazione"):
            st.markdown("**Esterne:** Due circonferenze si definiscono esterne quando non hanno nessun punto in comune")
            st.markdown("**Tangenti:** Due circonferenze si definiscono esterne quandohanno un punto in comune")
            st.markdown("**Secanti:** Due circonferenze si definiscono esterne quando hanno due punti in comune")
        with st.expander("🔹Poligoni Inscritti e Circoscritti"):
            st.markdown("**Inscritto:** Un poligono inscritto in una circonferenza è una figura geometrica in cui tutti i suoi vertici appartengono alla circonferenza")
            st.markdown("**Circoscritto:** Un poligono circoscritto a una circonferenza è un poligono in cui tutti i lati sono tangenti alla circonferenza")
        with st.expander("♦️ Quadrilateri"):
            st.markdown("** Quadrilatero Inscrivibile:** Un quadrilatero è inscrivibile in una circonferenza se e solo se gli angoli opposti sono supplementari")
            st.latex(r" S_somma_angoli = 180`")
            st.markdown("** Quadrilatero Circoscrivibile:** Un quadrilatero  è circoscrivibile a una circonferenza se e solo se la somma delle lunghezze di due lati opposti è uguale alla somma delle lunghezze degli altri due lati")
            st.info("💡 *Nota:* In pratica, se prendi un lato e lo sommi a quello che gli sta di fronte, devi ottenere lo stesso risultato sommando gli altri due lati rimasti")
        with st.expander("◽Area"):
            st.markdown("**Teorema:** In geometria, due figure piane sono equivalenti (o equiestese) quando hanno la stessa area, ovvero occupano la stessa estensione sul piano, indipendentemente dalla loro forma")
            st.markdown("**Teorema Con Parallelogramma e Rettangolo:** Un parallelogramma è equivalente a un rettangolo che possiede la stessa base e la stessa altezza")
            st.markdown("**Teorema Con Triangolo e Rettangolo:** Un triangolo è equivalente alla metà di un rettangolo avente la stessa base e la stessa altezza")
            st.markdown("**Teorema Con Trapezio e Triangolo:** Un trapezio è equivalente a un triangolo che possiede la stessa altezza ( h ) e una base pari alla somma delle due basi del trapezio ( B+b )")
        with st.expander("⬛Similitudine"):
            st.markdown("**Primo Criterio:** Due triangoli sono simili se hanno due angoli rispettivamente congruenti")
            st.markdown("**Secondo Criterio:**  Due triangoli sono simili se hanno un angolo congruente e i due lati che lo comprendono in proporzione")
            st.markdown("**Terzo Criterio:**  Due triangoli sono simili se hanno tutti e tre i lati ordinatamente proporzionali tra loro")
            


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
                    st.latex(r"P_\perp = P \cdot \frac {b}{l}")
                    st.latex(r"P_\perp = P \cdot \cos \alpha")
                    st.latex(r"a_\parallel = g \cdot \frac {h}{l}")
                    st.latex(r"a_\parallel = g \cdot \sin \alpha")
        st.markdown("### 🤖 Risolvitore Guidato di Cinematica")

        # 1. Capiamo subito il tipo di moto
    # 1. Capiamo subito il tipo di moto
        tipo_moto = st.selectbox("Che tipo di movimento fa il corpo?",
                                ["Velocità Costante (MRU)", "Accelerazione Costante (MRUA)", "Problema di Sorpasso (MRU + MRU)", "Incontro (MRU + MRUA)"])

        # === CASO 1: MRU ===
        if tipo_moto == "Velocità Costante (MRU)":
            st.write("---")
            st.markdown("**Inserisci i dati noti (metti 0 per l'incognita da calcolare):**")
        
        v_mru = st.number_input("Inserisci la velocità ($v$) in m/s:", value=0.0)
        s_mru = st.number_input("Inserisci lo spazio ($s$) in metri:", value=0.0)
        t_mru = st.number_input("Inserisci il tempo ($t$) in secondi:", value=0.0)
        
        if st.button("Risolvi Problema MRU"):
            st.write("### 🎯 Soluzione:")
            import sympy as sp
            
            if s_mru == 0.0 and v_mru > 0 and t_mru > 0:
                s_esatto = sp.Rational(str(v_mru)) * sp.Rational(str(t_mru))
                st.markdown("**1. Formula applicata:**")
                st.latex(r"s = v \cdot t")
                st.markdown("**2. Calcolo:**")
                st.latex(f"s = {v_mru} \\cdot {t_mru} = {sp.latex(s_esatto)} \\text{{ metri}}")
                
            elif t_mru == 0.0 and s_mru > 0 and v_mru > 0:
                t_esatto = sp.Rational(str(s_mru)) / sp.Rational(str(v_mru))
                st.markdown("**1. Formula inversa applicata:**")
                st.latex(r"t = \frac{s}{v}")
                st.markdown("**2. Calcolo:**")
                st.latex(f"t = \\frac{{{s_mru}}}{{{v_mru}}} = {sp.latex(t_esatto)} \\text{{ secondi}}")
                
            elif v_mru == 0.0 and s_mru > 0 and t_mru > 0:
                v_esatta = sp.Rational(str(s_mru)) / sp.Rational(str(t_mru))
                st.markdown("**1. Formula inversa applicata:**")
                st.latex(r"v = \frac{s}{t}")
                st.markdown("**2. Calcolo:**")
                st.latex(f"v = \\frac{{{s_mru}}}{{{t_mru}}} = {sp.latex(v_esatta)} \\text{{ m/s}}")
            else:
                st.warning("⚠️ Inserisci esattamente due dati per trovare il terzo!")

    # === CASO 2: MRUA ===
    elif tipo_moto == "Accelerazione Costante (MRUA)":
        st.write("---")
        st.markdown("**Aiutami a capire i dati del testo:**")
        
        da_fermo = st.checkbox("Il testo dice che il corpo 'parte da fermo'?")
        si_ferma = st.checkbox("Il testo dice che il corpo 'si ferma' o 'frena fino a fermarsi'?")
        
        if da_fermo:
            v0 = 0.0
            st.info("💡 *Dato automatico impostato:* Velocità iniziale $v_0 = 0$ m/s (perché parte da fermo).")
        else:
            v0 = st.number_input("Inserisci la velocità iniziale ($v_0$) in m/s:", value=0.0)
            
        if si_ferma:
            v_finale = 0.0
            st.info("💡 *Dato automatico impostato:* Velocità finale $v = 0$ m/s (perché si ferma).")
        else:
            v_finale = st.number_input("Inserisci la velocità finale ($v$) in m/s:", value=10.0)
            
        tempo = st.number_input("Inserisci il tempo ($t$) in secondi (metti 0 se è l'incognita):", value=0.0)
        spazio = st.number_input("Inserisci lo spazio ($s$) in metri (metti 0 se è l'incognita):", value=0.0)
        accelerazione = st.number_input("Inserisci l'accelerazione ($a$) in m/s² (metti 0 se è l'incognita):", value=0.0)
        
        if st.button("Risolvi Problema MRUA"):
            st.write("### 🎯 Soluzione:")
            import sympy as sp
            
            if tempo == 0.0 and spazio > 0 and accelerazione > 0:
                a_segno = -accelerazione if v_finale < v0 else accelerazione
                t_esatto = sp.Rational(str(v_finale - v0)) / sp.Rational(str(a_segno))
                st.markdown("**1. Scelta della formula più adatta:**")
                st.latex(r"v = v_0 + a \cdot t \implies t = \frac{v - v_0}{a}")
                st.markdown("**2. Sostituzione dei dati e calcolo:**")
                st.latex(f"t = \\frac{{{v_finale} - {v0}}}{{{a_segno}}} = {sp.latex(t_esatto)} \\text{{ secondi}}")
                
            elif accelerazione == 0.0 and tempo > 0:
                a_esatta = sp.Rational(str(v_finale - v0)) / sp.Rational(str(tempo))
                st.markdown("**1. Formula applicata:**")
                st.latex(r"a = \frac{v - v_0}{t}")
                st.markdown("**2. Calcolo:**")
                st.latex(f"a = \\frac{{{v_finale} - {v0}}}{{{tempo}}} = {sp.latex(a_esatta)} \\text{{ m/s}} ^2")
                
            elif spazio == 0.0 and tempo > 0 and accelerazione > 0:
                v0_sym = sp.Rational(str(v0))
                t_sym = sp.Rational(str(tempo))
                a_sym = sp.Rational(str(accelerazione))
                s_esatto = v0_sym * t_sym + sp.Rational(1, 2) * a_sym * t_sym**2
                st.markdown("**1. Formula applicata (Legge Oraria):**")
                st.latex(r"s = v_0 \cdot t + \frac{1}{2}a \cdot t^2")
                st.markdown("**2. Calcolo:**")
                st.latex(f"s = {v0} \\cdot {tempo} + \\frac{{1}}{{2}} \\cdot {accelerazione} \\cdot {tempo}^2 = {sp.latex(s_esatto)} \\text{{ metri}}")
            else:
                st.warning("⚠️ Combinazione di dati non ancora supportata o dati insufficienti per risolvere il problema.")

    # === CASO 3: SORPASSO ===
    elif tipo_moto == "Problema di Sorpasso (MRU + MRU)":
        st.write("---")
        st.markdown("### 🎯 Risoluzione del Sorpasso (MRU + MRU)")
        st.write("Immaginiamo l'Auto A che insegue l'Auto B che parte con un vantaggio iniziale.")

        st.markdown("#### Dati dell'Auto A")
        v_a = st.number_input("Velocità dell'Auto A ($v_A$) in m/s:", value=0.0, step=1.0)

        st.markdown("#### Dati dell'Auto B")
        v_b = st.number_input("Velocità dell'Auto B ($v_B$) in m/s:", value=0.0, step=1.0)
        distanza = st.number_input("Distanza o Vantaggio iniziale ($d$) in metri:", value=0.0, step=5.0)

        if st.button("Risolvi Sorpasso"):
            if distanza <= 0:
                st.warning("⚠️ Inserisci una distanza iniziale maggiore di 0.")
            elif v_a <= v_b:
                st.error("Il sorpasso è impossibile: le due auto viaggiano alla stessa velocità o l'auto dietro è più lenta!")
            else:
                import sympy as sp
                va_sym = sp.Rational(str(v_a))
                vb_sym = sp.Rational(str(v_b))
                d_sym = sp.Rational(str(distanza))
                
                t_sorpasso = d_sym / sp.Abs(va_sym - vb_sym)
                v_inseguitrice = va_sym if va_sym > vb_sym else vb_sym
                s_sorpasso = v_inseguitrice * t_sorpasso
                
                t_decimale = float(t_sorpasso.evalf())
                s_decimale = float(s_sorpasso.evalf())
                
                st.markdown("***1. Condizione di sorpasso/incontro:***")
                st.latex(r"t = \frac{d}{|v_A - v_B|}")
                st.markdown("***2. Sostituzione dei dati e calcolo del tempo:***")
                st.latex(f"t = \\frac{{{distanza}}}{{\\lvert {v_a} - {v_b} \\rvert}} = {sp.latex(t_sorpasso)} \\approx {t_decimale:.2f} \\text{{ secondi}}")
                st.markdown("***3. Calcolo dello spazio in cui avviene il sorpasso:***")
                st.latex(f"s = {float(v_inseguitrice.evalf()):.2f} \\cdot {t_decimale:.2f} = {sp.latex(s_sorpasso)} \\approx {s_decimale:.2f} \\text{{ metri}}")
                st.info(f"L'Auto A sorpasserà l'Auto B dopo {t_decimale:.2f} secondi, ad una distanza di {s_decimale:.2f} metri dal punto iniziale.")

    # === CASO 4: INCONTRO ===
    # === CASO 4: INCONTRO / SORPASSO UNIVERSALE ===
    # === CASO 4: INCONTRO / SORPASSO UNIVERSALE ===
    elif tipo_moto == "Incontro (MRU + MRUA)":
        st.write("---")
        st.markdown("### 🚀 Risolvitore di Incontri e Frenate Universale")
        st.write("Inserisci le condizioni di viaggio di entrambi i corpi. Se un corpo si ferma, imposta la sua Velocità Finale a 0.0.")

        # --- DATI CORPO A ---
        st.markdown("#### 🟥 CORPO A")
        col1, col2, col3 = st.columns(3)
        with col1:
            s0_a = st.number_input("Posizione Iniziale $s_{0A}$ (m):", value=0.0, key="s0_a")
            v0_a = st.number_input("Velocità Iniziale $v_{0A}$ (m/s):", value=0.0, key="v0_a")
        with col2:
            vf_a_inc = st.number_input("Velocità Finale $v_{fA}$ (m/s):", value=0.0, key="vf_a_inc")
            a_a = st.number_input("Accelerazione $a_A$ (m/s²):", value=0.0, key="a_a")
        with col3:
            t_a_inc_input = st.number_input("Tempo di moto / frenata $t_A$ (s):", value=0.0, placeholder="0.0 se incognito", key="t_a_inc_in")

        # --- DATI CORPO B ---
        st.markdown("#### 🟦 DATI CORPO B")
        col4, col5, col6 = st.columns(3)
        with col4:
            s0_b = st.number_input("Posizione Iniziale $s_{0B}$ (m):", value=0.0, key="s0_b")
            v0_b = st.number_input("Velocità Iniziale $v_{0B}$ (m/s):", value=0.0, key="v0_b")
        with col5:
            vf_b_inc = st.number_input("Velocità Finale $v_{fB}$ (m/s):", value=0.0, key="vf_b_inc")
            a_b = st.number_input("Accelerazione $a_B$ (m/s²):", value=0.0, key="a_b")
        with col6:
            t_b_inc_input = st.number_input("Tempo di moto / frenata $t_B$ (s):", value=0.0, placeholder="0.0 se incognito", key="t_b_inc_in")

        if st.button("Analizza e Risolvi Incontro"):
            st.write("### 🎯 Analisi Fisica del Problema:")
            import sympy as sp
            
            t = sp.Symbol('t', positive=True)
            
            # --- LOGICA CORPO A ---
            if t_a_inc_input == 0.0 and a_a != 0.0:
                t_frenata_a = sp.Rational(str(vf_a_inc - v0_a)) / sp.Rational(str(a_a))
                t_a_effettivo = float(t_frenata_a.evalf())
                st.success(f"⏱️ Corpo A: Calcolato tempo di frenata/accelerazione = **{t_a_effettivo:.2f} secondi**")
            else:
                t_a_effettivo = t_a_inc_input

            # --- LOGICA CORPO B ---
            if t_b_inc_input == 0.0 and a_b != 0.0:
                t_frenata_b = sp.Rational(str(vf_b_inc - v0_b)) / sp.Rational(str(a_b))
                t_b_effettivo = float(t_frenata_b.evalf())
                st.success(f"⏱️ Corpo B: Calcolato tempo di frenata/accelerazione = **{t_b_effettivo:.2f} secondi**")
            else:
                t_b_effettivo = t_b_inc_input

            # --- LEGGI ORARIE SIMBOLICHE ---
            s0a_s = sp.Rational(str(s0_a))
            v0a_s = sp.Rational(str(v0_a))
            aa_s = sp.Rational(str(a_a))
            
            s0b_s = sp.Rational(str(s0_b))
            v0b_s = sp.Rational(str(v0_b))
            ab_s = sp.Rational(str(a_b))
            
            legge_A = s0a_s + v0a_s * t + sp.Rational(1, 2) * aa_s * t**2
            legge_B = s0b_s + v0b_s * t + sp.Rational(1, 2) * ab_s * t**2
            
            st.markdown("***1. Equazioni Orarie dei due corpi:***")
            st.latex(f"s_A(t) = {sp.latex(legge_A)}")
            st.latex(f"s_B(t) = {sp.latex(legge_B)}")
            
            st.markdown("***2. Condizione di Incontro ($s_A(t) = s_B(t)$):***")
            equazione = sp.Eq(legge_A, legge_B)
            soluzioni = sp.solve(equazione, t)
            
            if not soluzioni:
                st.error("❌ Con queste traiettorie i due corpi non si incroceranno mai.")
            else:
                t_inc = soluzioni[0]
                s_inc = legge_A.subs(t, t_inc)
                
                t_dec = float(t_inc.evalf())
                s_dec = float(s_inc.evalf())
                
                st.latex(f"{sp.latex(legge_A)} = {sp.latex(legge_B)}")
                st.markdown("***3. Risultati del punto di contatto:***")
                st.latex(r"t_{\text{incontro}} = " + f"{sp.latex(t_inc)} \\approx {t_dec:.2f} \\text{{ secondi}}")
                st.latex(r"s_{\text{incontro}} = " + f"{sp.latex(s_inc)} \\approx {s_dec:.2f} \\text{{ metri}}")
                
                if t_a_effettivo > 0 and t_dec > t_a_effettivo and vf_a_inc == 0.0:
                    st.warning("⚠️ Nota: Il Corpo A ha completato la sua frenata e si è fermato prima dell'istante di incontro!")
                if t_b_effettivo > 0 and t_dec > t_b_effettivo and vf_b_inc == 0.0:
                    st.warning("⚠️ Nota: Il Corpo B ha completato la sua frenata e si è fermato prima dell'istante di incontro!")

                st.info(f"L'evento di incontro/sorpasso si verificherà dopo {t_dec:.2f} secondi a {s_dec:.2f} metri dall'origine.")
