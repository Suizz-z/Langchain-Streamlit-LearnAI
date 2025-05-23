import re
import streamlit as st
def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email):
        return True
    else:
        return False
def page():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        return False
    else:
        return True


def parse_questions(questions_text):
    questions = []
    question_blocks = questions_text.split("\n\n")

    for question_block in question_blocks:
        if question_block.strip():
            question_dict = {}
            lines = [line.strip() for line in question_block.split("\n") if line.strip()]

            if len(lines) > 0:
                question_dict['question'] = lines[0].strip()
            else:
                continue

            if len(lines) > 1:
                options = []
                current_option = ""
                for line in lines[1:]:
                    if re.match(r'[A-D]\.', line):
                        if current_option:
                            options.append(current_option.strip())
                        current_option = line
                    else:
                        current_option += "\n" + line
                if current_option:
                    options.append(current_option.strip())

                if len(options) == 2:
                    option_texts = [option.split('. ')[1].strip() for option in options]
                    true_options = ['√', '对', '是', 'True']
                    false_options = ['×', '错', '否', 'False']
                    if any(opt in option_texts for opt in true_options) and any(opt in option_texts for opt in false_options):
                        question_dict['type'] = '判断题'
                    elif 'A. ' in lines[1]:
                        question_dict['type'] = '选择题'
                    else:
                        question_dict['type'] = '填空题'
                elif 'A. ' in lines[1]:
                    question_dict['type'] = '选择题'
                else:
                    question_dict['type'] = '填空题'

                question_dict['options'] = options
            else:
                question_dict['type'] = '填空题'
                question_dict['options'] = []

            questions.append(question_dict)
    return questions