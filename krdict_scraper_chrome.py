import logging
import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class KrDictScraper:
    def __init__(self):
        self.base_url = "https://krdict.korean.go.kr/m/vie/searchDetailWordsResult?searchFlag=Y&nation=vie&nationCode=2&currentPage={}&divSearch=detail&ParaWordNo=&syllablePosition=&gubun_all=ALL&gubun=W&gubun=P&gubun=E&nativeCode_all=ALL&nativeCode=1&nativeCode=2&nativeCode=3&nativeCode=0&sp_code_all=ALL&sp_code=1&sp_code=2&sp_code=3&sp_code=4&sp_code=5&sp_code=6&sp_code=7&sp_code=8&sp_code=9&sp_code=10&sp_code=11&sp_code=12&sp_code=13&sp_code=14&sp_code=27&im_cnt_all=ALL&im_cnt=3&im_cnt=2&im_cnt=1&im_cnt=0&multimedia_all=ALL&multimedia=P&multimedia=I&multimedia=V&multimedia=A&multimedia=S&multimedia=N&searchSyllableStart=&searchSyllableEnd=&searchOp=AND&searchTarget=word&searchOrglanguage=all&wordCondition=wordAll&query=&_csrf=494b9051-0fba-4be7-9b33-3fe1866c83e2"
        self.base_folder = os.environ.get('KRDICT_BASE_FOLDER', os.path.abspath(os.path.dirname(__file__)))
        self.output_path = os.path.join(self.base_folder, "data", "database.txt")
        self.process_path = os.path.join(self.base_folder, "data", "process.txt")
        self.log_path = os.path.join(self.base_folder, "data", "log.txt")
        self.end_page = 5  # Trang kết thúc nếu muốn chạy hết là 1595
        self.wait_time = 20  # Thời gian chờ mặc định

        logging.basicConfig(
            filename=self.log_path,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            encoding='utf-8'
        )

        chrome_driver_path = os.path.join(self.base_folder, "chromedriver-win64", "chromedriver.exe")
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Chạy Chrome ở chế độ headless để không mở cửa sổ trình duyệt
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        self.current_page = self.get_last_saved_page()
        if self.current_page is None:
            self.create_process_file()
            self.current_page = 0  # Gán self.current_page = 0 nếu không tìm thấy file tiến trình
        else:
            print("Giá trị của trang hiện tại là:", self.current_page)

    def get_last_saved_page(self):
        last_page = None
        try:
            with open(self.process_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print("Đang đọc các dòng trong file tiến trình:")
                for line in lines:
                    print(line.strip())  # In ra từng dòng trong file để kiểm tra
                    if line.startswith("Trang"):
                        parts = line.split(",")
                        last_page = int(parts[0].split()[1])  # Lấy chỉ số 1 sau khi tách dòng thành các phần
                print(f"Đã tìm thấy trang cuối cùng: {last_page}")  # In ra trang cuối cùng được tìm thấy
        except FileNotFoundError:
            logging.info("Không tìm thấy file tiến trình. Tạo file mới.")
        except Exception as e:
            logging.error(f"Lỗi khi đọc tiến trình: {e}")
        return last_page

    def create_process_file(self):
        try:
            with open(self.process_path, "w", encoding="utf-8"):
                pass
        except Exception as e:
            logging.error(f"Lỗi khi tạo file tiến trình: {e}")

    def get_data(self, page):
        try:
            print(f"Đang truy cập trang {page}")
            self.driver.get(self.base_url.format(page))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search_result dl')))
            print(f"Đã tải xong trang {page}")

            words = self.driver.find_elements(By.CSS_SELECTOR, '.search_result dl')
            if not words:
                not_found_message = f"Không tìm thấy từ nào trên trang {page}"
                print(not_found_message)
                logging.info(not_found_message)
                return []

            data = []
            for word in words:
                word_data = self.parse_word(word)
                if word_data:
                    data.append(word_data)

            return data
        except TimeoutException:
            logging.error(f"Lỗi timeout khi tải trang {page}")
            return None
        except Exception as e:
            logging.error(f"Lỗi khi lấy dữ liệu từ trang {page}: {e}")
            return None

    def parse_word(self, word):
        try:
            dt = word.find_element(By.TAG_NAME, 'dt')
            main_word = dt.find_element(By.CSS_SELECTOR, 'span.word_type1_17').text.strip()
            sup = dt.find_elements(By.TAG_NAME, 'sup')
            hanja = dt.find_element(By.XPATH, 'span[not(@class)]').text.strip() if dt.find_elements(By.XPATH, 'span[not(@class)]') else ""

            if sup:
                main_word = main_word.split()[0]
                main_word_sup = f"{main_word}={sup[0].text.strip()} {hanja}"
            else:
                main_word_sup = f"{main_word}={hanja}"

            word_type = dt.find_element(By.CSS_SELECTOR, 'span.word_att_type1').text.strip()
            readings = dt.find_element(By.CSS_SELECTOR, 'span.search_sub').text.strip().replace('\n', '')

            result = f"{main_word_sup} {word_type} {readings}"

            dds = word.find_elements(By.CSS_SELECTOR, 'dd')
            for dd in dds:
                if dd.find_elements(By.TAG_NAME, 'strong'):
                    result += f"\\n\\t{dd.text.strip()}"
                else:
                    result += f"\\n{dd.text.strip()}"

            logging.info(f"Lấy được từ {main_word} trong Trang {self.current_page}!")

            return result
        except NoSuchElementException as e:
            logging.error(f"Không tìm thấy phần tử: {e}")
            return ""
        except Exception as e:
            logging.error(f"Lỗi khi phân tích từ: {e}")
            return ""

    def save_data(self, data, page):
        try:
            with open(self.output_path, "a", encoding="utf-8") as f:
                for word_data in data:
                    f.write(word_data + "\n")
        except Exception as e:
            logging.error(f"Lỗi khi lưu dữ liệu: {e}")

    def save_process(self, data, page):
        try:
            append_mode = True
            if os.path.exists(self.process_path):
                with open(self.process_path, "r+", encoding="utf-8") as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1]
                        if last_line.strip() and last_line.startswith("Trang"):
                            append_mode = False
                            f.write("\n")  # Thêm dòng mới nếu có dữ liệu tiến trình cũ

            with open(self.process_path, "a", encoding="utf-8") as f:
                start_result = (page - 1) * 10 + 1
                end_result = page * 10

                f.write(f"Trang {page}, kết quả {start_result}~{end_result}\n")

                result_number = start_result

                for word_data in data:
                    parts = word_data.split('=')
                    main_word_info = parts[0].strip()

                    if '(' in main_word_info:
                        main_word = main_word_info.split()[0]
                    else:
                        main_word = main_word_info

                    sup_info = ""
                    if len(parts) > 1:
                        sup_parts = parts[1].split()
                        if sup_parts and sup_parts[0].isdigit():
                            sup_info = sup_parts[0]

                    if sup_info:
                        f.write(f"{result_number}. {main_word} {sup_info}\n")
                        message = f"Lưu từ {main_word} {sup_info} trong trang {page}!"
                    else:
                        f.write(f"{result_number}. {main_word}\n")
                        message = f"Lưu từ {main_word} trong trang {page}!"

                    logging.info(message)
                    self.log(message)

                    result_number += 1

                self.current_page = page

                for j in range(result_number, end_result + 1):
                    f.write(f"{j}. \n")
        except Exception as e:
            logging.error(f"Lỗi khi lưu tiến trình: {e}")

    def log(self, message):
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        except Exception as e:
            logging.error(f"Lỗi khi ghi log: {e}")

    def scrape(self):
        start_page = self.current_page + 1

        if start_page > self.end_page:
            print("Đã thu thập đủ dữ liệu của trang yêu cầu!")
            logging.info("Đã thu thập đủ dữ liệu của trang yêu cầu!")
            return

        # Tiếp tục lấy dữ liệu từ các trang tiếp theo
        for page in range(start_page, self.end_page + 1):
            print(f"Tiếp tục lấy dữ liệu từ trang {page}...")
            logging.info(f"Tiếp tục lấy dữ liệu từ trang {page}...")
            self.scrape_page(page)

        self.driver.quit()

    def scrape_page(self, page):
        start_time = time.time()
        data = self.get_data(page)
        if data:
            self.save_data(data, page)
            self.save_process(data, page)
            elapsed_time = time.time() - start_time
            message = f"Đã lấy dữ liệu từ trang {page} trong {elapsed_time:.2f} giây"
            logging.info(message)
            self.log(message)

            # In tổng số từ đã lấy trong trang vào file log
            total_words = len(data)
            logging.info(f"Tổng từ đã lấy trong Trang {page} là {total_words}!")

            # Cập nhật self.current_page sau khi lấy dữ liệu từ trang hiện tại
            self.current_page = page
        time.sleep(self.wait_time)

if __name__ == "__main__":
    scraper = KrDictScraper()
    scraper.scrape()
