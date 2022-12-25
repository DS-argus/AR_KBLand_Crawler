import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

import time
from datetime import date

# selenium option settings
options = webdriver.ChromeOptions()

# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://kbland.kr/"
driver.get(url)

driver.maximize_window()

# 만약 팝업이 뜬다면,
try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.popConWrap > div.mainBnbtm > button")))

    button = driver.find_element(by=By.CSS_SELECTOR, value="div.popConWrap > div.mainBnbtm > button")
    button.click()
except:
    pass

for _ in range(7):
    action = ActionChains(driver)
    action.key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()

# 검색창 클릭
button = driver.find_element(by=By.CSS_SELECTOR, value="div.homeSerchBox > span")
button.click()
time.sleep(1)

# 주소로 찾기 클릭
button = driver.find_elements(by=By.CSS_SELECTOR, value="li.nav-item")[1].find_element(by=By.CSS_SELECTOR, value="a")
button.click()
time.sleep(1)

# 서울시 선택
def select_Seoul():
    button = driver.find_elements(by=By.CSS_SELECTOR, value="div.tab-content div.address-section > div.step")[1].find_element(by=By.CSS_SELECTOR, value="span")
    button.click()
    time.sleep(1)

    button = driver.find_elements(by=By.CSS_SELECTOR, value="div.tab-content div.address-item > div > label")[0]
    button.click()
    time.sleep(1)

    return

select_Seoul()

# 총 지역(구) 개수
area_list = driver.find_elements(by=By.CSS_SELECTOR, value="div.address-section > div.address-item label")
num_area = len(area_list)
print(f"number of area : {num_area}")

# 지역(구) 반복문
for i in range(num_area):

    # 반복문 돌다가 area_list가 변경되어 매번 다시 할당
    area_list = driver.find_elements(by=By.CSS_SELECTOR, value="div.address-section > div.address-item label")
    area = area_list[i]

    # 지역(구) 이름
    area_name = area.text
    print(f"지역(구) : {area_name}")

    # 지역(구) 클릭
    area.click()
    time.sleep(1)

    # 총 지역(동) 개수
    sub_area_list = driver.find_elements(by=By.CSS_SELECTOR, value="div.address-section > div.address-item label")
    num_sub_area = len(sub_area_list)
    print(f"number of sub_area : {num_sub_area}")

    # 지역(동) 반복문 
    for i in range(num_sub_area):

        sub_area_list = driver.find_elements(by=By.CSS_SELECTOR, value="div.address-section > div.address-item label")
        sub_area = sub_area_list[i]

        # 지역(동) 이름
        sub_area_name = sub_area.text
        print(f"지역(동) : {area_name} {sub_area_name}")

        # 지역(동) 클릭
        sub_area.click()
        time.sleep(1)   
        
        # 엑셀 다운로드
        house_list = driver.find_elements(by=By.CSS_SELECTOR, value="div.search-section div.item-search-poi")
        # APT_list = [house for house in house_list if house.find_element(by=By.CSS_SELECTOR, value="div > span > span").text == "아파트"]
        for i in range(len(house_list)):
            house_list = driver.find_elements(by=By.CSS_SELECTOR, value="div.search-section div.item-search-poi")

            house = house_list[i]

            # 아파트가 아니면 넘어감
            if house.find_element(by=By.CSS_SELECTOR, value="div > span > span").text != "아파트":
                continue

            # 아파트 이름 출력
            APT_name = house.find_element(by=By.CSS_SELECTOR, value="div > span > span.text").text
            print(APT_name)

            driver.execute_script("window.scrollTo(0, window.scrollY + 200);")

            # 아파트 클릭
            # 여기서 에러발생하면 스크롤 내리게 해야함
            try:
                house.click()
                time.sleep(2)
            except:
                pass
                # # #leftScroll > div > div.scroll-element.scroll-y.scroll-scrolly_visible > div > div.scroll-bar

                # action = ActionChains(driver)
                # action.move_to_element(house_list[i+11]).perform()
  
                # house.click()
                # time.sleep(2)


            # 확장 클릭
            button = driver.find_element(by=By.CSS_SELECTOR, value="span.bottomBtn")
            button.click()
            time.sleep(1)

            try:
                # 스크롤 내리기
                action = ActionChains(driver)
                action.move_to_element(driver.find_elements(by=By.CSS_SELECTOR, value="div.barbtnbox > button")[1]).perform()

                # KB시세 다운로드 클릭
                button = driver.find_elements(by=By.CSS_SELECTOR, value="div.barbtnbox > button")[1]
                button.click()
                time.sleep(1)

                # 과거 시세 엑셀다운로드 클릭
                button = driver.find_elements(by=By.CSS_SELECTOR, value="div.excelbtn > button")[0]
                button.click()
                time.sleep(1)

                # 닫기 클릭
                button = driver.find_element(by=By.CSS_SELECTOR, value="div.wh-layer > button")
                button.click()
                time.sleep(1)

            except:
                pass

            # 다시 복귀....
            button = driver.find_element(by=By.CSS_SELECTOR, value="div.topbtn-area > div > button.btn.btn-close")
            button.click()
            time.sleep(1)

            button = driver.find_elements(by=By.CSS_SELECTOR, value="#searchArea > div> button")[1]
            button.click()
            time.sleep(1)

            button = driver.find_element(by=By.CSS_SELECTOR, value="div.address-section > div.address-item label.btn.btn-secondary.active")
            button.click()
            time.sleep(1)


    print("======================================================\n")
    
    # 서울시 선택
    select_Seoul()



# def main():
#     KRLand_crawler()


# if __name__ == "__main__":
#     main()
