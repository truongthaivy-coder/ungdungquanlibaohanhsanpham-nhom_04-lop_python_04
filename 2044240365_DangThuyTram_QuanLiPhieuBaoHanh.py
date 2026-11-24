# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:49:37 2026

@author: ADMIN
"""


from abc import ABC, abstractmethod
from datetime import date
import calendar
import json
import os


# 1. Lop truu tuong BaoHanh
class BaoHanh(ABC):

    @abstractmethod
    def kiem_tra_bao_hanh(self):
        pass


# 2. Lop PhieuBaoHanh
class PhieuBaoHanh(BaoHanh):

    def __init__(self, ma_phieu, ma_san_pham, ngay_mua, thoi_han):
        self.__ma_phieu = ma_phieu.strip()
        self.__ma_san_pham = ma_san_pham.strip()
        self.__ngay_mua = date.fromisoformat(ngay_mua.strip())
        self.__thoi_han = self._kiem_tra_thoi_han(thoi_han)

    @staticmethod
    def _kiem_tra_thoi_han(thoi_han):
        so_thang = int(thoi_han)
        if so_thang <= 0:
            raise ValueError("Thoi han bao hanh phai lon hon 0.")
        return so_thang

    @property
    def ma_phieu(self):
        return self.__ma_phieu

    @property
    def ma_san_pham(self):
        return self.__ma_san_pham

    @property
    def ngay_mua(self):
        return self.__ngay_mua.isoformat()

    @property
    def thoi_han(self):
        return self.__thoi_han

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
            return "Con bao hanh"
        return "Het han bao hanh"

    def cap_nhat(self, ma_san_pham, ngay_mua, thoi_han):
        ngay_moi = date.fromisoformat(ngay_mua.strip())
        thoi_han_moi = self._kiem_tra_thoi_han(thoi_han)
        self.__ma_san_pham = ma_san_pham.strip()
        self.__ngay_mua = ngay_moi
        self.__thoi_han = thoi_han_moi

    def to_dict(self):
        return {
            "ma_phieu": self.__ma_phieu,
            "ma_san_pham": self.__ma_san_pham,
            "ngay_mua": self.__ngay_mua.isoformat(),
            "thoi_han": self.__thoi_han,
            "loai": "thuong"
        }

    def __str__(self):
        return (
            f"Ma phieu: {self.__ma_phieu} | "
            f"Ma san pham: {self.__ma_san_pham} | "
            f"Ngay het han: {self.ngay_het_han()} | "
            f"{self.kiem_tra_bao_hanh()}"
        )


# 3. Lop PhieuBaoHanhMoRong
class PhieuBaoHanhMoRong(PhieuBaoHanh):

    def ngay_het_han(self):
        ngay_goc = super().ngay_het_han()

        tong_thang = ngay_goc.month - 1 + 3
        nam = ngay_goc.year + tong_thang // 12
        thang = tong_thang % 12 + 1

        ngay = min(
            ngay_goc.day,
            calendar.monthrange(nam, thang)[1]
        )

        return date(nam, thang, ngay)

    def kiem_tra_bao_hanh(self):
        if date.today() <= self.ngay_het_han():
            return "Con bao hanh mo rong"
        return "Het han bao hanh mo rong"

    def to_dict(self):
        du_lieu = super().to_dict()
        du_lieu["loai"] = "mo_rong"
        return du_lieu


# 4. Lop BaoHanhService
class BaoHanhService:

    def __init__(self, ten_file="phieu_bao_hanh.json"):
        self.__danh_sach = []
        self.__ten_file = ten_file

    @staticmethod
    def _tao_phieu(loai, ma_phieu, ma_san_pham, ngay_mua, thoi_han):
        if loai == "mo_rong":
            return PhieuBaoHanhMoRong(ma_phieu, ma_san_pham, ngay_mua, thoi_han)
        if loai == "thuong":
            return PhieuBaoHanh(ma_phieu, ma_san_pham, ngay_mua, thoi_han)
        raise ValueError("Loai phieu khong hop le.")

    def them_phieu(self, phieu):
        if not phieu.ma_phieu:
            print("Ma phieu khong duoc de trong.")
            return

        if self.tim_phieu(phieu.ma_phieu) is not None:
            print("Ma phieu da ton tai.")
            return

        self.__danh_sach.append(phieu)
        self.ghi_du_lieu()
        print("Them phieu thanh cong.")

    def cap_nhat_phieu(self, ma_phieu, ma_san_pham, ngay_mua, thoi_han, loai=None):
        ma_chuan = ma_phieu.strip()
        for idx, phieu in enumerate(self.__danh_sach):
            if phieu.ma_phieu == ma_chuan:
                loai_moi = loai if loai in ("thuong", "mo_rong") else phieu.to_dict()["loai"]
                try:
                    phieu_moi = self._tao_phieu(
                        loai_moi, ma_chuan, ma_san_pham, ngay_mua, thoi_han
                    )
                    self.__danh_sach[idx] = phieu_moi
                    self.ghi_du_lieu()
                    print("Cap nhat phieu thanh cong.")
                except ValueError as err:
                    print(f"Du lieu khong hop le: {err}")
                return

        print("Khong tim thay phieu bao hanh.")

    def hien_thi(self):
        if not self.__danh_sach:
            print("Danh sach phieu bao hanh rong.")
            return

        for phieu in self.__danh_sach:
            print(phieu)

    def tim_phieu(self, ma_phieu):
        ma_chuan = ma_phieu.strip()
        for phieu in self.__danh_sach:
            if phieu.ma_phieu == ma_chuan:
                return phieu
        return None

    def ghi_du_lieu(self):
        danh_sach = [phieu.to_dict() for phieu in self.__danh_sach]
        with open(self.__ten_file, "w", encoding="utf-8") as file:
            json.dump(danh_sach, file, ensure_ascii=False, indent=4)

    def doc_du_lieu(self):
        if not os.path.exists(self.__ten_file):
            return

        try:
            with open(self.__ten_file, "r", encoding="utf-8") as file:
                danh_sach = json.load(file)

            if not isinstance(danh_sach, list):
                raise ValueError("Cau truc JSON phai la mot danh sach.")

            danh_sach_moi = []
            for p in danh_sach:
                phieu = self._tao_phieu(
                    p["loai"],
                    p["ma_phieu"],
                    p["ma_san_pham"],
                    p["ngay_mua"],
                    p["thoi_han"]
                )
                danh_sach_moi.append(phieu)

            self.__danh_sach = danh_sach_moi
            print("Doc du lieu thanh cong.")

        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            print("Du lieu trong file khong hop le. Giu nguyen danh sach hien tai.")


def chon_loai_phieu():
    loai_chon = input("Chon loai (1. Thuong / 2. Mo rong): ").strip()
    if loai_chon == "1":
        return "thuong"
    if loai_chon == "2":
        return "mo_rong"
    raise ValueError("Loai phieu khong hop le.")


# 5. Chuong trinh chinh
if __name__ == "__main__":
    service = BaoHanhService()
    service.doc_du_lieu()

    while True:
        print("\n===== QUAN LY PHIEU BAO HANH =====")
        print("1. Tao moi phieu bao hanh")
        print("2. Cap nhat phieu bao hanh")
        print("3. Hien thi danh sach")
        print("4. Tim kiem phieu bao hanh")
        print("5. Luu va thoat")

        chon = input("Nhap lua chon: ").strip()

        try:
            if chon == "1":
                ma_phieu = input("Nhap ma phieu: ")
                ma_sp = input("Nhap ma san pham: ")
                ngay_mua = input("Nhap ngay mua (YYYY-MM-DD): ")
                thoi_han = int(input("Nhap thoi han (thang): "))
                loai = chon_loai_phieu()

                phieu = BaoHanhService._tao_phieu(
                    loai, ma_phieu, ma_sp, ngay_mua, thoi_han
                )
                service.them_phieu(phieu)

            elif chon == "2":
                ma_phieu = input("Nhap ma phieu can cap nhat: ")
                ma_sp = input("Nhap ma san pham moi: ")
                ngay_mua = input("Nhap ngay mua moi (YYYY-MM-DD): ")
                thoi_han = int(input("Nhap thoi han moi (thang): "))
                loai = chon_loai_phieu()

                service.cap_nhat_phieu(
                    ma_phieu, ma_sp, ngay_mua, thoi_han, loai
                )

            elif chon == "3":
                print("\nDanh sach phieu bao hanh:")
                service.hien_thi()

            elif chon == "4":
                ma_phieu = input("Nhap ma phieu can tim: ")
                ket_qua = service.tim_phieu(ma_phieu)

                if ket_qua:
                    print(ket_qua)
                else:
                    print("Khong tim thay phieu.")

            elif chon == "5":
                service.ghi_du_lieu()
                print("Da luu du lieu. Ket thuc chuong trinh.")
                break

            else:
                print("Lua chon khong hop le.")

        except ValueError as err:
            print(f"Vui long nhap dung dinh dang du lieu ({err}).")
