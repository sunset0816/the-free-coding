import streamlit as st
import pandas as pd
import json as j
import os

# 웹페이지 설정
st.set_page_config(
    page_title="KNU 수강신청 도우미",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# JSON 데이터 로드 함수
def load_all_courses(directory):
    combined_data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):  # JSON 파일만 처리
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                file_data = j.load(file)
                combined_data.update(file_data)  # 데이터를 병합
    return combined_data

# JSON 데이터 저장 함수
def save_data(data, filepath):
    
    with open(filepath, 'w', encoding='utf-8') as file:
        j.dump(data, file, ensure_ascii=False, indent=4)

# JSON 데이터 불러오기
data_directory = "C:\Users\noul0\OneDrive\바탕 화면\코딩뒷풀이\json_files"  # JSON 파일이 있는 디렉토리 경로
data = load_all_courses(data_directory)

# 단과대학과 학과 데이터
colleges = {
    "산림환경과학대학": ["산림자원학","산림경영학","산림환경보호학","생태조경디자인학","목재종이과학부(종이소재과학전공)","목재종이과학부(목재과학전공)"],
    "사회과학대학": ["사회학","정치외교학","행정학","심리학","부동산학","미디어커뮤니케이션학","문화인류학"],
    "동물생명과학대학": ["동물자원과학학", "동물산업융합학", "동물응용과학학"],
    "의생명과학대학": ["분자생명과학", "생명건강공학", "생물의소재공학", "의생명공학", "시스템면역과학"]
}

# Streamlit 앱 설정
def course_selection():
    st.title("KNU 수강신청 도우미🎓")
    st.markdown(
        '<p style="font-size:14px; color:gray;">인기있는 과목을 추천해드려요!</p>',
        unsafe_allow_html=True
    )

    # 단과대 입력 받기
    college = st.selectbox("단과대학을 선택하세요", list(colleges.keys()), key="college_select")

    # 학과 선택: 선택한 단과대학에 해당하는 학과만 표시
    if college:
        department = st.selectbox("학과를 선택하세요", colleges[college], key="department_select")
        department = department.strip()
    else:
        department = None

    # 학년/학기 입력 받기
    year = st.selectbox("학년과 학기를 선택하세요", ['1-1', '1-2', '2-1', '2-2', '3-1', '3-2', '4-1', '4-2'], key="year_select")

    # 디버깅 정보 표시
    st.write(f"선택된 단과대학: {college}")
    st.write(f"선택된 학과: {department}")
    st.write(f"선택된 학년/학기: {year}")
    st.write(f"JSON에서 학과 키 확인: {list(data.get(college, {}).keys())}")

# 초기 세션 상태 설정
if "courses" not in st.session_state:
    st.session_state["courses"] = []

# 데이터 예제
if "data" not in st.session_state:
    st.session_state["data"] = {
        "공과대학": {
            "컴퓨터공학과": {
                "2023": [
                    {
                        "과목명": "프로그래밍 기초",
                        "이수구분": "필수",
                        "학점": 3,
                        "실습여부": "Y",
                        "과목설명": "프로그래밍의 기본 개념을 학습합니다."
                    },
                    {
                        "과목명": "알고리즘",
                        "이수구분": "선택",
                        "학점": 3,
                        "실습여부": "N",
                        "과목설명": "효율적인 알고리즘 설계를 학습합니다."
                    }
                ]
            }
        }
    }

# 데이터 조회
st.header("과목 조회")
college = st.selectbox("단과대학 선택", list(st.session_state["data"].keys()))
department = st.selectbox("학과 선택", list(st.session_state["data"][college].keys()))
year = st.selectbox("학년/학기 선택", list(st.session_state["data"][college][department].keys()))

if st.button("조회"):
    data = st.session_state["data"]
    if college in data:
        st.write(f"단과대학 {college} 데이터 있음")
        if department in data[college]:
            st.write(f"학과 {department} 데이터 있음")
            if year in data[college][department]:
                st.write(f"학년/학기 {year} 데이터 있음")
                st.session_state["courses"] = data[college][department][year]
                for idx, course in enumerate(data[college][department][year]):
                    st.write(f"### {course['과목명']}")
                    st.write(f"이수구분: {course['이수구분']}, 학점: {course['학점']}, 실습여부: {course['실습여부']}")
                    st.write(f"설명: {course['과목설명']}")

# 좋아요/나빠요 버튼 추가
for idx, course in enumerate(st.session_state["courses"]):
    st.subheader(course["과목명"])

    # 버튼을 위한 열 구성
    col1, col2 = st.columns(2)

    # 좋아요 초기화
    if "likes" not in course:
        course["likes"] = 0
    if "dislikes" not in course:
        course["dislikes"] = 0

    # 좋아요 버튼
    with col1:
        if st.button(f"👍 듣고싶어요 {course['likes']}", key=f"like_{idx}"):
            st.session_state["courses"][idx]["likes"] += 1

    # 나빠요 버튼
    with col2:
        if st.button(f"👎 별로에요 {course['dislikes']}", key=f"dislike_{idx}"):
            st.session_state["courses"][idx]["dislikes"] += 1

    # 좋아요/나빠요 상태 표시
    st.write(f"듣고싶어요: {course['likes']} | 별로에요: {course['dislikes']}")

if __name__ == "__main__":
    course_selection()

