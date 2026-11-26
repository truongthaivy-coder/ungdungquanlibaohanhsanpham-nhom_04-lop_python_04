
import json


# ==================================================
# 1. CLASS TAI KHOAN
# ==================================================

class TaiKhoan:
    def __init__(self, ma_tai_khoan, ten_dang_nhap, mat_khau, vai_tro):
        self.__ma_tai_khoan = ma_tai_khoan.strip()
        self.__ten_dang_nhap = ten_dang_nhap.strip()
        self.__mat_khau = mat_khau.strip()
        self.__vai_tro = vai_tro.strip()

    @property
    def ma_tai_khoan(self):
        return self.__ma_tai_khoan

    @property
    def ten_dang_nhap(self):
        return self.__ten_dang_nhap

    @property
    def mat_khau(self):
        return self.__mat_khau

    @property
    def vai_tro(self):
        return self.__vai_tro

    def cap_nhat(self, ten_dang_nhap, mat_khau, vai_tro):
        self.__ten_dang_nhap = ten_dang_nhap.strip()
        self.__mat_khau = mat_khau.strip()
        self.__vai_tro = vai_tro.strip()

    def to_dict(self):
        return {
            "ma_tai_khoan": self.__ma_tai_khoan,
            "ten_dang_nhap": self.__ten_dang_nhap,
            "mat_khau": self.__mat_khau,
            "vai_tro": self.__vai_tro
        }

    def __str__(self):
        return (
            "Ma tai khoan: " + self.__ma_tai_khoan +
            "\nTen dang nhap: " + self.__ten_dang_nhap +
            "\nVai tro: " + self.__vai_tro
        )


# ==================================================
# 2. CLASS LICH SU SUA CHUA
# ==================================================

class LichSuSuaChua:
    def __init__(self, ma_lich_su, ma_phieu_bao_hanh,
                 ngay_sua_chua, noi_dung, ket_qua):

        self.__ma_lich_su = ma_lich_su.strip()
        self.__ma_phieu_bao_hanh = ma_phieu_bao_hanh.strip()
        self.__ngay_sua_chua = ngay_sua_chua.strip()
        self.__noi_dung = noi_dung.strip()
        self.__ket_qua = ket_qua.strip()

    @property
    def ma_lich_su(self):
        return self.__ma_lich_su

    @property
    def ma_phieu_bao_hanh(self):
        return self.__ma_phieu_bao_hanh

    @property
    def ngay_sua_chua(self):
        return self.__ngay_sua_chua

    @property
    def noi_dung(self):
        return self.__noi_dung

    @property
    def ket_qua(self):
        return self.__ket_qua

    def cap_nhat(self, ma_phieu_bao_hanh,
                 ngay_sua_chua, noi_dung, ket_qua):

        self.__ma_phieu_bao_hanh = ma_phieu_bao_hanh.strip()
        self.__ngay_sua_chua = ngay_sua_chua.strip()
        self.__noi_dung = noi_dung.strip()
        self.__ket_qua = ket_qua.strip()

    def to_dict(self):
        return {
            "ma_lich_su": self.__ma_lich_su,
            "ma_phieu_bao_hanh": self.__ma_phieu_bao_hanh,
            "ngay_sua_chua": self.__ngay_sua_chua,
            "noi_dung": self.__noi_dung,
            "ket_qua": self.__ket_qua
        }

    def __str__(self):
        return (
            "Ma lich su: " + self.__ma_lich_su +
            "\nMa phieu bao hanh: " + self.__ma_phieu_bao_hanh +
            "\nNgay sua chua: " + self.__ngay_sua_chua +
            "\nNoi dung: " + self.__noi_dung +
            "\nKet qua: " + self.__ket_qua
        )


# ==================================================
# 3. CLASS QUAN LY TAI KHOAN
# ==================================================

class TaiKhoanService:
    def __init__(self, ten_file="tai_khoan.json"):
        self.__ten_file = ten_file
        self.__danh_sach = []
        self.doc_du_lieu()

    def tim_tai_khoan(self, ma_tai_khoan):
        ma_tai_khoan = ma_tai_khoan.strip()

        for tai_khoan in self.__danh_sach:
            if tai_khoan.ma_tai_khoan == ma_tai_khoan:
                return tai_khoan

        return None

    def them_tai_khoan(self, tai_khoan):
        if tai_khoan.ma_tai_khoan == "":
            print("Ma tai khoan khong duoc de trong!")
            return False

        if self.tim_tai_khoan(tai_khoan.ma_tai_khoan) is not None:
            print("Ma tai khoan da ton tai!")
            return False

        self.__danh_sach.append(tai_khoan)
        self.ghi_du_lieu()

        print("Them tai khoan thanh cong!")
        return True

    def cap_nhat_tai_khoan(self, ma_tai_khoan,
                           ten_dang_nhap, mat_khau, vai_tro):

        tai_khoan = self.tim_tai_khoan(ma_tai_khoan)

        if tai_khoan is None:
            print("Khong tim thay tai khoan!")
            return False

        if (ten_dang_nhap.strip() == "" or
                mat_khau.strip() == "" or
                vai_tro.strip() == ""):
            print("Thong tin khong duoc de trong!")
            return False

        tai_khoan.cap_nhat(ten_dang_nhap, mat_khau, vai_tro)
        self.ghi_du_lieu()

        print("Cap nhat tai khoan thanh cong!")
        return True

    def hien_thi_danh_sach(self):
        if len(self.__danh_sach) == 0:
            print("Danh sach tai khoan rong!")
            return

        for tai_khoan in self.__danh_sach:
            print(tai_khoan)
            print("------------------------")

    def ghi_du_lieu(self):
        danh_sach = []

        for tai_khoan in self.__danh_sach:
            danh_sach.append(tai_khoan.to_dict())

        with open(self.__ten_file, "w", encoding="utf-8") as file:
            json.dump(danh_sach, file, ensure_ascii=False, indent=4)

    def doc_du_lieu(self):
        try:
            with open(self.__ten_file, "r", encoding="utf-8") as file:
                danh_sach = json.load(file)

            if not isinstance(danh_sach, list):
                raise ValueError("Du lieu phai la mot danh sach!")

            danh_sach_moi = []

            for p in danh_sach:
                tai_khoan = TaiKhoan(
                    p["ma_tai_khoan"],
                    p["ten_dang_nhap"],
                    p["mat_khau"],
                    p["vai_tro"]
                )
                danh_sach_moi.append(tai_khoan)

            self.__danh_sach = danh_sach_moi

        except FileNotFoundError:
            self.__danh_sach = []

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as loi:
            print("Loi doc file tai khoan:", loi)


# ==================================================
# 4. CLASS QUAN LY LICH SU SUA CHUA
# ==================================================

class LichSuSuaChuaService:
    def __init__(self, ten_file="lich_su_sua_chua.json"):
        self.__ten_file = ten_file
        self.__danh_sach = []
        self.doc_du_lieu()

    def tim_lich_su(self, ma_lich_su):
        ma_lich_su = ma_lich_su.strip()

        for lich_su in self.__danh_sach:
            if lich_su.ma_lich_su == ma_lich_su:
                return lich_su

        return None

    def them_lich_su(self, lich_su):
        if lich_su.ma_lich_su == "":
            print("Ma lich su khong duoc de trong!")
            return False

        if self.tim_lich_su(lich_su.ma_lich_su) is not None:
            print("Ma lich su da ton tai!")
            return False

        self.__danh_sach.append(lich_su)
        self.ghi_du_lieu()

        print("Them lich su sua chua thanh cong!")
        return True

    def cap_nhat_lich_su(self, ma_lich_su,
                         ma_phieu_bao_hanh, ngay_sua_chua,
                         noi_dung, ket_qua):

        lich_su = self.tim_lich_su(ma_lich_su)

        if lich_su is None:
            print("Khong tim thay lich su sua chua!")
            return False

        if (ma_phieu_bao_hanh.strip() == "" or
                ngay_sua_chua.strip() == "" or
                noi_dung.strip() == "" or
                ket_qua.strip() == ""):
            print("Thong tin khong duoc de trong!")
            return False

        lich_su.cap_nhat(
            ma_phieu_bao_hanh,
            ngay_sua_chua,
            noi_dung,
            ket_qua
        )

        self.ghi_du_lieu()

        print("Cap nhat lich su sua chua thanh cong!")
        return True

    def hien_thi_danh_sach(self):
        if len(self.__danh_sach) == 0:
            print("Danh sach lich su sua chua rong!")
            return

        for lich_su in self.__danh_sach:
            print(lich_su)
            print("------------------------")

    def ghi_du_lieu(self):
        danh_sach = []

        for lich_su in self.__danh_sach:
            danh_sach.append(lich_su.to_dict())

        with open(self.__ten_file, "w", encoding="utf-8") as file:
            json.dump(danh_sach, file, ensure_ascii=False, indent=4)

    def doc_du_lieu(self):
        try:
            with open(self.__ten_file, "r", encoding="utf-8") as file:
                danh_sach = json.load(file)

            if not isinstance(danh_sach, list):
                raise ValueError("Du lieu phai la mot danh sach!")

            danh_sach_moi = []

            for p in danh_sach:
                lich_su = LichSuSuaChua(
                    p["ma_lich_su"],
                    p["ma_phieu_bao_hanh"],
                    p["ngay_sua_chua"],
                    p["noi_dung"],
                    p["ket_qua"]
                )
                danh_sach_moi.append(lich_su)

            self.__danh_sach = danh_sach_moi

        except FileNotFoundError:
            self.__danh_sach = []

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as loi:
            print("Loi doc file lich su sua chua:", loi)


# ==================================================
# 5. CAC HAM NHAP DU LIEU
# ==================================================

def tao_tai_khoan(service):
    print("\n--- TAO TAI KHOAN ---")

    ma = input("Nhap ma tai khoan: ").strip()
    ten = input("Nhap ten dang nhap: ").strip()
    mat_khau = input("Nhap mat khau: ").strip()
    vai_tro = input("Nhap vai tro: ").strip()

    if ma == "" or ten == "" or mat_khau == "" or vai_tro == "":
        print("Vui long nhap day du thong tin!")
        return

    tai_khoan = TaiKhoan(ma, ten, mat_khau, vai_tro)
    service.them_tai_khoan(tai_khoan)


def cap_nhat_tai_khoan(service):
    print("\n--- CAP NHAT TAI KHOAN ---")

    ma = input("Nhap ma tai khoan can cap nhat: ").strip()
    ten = input("Nhap ten dang nhap moi: ").strip()
    mat_khau = input("Nhap mat khau moi: ").strip()
    vai_tro = input("Nhap vai tro moi: ").strip()

    service.cap_nhat_tai_khoan(ma, ten, mat_khau, vai_tro)


def tao_lich_su(service):
    print("\n--- TAO LICH SU SUA CHUA ---")

    ma = input("Nhap ma lich su: ").strip()
    ma_phieu = input("Nhap ma phieu bao hanh: ").strip()
    ngay = input("Nhap ngay sua chua: ").strip()
    noi_dung = input("Nhap noi dung sua chua: ").strip()
    ket_qua = input("Nhap ket qua sua chua: ").strip()

    if (ma == "" or ma_phieu == "" or ngay == "" or
            noi_dung == "" or ket_qua == ""):
        print("Vui long nhap day du thong tin!")
        return

    lich_su = LichSuSuaChua(
        ma, ma_phieu, ngay, noi_dung, ket_qua
    )

    service.them_lich_su(lich_su)


def cap_nhat_lich_su(service):
    print("\n--- CAP NHAT LICH SU SUA CHUA ---")

    ma = input("Nhap ma lich su can cap nhat: ").strip()
    ma_phieu = input("Nhap ma phieu bao hanh moi: ").strip()
    ngay = input("Nhap ngay sua chua moi: ").strip()
    noi_dung = input("Nhap noi dung moi: ").strip()
    ket_qua = input("Nhap ket qua moi: ").strip()

    service.cap_nhat_lich_su(
        ma, ma_phieu, ngay, noi_dung, ket_qua
    )


# ==================================================
# 6. CHUONG TRINH CHINH
# ==================================================

def chuong_trinh_chinh():
    tai_khoan_service = TaiKhoanService()
    lich_su_service = LichSuSuaChuaService()

    while True:
        print("\n========== QUAN LY TV4 ==========")
        print("1. Tao tai khoan")
        print("2. Cap nhat tai khoan")
        print("3. Hien thi tai khoan")
        print("4. Tao lich su sua chua")
        print("5. Cap nhat lich su sua chua")
        print("6. Hien thi lich su sua chua")
        print("0. Thoat")

        lua_chon = input("Nhap lua chon: ").strip()

        try:
            if lua_chon == "1":
                tao_tai_khoan(tai_khoan_service)

            elif lua_chon == "2":
                cap_nhat_tai_khoan(tai_khoan_service)

            elif lua_chon == "3":
                tai_khoan_service.hien_thi_danh_sach()

            elif lua_chon == "4":
                tao_lich_su(lich_su_service)

            elif lua_chon == "5":
                cap_nhat_lich_su(lich_su_service)

            elif lua_chon == "6":
                lich_su_service.hien_thi_danh_sach()

            elif lua_chon == "0":
                print("Ket thuc chuong trinh!")
                break

            else:
                print("Lua chon khong hop le!")

        except Exception as loi:
            print("Co loi xay ra:", loi)


# Chay chuong trinh
chuong_trinh_chinh()
