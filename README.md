# KrDictScraper

KrDictScraper là một công cụ tự động để lấy dữ liệu từ trang web [KrDict](https://krdict.korean.go.kr/m/vie) (Korea-Vietnam Dictionary) và lưu vào một tệp văn bản để sử dụng sau này. Công cụ này được viết bằng Python và sử dụng thư viện Selenium để tự động duyệt web.

## Thời gian phát triển
- Bắt đầu từ 22/05/2024
- Hoàn thiện vào 25/05/2024

## Cấu trúc lưu dữ liệu
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

## Cấu trúc lưu tiến trình

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

## Cài Đặt

### Yêu Cầu

- Microsoft Edge Version 125.0.2535.51 hoặc mới hơn
- Webdriver Edge Version 125.0.2535.51 Win64 hoặc mới hơn
- Selenium 4.21.0 hoặc mới hơn
- Python 3.11 hoặc mới hơn

#### Bước 1: Cài Đặt Microsoft Edge hoặc Chrome và Webdriver

Đảm bảo bạn đã cài đặt Microsoft Edge phiên bản 125.0.2535.51 hoặc mới hơn. Sau đó, tải về và cài đặt Webdriver Edge phiên bản 125.0.2535.51 Win64 hoặc mới hơn từ trang web chính thức của Microsoft Edge Developer.

Nếu dùng Chrome, đảm bảo bạn đã cài đặt Chrome phiên bản 125.0.6422.78 hoặc mới hơn. Sau đó, tải về và cài đặt Webdriver Chrome phiên bản 125.0.6422.78 Win64 hoặc mới hơn từ trang web chính thức của Chrome for Testing.

#### Bước 2: Cài Đặt Selenium

Sử dụng pip để cài đặt thư viện Selenium:

```bash
pip install selenium==4.21.0
```

#### Bước 3: Tải Về Mã Nguồn

Tải về mã nguồn từ kho lưu trữ GitHub bằng cách sử dụng lệnh git clone hoặc tải dưới dạng tệp ZIP.

#### Bước 4: Chạy Mã

Chạy chương trình bằng cách chạy tệp `main.py`:

```bash
python main.py
```

Chạy tệp `main_chrome.py` nếu dùng Chrome:

```bash
python main_chrome.py
```

## Sử Dụng

Khi chạy, chương trình sẽ tự động lấy dữ liệu từ trang KrDict và lưu vào tệp văn bản theo định dạng đã được chỉ định trong mã nguồn.

## Đóng Góp

Nếu bạn muốn đóng góp vào dự án, vui lòng mở một yêu cầu kéo trên GitHub và chúng tôi sẽ xem xét.

## Giấy Phép

Dự án được cấp phép dưới Giấy Phép GPL-3.0. Xem tệp [LICENSE](LICENSE) để biết chi tiết.
