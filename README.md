# Krdict2Text

Là dự án gồm 2 chương trình dùng để thực hiện cùng một công việc lấy văn bản từ trang web [KrDict](https://krdict.korean.go.kr/m/vie) với hai phương thức khác nhau nhưng cùng lưu một cấu trúc.
- KrdictScraper sẽ lấy dữ liệu từ trang web của Từ điển học tiếng Hàn-tiếng Việt của Viện Quốc ngữ Quốc gia và lưu vào tệp text.
- Xml2text sẽ lấy dữ liệu từ file từ điển định dạng XML của Từ điển học tiếng Hàn-tiếng Việt của Viện Quốc ngữ Quốc gia và lưu vào tệp text.

## KrdictScraper

KrDictScraper là một công cụ tự động để lấy dữ liệu từ trang web [KrDict](https://krdict.korean.go.kr/m/vie) (Korea-Vietnam Dictionary) và lưu vào một tệp văn bản để sử dụng sau này. Công cụ này được viết bằng Python và sử dụng thư viện Selenium để tự động duyệt web.

### Thời gian phát triển
- Bắt đầu từ 22/05/2024
- Hoàn thiện vào 25/05/2024

### Cấu trúc lưu dữ liệu
Có thể xem dữ liệu mẫu ở đây: [data_sample](data_sample)

Ví dụ
- Từ một nghĩa: 가계=1 (家系) 「명사」 Danh từ [가계듣기/가게듣기]\ngia tộc, dòng dõi\n조상에서부터 후손으로 이어지는 한 집안.\nMột gia đình được tiếp nối từ tổ tiên tới con cháu hậu thế.
- Từ nhiều nghĩa: 가계=2 (家計) 「명사」 Danh từ [가계듣기/가게듣기]\n\t1. hộ kinh doanh\n경제 단위로서의 가정.\nGia đình với tư cách là đơn vị kinh tế.\n\t2. kinh tế gia đình\n한 집안의 경제를 이끌어 나가는 방법이나 형편.\nTình hình hay phương pháp đưa kinh tế của một gia đình đi lên.

Giải thích cách trình bày từ một nghĩa và từ nhiều nghĩa:
- [từ hàn]=[1][từ hán; từ loại; cách đọc][\n][phần giải nghĩa][\n][câu tiếng hàn ví dụ][\n][câu tiếng việt giải nghĩa câu ví dụ trên]
- [từ hàn]=[1][từ hán; từ loại; cách đọc][\n][\t][1. phần giải nghĩa thứ 1][\n][câu tiếng hàn ví dụ 1][\n][câu tiếng việt giải nghĩa câu ví dụ 1 trên][\n][\t][2. phần giải nghĩa thứ 2][\n][câu tiếng hàn ví dụ 2][\n][câu tiếng việt giải nghĩa câu ví dụ 2 trên]

- Chú thích
  - `[1]` thể hiện một từ chia làm từng phần giải nghĩa.
  - `[\n]` thể hiện xuống dòng.
  - `[\t]` thể hiện đánh số cho từng loại nghĩa.

### Cấu trúc lưu tiến trình

```
Trang [số trang], kết quả [kết quả đầu]~[kết quả cuối]
1. [từ hàn] [1 (số nếu có)]
2. [từ hàn]
3. [từ hàn] [3]
...
10. [từ hàn]
Trang [số trang], kết quả [kết quả đầu]~[kết quả cuối]
12. [từ hàn] [1]
13. [từ hàn]
14. [từ hàn] [3]
...
20. [từ hàn]
```

- Chú thích
  - `[số trang]` được bắt đầu bằng số `1 đến 1595`.
  - `[kết quả đầu]` được tính bằng `([số trang] - 1) * 10 + 1`.
  - `[kết quả cuối]` được tính bằng `[số trang] * 10`.

### Cài Đặt

#### Yêu Cầu

- Microsoft Edge `125.0.2535.51` hoặc mới hơn/Chrome `125.0.6422.78` hoặc mới hơn
- Webdriver Edge `125.0.2535.51` Win64 hoặc mới hơn/Chrome `125.0.6422.78` hoặc mới hơn
- Selenium `4.21.0` hoặc mới hơn
- Python `3.11` hoặc mới hơn

###### Bước 1: Cài Đặt Microsoft Edge hoặc Chrome và Webdriver

Đảm bảo bạn đã cài đặt Microsoft Edge phiên bản 125.0.2535.51 hoặc mới hơn. Sau đó, tải về và cài đặt Webdriver Edge phiên bản 125.0.2535.51 Win64 hoặc mới hơn từ trang web chính thức của Microsoft Edge Developer.

Nếu dùng Chrome, đảm bảo bạn đã cài đặt Chrome phiên bản 125.0.6422.78 hoặc mới hơn. Sau đó, tải về và cài đặt Webdriver Chrome phiên bản 125.0.6422.78 Win64 hoặc mới hơn từ trang web chính thức của Chrome for Testing.

###### Bước 2: Cài Đặt Selenium

Sử dụng pip để cài đặt thư viện Selenium:

```bash
pip install selenium==4.21.0
```

###### Bước 3: Tải Về Mã Nguồn

Tải về mã nguồn từ kho lưu trữ GitHub bằng cách sử dụng lệnh git clone hoặc tải dưới dạng tệp ZIP.

###### Bước 4: Chạy Mã

Chạy chương trình bằng cách chạy tệp `main.py`:

```bash
python krdict_scraper.py
```

Chạy tệp `main_chrome.py` nếu dùng Chrome:

```bash
python krdict_scraper_chrome.py
```

### Sử Dụng

Khi chạy, chương trình sẽ tự động lấy dữ liệu từ trang KrDict và lưu vào tệp văn bản theo định dạng đã được chỉ định trong mã nguồn.

## Xml2text

Chương trình này là một công cụ tự động để phân tích và biên soạn dữ liệu từ điển từ các tệp XML được cung cấp. Nó có khả năng trích xuất thông tin từ các tệp XML chứa dữ liệu từ điển và tự động tạo ra một tệp văn bản chứa thông tin từ điển được biên soạn.

### Cài đặt
1. Đảm bảo bạn đã cài đặt Python trên máy tính của mình.
2. Tải mã nguồn của chương trình từ [repository](link-to-repo).
3. Mở terminal/command prompt và di chuyển đến thư mục chứa mã nguồn của chương trình.
4. Chạy lệnh sau để cài đặt các thư viện cần thiết:
   ```
   pip install xml.etree.ElementTree
   ```
5. Chạy chương trình bằng lệnh sau:
   ```
   python xml2text.py
   ```

### Cấu trúc dữ liệu và Giải thích

#### Biến và Cấu trúc Dữ liệu

- `base_folder`: Đường dẫn tới thư mục gốc của dự án. Nó được lấy từ biến môi trường hoặc thư mục chứa tệp mã nguồn.
- `xml_folder`: Đường dẫn tới tệp XML chứa dữ liệu từ điển. Nó được xác định bằng cách kết hợp `base_folder` với thư mục chứa dữ liệu XML.
- `output_path`: Đường dẫn tới tệp văn bản đầu ra chứa thông tin từ điển được biên soạn. Nó được xác định bằng cách kết hợp `base_folder` với thư mục đầu ra.
- `pos_mapping`: Một từ điển ánh xạ từ loại từ tiếng Hàn sang tiếng Việt. Nó dùng để chuyển đổi các loại từ tiếng Hàn sang tiếng Việt trong kết quả đầu ra.
- `vocabulary_level_mapping`: Một từ điển ánh xạ từ cấp độ từ vựng tiếng Hàn sang các dấu sao. Nó dùng để đánh giá cấp độ từ vựng của các mục từ điển.

#### Ý nghĩa các biến

- `parse_lexical_entry`: Hàm này nhận một mục `LexicalEntry` từ tệp XML và phân tích thông tin từ điển từ nó.
- `tree`: Biến này đại diện cho cấu trúc cây của tệp XML.
- `root`: Nút gốc của cây XML, chứa toàn bộ dữ liệu từ điển.
- `entries_by_val`: Một từ điển dùng để lưu trữ các mục từ điển theo giá trị `val`. Mỗi khóa là một giá trị `val`, và mỗi giá trị là một danh sách các mục từ điển có cùng giá trị `val`.
- `f`: Tệp văn bản đầu ra được mở để ghi thông tin từ điển biên soạn.

#### Kết quả mẫu

Mỗi dòng trong tệp văn bản đầu ra biểu diễn một mục từ điển và thông tin của nó. Dưới đây là một cấu trúc mẫu của một dòng và ý nghĩa của các phần tử trong dòng:

```
[Loại từ] [Từ viết] [Từ viết in] [Số homonym] [Nguồn gốc] [Cấp độ từ vựng] Phát âm [Phát âm] Ứng dụng [Ứng dụng] Tham khảo toàn bộ [Tham khảo toàn bộ] ☞ [Từ liên quan] Từ phái sinh [Từ phái sinh] Từ loại [Loại từ] [Loại từ tiếng Việt] [Ngữ nghĩa] [Ngữ nghĩa tiếng Việt] * [Ví dụ] Đa truyền thông [Số lượng] [Nhãn]
```

- `[Loại từ]`: Loại từ của mục từ điển (ví dụ: Danh từ, Động từ).
- `[Từ viết]`: Từ viết của mục từ điển.
- `[Từ viết in]`: Từ viết in của mục từ điển.
- `[Số homonym]`: Số homonym của mục từ điển.
- `[Nguồn gốc]`: Nguồn gốc của mục từ điển.
- `[Cấp độ từ vựng]`: Cấp độ từ vựng của mục từ điển (được biểu diễn bằng dấu sao).
- `Phát âm [Phát âm]`: Phần phát âm của mục từ điển.
- `Ứng dụng [Ứng dụng]`: Các ứng dụng của mục từ điển.
- `Tham khảo toàn bộ [Tham khảo toàn bộ]`: Tham khảo toàn bộ của mục từ điển.
- `☞ [Từ liên quan]`: Danh sách các từ liên quan của mục từ điển.
- `Từ phái sinh [Từ phái sinh]`: Danh sách các từ phái sinh của mục từ điển.
- `Từ loại [Loại từ]`: Loại từ của mục từ điển (bổ sung từ loại tiếng Việt).
- `[Ngữ nghĩa]`: Ngữ nghĩa của mục từ điển.
- `[Ngữ nghĩa tiếng Việt`: Ngữ nghĩa tiếng Việt tương ứng với mục từ điển.
- `* [Ví dụ]`: Danh sách các ví dụ minh họa cho mục từ điển.
- `Đa truyền thông [Số lượng] [Nhãn]`: Thông tin về các tệp đa truyền thông liên quan đến mục từ điển.

#### Giải thích các thuộc tính

- `Loại từ`: Loại từ của mục từ điển, ví dụ: Danh từ, Động từ.
- `Từ viết`: Từ viết của mục từ điển.
- `Từ viết in`: Từ viết in của mục từ điển.
- `Số homonym`: Số homonym của mục từ điển.
- `Nguồn gốc`: Nguồn gốc của mục từ điển, nơi mà từ này có nguồn gốc.
- `Cấp độ từ vựng`: Cấp độ từ vựng của mục từ điển, được biểu diễn bằng số sao, với mỗi sao đại diện cho một cấp độ khác nhau.
- `Phát âm`: Phần phát âm của mục từ điển.
- `Ứng dụng`: Các ứng dụng của mục từ điển, ví dụ: các từ đồng nghĩa, từ trái nghĩa.
- `Tham khảo toàn bộ`: Tham khảo toàn bộ của mục từ điển, bao gồm thông tin bổ sung hoặc giải thích.
- `Từ liên quan`: Danh sách các từ liên quan của mục từ điển, ví dụ: từ tham khảo, từ phái sinh.
- `Từ phái sinh`: Danh sách các từ phái sinh của mục từ điển.
- `Từ loại`: Loại từ của mục từ điển dưới dạng tiếng Việt.
- `Ngữ nghĩa`: Ngữ nghĩa của mục từ điển.
- `Ngữ nghĩa tiếng Việt`: Ngữ nghĩa của mục từ điển dưới dạng tiếng Việt.
- `Ví dụ`: Các ví dụ minh họa cho mục từ điển.
- `Đa truyền thông`: Thông tin về các tệp đa truyền thông liên quan đến mục từ điển, bao gồm số lượng và nhãn của chúng.

Với cấu trúc dữ liệu và giải thích trên, chương trình giải thích tự động từ điển này cung cấp một cách tự động và dễ dàng để phân tích và biên soạn dữ liệu từ điển từ các tệp XML.

## Đóng Góp

Nếu bạn muốn đóng góp vào dự án, vui lòng mở một yêu cầu kéo trên GitHub và chúng tôi sẽ xem xét.

## Giấy Phép

Dự án được cấp phép dưới Giấy Phép GPL-3.0. Xem tệp [LICENSE](LICENSE) để biết chi tiết.
