# @st.cache(suppress_st_warning=True)
def p_welcome(st, **state):
    a, b = 3, 3
    c1, c2 = st.columns([a, b])
    c2.image("./media/welcome.jpg")
    c1.title("Supply Chain Wizard")
    c1.subheader("")
    c1.subheader("")
    c1.subheader("")
    c1.subheader(f"Stop overpaying and underperforming.")
    c1.subheader("Step up your Supply Chain game")
