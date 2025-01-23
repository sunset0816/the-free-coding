import pandas as pd
import streamlit as st
#import openpyxl
import os

# ----- Streamlit 기본 설정 -----
st.set_page_config(
    page_title="KNU 과목조회 도우미",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----- CSS 스타일 추가 -----
st.markdown(
    """
    <style>
    .css-18e3th9 {
        padding: 1rem 1rem; /* 좌우 여백 확장 */
    }
    .css-1d391kg {
        padding: 1rem 1rem; /* 좌우 여백 확장 */
    }
    .stDivider {
        margin: 1rem 1; /* 구분선 여백 조정 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 엑셀 파일 경로
file_path = 'merged_v3.xlsx'

# 엑셀에서 최초 한 번만 로드하는 함수
def load_data():
    """엑셀에서 데이터를 불러와서 DataFrame으로 반환합니다.
       파일이 없으면 빈 DataFrame을 반환합니다."""
    if os.path.exists(file_path):
        return pd.read_excel(file_path, engine='openpyxl')
    else:
        st.warning("엑셀 파일이 존재하지 않아 빈 데이터를 사용합니다.")
        return pd.DataFrame()

# ----- 콜백 함수들 -----
def increment_likes(idx):
    """좋아요 수를 1 증가시킨다."""
    # 세션에 저장된 df와 filtered_data 둘 다 갱신
    st.session_state['df'].at[idx, 'likes'] += 1
    if idx in st.session_state["filtered_data"].index:
        st.session_state["filtered_data"].at[idx, 'likes'] += 1

def increment_dislikes(idx):
    """나빠요 수를 1 증가시킨다."""
    st.session_state['df'].at[idx, 'dislikes'] += 1
    if idx in st.session_state["filtered_data"].index:
        st.session_state["filtered_data"].at[idx, 'dislikes'] += 1

# ----- 세션 초기화 -----
# 처음 로드될 때만 엑셀 → df 전처리
if 'df' not in st.session_state:
    df_temp = load_data()
    
    # '파일이름'에서 '단과대', '학과'를 분리
    if '파일이름' in df_temp.columns and len(df_temp) > 0:
        df_temp[['단과대', '학과']] = df_temp['파일이름'].str.split('_', expand=True).iloc[:, :2]
    
    # '학년/학기'를 '학년', '학기'로 분리
    if '학년/학기' in df_temp.columns and len(df_temp) > 0:
        df_temp[['학년', '학기']] = df_temp['학년/학기'].str.split('/', expand=True)
        df_temp['학기'] = df_temp['학기'].str.replace('학기', '').str.strip()
        df_temp['학년'] = df_temp['학년'].astype(str).str.strip()
        df_temp['학기'] = df_temp['학기'].astype(str).str.strip()

    # likes / dislikes 컬럼이 없으면 0으로 추가
    if 'likes' not in df_temp.columns:
        df_temp['likes'] = 0
    if 'dislikes' not in df_temp.columns:
        df_temp['dislikes'] = 0
    
    # 세션에 df 저장
    st.session_state['df'] = df_temp

# 만약 'filtered_data'가 세션에 없다면 빈 데이터프레임으로 초기화
if 'filtered_data' not in st.session_state:
    st.session_state['filtered_data'] = pd.DataFrame()

# 이제부터는 세션에 저장된 df만 사용
df = st.session_state['df']

# ----- 메인 UI 구성 -----
st.title("KNU 과목조회 도우미🎓")
st.markdown(
    '<p style="font-size:14px; color:gray;">학기별 인기있는 과목까지 한 눈에 보기!</p>',
    unsafe_allow_html=True
)

# 단과대 선택
if '단과대' not in df.columns:
    st.error("'단과대' 컬럼이 없습니다.")
    st.stop()

dept_options = df['단과대'].unique()
selected_dept = st.sidebar.selectbox("단과대학을 선택하세요", options=dept_options)

# 학과 선택
if '학과' not in df.columns:
    st.error("'학과' 컬럼이 없습니다.")
    st.stop()

dept_options2 = df[df['단과대'] == selected_dept]['학과'].unique()
selected_dept2 = st.sidebar.selectbox("학과를 선택하세요", options=dept_options2)

# 학년/학기 선택
if ('학년' not in df.columns) or ('학기' not in df.columns):
    st.error("'학년/학기' 관련 컬럼이 없습니다.")
    st.stop()

semester_options = (df['학년'] + '-' + df['학기']).unique()
selected_semester = st.sidebar.selectbox("학년과 학기를 선택하세요", options=semester_options)

# 조회 버튼
if st.sidebar.button("조회"):
    # 필터링된 데이터 세션에 저장
    st.session_state["filtered_data"] = df[
        (df['단과대'] == selected_dept) &
        (df['학과'] == selected_dept2) &
        ((df['학년'] + '-' + df['학기']) == selected_semester)
    ]

# ----- 조회 결과 화면 -----
filtered_df = st.session_state["filtered_data"]

if not filtered_df.empty:

    # 좋아요가 가장 많은 과목 찾기
    most_liked_course = None
    max_likes = -1

    for idx, row in filtered_df.iterrows():
        if row['likes'] > max_likes:
            max_likes = row['likes']
            most_liked_course = row

    for idx, row in filtered_df.iterrows():
        course_name = row['교과목명']

        # 좋아요가 가장 많은 과목 강조
        if most_liked_course is not None and max_likes > 0 and row.equals(most_liked_course):
            st.markdown(
                f"🔥🔥 <span style='font-size:30px; color: #e6c55a; font-weight:bold;'>{course_name}</span>",
                unsafe_allow_html=True
    )
        else:
            st.markdown(
                f"<span style='font-size:25px; font-weight:bold;'>{course_name}</span>",
                unsafe_allow_html=True
    )

        st.write(
            f"이수구분: {row['이수구분']} | "
            f"학점: {row['학점']} | "
            f"실습여부: {row['실습여부']}"
        )

        col1, col2 = st.columns(2)

        # 좋아요 버튼
        col1.button(
            f"💓 수강 희망해요  {row['likes']}",
            key=f"like_btn_{idx}",
            on_click=increment_likes,
            args=(idx,)  # 콜백에 인덱스 전달
        )

        # 나빠요 버튼
        col2.button(
            f"❌ 수강 안해요 {row['dislikes']}",
            key=f"dislike_btn_{idx}",
            on_click=increment_dislikes,
            args=(idx,)
        )

        # 각 과목 사이에 구분선 추가
        st.divider()

else:
    st.write("조회 결과가 없습니다.")
