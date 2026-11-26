import streamlit as st
import pandas as pd

# 1. 함수(def): 음식 재료 속에 알레르기 성분이 있는지 검사하는 함수
def check_allergy(my_allergies, food_ingredients):
    detected = []  # 발견된 알레르기 성분을 담을 리스트
    
    # 2. 반복구조(for): 음식 재료를 하나씩 확인
    for ingredient in food_ingredients:
        if ingredient in my_allergies:
            detected.append(ingredient)
            
    return detected

# 도표 출력 및 안전/위험 음식 분류 함수(def)
def print_summary_table(records, safe_foods, danger_foods):
    st.subheader("📊 검사 결과 요약표")
    
    # 스트림릿 표(DataFrame) 형태로 변환하여 깔끔하게 출력
    df = pd.DataFrame(records, columns=["음식 이름", "섭취 여부", "포함된 알레르기 유발 성분"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 최종 식단 가이드 출력
    st.subheader("🍽️ 최종 식단 가이드")
    st.success(f"**▶ 먹어도 되는 음식 (안전):** {', '.join(safe_foods) if safe_foods else '없음'}")
    st.error(f"**▶ 먹으면 안 되는 음식 (위험):** {', '.join(danger_foods) if danger_foods else '없음'}")

# 메인 프로그램 실행 함수
def main():
    st.title("🚨 알레르기 유발 식품 판별기")
    
    # 3. 리스트(list): 미리 등록된 기본 음식 데이터 [음식명, [재료 리스트]]
    default_foods = [
        ["까르보나라", ["밀가루", "우유", "계란", "베이컨", "치즈"]],
        ["새우볶음밥", ["쌀", "새우", "계란", "당근", "대파"]],
        ["양념치킨", ["닭고기", "밀가루", "땅콩", "간장", "마늘"]],
        ["된장찌개", ["대두", "두부", "애호박", "양파", "멸치"]],
        ["페퍼로니피자", ["밀가루", "치즈", "우유", "돼지고기", "토마토"]],
        ["복숭아아이스티", ["복숭아", "설탕", "홍차"]],
        ["고등어구이", ["고등어", "소금"]],
        ["소고기미역국", ["소고기", "미역", "참기름", "마늘", "간장"]],
        ["삼겹살구이", ["돼지고기", "상추", "마늘", "쌈장"]],
        ["과일샐러드", ["사과", "바나나", "양상추", "방울토마토"]],
        ["현미밥", ["현미", "쌀", "물"]]
    ]

    # 사용자가 추가로 입력한 음식을 웹 화면이 새로고침되어도 기억하기 위한 저장 공간
    if "custom_foods" not in st.session_state:
        st.session_state.custom_foods = []

    # 사용자 알레르기 입력받기 (input -> st.text_input)
    user_input = st.text_input("본인의 알레르기 성분을 쉼표(,)로 구분해 입력하세요 (예: 우유, 땅콩, 새우)")
    my_allergies = [item.strip() for item in user_input.split(",") if item.strip()]
    
    if not my_allergies:
        st.info("👆 위 입력창에 알레르기 성분을 입력하면 기본 11가지 음식에 대한 검사가 자동으로 시작됩니다.")
        return

    st.write(f"**등록된 알레르기:** `{', '.join(my_allergies)}`")
    st.divider()

    # 추가 음식 입력 폼 (while True 반복 입력 대신 웹 폼 사용)
    with st.expander("➕ 추가로 검사할 음식 직접 입력하기", expanded=True):
        with st.form("add_food_form", clear_on_submit=True):
            food_name = st.text_input("추가로 검사할 음식 이름").strip()
            ing_input = st.text_input("음식에 들어간 재료를 쉼표(,)로 구분해 입력하세요 (예: 밀가루, 계란, 설탕)")
            submitted = st.form_submit_button("음식 추가 및 검사")
            
            if submitted:
                if food_name == "":
                    st.warning("음식 이름을 정확히 입력해주세요.")
                else:
                    food_ingredients = [item.strip() for item in ing_input.split(",") if item.strip()]
                    st.session_state.custom_foods.append([food_name, food_ingredients])
                    
                    # 즉시 판별 알림 출력
                    danger_list = check_allergy(my_allergies, food_ingredients)
                    if len(danger_list) > 0:
                        st.error(f"[위험!] '{food_name}'에는 알레르기 성분({', '.join(danger_list)})이 들어있습니다.")
                    else:
                        st.success(f"[안전] '{food_name}'에는 알레르기 성분이 없습니다.")

    records = []       # 도표 출력용 리스트
    safe_foods = []    # 먹어도 되는 음식 리스트
    danger_foods = []  # 먹으면 안 되는 음식 리스트

    # 기본 음식 + 사용자가 추가한 음식을 합쳐서 한 번에 검사
    all_foods = default_foods + st.session_state.custom_foods

    # 4. 반복구조(for): 모든 음식을 검사하여 분류
    for food_item in all_foods:
        f_name = food_item[0]
        f_ings = food_item[1]
        
        danger_list = check_allergy(my_allergies, f_ings)
        
        # 선택구조(if - else)로 안전/위험 분류
        if len(danger_list) > 0:
            allergen_str = ", ".join(danger_list)
            danger_foods.append(f_name)
            records.append([f_name, "❌ 섭취 불가", allergen_str])
        else:
            safe_foods.append(f_name)
            records.append([f_name, "✅ 섭취 가능", "없음"])

    # 최종 도표 및 먹어도 되는/안 되는 음식 목록 출력
    print_summary_table(records, safe_foods, danger_foods)

# 프로그램 시작
if __name__ == "__main__":
    main()
