import random
import streamlit as st
from typing import List, Dict


st.set_page_config(page_title="🛒 마트 계산 대장", layout="centered")
st.title("🛒 마트 계산 대장")
st.write("초등학생을 위한 마트 계산 놀이입니다. 상품을 보고 총 금액을 계산해보세요!")

# 1) 데이터 설정: 상품 목록
PRODUCTS: List[Dict] = [
    {"name": "사과", "price": 500, "emoji": "🍎"},
    {"name": "우유", "price": 1000, "emoji": "🥛"},
    {"name": "과자", "price": 1500, "emoji": "🍪"},
    {"name": "아이스크림", "price": 800, "emoji": "🍦"},
    {"name": "바나나", "price": 300, "emoji": "🍌"},
    {"name": "주스", "price": 1200, "emoji": "🧃"},
]


# 2) 세션 상태 초기화
def init_session():
    if "current_items" not in st.session_state:
        st.session_state.current_items = []
    if "current_answer" not in st.session_state:
        st.session_state.current_answer = None
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "total_correct" not in st.session_state:
        st.session_state.total_correct = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "user_input" not in st.session_state:
        st.session_state.user_input = 0


init_session()


def generate_problem():
    # pick 2 or 3 random products
    count = random.choice([2, 3])
    items = random.sample(PRODUCTS, k=count)
    total = sum(item["price"] for item in items)
    st.session_state.current_items = items
    st.session_state.current_answer = total
    st.session_state.answered = False
    st.session_state.user_input = 0


# If no problem exists yet, generate one
if not st.session_state.current_items:
    generate_problem()


# 3) UI 레이아웃: 문제 출제 영역
st.subheader("📦 문제 출제")
cols = st.columns(len(st.session_state.current_items))
for col, item in zip(cols, st.session_state.current_items):
    with col:
        st.markdown(f"<div style='text-align:center; padding:10px; border:1px solid #eee; border-radius:8px;'>"
                    f"<div style='font-size:40px'>{item['emoji']}</div>"
                    f"<div style='font-weight:600'>{item['name']}</div>"
                    f"<div style='color:#555'>{item['price']}원</div>"
                    f"</div>", unsafe_allow_html=True)


# 4) 계산대 영역
st.subheader("🧾 계산대")
st.write("총 금액은 얼마인가요?")
user_answer = st.number_input("금액 입력 (원)", min_value=0, value=int(st.session_state.user_input), step=100, key="money_input")

col_check, col_next = st.columns(2)
with col_check:
    if st.button("정답 확인"):
        if st.session_state.current_answer is None:
            st.warning("먼저 문제를 생성해 주세요.")
        else:
            # compare integers
            try:
                if int(user_answer) == int(st.session_state.current_answer):
                    st.success("정답입니다! 🎉")
                    st.balloons()
                    st.session_state.score += 1
                    st.session_state.total_correct += 1
                    st.session_state.answered = True
                else:
                    st.error("아쉬워요, 다시 계산해볼까요?")
            except Exception:
                st.error("숫자를 올바르게 입력해주세요.")

with col_next:
    if st.button("다음 손님 받기(새 문제)"):
        generate_problem()


# 5) 사이드바: 현재 점수 및 누적 정답 횟수
with st.sidebar:
    st.header("게임 정보")
    st.metric("현재 점수", st.session_state.score)
    st.metric("누적 정답 횟수", st.session_state.total_correct)
    st.markdown("---")
    st.caption("답을 제출하기 전까지는 문제가 유지됩니다.")

st.markdown("---")
st.caption("즐겁게 계산 놀이를 해보세요!")
