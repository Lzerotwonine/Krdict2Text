import os
import time
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service

class KrDictScraper:
    def __init__(self):
        self.base_url = "https://krdict.korean.go.kr/m/vie/searchDetailWordsResult?searchFlag=Y&nation=vie&nationCode=2&currentPage={}&divSearch=detail&ParaWordNo=&syllablePosition=&gubun_all=ALL&gubun=W&gubun=P&gubun=E&nativeCode_all=ALL&nativeCode=1&nativeCode=2&nativeCode=3&nativeCode=0&sp_code_all=ALL&sp_code=1&sp_code=2&sp_code=3&sp_code=4&sp_code=5&sp_code=6&sp_code=7&sp_code=8&sp_code=9&sp_code=10&sp_code=11&sp_code=12&sp_code=13&sp_code=14&sp_code=27&im_cnt_all=ALL&im_cnt=3&im_cnt=2&im_cnt=1&im_cnt=0&multimedia_all=ALL&multimedia=P&multimedia=I&multimedia=V&multimedia=A&multimedia=S&multimedia=N&searchSyllableStart=&searchSyllableEnd=&searchOp=AND&searchTarget=word&searchOrglanguage=all&wordCondition=wordAll&query=&_csrf=494b9051-0fba-4be7-9b33-3fe1866c83e2"
        self.base_folder = os.environ.get('KRDICT_BASE_FOLDER', os.path.abspath(os.path.dirname(__file__)))
        self.output_path = os.path.join(self.base_folder, "data", "database.txt")
        self.process_path = os.path.join(self.base_folder, "data", "process.txt")
        self.log_path = os.path.join(self.base_folder, "data", "log.txt")
        self.end_page = 1  # Chạy thử nghiệm trên trang đầu tiên

        # Gọi hàm create_process_file() trong __init__()
        self.create_process_file()

        # Kiểm tra giá trị của self.current_page
        if self.current_page is None:
            print("Giá trị của self.current_page là None sau khi gọi hàm create_process_file() trong __init__.")
        else:
            print("Giá trị của trang hiện tại là:", self.current_page)

        logging.basicConfig(filename=self.log_path, level=logging.INFO, format='%(asctime)s - %(message)s')

        # Cấu hình WebDriver
        edge_driver_path = os.path.join(self.base_folder, "edgedriver_win64", "msedgedriver.exe")
        service = Service(edge_driver_path)
        self.driver = webdriver.Edge(service=service)
        self.wait = WebDriverWait(self.driver, 10)

    def get_last_saved_page(self):
        try:
            with open(self.process_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    # Tìm dòng chứa số thứ tự và trang
                    if line.startswith("Trang"):
                        continue
                    if line.strip() and line.strip()[1:].isdigit():
                        index = int(line.split(".")[0])
                        # Bỏ qua các số thứ tự đã được lưu
                        if index > 10:
                            # Đọc dữ liệu từ vị trí này
                            data = lines[index-1]
                            # Bỏ số thứ tự và dấu cách ở đầu dòng
                            return data[3:].strip()
        except FileNotFoundError:
            print("Không tìm thấy file tiến trình. Tạo file mới.")
            self.create_process_file()
        except Exception as e:
            print(f"Lỗi khi đọc tiến trình: {e}")
        return None

    def create_process_file(self):
        try:
            with open(self.process_path, "w", encoding="utf-8"):
                pass  # Không ghi bất kỳ thông tin nào
            # Gán giá trị mặc định cho current_page
            self.current_page = 1
        except Exception as e:
            print(f"Lỗi khi tạo file tiến trình: {e}")

    def get_data(self, page):
        try:
            print(f"Đang truy cập trang {page}")
            self.driver.get(self.base_url.format(page))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search_result dl')))
            print(f"Đã tải xong trang {page}")

            words = self.driver.find_elements(By.CSS_SELECTOR, '.search_result dl')
            if not words:
                print(f"Không tìm thấy từ nào trên trang {page}")
                return []

            data = []
            for word in words:
                word_data = self.parse_word(word)
                if word_data:
                    data.append(word_data)

            return data
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu từ trang {page}: {e}")
            return None

    def parse_word(self, word):
        try:
            # Lấy thông tin từ thẻ dt
            dt = word.find_element(By.TAG_NAME, 'dt')
            main_word = dt.find_element(By.CSS_SELECTOR, 'span.word_type1_17').text.strip()
            sup = dt.find_elements(By.TAG_NAME, 'sup')
            hanja = dt.find_element(By.XPATH, 'span[not(@class)]').text.strip() if dt.find_elements(By.XPATH, 'span[not(@class)]') else ""

            if sup:
                main_word = main_word.split()[0]  # Loại bỏ số trong main_word
                main_word_sup = f"{main_word}={sup[0].text.strip()} {hanja}"
            else:
                main_word_sup = f"{main_word}={hanja}"

            word_type = dt.find_element(By.CSS_SELECTOR, 'span.word_att_type1').text.strip()
            word_type_trans = dt.find_element(By.CSS_SELECTOR, 'span.manyLang2').text.strip()
            readings = dt.find_element(By.CSS_SELECTOR, 'span.search_sub').text.strip().replace('\n', '')

            # Bắt đầu tạo chuỗi kết quả
            result = f"{main_word_sup} {word_type} {word_type_trans} {readings}"

            # Lấy thông tin từ các thẻ dd
            dds = word.find_elements(By.CSS_SELECTOR, 'dd')
            for dd in dds:
                # Nếu dd chứa thẻ strong, thì đây là phần giải nghĩa số
                if dd.find_elements(By.TAG_NAME, 'strong'):
                    result += f"\\n\\t{dd.text.strip()}"
                else:
                    result += f"\\n{dd.text.strip()}"

            # In thông báo và ghi log
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
            print(f"Lỗi khi lưu dữ liệu: {e}")

    def save_process(self, data, page):
        try:
            with open(self.process_path, "a", encoding="utf-8") as f:
                # Tính toán số kết quả bắt đầu và kết thúc cho trang hiện tại
                start_result = (page - 1) * 10 + 1
                end_result = page * 10

                # Ghi thông tin trang và kết quả
                f.write(f"Trang {page}, kết quả {start_result}~{end_result}\n")

                # Biến để đánh số kết quả
                result_number = start_result

                for word_data in data:
                    main_word_info = word_data.split('=')[0]
                    if '(' in main_word_info:
                        main_word = main_word_info.split()[0]
                    else:
                        main_word = main_word_info

                    # Lưu số thứ tự và dữ liệu của từ
                    f.write(f"{result_number}. {main_word}\n")
                    result_number += 1

                # Đảm bảo lưu đủ 10 từ cho mỗi trang
                for j in range(result_number, end_result + 1):
                    f.write(f"{j}. \n")   # Lưu một dòng trống để đảm bảo có 10 dòng
        except Exception as e:
            print(f"Lỗi khi lưu tiến trình: {e}")

    def log(self, message):
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        except Exception as e:
            print(f"Lỗi khi ghi log: {e}")

    def scrape(self):
        # Kiểm tra xem có dữ liệu tiến trình hay không
        if self.current_page is None:
            print("Không tìm thấy file tiến trình. Chạy lại từ trang đầu để có dữ liệu tiến trình.")
            logging.info("Không tìm thấy file tiến trình. Chạy lại từ trang đầu để có dữ liệu tiến trình.")
            self.current_page = 1
        else:
            print(f"Dữ liệu tiến trình được đọc từ trang {self.current_page}.")
            logging.info(f"Dữ liệu tiến trình được đọc từ trang {self.current_page}.")

        while self.current_page <= self.end_page:
            # Đọc dữ liệu từ tiến trình
            data = self.get_last_saved_page()

            # Nếu không có dữ liệu từ tiến trình, tiếp tục lấy dữ liệu từ trang đầu tiên
            if data is None:
                print(f"Không có dữ liệu từ tiến trình. Tiếp tục lấy dữ liệu từ trang {self.current_page}...")
                logging.info(f"Không có dữ liệu từ tiến trình. Tiếp tục lấy dữ liệu từ trang {self.current_page}...")
                data = self.get_data(self.current_page)
            else:
                print("Đang lấy dữ liệu từ tiến trình...")
                logging.info("Đang lấy dữ liệu từ tiến trình...")
                print(f"Dữ liệu được lấy từ tiến trình: {data}")
                logging.info(f"Dữ liệu được lấy từ tiến trình: {data}")

            # Nếu có dữ liệu, lưu và tiếp tục
            if data:
                self.save_data(data, self.current_page)
                self.save_process(data, self.current_page)
            self.current_page += 1

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
        time.sleep(15)

if __name__ == "__main__":
    scraper = KrDictScraper()
    scraper.scrape()
