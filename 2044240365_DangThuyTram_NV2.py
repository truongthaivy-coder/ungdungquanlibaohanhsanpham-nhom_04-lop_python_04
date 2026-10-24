import json
from pathlib import Path
from datetime import date, datetime
from calendar import monthrange


class PhieuBaoHanh:
    def __init__(self, ma_phieu, ma_khach_hang, ma_san_pham,
                 ngay_mua, thoi_han_thang):
        self.ma_phieu = ma_phieu
        self.ma_khach_hang = ma_khach_hang
        self.ma_san_pham = ma_san_pham
        self.ngay_mua = self.chuan_hoa_ngay(ngay_mua)
        self.thoi_han_thang = int(thoi_han_thang)

        if not ma_phieu or not ma_khach_hang or not ma_san_pham:
            raise ValueError("Mã phiếu, mã khách hàng và mã sản phẩm không được để trống.")

        if self.thoi_han_thang <= 0:
            raise ValueError("Thời hạn bảo hành phải lớn hơn 0 tháng.")

    @staticmethod
    def chuan_hoa_ngay(ngay):
        if isinstance(ngay, datetime):
            return ngay.date()
        if isinstance(ngay, date):
            return ngay
        return datetime.strptime(ngay, "%Y-%m-%d").date()

    @staticmethod
    def cong_thang(ngay, so_thang):
        tong_thang = ngay.month - 1 + so_thang
        nam = ngay.year + tong_thang // 12
        thang = tong_thang % 12 + 1
        ngay_cuoi = monthrange(nam, thang)[1]
        return date(nam, thang, min(ngay.day, ngay_cuoi))

    def ngay_het_han(self):
        return self.cong_thang(self.ngay_mua, self.thoi_han_thang)

    def kiem_tra_bao_hanh(self, ngay_kiem_tra=None):
        if ngay_kiem_tra is None:
            ngay_kiem_tra = date.today()
        else:
            ngay_kiem_tra = self.chuan_hoa_ngay(ngay_kiem_tra)

        return self.ngay_mua <= ngay_kiem_tra <= self.ngay_het_han()

    def trang_thai_bao_hanh(self, ngay_kiem_tra=None):
        if ngay_kiem_tra is None:
            ngay_kiem_tra = date.today()
        else:
            ngay_kiem_tra = self.chuan_hoa_ngay(ngay_kiem_tra)

        if ngay_kiem_tra < self.ngay_mua:
            return "Chưa đến thời gian bảo hành"

        if self.kiem_tra_bao_hanh(ngay_kiem_tra):
            return "Còn bảo hành"

        return "Hết hạn bảo hành"

    def to_dict(self):
        return {
            "ma_phieu": self.ma_phieu,
            "ma_khach_hang": self.ma_khach_hang,
            "ma_san_pham": self.ma_san_pham,
            "ngay_mua": self.ngay_mua.isoformat(),
            "thoi_han_thang": self.thoi_han_thang
        }

    @classmethod
    def from_dict(cls, du_lieu):
        return cls(
            du_lieu["ma_phieu"],
            du_lieu["ma_khach_hang"],
            du_lieu["ma_san_pham"],
            du_lieu["ngay_mua"],
            du_lieu["thoi_han_thang"]
        )

    def __str__(self):
        return (
            f"Mã phiếu: {self.ma_phieu} | "
            f"Mã khách hàng: {self.ma_khach_hang} | "
            f"Mã sản phẩm: {self.ma_san_pham} | "
            f"Ngày mua: {self.ngay_mua} | "
            f"Ngày hết hạn: {self.ngay_het_han()} | "
            f"Trạng thái: {self.trang_thai_bao_hanh()}"
        )


class BaoHanhService:
    def __init__(self, duong_dan="phieu_bao_hanh.json"):
        self.duong_dan = Path(duong_dan)
        self.danh_sach_phieu = []
        self.doc_du_lieu()

    def doc_du_lieu(self):
        if not self.duong_dan.exists():
            self.luu_du_lieu()
            return

        try:
            with open(self.duong_dan, "r", encoding="utf-8") as file:
                du_lieu = json.load(file)

            if not isinstance(du_lieu, list):
                raise ValueError("Dữ liệu JSON phải là một danh sách.")

            self.danh_sach_phieu = [
                PhieuBaoHanh.from_dict(item) for item in du_lieu
            ]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            raise ValueError(f"Lỗi đọc dữ liệu bảo hành: {e}") from e

    def luu_du_lieu(self):
        with open(self.duong_dan, "w", encoding="utf-8") as file:
            json.dump(
                [phieu.to_dict() for phieu in self.danh_sach_phieu],
                file,
                ensure_ascii=False,
                indent=4
            )

    def them_phieu(self, phieu):
        if not isinstance(phieu, PhieuBaoHanh):
            raise TypeError("Dữ liệu phải là phiếu bảo hành.")

        if self.tim_phieu(phieu.ma_phieu):
            raise ValueError("Mã phiếu bảo hành đã tồn tại.")

        self.danh_sach_phieu.append(phieu)
        self.luu_du_lieu()
        return True

    def hien_thi_danh_sach(self):
        return self.danh_sach_phieu.copy()

    def tim_phieu(self, ma_phieu):
        for phieu in self.danh_sach_phieu:
            if phieu.ma_phieu == ma_phieu:
                return phieu
        return None

    def cap_nhat_phieu(self, ma_phieu, **du_lieu_moi):
        phieu = self.tim_phieu(ma_phieu)

        if phieu is None:
            return False

        du_lieu = phieu.to_dict()
        truong_hop_le = {
            "ma_khach_hang",
            "ma_san_pham",
            "ngay_mua",
            "thoi_han_thang"
        }

        if not set(du_lieu_moi).issubset(truong_hop_le):
            raise ValueError("Thuộc tính cập nhật không hợp lệ.")

        du_lieu.update(du_lieu_moi)
        phieu_moi = PhieuBaoHanh.from_dict(du_lieu)
        vi_tri = self.danh_sach_phieu.index(phieu)
        self.danh_sach_phieu[vi_tri] = phieu_moi
        self.luu_du_lieu()
        return True

    def xoa_phieu(self, ma_phieu):
        phieu = self.tim_phieu(ma_phieu)

        if phieu is None:
            return False

        self.danh_sach_phieu.remove(phieu)
        self.luu_du_lieu()
        return True

    def kiem_tra_thoi_han(self, ma_phieu, ngay_kiem_tra=None):
        phieu = self.tim_phieu(ma_phieu)

        if phieu is None:
            return None

        return {
            "ma_phieu": phieu.ma_phieu,
            "ngay_het_han": phieu.ngay_het_han().isoformat(),
            "trang_thai": phieu.trang_thai_bao_hanh(ngay_kiem_tra)
        }


if __name__ == "__main__":
    service = BaoHanhService()

    phieu = PhieuBaoHanh(
        "BH001",
        "KH001",
        "SP001",
        "2026-10-01",
        12
    )

    try:
        service.them_phieu(phieu)
        print("Thêm phiếu bảo hành thành công.")
    except ValueError as e:
        print(e)

    print("\nDANH SÁCH PHIẾU BẢO HÀNH")
    for item in service.hien_thi_danh_sach():
        print(item)

    print("\nKIỂM TRA THỜI HẠN")
    ket_qua = service.kiem_tra_thoi_han("BH001")

    if ket_qua:
        print("Mã phiếu:", ket_qua["ma_phieu"])
        print("Ngày hết hạn:", ket_qua["ngay_het_han"])
        print("Trạng thái:", ket_qua["trang_thai"])
    else:
        print("Không tìm thấy phiếu bảo hành.")