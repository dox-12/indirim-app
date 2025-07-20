import tkinter as tk
from tkinter import ttk
import csv
from tkcalendar import DateEntry
from datetime import datetime

def formatla(sayi):
    return f"{sayi:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def hesapla():
    try:
        isim = entry_isim.get()
        fiyat = float(entry_fiyat.get())
        oran = float(entry_indirim.get())
        indirim = fiyat * (oran / 100)
        yeni_fiyat = fiyat - indirim
        tarih = datetime.now().strftime("%d.%m.%Y")

        sonuc_label.config(
            text=f"{isim}\nİndirimli Fiyat: {formatla(yeni_fiyat)} TL",
            font=("Arial", 16, "bold"),
            fg="gold"
        )

        tablo.insert("", "end", values=(
            isim,
            formatla(fiyat) + " TL",
            f"%{oran:.1f}",
            formatla(yeni_fiyat) + " TL",
            tarih
        ))

        with open("veriler.csv", "a", encoding="utf-8", newline="") as dosya:
            csv.writer(dosya).writerow([isim, fiyat, oran, indirim, yeni_fiyat, tarih])

        entry_isim.delete(0, tk.END)
        entry_fiyat.delete(0, tk.END)
        entry_indirim.delete(0, tk.END)

    except ValueError:
        sonuc_label.config(text="Geçerli sayılar girin!", fg="red")

def filtrele():
    arama = filtre_entry.get().lower()
    for item in tablo.get_children():
        tablo.delete(item)
    try:
        with open("veriler.csv", "r", encoding="utf-8") as dosya:
            for satir in csv.reader(dosya):
                if arama in satir[0].lower():
                    tablo.insert("", "end", values=(
                        satir[0],
                        formatla(float(satir[1])) + " TL",
                        f"%{float(satir[2]):.1f}",
                        formatla(float(satir[4])) + " TL",
                        satir[5]
                    ))
    except FileNotFoundError:
        pass

def tarih_filtrele():
    secilen = tarih_secici.get()
    for item in tablo.get_children():
        tablo.delete(item)
    try:
        with open("veriler.csv", "r", encoding="utf-8") as dosya:
            for satir in csv.reader(dosya):
                if len(satir) >= 6 and satir[5] == secilen:
                    tablo.insert("", "end", values=(
                        satir[0],
                        formatla(float(satir[1])) + " TL",
                        f"%{float(satir[2]):.1f}",
                        formatla(float(satir[4])) + " TL",
                        satir[5]
                    ))
    except FileNotFoundError:
        pass

def klavye_kisayollari(entry):
    entry.bind("<Control-c>", lambda e: entry.event_generate("<<Copy>>"))
    entry.bind("<Control-v>", lambda e: entry.event_generate("<<Paste>>"))
    entry.bind("<Control-x>", lambda e: entry.event_generate("<<Cut>>"))

pencere = tk.Tk()
pencere.title("Otel İndirim Hesaplayıcı")
pencere.geometry("950x500")
pencere.configure(bg="#2b2b2b")

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#3c3c3c", fieldbackground="#3c3c3c", foreground="white")
style.configure("Treeview.Heading", background="gray", foreground="white")

# Sol panel
sol = tk.Frame(pencere, bg="#2b2b2b")
sol.pack(side=tk.LEFT, padx=20, pady=20)

tk.Label(sol, text="Misafir İsmi:", bg="#2b2b2b", fg="white").pack()
entry_isim = tk.Entry(sol, bg="#444", fg="white", insertbackground="white")
entry_isim.pack()
klavye_kisayollari(entry_isim)

tk.Label(sol, text="Otel Fiyatı (TL):", bg="#2b2b2b", fg="white").pack(pady=(10,0))
entry_fiyat = tk.Entry(sol, bg="#444", fg="white", insertbackground="white")
entry_fiyat.pack()
klavye_kisayollari(entry_fiyat)

tk.Label(sol, text="İndirim Oranı (%):", bg="#2b2b2b", fg="white").pack(pady=(10,0))
entry_indirim = tk.Entry(sol, bg="#444", fg="white", insertbackground="white")
entry_indirim.pack()
klavye_kisayollari(entry_indirim)

tk.Button(sol, text="HESAPLA", bg="#ffd700", command=hesapla).pack(pady=15)
sonuc_label = tk.Label(sol, text="", bg="#2b2b2b")
sonuc_label.pack(pady=10)

# Sağ panel
sag = tk.Frame(pencere, bg="#2b2b2b")
sag.pack(side=tk.RIGHT, padx=10, pady=20)

tk.Label(sag, text="Hesap Geçmişi (Tablo):", bg="#2b2b2b", fg="white", font=("Arial", 10, "bold")).pack()

filtre_entry = tk.Entry(sag, bg="#444", fg="white", insertbackground="white")
filtre_entry.pack(pady=5)
klavye_kisayollari(filtre_entry)

tk.Button(sag, text="İsme Göre Filtrele", command=filtrele, bg="#ffd700").pack(pady=5)

tk.Label(sag, text="Tarih Seç:", bg="#2b2b2b", fg="white").pack(pady=(10,0))
tarih_secici = DateEntry(sag, locale="tr_TR", date_pattern="dd.MM.yyyy", background='darkblue',
                         foreground='white', borderwidth=2)
tarih_secici.pack(pady=5)
tk.Button(sag, text="Tarihe Göre Filtrele", command=tarih_filtrele, bg="#90ee90").pack(pady=5)

tablo = ttk.Treeview(sag, columns=("isim", "fiyat", "oran", "sonuc", "tarih"), show="headings", height=10)
tablo.pack()

tablo.heading("isim", text="Misafir")
tablo.heading("fiyat", text="Otel Fiyatı")
tablo.heading("oran", text="İndirim Oranı")
tablo.heading("sonuc", text="İndirimli Fiyat")
tablo.heading("tarih", text="Tarih")

for col in ("isim", "fiyat", "oran", "sonuc", "tarih"):
    tablo.column(col, width=140)

pencere.mainloop()
