import openai
import streamlit as st

st.title("IT recruiter")

openai.api_key = st.secrets["openai"]

#context of the discussion
context= "Evaluate competencies of an IT candidate to be recruited." 
context+="and a code with a mistake to correct by the candidate by field of expertise based on the level of expertise. "
                
messages = [{"role": "system", "content": context}]

with st.form("input form"):
    st.write("<h3>Enter the experience of the candidate ✨</h3>", unsafe_allow_html=True)
    expertise_1 = st.text_input("Enter the 1st expertise:")
    level_expertise_1=st.selectbox("Choose level of the 1st expertise:",('Expert','intermediate','beginner'))
    question_1=f"propose a multiple choice question to test the candidate on aera of expertise {expertise_1} with the level of expertise {level_expertise_1}"
    #expertise_2 = st.text_input("Enter the 2nd expertise:")
    #level_expertise_2=st.selectbox("Choose level of the 2nd expertise:",('Expert','intermediate','beginner'))

    if st.form_submit_button("Start"):
        if discussion is not None:
            if "openai_model" not in st.session_state:
                st.session_state["openai_model"] = "gpt-3.5-turbo"
            
            if "messages" not in st.session_state:
                st.session_state.messages = messages
            
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            st.session_state.messages.append({"role": "user", "content": question_1})

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
        
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages,
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")

            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
