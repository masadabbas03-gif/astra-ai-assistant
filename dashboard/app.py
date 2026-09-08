import streamlit as st


st.set_page_config(

    page_title="Astra",

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="expanded"
)


with open(

    "dashboard/assets/style.css",

    encoding="utf-8"

) as css:
    st.markdown(

        f"<style>{css.read()}</style>",

        unsafe_allow_html=True

    )


with st.sidebar:

    st.title("🤖 Astra")

    st.write(

        "Personal AI Assistant"
    )

    st.divider()

    st.button(

        "💬 Chat"
    )

    st.button(

        "🧠 Memory"
    )

    st.button(

        "📋 Tasks"
    )

    st.button(

        "🛠 Tools"
    )

    st.button(

        "⚙ Settings"
    )


st.title(

    "Welcome back, Boss"
)

st.caption(

    "Your AI assistant is online."
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(

        "Status",

        "Online"
    )


with col2:

    st.metric(

        "Model",

        "Qwen 2.5"
    )


with col3:

    st.metric(

        "Voice",

        "Piper"
    )


st.divider()


if "messages" not in st.session_state:

    st.session_state.messages = [

        {

            "role": "assistant",

            "content": "Hello Boss. I am Astra."
        }

    ]


for message in st.session_state.messages:

    with st.chat_message(

        message["role"]

    ):

        st.write(

            message["content"]
        )


prompt = st.chat_input(

    "Talk to Astra..."
)


if prompt:

    st.session_state.messages.append(

        {

            "role": "user",

            "content": prompt
        }

    )

    st.rerun()