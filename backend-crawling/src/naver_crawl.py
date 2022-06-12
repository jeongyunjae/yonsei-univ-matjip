import time

from io import TextIOWrapper
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# 크롬 드라이버 실행
def get_driver():
  options = webdriver.ChromeOptions()
  # 지정한 user-agent로 설정
  options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664 Safari/537.36") 
  # 크롬 화면 크기를 설정(but 반응형 사이트에서는 html요소가 달라질 수 있음)
  options.add_argument("window-size=1440x900")
  # 브라우저가 백그라운드에서 실행됩니다.
  # options.add_argument("headless")

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # chromedriver 열기
  driver.get('https://map.naver.com')  # 주소 가져오기
  driver.implicitly_wait(60)
  return driver

# 검색어 입력
def search_place(driver:WebDriver, search_text: str):
  search_input_box = driver.find_element_by_css_selector("div.input_box>input.input_search")
  search_input_box.send_keys(search_text)
  search_input_box.send_keys(Keys.ENTER)
  time.sleep(5)

# 다음 페이지 이동 및 마지막 페이지 검사
def next_page_move(driver:WebDriver):
  # 페이지네이션 영역에 마지막 버튼 선택
  next_page_btn = driver.find_element_by_css_selector('div._2ky45>a:last-child')
  next_page_class_name = BeautifulSoup(next_page_btn.get_attribute('class'), "html.parser")

  if len(next_page_class_name.text) > 10:
    print("검색완료")
    driver.quit()
    return False
  else:
    next_page_btn.send_keys(Keys.ENTER)
    return True

# 검색 iframe 이동
def to_search_iframe(driver:WebDriver):
  driver.switch_to.default_content()
  driver.switch_to.frame('searchIframe')

# 매장정보 추출
def get_store_data(driver:WebDriver, scroll_container: WebElement, file: TextIOWrapper):
  get_store_li = scroll_container.find_elements_by_css_selector('ul > li')
  
  for index in range(len(get_store_li)):
    get_store_li[index].find_element_by_css_selector('div:nth-child(1)').click()
    driver.switch_to.default_content()
    driver.switch_to.frame('entryIframe')
    
    time.sleep(2)
    try:
      try: 
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, "place_didmount")))
      except TimeoutException:
        to_search_iframe(driver)

      title_element = driver.find_element_by_css_selector('#_title > span:nth-child(1)').get_attribute('innerHTML')
      address_element = driver.find_element_by_css_selector('div.place_section_content > ul >li:nth-child(2) > div > a > span').get_attribute('innerHTML')

      title = BeautifulSoup(title_element, "html.parser").get_text()
      address = BeautifulSoup(address_element, "html.parser").get_text()

      file.write(title + "|" + address + "\n")
      to_search_iframe(driver)
    except TimeoutException:
      to_search_iframe(driver)

# 메인 함수
def naver_crawl():
  filer = open('src/list.csv','a',encoding='utf-8')
  driver = get_driver()
  search_place(driver,'연세대학교 맛집')
  to_search_iframe(driver)
  time.sleep(2)

  try:
    scroll_container = driver.find_element_by_id("_pcmap_list_scroll_container")
  except:
    print("스크롤 영역 감지 실패")

  try:
    while True:
      for i in range(6):
        # 자바 스크립트 실행
        driver.execute_script("arguments[0].scrollBy(0,2000)",scroll_container)
        time.sleep(1)
      get_store_data(driver,scroll_container,filer)
      is_continue = next_page_move(driver)
      if is_continue == False:
        break
  except:
    print("크롤링 과정 중 에러 발생")
