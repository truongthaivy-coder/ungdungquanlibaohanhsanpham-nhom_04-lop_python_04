# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 21:16:34 2026

@author: ADMIN
"""

from abc import ABC, abstractmethod


class QuanLy(ABC):
    @abstractmethod
    def hien_thi_thong_tin(self):
        pass


class KhachHang(QuanLy):
    def __init__(self, ma_kh, ten_kh, so_dien_thoai):
        self.__ma_kh = ma_kh
        self.__ten_kh = ten_kh
        self.__so_dien_thoai = so_dien_thoai

    @property
    def ma_kh(self):
        return self.__ma_kh

    def hien_thi_thong_tin(self):
        return (
            f"Mã khách hàng: {self.__ma_kh} | "
            f"Tên: {self.__ten_kh} | "
            f"SĐT: {self.__so_dien_thoai}"
        )

    def __str__(self):
        return self.hien_thi_thong_tin()


class SanPham(QuanLy):
    def __init__(self, ma_sp, ten_sp, hang_san_xuat):
        self.__ma_sp = ma_sp
        self.__ten_sp = ten_sp
        self.__hang_san_xuat = hang_san_xuat

    @property
    def ma_sp(self):
        return self.__ma_sp

    def hien_thi_thong_tin(self):
        return (
            f"Mã sản phẩm: {self.__ma_sp} | "
            f"Tên sản phẩm: {self.__ten_sp} | "
            f"Hãng sản xuất: {self.__hang_san_xuat}"
        )

    def __str__(self):
        return self.hien_thi_thong_tin()


class QuanLyService:
    def __init__(self):
        self.__danh_sach_khach_hang = []
        self.__danh_sach_san_pham = []

    def them_khach_hang(self, khach_hang):
        for kh in self.__danh_sach_khach_hang:
            if kh.ma_kh == khach_hang.ma_kh:
                print("Mã khách hàng đã tồn tại.")
                return

        self.__danh_sach_khach_hang.append(khach_hang)
        print("Thêm khách hàng thành công.")

    def them_san_pham(self, san_pham):
        for sp in self.__danh_sach_san_pham:
            if sp.ma_sp == san_pham.ma_sp:
                print("Mã sản phẩm đã tồn tại.")
                return

        self.__danh_sach_san_pham.append(san_pham)
        print("Thêm sản phẩm thành công.")

    def hien_thi_khach_hang(self):
        for kh in self.__danh_sach_khach_hang:
            print(kh)

    def hien_thi_san_pham(self):
        for sp in self.__danh_sach_san_pham:
            print(sp)

    def tim_khach_hang(self, ma_kh):
        for kh in self.__danh_sach_khach_hang:
            if kh.ma_kh == ma_kh:
                return kh
        return None

    def tim_san_pham(self, ma_sp):
        for sp in self.__danh_sach_san_pham:
            if sp.ma_sp == ma_sp:
                return sp
        return None


if __name__ == "__main__":
    service = QuanLyService()

    kh1 = KhachHang("KH001", "Nguyen Van A", "0901234567")
    kh2 = KhachHang("KH002", "Tran Thi B", "0912345678")

    sp1 = SanPham("SP001", "Laptop", "Dell")
    sp2 = SanPham("SP002", "Dien thoai", "Samsung")

    service.them_khach_hang(kh1)
    service.them_khach_hang(kh2)

    service.them_san_pham(sp1)
    service.them_san_pham(sp2)

    print("\nDanh sach khach hang:")
    service.hien_thi_khach_hang()

    print("\nDanh sach san pham:")
    service.hien_thi_san_pham()

    print("\nTim khach hang KH001:")
    ket_qua = service.tim_khach_hang("KH001")
    print(ket_qua if ket_qua else "Khong tim thay khach hang.")

    print("\nTim san pham SP001:")
    ket_qua = service.tim_san_pham("SP001")
    print(ket_qua if ket_qua else "Khong tim thay san pham.")
