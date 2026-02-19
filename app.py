import streamlit as st
import google.generativeai as genai

# --- 페이지 설정 ---
st.set_page_config(page_title="B-Move AI 블로그 코치", page_icon="💪", layout="wide")

st.title("💪 B-Move Gym: AI 블로그 코치")
st.markdown("매니저님! 주제만 던져주시면 **노출 잘 되는 제목**과 **글감**을 짜드립니다.")
st.divider()

# --- 사이드바: API 키 입력 ---
with st.sidebar:
    st.header("🔑 설정")
    api_key = st.text_input("API Key를 입력하세요", type="password")
    
    if not api_key:
        st.warning("👈 먼저 API 키를 넣어주세요!")

# --- 메인 입력 화면 ---
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("📝 오늘의 주제는?", placeholder="예: 30대 뱃살, 라운드숄더, 헬스장 이벤트")
with col2:
    target = st.selectbox("🎯 타겟 독자는 누구?", ["3040 직장인", "20대 대학생", "주부/산후", "헬스 초보", "전체"])

# --- AI 실행 버튼 ---
if st.button("🚀 AI야, 블로그 기획해줘! (Click)", use_container_width=True):
    if not api_key:
        st.error("왼쪽 사이드바에 API Key가 비어있어요!")
    elif not topic:
        st.warning("주제를 입력해주세요!")
    else:
        # AI 설정
        genai.configure(api_key=api_key)
        
        # 💡 [핵심 기술] 구글 서버를 뒤져서 내 키로 쓸 수 있는 모델을 '자동'으로 찾아옵니다.
        my_model = 'gemini-1.0-pro' # 만약을 위한 기본값
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                my_model = m.name # 쓸 수 있는 모델을 발견하면 자동으로 입력!
                break
        
        model = genai.GenerativeModel(my_model)
        
        # 프롬프트(명령서)
        prompt = f"""
        나는 울산 헬스장 'B-Move Gym' 블로그를 운영해.
        주제: '{topic}'
        타겟: '{target}'
        
        이 정보를 바탕으로 블로그 포스팅 가이드를 작성해줘.
        1. [제목 추천]: 클릭률 높은 제목 5가지 (이모지 포함, 숫자/호기심 자극)
        2. [본문 구성]: 서론-본론-결론 핵심 내용 요약 (전문성 강조)
        3. [해시태그]: 인스타/블로그용 태그 10개
        """
        
        with st.spinner("🧠 AI가 최신 트렌드를 분석 중입니다... (약 5~10초 소요)"):
            try:
                response = model.generate_content(prompt)
                st.balloons() # 성공 축하 풍선 팡팡!
                st.success(f"✅ 분석 완료! (사용한 인공지능: {my_model})")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")
