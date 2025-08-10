# import csv
# import time
# import os
# import re
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
# from dotenv import load_dotenv

# load_dotenv()
# CSV_FILE = "mit_ocw_courses_keywords.csv"
# BASE_URL = "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/"

# def setup_driver():
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--window-size=1920,1080")
#     try:
#         driver = webdriver.Chrome(options=options)
#         return driver
#     except WebDriverException as e:
#         print(f"❌ Error al iniciar el WebDriver: {e}")
#         return None

# def generar_keywords_simples(titulo):
#     # Generar palabras clave simples separando el título en palabras clave significativas:
#     # quitamos palabras muy comunes y números, y dejamos las relevantes.
#     stopwords = {'and', 'of', 'to', 'in', 'the', 'for', 'with', 'on', 'a', 'an', 'fall', 'spring'}
#     palabras = titulo.lower().replace(',', '').split()
#     keywords = [p for p in palabras if p not in stopwords and not p.isdigit()]
#     # Quitar duplicados manteniendo orden:
#     seen = set()
#     kws = []
#     for kw in keywords:
#         if kw not in seen:
#             seen.add(kw)
#             kws.append(kw)
#     return ", ".join(kws)

# def scrape_mit_ocw_courses():
#     driver = setup_driver()
#     if not driver:
#         return []

#     driver.get(BASE_URL)
#     wait = WebDriverWait(driver, 20)
#     courses = []

#     try:
#         course_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))
#         print(f"🔍 Encontrados {len(course_elements)} cursos en la página.")

#         for course in course_elements:
#             try:
#                 title_link_el = course.find_element(By.CSS_SELECTOR, "div.course-title a")
#                 link = title_link_el.get_attribute("href")

#                 title_parts = link.split('/')[-2].split('-')
#                 clean_title = ' '.join(title_parts[2:-1]).replace("science", "Science").title()

#                 course_info_el = course.find_element(By.CSS_SELECTOR, "div.resource-type")
#                 course_info = course_info_el.text.strip()

#                 description = "N/A"
#                 try:
#                     desc_el = course.find_element(By.CSS_SELECTOR, "div.course-description")
#                     description = desc_el.text.strip()
#                 except NoSuchElementException:
#                     pass

#                 keywords = generar_keywords_simples(clean_title)

#                 courses.append({
#                     "title": clean_title,
#                     "link": link,
#                     "course_info": course_info,
#                     "description": description,
#                     "keywords": keywords
#                 })
#             except (NoSuchElementException, IndexError) as e:
#                 print(f"⚠️ Curso con info incompleta o formato inesperado, se omite. Error: {e}")
#                 continue
#     except TimeoutException:
#         print("⚠️ Tiempo de espera agotado o no se encontraron cursos.")
#     finally:
#         driver.quit()

#     return courses

# if __name__ == "__main__":
#     cursos = scrape_mit_ocw_courses()
#     if cursos:
#         with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
#             fieldnames = ["title", "link", "course_info", "description", "keywords"]
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerows(cursos)
#         print(f"✅ Guardados {len(cursos)} cursos con keywords simples en '{CSV_FILE}'.")
#     else:
#         print("⚠️ No se encontraron cursos para guardar.")