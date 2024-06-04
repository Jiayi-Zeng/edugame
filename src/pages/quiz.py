import streamlit as st
import random

def generate_question():
    """生成一个简单的加法或减法问题"""
    num1 = random.randint(0, 10)
    num2 = random.randint(0, 10)
    if random.choice([True, False]):
        question = f"{num1} + {num2}"
        answer = num1 + num2
    else:
        question = f"{num1} - {num2}"
        answer = num1 - num2
    return question, answer

def create_quiz():
    """生成五道加减法选择题和填空题"""
    questions = []
    for _ in range(5):
        question, answer = generate_question()
        questions.append((question, answer))
    return questions

def display_question(idx, question):
    """显示问题并获取用户答案"""
    st.write(f"问题 {idx + 1}: {question} = ?")
    user_answer = st.text_input(f"您的答案", key=f"answer_{idx}")
    return user_answer

def main():
    st.title("Quiz")
    
    st.text("当前进度为：")
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = create_quiz()
        st.session_state.current_question = 0
        st.session_state.correct_answers = 0

    quiz_questions = st.session_state.quiz_questions
    current_question = st.session_state.current_question

    # 显示进度条
    progress = (current_question / len(quiz_questions)) 
    st.progress(progress)

    if current_question < len(quiz_questions):
        question, correct_answer = quiz_questions[current_question]
        st.write("请回答以下加减法问题:")
        user_answer = display_question(current_question, question)

        if st.button("提交答案"):
            if user_answer == str(correct_answer):
                st.session_state.correct_answers += 1
                st.session_state.correct = True
                st.button("下一题")
                st.success("回答正确！点击下一个题目继续。")
                st.session_state.current_question += 1
                st.session_state.correct = False
            else:
                st.session_state.correct = False
                st.error("回答错误，请重试。")

    else:
        st.write(f"您已完成所有问题！")
        st.balloons()

if __name__ == "__main__":
    main()
