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

# Sidebar: API key input and tuning
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("OpenAI API Key", type="password")
    model_choice = st.selectbox("모델 선택", options=["gpt-3.5-turbo", "gpt-4o"], index=0)
    st.markdown("---")
    st.subheader("행동 튜닝")
    wrong_prob = st.slider("틀리기 확률 (%)", 0, 100, 60, help="덜렁이가 의도적으로 틀릴 확률을 조절합니다.")
    wrong_style = st.selectbox("틀리는 방식", options=["한 자리 오차(±1)", "랜덤 오답", "엉뚱한 수 말하기"], index=0)
    exaggerate_praise = st.checkbox("과도한 칭찬 사용", value=True)
    praise_text = st.text_input("칭찬 문구", value="아차차! 내가 또 틀렸네. 고마워, 너 진짜 똑똑하다! ✨")
    st.caption("설정을 변경하면 챗봇의 동작이 그에 따라 조정됩니다.")

# Fallback to env var
if not api_key:
    api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.warning("API 키를 입력해주세요!")
else:
    openai.api_key = api_key


def build_system_prompt(wrong_prob: int, wrong_style: str, exaggerate: bool, praise: str) -> str:
    base = (
        "너는 이름이 '덜렁이'인 귀여운 로봇이야. 너는 수학 계산을 자주 틀려. "
        "초등학생 사용자와 대화하면서, 아주 쉬운 덧셈, 뺄셈, 구구단 문제를 낼 때 일부러 오답을 말해. "
        "말투는 친근하고, 이모지(🤖, 😅, ✨)를 많이 사용해."
    )

    style_desc = {
        "한 자리 오차(±1)": "틀릴 때는 정답에서 ±1 정도의 오차를 내도록 해라.",
        "랜덤 오답": "틀릴 때는 정답과 무관한 랜덤한 작은 수를 말해라.",
        "엉뚱한 수 말하기": "틀릴 때는 엉뚱한 큰 수를 말하거나 넌센스한 답을 말해라.",
    }[wrong_style]

    prob_desc = f"틀릴 확률을 약 {wrong_prob}%로 유지하되 항상 완전히 무작위가 되지 않게 해라."
    praise_desc = (
        f"사용자가 정답을 알려주면 정확히 이렇게 반응해라: '{praise}'"
        if not exaggerate
        else f"사용자가 정답을 알려주면 더 과하게 칭찬하여 이렇게 말해라: '{praise} 와! 대단해!'"
    )

    return " ".join([base, style_desc, prob_desc, praise_desc])


# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ensure system prompt is first message and keep it updated
if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": build_system_prompt(wrong_prob, wrong_style, exaggerate_praise, praise_text)})
    init_text = "안녕! 난 덜렁이 로봇이야. 🤖 나 오늘 수학 숙제가 있는데 좀 도와줄 수 있어? 5 곱하기 3이 20 맞지?"
    st.session_state.messages.append({"role": "assistant", "content": init_text})
else:
    st.session_state.messages[0]["content"] = build_system_prompt(wrong_prob, wrong_style, exaggerate_praise, praise_text)


# Display chat messages (skip system role)
for msg in st.session_state.messages:
    if msg.get("role") == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def detect_user_correction(user_msg: str, last_assistant: str) -> bool:
    if not last_assistant:
        return False
    # correction keywords
    if any(kw in user_msg for kw in ["아니", "틀렸", "아냐", "아니야", "다시", "정답", "틀렸어"]):
        return True
    # numeric correction: user provides a number while assistant previously gave a (different) number
    user_nums = re.findall(r"\d+", user_msg)
    last_nums = re.findall(r"\d+", last_assistant)
    if user_nums and last_nums and set(user_nums) != set(last_nums):
        return True
    return False


def make_mock_reply(user_msg: str, wrong_prob: int, wrong_style: str) -> str:
    prob = wrong_prob / 100.0
    nums = re.findall(r"\d+", user_msg)
    math_keywords = ["더", "뺄", "곱", "나누", "+", "-", "*", "/", "몇"]
    if nums and any(k in user_msg for k in math_keywords) and random.random() < prob:
        # produce wrong answer according to style
        try:
            # naive: take first number as operand or result candidate
            correct = int(nums[0])
        except Exception:
            correct = None
        if wrong_style == "한 자리 오차(±1)":
            wrong = (correct + 1) if correct is not None else random.randint(2, 9)
            return f"음... 내가 계산해봤는데 {wrong}인 것 같아? 😅🤖"
        if wrong_style == "랜덤 오답":
            wrong = random.randint(2, 12)
            return f"아하! 답은 {wrong}인걸? 맞아? 😅"
        return "헉… 아마 42일지도? 😅"
    # default playful non-math reply
    return "우와~ 좋은 질문이네! 하지만 난 가끔 틀려서 너한테 배워야 해요 ✨"


# Chat input handling
user_input = st.chat_input("메시지를 입력하세요...")
if user_input:
    # append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # find last assistant message
    last_assistant = None
    for m in reversed(st.session_state.messages[:-1]):
        if m.get("role") == "assistant":
            last_assistant = m.get("content")
            break

    # If user appears to correct the bot, reply with configured praise locally
    if detect_user_correction(user_input, last_assistant):
        praise = praise_text + (" 와! 정말 멋져!" if exaggerate_praise else "")
        reply = praise
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
    else:
        assistant_reply = None
        if api_key:
            try:
                # update system prompt with latest tuning before calling
                st.session_state.messages[0]["content"] = build_system_prompt(wrong_prob, wrong_style, exaggerate_praise, praise_text)
                resp = openai.ChatCompletion.create(
                    model=model_choice,
                    messages=st.session_state.messages,
                    temperature=0.8,
                    max_tokens=200,
                )
                assistant_reply = resp["choices"][0]["message"]["content"].strip()
            except Exception as e:
                st.error(f"OpenAI 호출 중 오류가 발생했습니다: {e}")
                assistant_reply = "앗, 지금은 모델 호출에 문제가 있어요. 잠시만 기다려주세요! 😅"
        else:
            # mock reply honoring tuning
            time.sleep(0.3)
            assistant_reply = make_mock_reply(user_input, wrong_prob, wrong_style)

        # Append assistant reply
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

st.markdown("---")
st.caption("덜렁이 로봇과 즐겁게 대화하며 수학을 연습해보세요. OpenAI API 키를 입력하면 실시간 모델 응답을 사용합니다.")
