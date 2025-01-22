import streamlit as st
import pandas as pd

# 웹페이지 구현
st.set_page_config(
    page_title="KNU 수강신청 도우미",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

courses = {
    "컴퓨터공학": {
        1: {  # 1학년
            1: [
                {"name": "프로그래밍 기초", "credits": 3, "has_lab": "없음", "description": "프로그래밍 언어의 기초를 배우는 과목"},
                {"name": "알고리즘 기초", "credits": 3, "has_lab": "없음", "description": "기본적인 알고리즘과 문제 해결 방법을 학습하는 과목"}
            ],
            2: [
                {"name": "기초 수학", "credits": 3, "has_lab": "없음", "description": "수학적 기초를 다지는 과목"},
                {"name": "컴퓨터 개론", "credits": 2, "has_lab": "없음", "description": "컴퓨터 과학의 기본 이론을 배우는 과목"}
            ]
        },
        2: {  # 2학년
            1: [
                {"name": "자료구조", "credits": 3, "has_lab": "없음", "description": "효율적인 데이터 저장과 처리 방법을 다루는 과목"},
                {"name": "운영체제 기초", "credits": 3, "has_lab": "없음", "description": "운영체제의 기본 개념과 원리를 배우는 과목"}
            ],
            2: [
                {"name": "웹 개발", "credits": 3, "has_lab": "있음", "description": "웹 애플리케이션 개발 기술을 배우는 과목"},
                {"name": "수학적 모델링", "credits": 3, "has_lab": "없음", "description": "수학적 개념을 이용한 문제 해결 방법을 학습하는 과목"}
            ]
        },
        3: {  # 3학년
            1: [
                {"name": "컴퓨터 네트워크", "credits": 3, "has_lab": "있음", "description": "컴퓨터 간의 통신 원리와 기술을 배우는 과목"},
                {"name": "데이터베이스 시스템", "credits": 3, "has_lab": "없음", "description": "데이터베이스의 설계와 관리 방법을 배우는 과목"}
            ],
            2: [
                {"name": "인공지능", "credits": 3, "has_lab": "있음", "description": "기계 학습과 인공지능 알고리즘을 배우는 과목"},
                {"name": "소프트웨어 공학", "credits": 3, "has_lab": "없음", "description": "소프트웨어 개발 및 관리 방법론을 학습하는 과목"}
            ]
        },
        4: {  # 4학년
            1: [
                {"name": "졸업 프로젝트", "credits": 3, "has_lab": "있음", "description": "학생이 직접 프로젝트를 진행하며 실력을 쌓는 과목"},
                {"name": "고급 알고리즘", "credits": 3, "has_lab": "없음", "description": "고급 알고리즘과 문제 해결 기술을 배우는 과목"}
            ],
            2: [
                {"name": "캡스톤 디자인", "credits": 3, "has_lab": "있음", "description": "실제 산업 문제를 해결하는 프로젝트 기반 과목"},
                {"name": "산업체 실습", "credits": 2, "has_lab": "있음", "description": "산업체에서 실무 경험을 쌓는 과목"}
            ]
        }
    },
    "전기전자공학": {
        1: {  # 1학년
            1: [
                {"name": "회로이론", "credits": 3, "has_lab": "있음", "description": "회로의 기본 원리와 해석 방법을 배우는 과목"},
                {"name": "기초 전자회로", "credits": 3, "has_lab": "있음", "description": "기초적인 전자회로 설계와 분석을 배우는 과목"}
            ],
            2: [
                {"name": "전기기기", "credits": 3, "has_lab": "있음", "description": "전기기기의 동작 원리와 특성을 배우는 과목"},
                {"name": "기초 물리학", "credits": 3, "has_lab": "없음", "description": "물리학의 기초 이론을 배우는 과목"}
            ]
        },
        2: {  # 2학년
            1: [
                {"name": "전자기학", "credits": 3, "has_lab": "없음", "description": "전자기학의 기본 원리와 응용을 배우는 과목"},
                {"name": "신호 및 시스템", "credits": 3, "has_lab": "없음", "description": "신호 처리 및 시스템의 분석 방법을 배우는 과목"}
            ],
            2: [
                {"name": "디지털 회로", "credits": 3, "has_lab": "있음", "description": "디지털 회로 설계 및 분석을 배우는 과목"},
                {"name": "확률 및 통계", "credits": 3, "has_lab": "없음", "description": "확률과 통계 이론을 활용한 문제 해결 과목"}
            ]
        },
        3: {  # 3학년
            1: [
                {"name": "제어 시스템", "credits": 3, "has_lab": "있음", "description": "자동 제어 시스템의 원리와 설계를 배우는 과목"},
                {"name": "반도체 소자", "credits": 3, "has_lab": "있음", "description": "반도체 소자의 원리와 응용을 배우는 과목"}
            ],
            2: [
                {"name": "전력 시스템", "credits": 3, "has_lab": "없음", "description": "전력 시스템의 설계 및 운용 원리를 배우는 과목"},
                {"name": "디지털 신호 처리", "credits": 3, "has_lab": "있음", "description": "디지털 신호의 처리 방법을 배우는 과목"}
            ]
        },
        4: {  # 4학년
            1: [
                {"name": "고급 제어 시스템", "credits": 3, "has_lab": "없음", "description": "고급 제어 이론과 응용을 배우는 과목"},
                {"name": "산업 자동화", "credits": 3, "has_lab": "있음", "description": "산업 자동화 시스템의 설계 및 구현을 배우는 과목"}
            ],
            2: [
                {"name": "전기설비", "credits": 3, "has_lab": "있음", "description": "전기설비의 설계 및 설치 방법을 배우는 과목"},
                {"name": "졸업 논문", "credits": 3, "has_lab": "없음", "description": "졸업을 위한 연구 및 논문 작성을 배우는 과목"}
            ]
        }
    }
}

# Streamlit 앱 설정
def course_selection():
    st.title("KNU 수강신청 도우미🎓")

    # 학과 입력 받기
    department = st.selectbox("학과를 선택하세요", ["컴퓨터공학", "전기전자공학"], key="department_select")

    # 학년 입력 받기
    year = st.selectbox("학년을 선택하세요", [1, 2, 3, 4], key="year_select")

    # 학기 입력 받기
    semester = st.selectbox("학기를 선택하세요", [1, 2], key="semester_select")

    # 선택된 정보로 교과목 조회하기
    if st.button("조회"):
        if department in courses and year in courses[department] and semester in courses[department][year]:
            course_list = []
            for course in courses[department][year][semester]:
                course_list.append({
                    "학년": year,
                    "학기": semester,
                    "과목 이름": course['name'],
                    "학점": course['credits'],
                    "실습여부": course['has_lab'],
                    "한줄소개": course['description']
                })
            # Pandas DataFrame으로 변환 후 테이블 형식으로 출력
            course_df = pd.DataFrame(course_list)
            # 테이블 가운데 정렬 스타일 적용
            st.write(course_df.style.set_table_styles(
                [{'selector': 'th, td', 'props': [('text-align', 'center')]}]
            ))
        else:
            st.error("잘못된 입력입니다. 다시 시도해주세요.")

# Streamlit 실행
if __name__ == "__main__":
    course_selection()
