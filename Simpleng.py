import streamlit as st
import time
from simpleng.db.retrieve_history import HistoryRetrieval
from simpleng.llm.llm import LLM
import pyperclip
from dotenv import load_dotenv
from os.path import join, dirname
import streamlit_scrollable_textbox as stx

load_dotenv(join(dirname(__file__), "/Users/andreafavia/development/simpleng/.env"))

if "input_text" not in st.session_state:
    st.session_state.input_text = None
if "older_input_text" not in st.session_state:
    st.session_state.input_text = None
if "user" not in st.session_state:
    st.session_state.user = None
if "history_user" not in st.session_state:
    st.session_state.history_user = None
if "output_text" not in st.session_state:
    st.session_state.output_text = None
if "phrasal" not in st.session_state:
    st.session_state.phrasal = None
if "difficult_words" not in st.session_state:
    st.session_state.difficult_words = None
llm = LLM()

STATIC_FILE = "../simpleng/simpleng/assets/example.txt"

# add a jscript function to copy to clipboard
st.markdown(
    """
    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text);
        }
    </script>
    """,
    unsafe_allow_html=True,
)


def input_text():
    st.title("SimplEng 🇬🇧 \n Just Simplify English ")
    st.sidebar.title("SimplEng 🇬🇧 \n Just Simplify English ")

    with st.form(key="input_form", clear_on_submit=True):
        text = st.text_input(
            label="Input label",
            label_visibility="hidden",
            placeholder="Insert any text in english you want to simplify and analyze",
        )
        submitted = st.form_submit_button()

    if submitted or text:
        # st.write(text)
        st.session_state.input_text = text


def login_and_history_retrieval():
    with st.sidebar.status("Loggin with google"):
        time.sleep(1)
        st.session_state.user = "User X"
        hr = HistoryRetrieval(st.session_state.user)
        st.session_state.history_user = hr.load_history()


def sidebar():
    if st.session_state.user:
        st.sidebar.caption(f"Welcome {st.session_state.user}")

        if st.session_state.history_user is not None:
            pass
            # st.sidebar.subheader("History")
            # st.sidebar.dataframe(st.session_state.history_user)  # TODO: better visualization of the past

    else:
        st.sidebar.button("Login with Google", on_click=login_and_history_retrieval)

    st.sidebar.divider()


def check_text():
    if st.session_state.input_text:
        if len(st.session_state.input_text) < 50:
            st.error("The text is not long enough - insert a longer one sentence")
        elif len(st.session_state.input_text.split()) < 5:
            st.error("There's no enough words in this sentence, please provide a longer sentence.")


def copy_to_clipboard(text):
    st.success("Text copied to clipboard")


@st.cache_data(show_spinner=False)
def get_result_llm(text):
    return llm.analyze_text(text)


def output_text():
    if st.session_state.input_text and len(st.session_state.input_text) > 50:
        st.header("Results ")
        with st.spinner("Simplifying text ..."):
            output = get_result_llm(st.session_state.input_text)
            print(output)
            st.session_state.older_input_text = st.session_state.input_text
            st.session_state.input_text = None

        st.session_state.output_text = output.get("simplified_text")
        st.session_state.phrasal = output.get("phrasal_verbs") or output.get("phrasal") or output.get("verbs")
        st.session_state.difficult_words = output.get("difficult_words")

    try:
        if st.session_state.output_text:
            with st.expander("original text", expanded=False, icon="⬇"):
                st.write(st.session_state.older_input_text)
            with st.expander("simplenged text", expanded=True, icon="⬇"):
                st.code(st.session_state.output_text, wrap_lines=True, language="text")

            with st.sidebar.expander("**Difficult words**", expanded=True):
                for obj in st.session_state.difficult_words:
                    word, meaning = obj.get("word"), obj.get("meaning")
                    st.code(f" {word.title()}: {meaning}", language="text", wrap_lines=True)

            with st.sidebar.expander("**Phrasal verbs**", expanded=True):
                for obj in st.session_state.phrasal:
                    verb, meaning = obj.get("verb") or obj.get("phrasal_verb"), obj.get("meaning")
                    st.code(f" {verb.title()}: {meaning}", language="text", wrap_lines=True)

            st.sidebar.divider()

            if st.session_state.user and st.button("Save results?"):
                with st.status("Saving in your profile ..."):
                    time.sleep(2)
                    st.success("Data has been saved")

    except Exception as e:
        st.error(f"An error occurred, please try again: {e}")


def main():
    # Side bar
    # sidebar()

    # Input text
    input_text()

    st.divider()

    example_container = st.sidebar.container()
    with example_container:
        stx.scrollableTextbox(open(f"{STATIC_FILE}").read(), height=300)
        if st.sidebar.button("Try with the example"):
            st.session_state.input_text = open(f"{STATIC_FILE}").read()

            pass

    output_text()


main()
