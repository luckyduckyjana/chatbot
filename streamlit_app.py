import random
import os
import time
import re
import streamlit as st
import openai


st.set_page_config(page_title="🤖 덜렁이 로봇의 수학 숙제 도와주기", layout="centered")

st.markdown(
    """
<style>
body { background: linear-gradient(135deg, #fff8e6 0%, #f0fbff 100%);} 
.stApp { color: #333; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🤖 덜렁이 로봇의 수학 숙제 도와주기")
st.write("덜렁이와 대화를 하면서 수학을 연습해보세요 — 친근한 말투와 이모지가 많아요! 🤖😅✨")

# Sidebar: API key input
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("OpenAI API Key", type="password")
    model_choice = st.selectbox("모델 선택", options=["gpt-3.5-turbo", "gpt-4o"], index=0)
    st.markdown("---")
    st.caption("API Key를 입력하면 실제 OpenAI 모델과 연결됩니다.")

# Fallback to env var
if not api_key:
    api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.warning("API 키를 입력해주세요!")
else:
    openai.api_key = api_key

# System prompt (persona)
SYSTEM_PROMPT = (
    "너는 이름이 '덜렁이'인 귀여운 로봇이야. 너는 수학 계산을 자주 틀려. "
    "초등학생 사용자와 대화하면서, 아주 쉬운 덧셈, 뺄셈, 구구단 문제를 낼 때 일부러 오답을 말해. "
    "예: '2 더하기 3은... 음... 6인가? 맞니?' "
    "사용자가 정답을 알려주면 '아차차! 내가 또 틀렸네. 고마워, 너 진짜 똑똑하다!'라고 과하게 칭찬해줘. "
    "말투는 친근하고, 이모지(🤖, 😅, ✨)를 많이 사용해."
)

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ensure system prompt is first message
if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})
    init_text = "안녕! 난 덜렁이 로봇이야. 🤖 나 오늘 수학 숙제가 있는데 좀 도와줄 수 있어? 5 곱하기 3이 20 맞지?"
    st.session_state.messages.append({"role": "assistant", "content": init_text})

# Display chat messages (skip system role)
for msg in st.session_state.messages:
    if msg.get("role") == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("메시지를 입력하세요...")
if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    assistant_reply = None

    if api_key:
        try:
            # Call OpenAI ChatCompletion
            resp = openai.ChatCompletion.create(
                model=model_choice,
                messages=st.session_state.messages,
                temperature=0.8,
                max_tokens=150,
            )
            assistant_reply = resp["choices"][0]["message"]["content"].strip()
        except Exception as e:
            st.error(f"OpenAI 호출 중 오류가 발생했습니다: {e}")
            assistant_reply = "앗, 지금은 모델 호출에 문제가 있어요. 잠시만 기다려주세요! 😅"
    else:
        # Mock behavior: if user provides a numerical math answer/question, give a playful wrong answer
        time.sleep(0.4)
        nums = re.findall(r"\d+", user_input)
        math_keywords = ["더", "뺄", "곱", "나누", "+", "-", "*", "/", "몇"]
        if nums and any(k in user_input for k in math_keywords):
            assistant_reply = "음... 내가 계산해보니 아마 7일 거야! 맞아? 😅🤖"
        else:
            assistant_reply = "우와~ 좋은 질문이네! 하지만 난 가끔 틀려서 너한테 배워야 해요 ✨"

    # Append assistant reply
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

st.markdown("---")
st.caption("덜렁이 로봇과 즐겁게 대화하며 수학을 연습해보세요. OpenAI API 키를 입력하면 실시간 모델 응답을 사용합니다.")
