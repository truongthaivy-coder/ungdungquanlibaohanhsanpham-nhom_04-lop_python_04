from abc import ABC, abstractmethod
from datetime import date
import calendar


class BaoHanh(ABC):
    @abstractmethod
    def kiem_tra_bao_hanh(self):
        pass


class PhieuBaoHanh(BaoHanh):
    def __init__(self, ma_phieu, ma_san_pham, ngay_mua, thoi_han):
        self.__ma_phieu = ma_phieu
        self.__ma_san_pham = ma_san_pham
        self.__ngay_mua = date.fromisoformat(ngay_mua)
        self.__thoi_han = int(thoi_han)

    @property
    def ma_phieu(self):
        return self.__ma_phieu

    @property
    def ma_san_pham(self):
        return self.__ma_san_pham

    def ngay_het_han(self):
        tong_thang = self.__ngay_mua.month - 1 + self.__thoi_han
        nam = self.__ngay_mua.year + tong_thang // 12
        thang = tong_thang % 12 + 1
        ngay = min(
            self.__ngay_mua.day,
            calendar.monthrange(nam, thang)[1]
        )
        return date(nam, thang, ngay)

    def kiem_tra_bao_hanh(self):
        if date.today() <= self.ngay_het_han():
            return "Còn bảo hành"
        return "Hết hạn bảo hành"

    def __str__(self):
        return (
            f"Mã phiếu: {self.__ma_phieu} | "
            f"Mã sản phẩm: {self.__ma_san_pham} | "
            f"Ngày hết hạn: {self.ngay_het_han()} | "
            f"{self.kiem_tra_bao_hanh()}"
        )


class PhieuBaoHanhMoRong(PhieuBaoHanh):
    def ngay_het_han(self):
        ngay_goc = super().ngay_het_han()
        tong_thang = ngay_goc.month - 1 + 3
        nam = ngay_goc.year + tong_thang // 12
        thang = tong_thang % 12 + 1
        ngay = min(ngay_goc.day, calendar.monthrange(nam, thang)[1])
        return date(nam, thang, ngay)

    def kiem_tra_bao_hanh(self):
        if date.today() <= self.ngay_het_han():
            return "Còn bảo hành mở rộng"
        return "Hết hạn bảo hành mở rộng"


class BaoHanhService:
    def __init__(self):
        self.__danh_sach = []

    def them_phieu(self, phieu):
        for p in self.__danh_sach:
            if p.ma_phieu == phieu.ma_phieu:
                print("Mã phiếu đã tồn tại.")
                return

        self.__danh_sach.append(phieu)
        print("Thêm phiếu thành công.")

    def hien_thi(self):
        for phieu in self.__danh_sach:
            print(phieu)

    def tim_phieu(self, ma_phieu):
        for phieu in self.__danh_sach:
            if phieu.ma_phieu == ma_phieu:
                return phieu
        return None


if __name__ == "__main__":
    service = BaoHanhService()

    phieu1 = PhieuBaoHanh("BH001", "SP001", "2026-01-01", 12)
    phieu2 = PhieuBaoHanhMoRong("BH002", "SP002", "2026-01-01", 12)

    service.them_phieu(phieu1)
    service.them_phieu(phieu2)

    print("\nDanh sách phiếu bảo hành:")
    service.hien_thi()

    print("\nTìm phiếu BH001:")
    ket_qua = service.tim_phieu("BH001")

    if ket_qua:
        print(ket_qua)
    else:
        print("Không tìm thấy phiếu.")