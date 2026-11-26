# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 17:30:46 2026

@author: ADMIN
"""

# -*- coding: utf-8 -*-
# =================================================================
# PHẦN 1. KHAI BÁO THƯ VIỆN
# =================================================================
# ABC và abstractmethod hỗ trợ xây dựng lớp trừu tượng.
from abc import ABC, abstractmethod
# Thư viện json dùng để đọc và ghi dữ liệu dạng JSON.
import json
# Path hỗ trợ thao tác với đường dẫn và thư mục.
from pathlib import Path


# =================================================================
# PHẦN 2. LỚP TRỪU TƯỢNG QuanLy (mục 2.2)
# =================================================================
class QuanLy(ABC):
    # Các lớp con phải triển khai phương thức hiển thị thông tin.
    @abstractmethod
    # Trả về chuỗi thông tin của đối tượng (triển khai phương thức của lớp cha).
    def hien_thi_thong_tin(self):
        pass


# =================================================================
# PHẦN 3. LỚP KhachHang (mục 2.2)
# =================================================================
class KhachHang(QuanLy):
    # Khởi tạo khách hàng; thuộc tính có hai dấu gạch dưới thể hiện đóng gói.
    def __init__(self, ma_kh, ten_kh, so_dien_thoai):
        self.__ma_kh = ma_kh.strip()
        if not self.__ma_kh:
            raise ValueError("Mã khách hàng không được để trống.")
        self.cap_nhat(ten_kh, so_dien_thoai)

    # Cho phép đọc mã định danh mà không cung cấp setter thay đổi mã.
    @property
    def ma_kh(self):
        return self.__ma_kh

    # Kiểm tra tên và số điện thoại trước khi cập nhật; giữ nguyên mã khách hàng.
    def cap_nhat(self, ten_kh, so_dien_thoai):
        ten_kh = ten_kh.strip()
        so_dien_thoai = so_dien_thoai.strip()
        if not ten_kh or not so_dien_thoai:
            raise ValueError("Tên và số điện thoại không được để trống.")
        self.__ten_kh = ten_kh
        self.__so_dien_thoai = so_dien_thoai

    # Chuyển đối tượng thành từ điển để thư viện json có thể lưu trữ.
    def to_dict(self):
        return {
            "ma_kh": self.__ma_kh,
            "ten_kh": self.__ten_kh,
            "so_dien_thoai": self.__so_dien_thoai
        }

    # Trả về chuỗi thông tin của đối tượng (triển khai phương thức của lớp cha).
    def hien_thi_thong_tin(self):
        return (f"Mã khách hàng: {self.__ma_kh} | "
                f"Tên: {self.__ten_kh} | "
                f"SĐT: {self.__so_dien_thoai}")

    # Quy định nội dung hiển thị khi gọi print(đối tượng).
    def __str__(self):
        return self.hien_thi_thong_tin()


# =================================================================
# PHẦN 4. LỚP SanPham (mục 2.2)
# =================================================================
class SanPham(QuanLy):
    # Khởi tạo sản phẩm; chuẩn hóa mã và kiểm tra dữ liệu bắt buộc.
    def __init__(self, ma_sp, ten_sp, hang_san_xuat):
        self.__ma_sp = ma_sp.strip()
        if not self.__ma_sp:
            raise ValueError("Mã sản phẩm không được để trống.")
        self.cap_nhat(ten_sp, hang_san_xuat)

    # Cho phép đọc mã định danh mà không cung cấp setter thay đổi mã.
    @property
    def ma_sp(self):
        return self.__ma_sp

    # Kiểm tra tên và hãng trước khi cập nhật; giữ nguyên mã sản phẩm.
    def cap_nhat(self, ten_sp, hang_san_xuat):
        ten_sp = ten_sp.strip()
        hang_san_xuat = hang_san_xuat.strip()
        if not ten_sp or not hang_san_xuat:
            raise ValueError("Tên sản phẩm và hãng không được để trống.")
        self.__ten_sp = ten_sp
        self.__hang_san_xuat = hang_san_xuat

    # Chuyển đối tượng thành từ điển để thư viện json có thể lưu trữ.
    def to_dict(self):
        return {
            "ma_sp": self.__ma_sp,
            "ten_sp": self.__ten_sp,
            "hang_san_xuat": self.__hang_san_xuat
        }

    # Trả về chuỗi thông tin của đối tượng (triển khai phương thức của lớp cha).
    def hien_thi_thong_tin(self):
        return (f"Mã sản phẩm: {self.__ma_sp} | "
                f"Tên: {self.__ten_sp} | "
                f"Hãng sản xuất: {self.__hang_san_xuat}")

    # Quy định nội dung hiển thị khi gọi print(đối tượng).
    def __str__(self):
        return self.hien_thi_thong_tin()


# =================================================================
# PHẦN 5. LỚP XỬ LÝ NGHIỆP VỤ QuanLyService
# =================================================================
class QuanLyService:
    # 5.1. Khởi tạo danh sách và cấu trúc lưu trữ (mục 2.4.1).
    def __init__(self, thu_muc=None):
        self.__danh_sach_khach_hang = []
        self.__danh_sach_san_pham = []
        # Mặc định lưu trong thư mục data nằm cạnh file Python.
        self.__thu_muc = (Path(thu_muc) if thu_muc is not None
                          else Path(__file__).resolve().parent / "data")
        # Tạo thư mục nếu chưa tồn tại.
        self.__thu_muc.mkdir(parents=True, exist_ok=True)
        self.__file_kh = self.__thu_muc / "khach_hang.json"
        self.__file_sp = self.__thu_muc / "san_pham.json"
        # Khôi phục dữ liệu đã lưu ngay khi khởi tạo service.
        self.doc_du_lieu()

    # =================================================================
    # 5.2. Tìm kiếm đối tượng theo mã
    # =================================================================
    # Duyệt danh sách, trả về khách hàng khớp mã hoặc None nếu không tìm thấy.
    def tim_khach_hang(self, ma_kh):
        for kh in self.__danh_sach_khach_hang:
            if kh.ma_kh == ma_kh.strip():
                return kh
        return None

    # Duyệt danh sách, trả về sản phẩm khớp mã hoặc None nếu không tìm thấy.
    def tim_san_pham(self, ma_sp):
        for sp in self.__danh_sach_san_pham:
            if sp.ma_sp == ma_sp.strip():
                return sp
        return None

    # =================================================================
    # 5.3. Tạo mới khách hàng và sản phẩm (mục 2.3.1)
    # =================================================================
    def them_khach_hang(self, khach_hang):
        # Kiểm tra mã trùng trước khi thêm khách hàng.
        if self.tim_khach_hang(khach_hang.ma_kh) is not None:
            print("Mã khách hàng đã tồn tại.")
            return
        # Thêm đối tượng vào danh sách trong bộ nhớ.
        self.__danh_sach_khach_hang.append(khach_hang)
        # Ghi lại dữ liệu sau khi thay đổi danh sách hoặc thông tin đối tượng.
        self.ghi_du_lieu()
        print("Thêm khách hàng thành công.")

    def them_san_pham(self, san_pham):
        # Kiểm tra mã trùng trước khi thêm sản phẩm.
        if self.tim_san_pham(san_pham.ma_sp) is not None:
            print("Mã sản phẩm đã tồn tại.")
            return
        # Thêm đối tượng vào danh sách trong bộ nhớ.
        self.__danh_sach_san_pham.append(san_pham)
        # Ghi lại dữ liệu sau khi thay đổi danh sách hoặc thông tin đối tượng.
        self.ghi_du_lieu()
        print("Thêm sản phẩm thành công.")

    # =================================================================
    # 5.4. Cập nhật khách hàng và sản phẩm (mục 2.3.2)
    # =================================================================
    def cap_nhat_khach_hang(self, ma_kh, ten_kh, so_dien_thoai):
        # Tìm khách hàng cần cập nhật theo mã định danh.
        kh = self.tim_khach_hang(ma_kh)
        if kh is None:
            print("Không tìm thấy khách hàng.")
            return
        # Gọi phương thức của đối tượng để cập nhật trực tiếp thông tin.
        kh.cap_nhat(ten_kh, so_dien_thoai)
        # Ghi lại dữ liệu sau khi thay đổi danh sách hoặc thông tin đối tượng.
        self.ghi_du_lieu()
        print("Cập nhật khách hàng thành công.")

    def cap_nhat_san_pham(self, ma_sp, ten_sp, hang_san_xuat):
        # Tìm sản phẩm cần cập nhật theo mã định danh.
        sp = self.tim_san_pham(ma_sp)
        if sp is None:
            print("Không tìm thấy sản phẩm.")
            return
        # Gọi phương thức của đối tượng để cập nhật trực tiếp thông tin.
        sp.cap_nhat(ten_sp, hang_san_xuat)
        # Ghi lại dữ liệu sau khi thay đổi danh sách hoặc thông tin đối tượng.
        self.ghi_du_lieu()
        print("Cập nhật sản phẩm thành công.")

    # =================================================================
    # 5.5. Hiển thị danh sách
    # =================================================================
    # Thông báo nếu danh sách trống; nếu có dữ liệu thì in từng khách hàng.
    def hien_thi_khach_hang(self):
        if not self.__danh_sach_khach_hang:
            print("Danh sách khách hàng trống.")
        for kh in self.__danh_sach_khach_hang:
            print(kh)

    # Thông báo nếu danh sách trống; nếu có dữ liệu thì in từng sản phẩm.
    def hien_thi_san_pham(self):
        if not self.__danh_sach_san_pham:
            print("Danh sách sản phẩm trống.")
        for sp in self.__danh_sach_san_pham:
            print(sp)

    # =================================================================
    # 5.6. Ghi dữ liệu JSON (mục 2.4.2)
    # =================================================================
    # Chế độ w ghi lại toàn bộ nội dung; UTF-8 và ensure_ascii=False giữ tiếng Việt, indent=4 giúp dễ đọc.
    def ghi_du_lieu(self):
        with self.__file_kh.open("w", encoding="utf-8") as f:
            json.dump([kh.to_dict() for kh in self.__danh_sach_khach_hang],
                      f, ensure_ascii=False, indent=4)
        with self.__file_sp.open("w", encoding="utf-8") as f:
            json.dump([sp.to_dict() for sp in self.__danh_sach_san_pham],
                      f, ensure_ascii=False, indent=4)

    # =================================================================
    # 5.7. Đọc và kiểm tra dữ liệu JSON (mục 2.4.2)
    # =================================================================
    @staticmethod
    # Hàm dùng chung để đọc một file và tạo lại danh sách đối tượng.
    def _doc_file(duong_dan, lop, khoa_ma):
        # Nếu chưa có file, trả về danh sách rỗng.
        if not duong_dan.exists():
            return []
        with duong_dan.open("r", encoding="utf-8") as f:
            du_lieu = json.load(f)
        # Kiểm tra cấu trúc ngoài cùng của JSON phải là danh sách.
        if not isinstance(du_lieu, list):
            raise ValueError("Cấu trúc JSON phải là danh sách.")
        danh_sach = []
        # Tập hợp các mã đã đọc, dùng để phát hiện mã trùng trong file.
        ma_da_co = set()
        for item in du_lieu:
            if not isinstance(item, dict) or not all(
                    isinstance(v, str) for v in item.values()):
                raise ValueError("Bản ghi JSON không hợp lệ.")
            # Giải nén từ điển thành đối số để khởi tạo đúng lớp.
            doi_tuong = lop(**item)
            ma = getattr(doi_tuong, khoa_ma)
            if ma in ma_da_co:
                raise ValueError("Dữ liệu có mã bị trùng.")
            ma_da_co.add(ma)
            danh_sach.append(doi_tuong)
        return danh_sach

    # Đọc cả hai file vào danh sách tạm trước khi thay thế dữ liệu hiện tại.
    def doc_du_lieu(self):
        # Chỉ thay danh sách khi cả hai file được đọc thành công.
        ds_kh = self._doc_file(self.__file_kh, KhachHang, "ma_kh")
        ds_sp = self._doc_file(self.__file_sp, SanPham, "ma_sp")
        self.__danh_sach_khach_hang = ds_kh
        self.__danh_sach_san_pham = ds_sp


# =================================================================
# PHẦN 6. MENU CHỨC NĂNG
# =================================================================
def menu():
    print("\n===== QUẢN LÝ KHÁCH HÀNG VÀ SẢN PHẨM =====")
    print("1. Thêm khách hàng")
    print("2. Thêm sản phẩm")
    print("3. Cập nhật khách hàng")
    print("4. Cập nhật sản phẩm")
    print("5. Hiển thị danh sách khách hàng")
    print("6. Hiển thị danh sách sản phẩm")
    print("7. Tìm kiếm khách hàng")
    print("8. Tìm kiếm sản phẩm")
    print("9. Lưu dữ liệu và thoát")


# =================================================================
# PHẦN 7. CHƯƠNG TRÌNH CHÍNH
# =================================================================
def main():
    try:
        service = QuanLyService()
    # Dừng nếu không thể khôi phục dữ liệu, tránh ghi đè file cũ.
    except (OSError, ValueError, TypeError) as err:
        print(f"Không thể đọc dữ liệu: {err}")
        print("Dừng chương trình để tránh ghi đè dữ liệu cũ.")
        return

    # Lặp menu cho đến khi người dùng chọn lưu và thoát.
    while True:
        menu()
        chon = input("Nhập lựa chọn: ").strip()
        try:
            # Tạo mới khách hàng từ dữ liệu nhập bàn phím (mục 2.3.1).
            if chon == "1":
                ma = input("Nhập mã khách hàng: ")
                ten = input("Nhập tên khách hàng: ")
                sdt = input("Nhập số điện thoại: ")
                service.them_khach_hang(KhachHang(ma, ten, sdt))
            # Tạo mới sản phẩm từ dữ liệu nhập bàn phím (mục 2.3.1).
            elif chon == "2":
                ma = input("Nhập mã sản phẩm: ")
                ten = input("Nhập tên sản phẩm: ")
                hang = input("Nhập hãng sản xuất: ")
                service.them_san_pham(SanPham(ma, ten, hang))
            # Cập nhật khách hàng theo mã (mục 2.3.2).
            elif chon == "3":
                ma = input("Nhập mã khách hàng cần cập nhật: ")
                ten = input("Nhập tên mới: ")
                sdt = input("Nhập số điện thoại mới: ")
                service.cap_nhat_khach_hang(ma, ten, sdt)
            # Cập nhật sản phẩm theo mã (mục 2.3.2).
            elif chon == "4":
                ma = input("Nhập mã sản phẩm cần cập nhật: ")
                ten = input("Nhập tên sản phẩm mới: ")
                hang = input("Nhập hãng sản xuất mới: ")
                service.cap_nhat_san_pham(ma, ten, hang)
            # Hiển thị toàn bộ khách hàng.
            elif chon == "5":
                service.hien_thi_khach_hang()
            # Hiển thị toàn bộ sản phẩm.
            elif chon == "6":
                service.hien_thi_san_pham()
            # Tìm kiếm và hiển thị một khách hàng.
            elif chon == "7":
                kh = service.tim_khach_hang(input("Nhập mã khách hàng: "))
                print(kh if kh is not None else "Không tìm thấy khách hàng.")
            # Tìm kiếm và hiển thị một sản phẩm.
            elif chon == "8":
                sp = service.tim_san_pham(input("Nhập mã sản phẩm: "))
                print(sp if sp is not None else "Không tìm thấy sản phẩm.")
            # Ghi dữ liệu lần cuối và thoát vòng lặp bằng break.
            elif chon == "9":
                service.ghi_du_lieu()
                print("Đã lưu dữ liệu. Kết thúc chương trình.")
                break
            else:
                print("Lựa chọn không hợp lệ.")
        # Thông báo lỗi dữ liệu nhập và tiếp tục menu.
        except ValueError as err:
            print(f"Dữ liệu không hợp lệ: {err}")
        # Thông báo lỗi thao tác với file; dữ liệu có thể chưa được lưu đầy đủ.
        except OSError as err:
            print(f"Lỗi lưu dữ liệu: {err}")
            print("Thay đổi trong bộ nhớ có thể chưa được lưu đầy đủ.")


# =================================================================
# PHẦN 8. ĐIỂM BẮT ĐẦU CHƯƠNG TRÌNH
# =================================================================
# Chỉ gọi main khi chạy trực tiếp file, không gọi khi import vào module khác.
if __name__ == "__main__":
    main()
