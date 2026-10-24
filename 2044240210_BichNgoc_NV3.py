from abc import ABC, abstractmethod


# Lớp trừu tượng quản lý sửa chữa
class SuaChua(ABC):
    @abstractmethod
    def cap_nhat_tien_do(self, trang_thai):
        pass


# Lớp quản lý kỹ thuật viên
class KyThuatVien:
    def __init__(self, ma_ktv, ho_ten, so_dien_thoai, chuyen_mon):
        self.ma_ktv = ma_ktv
        self.ho_ten = ho_ten
        self.so_dien_thoai = so_dien_thoai
        self.chuyen_mon = chuyen_mon
        self.trang_thai = "Rảnh"

    def hien_thi_thong_tin(self):
        print("Mã kỹ thuật viên:", self.ma_ktv)
        print("Họ tên:", self.ho_ten)
        print("Số điện thoại:", self.so_dien_thoai)
        print("Chuyên môn:", self.chuyen_mon)
        print("Trạng thái:", self.trang_thai)

    def cap_nhat_thong_tin(self, ho_ten, so_dien_thoai, chuyen_mon):
        self.ho_ten = ho_ten
        self.so_dien_thoai = so_dien_thoai
        self.chuyen_mon = chuyen_mon

    def nhan_sua_chua(self):
        self.trang_thai = "Đang sửa chữa"

    def hoan_thanh_cong_viec(self):
        self.trang_thai = "Rảnh"


# Lớp quản lý sửa chữa kế thừa lớp trừu tượng
class SuaChuaService(SuaChua):
    def __init__(self, ma_sua_chua, ma_phieu_bao_hanh,
                 ten_san_pham, mo_ta_loi, ky_thuat_vien):
        self.ma_sua_chua = ma_sua_chua
        self.ma_phieu_bao_hanh = ma_phieu_bao_hanh
        self.ten_san_pham = ten_san_pham
        self.mo_ta_loi = mo_ta_loi
        self.ky_thuat_vien = ky_thuat_vien
        self.trang_thai = "Chờ sửa chữa"
        self.chi_phi = 0

    def hien_thi_thong_tin(self):
        print("Mã sửa chữa:", self.ma_sua_chua)
        print("Mã phiếu bảo hành:", self.ma_phieu_bao_hanh)
        print("Tên sản phẩm:", self.ten_san_pham)
        print("Mô tả lỗi:", self.mo_ta_loi)
        print("Kỹ thuật viên:", self.ky_thuat_vien.ho_ten)
        print("Trạng thái:", self.trang_thai)
        print("Chi phí sửa chữa:", self.chi_phi, "VNĐ")

    def cap_nhat_loi(self, mo_ta_loi):
        self.mo_ta_loi = mo_ta_loi

    def bat_dau_sua_chua(self):
        self.trang_thai = "Đang sửa chữa"
        self.ky_thuat_vien.nhan_sua_chua()

    def cap_nhat_tien_do(self, trang_thai):
        if trang_thai in ["Chờ sửa chữa", "Đang sửa chữa",
                          "Hoàn thành"]:
            self.trang_thai = trang_thai

            if trang_thai == "Đang sửa chữa":
                self.ky_thuat_vien.nhan_sua_chua()
            else:
                self.ky_thuat_vien.hoan_thanh_cong_viec()
        else:
            print("Trạng thái không hợp lệ!")

    def cap_nhat_chi_phi(self, chi_phi):
        if chi_phi >= 0:
            self.chi_phi = chi_phi
        else:
            print("Chi phí không hợp lệ!")

    def hoan_thanh_sua_chua(self):
        self.cap_nhat_tien_do("Hoàn thành")


# Kiểm tra chương trình
ktv1 = KyThuatVien(
    "KTV01",
    "Nguyễn Văn A",
    "0901234567",
    "Điện tử"
)

sc1 = SuaChuaService(
    "SC01",
    "BH01",
    "Laptop Dell",
    "Máy không lên nguồn",
    ktv1
)

sc1.bat_dau_sua_chua()
sc1.cap_nhat_chi_phi(250000)
sc1.hoan_thanh_sua_chua()

print("===== THÔNG TIN KỸ THUẬT VIÊN =====")
ktv1.hien_thi_thong_tin()

print("\n===== THÔNG TIN SỬA CHỮA =====")
sc1.hien_thi_thong_tin()

