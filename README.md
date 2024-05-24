### KrDictScraper

KrDictScraper là một công cụ tự động để lấy dữ liệu từ trang web [KrDict](https://krdict.korean.go.kr/m/vie) (Korea-Vietnam Dictionary) và lưu vào một tệp văn bản để sử dụng sau này. Công cụ này được viết bằng Python và sử dụng thư viện Selenium để tự động duyệt web.

### Cài Đặt

#### Yêu Cầu

- Microsoft Edge Version 125.0.2535.51 hoặc mới hơn
- Webdriver Edge Version 125.0.2535.51 hoặc mới hơn
- Selenium 4.21.0 hoặc mới hơn
- Python 3.11 hoặc mới hơn

#### Bước 1: Cài Đặt Microsoft Edge và Webdriver

Đảm bảo bạn đã cài đặt Microsoft Edge phiên bản 125.0.2535.51 hoặc mới hơn. Sau đó, tải về và cài đặt Webdriver Edge phiên bản 125.0.2535.51 hoặc mới hơn từ trang web chính thức của Microsoft Edge Developer.

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

### Sử Dụng

Khi chạy, chương trình sẽ tự động lấy dữ liệu từ trang KrDict và lưu vào tệp văn bản theo định dạng đã được chỉ định trong mã nguồn.

### Đóng Góp

Nếu bạn muốn đóng góp vào dự án, vui lòng mở một yêu cầu kéo trên GitHub và chúng tôi sẽ xem xét.

### Giấy Phép

Dự án được cấp phép dưới Giấy Phép GPL-3.0. Xem tệp [LICENSE](LICENSE) để biết chi tiết.
