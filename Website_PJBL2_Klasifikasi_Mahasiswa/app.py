from flask import Flask, render_template
import csv
from pathlib import Path

app = Flask(__name__)
FILE_DATA = Path(__file__).parent / "data" / "dataset_mahasiswa.csv"

def baca_data():
    with open(FILE_DATA, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

@app.route("/")
def beranda():
    data = baca_data()
    U = {m["id"] for m in data}
    A = {m["id"] for m in data if float(m["kehadiran_persen"]) >= 80}
    B = {m["id"] for m in data if float(m["nilai_akhir"]) >= 80}
    hasil = []
    for m in data:
        hadir, nilai = m["id"] in A, m["id"] in B
        if hadir and nilai:
            kategori, kelas = "Keduanya tinggi", "both"
        elif hadir:
            kategori, kelas = "Kehadiran tinggi saja", "attendance"
        elif nilai:
            kategori, kelas = "Nilai tinggi saja", "grade"
        else:
            kategori, kelas = "Belum memenuhi keduanya", "neither"
        hasil.append({**m, "kategori": kategori, "kelas": kelas})
    ringkasan = {
        "total": len(U), "kehadiran": len(A), "nilai": len(B),
        "irisan": len(A & B), "gabungan": len(A | B),
        "hanya_kehadiran": len(A - B), "hanya_nilai": len(B - A),
        "belum": len(U - (A | B))
    }
    return render_template("index.html", data=hasil, r=ringkasan)

if __name__ == "__main__":
    app.run(debug=True)
