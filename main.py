import streamlit as st
import json
import random



def run():
    st.set_page_config(
        page_title="Streamlit quizz app",
        page_icon="❓",
    )

if __name__ == "__main__":
    run()

# Custom CSS for the buttons
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
#GithubIcon {
  visibility: hidden;
}
</style>
""", hide_github_icon, unsafe_allow_html=True)

# Initialize session variables if they do not exist
default_values = {'current_index': 0, 'current_question': 0, 'score': 0, 'selected_option': None, 'answer_submitted': False, 'counter':0, 'maxcounter':2}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Load quiz data
with open('content/sat.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False
    st.session_state.counter = 0
    st.session_state.maxcounter = 2

def submit_answer():

    # Check if an option has been selected
    if st.session_state.selected_option is not None:
        # Mark the answer as submitted
        st.session_state.answer_submitted = True
        # Check if the selected option is correct
        if st.session_state.selected_option == quiz_data['math'][st.session_state.current_index]['question']['correct_answer']:
            st.session_state.score += 10
    else:
        # If no option selected, show a message and do not mark as submitted
        st.warning("Please select an option before submitting.")

def next_question():
    st.session_state.current_index = random.randint(1,len(quiz_data['math']))
    st.session_state.counter +=1
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

# Title and description
st.title("Answer the Question to Get the Secret Code. Only One Mistake is Allowed.")

# Progress bar
progress_bar_value = (st.session_state.counter + 1) / st.session_state.maxcounter
st.metric(label="Score", value=f"{st.session_state.score} / {st.session_state.maxcounter * 10}")
st.progress(progress_bar_value)

# Display the question and answer options
question_item = quiz_data['math'][st.session_state.current_index]
#st.subheader(f"Question {st.session_state.current_index + 1}")
st.subheader(f"Question {st.session_state.counter + 1}")
st.title(f"{question_item['question']['question']}")
# st.write(question_item['information'])
if st.session_state.counter == 0:
    st.write("This is demo question. The answer is C")
st.write("A:", question_item['question']['choices']['A'])
st.write("B:", question_item['question']['choices']['B'])
st.write("C:", question_item['question']['choices']['C'])
st.write("D:", question_item['question']['choices']['D'])
st.markdown(""" ___""")

# Answer selection
options = question_item['question']['choices']
correct_answer = question_item['question']['correct_answer']

if st.session_state.answer_submitted:
    for i, option in enumerate(options):
        label = option
        if option == correct_answer:
            st.success(f"{label} (Correct answer)")
        elif option == st.session_state.selected_option:
            st.error(f"{label} (Incorrect answer)")
        else:
            st.write(label)
else:
    for i, option in enumerate(options):
        if st.button(option, key=i, use_container_width=True):
            st.session_state.selected_option = option

st.markdown(""" ___""")

# Submission button and response logic
if st.session_state.answer_submitted:
    if st.session_state.counter < st.session_state.maxcounter - 1:
        st.button('Next', on_click=next_question)
    else:
        st.write(f"Quiz completed! Your score is: {st.session_state.score} / {st.session_state.maxcounter * 10}")
        if st.session_state.score > (st.session_state.maxcounter-2) * 10:
            st.write(st.secrets["secret"])
            
        if st.button('Restart', on_click=restart_quiz):
            pass
else:
    if st.session_state.counter < st.session_state.maxcounter:
        st.button('Submit', on_click=submit_answer)
