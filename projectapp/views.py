from django.shortcuts import render

# Create your views here.


# accounts = [
#     {"session": "acc1", "api_id": 21825034, "api_hash": "54914cdafa40fbb22d574799c0f38a9e"},
#     {"session": "acc2", "api_id": 27622829, "api_hash": "070517eac99ddbdcbdbc6ef3113a120b"},
#     {"session": "acc3", "api_id": 28796243, "api_hash": "59915e8540fed369e2b1d633c1a7c82d"},
# ]
from docx import Document

# Yangi Word hujjat yaratish
doc = Document()
doc.add_heading("Oracle Ma'lumotlar Bazasi Joy Holati", level=0)

# Kirish
doc.add_paragraph(
    "Ushbu hujjat Oracle ma'lumotlar bazasining joriy joy holatini ko'rsatadi. "
    "Quyida umumiy hajm, band joy, bo'sh joy va bandlik foizi keltirilgan."
)

# Tablespace jadvali
tablespace_data = [
    ["RBS_TRAN", 30.39, 23.87, 6.52, 78.6],
    ["RADIX_EVENTLOG", 20.93, 15.92, 5.01, 76.0],
    ["RADIX", 17.64, 13.50, 4.14, 76.6],
    ["RBS_DOER", 17.52, 13.37, 4.15, 76.3],
    ["RBS_ENTRY", 9.37, 7.15, 2.22, 76.3],
    ["TXPG_ACTION", 7.46, 5.68, 1.78, 76.1],
    ["RBS_TRANLINK", 3.94, 3.00, 0.94, 76.1],
    ["TXPG_TRAN", 1.98, 1.51, 0.47, 76.3],
    ["SYSAUX", 1.83, 1.40, 0.43, 76.5],
    ["SYSTEM", 1.48, 1.13, 0.35, 76.4],
    ["RBS_POSTING", 0.32, 0.24, 0.08, 75.0],
    ["RBS_ACCOUNT", 0.31, 0.23, 0.08, 74.2],
    ["RBS_DOER_IDX", 0.09, 0.07, 0.02, 77.8],
    ["UNDOTBS1", 0.08, 0.06, 0.02, 75.0],
    ["RBS", 0.06, 0.05, 0.01, 83.3],
    ["RBS_TRANLINK_IDX", 0.03, 0.02, 0.01, 66.7],
    ["TXPG_TRAN_IDX", 0.02, 0.02, 0, 100.0],
    ["RBS_IDX", 0.02, 0.01, 0.01, 50.0],
    ["TXPG_ACTION_IDX", 0.02, 0.01, 0.01, 50.0],
    ["RBS_TRAN_IDX", 0.02, 0.01, 0.01, 50.0],
    ["TXPG", 0.02, 0.01, 0.01, 50.0],
    ["RBS_ENTRY_IDX", 0.02, 0.01, 0.01, 50.0],
    ["TXPG_IDX", 0.01, 0.01, 0, 100.0],
    ["RBS_ACCOUNT_IDX", 0.01, 0.01, 0, 100.0],
    ["RBS_CONTRACT_IDX", 0.01, 0.01, 0, 100.0],
    ["RBS_CONTRACT", 0.01, 0.01, 0, 100.0],
    ["RBS_TOKEN", 0, 0, 0, 0],
    ["RBS_POSTING_IDX", 0, 0, 0, 0],
    ["TXPG_TOKEN", 0, 0, 0, 0],
    ["RBS_SUBJECT", 0, 0, 0, 0],
    ["USERS", 0, 0, 0, 0],
    ["RBS_SUBJECT_IDX", 0, 0, 0, 0],
    ["RBS_TOKEN_IDX", 0, 0, 0, 0],
    ["TXPG_TOKEN_IDX", 0, 0, 0, 0],
    ["TXPG_ORDER_IDX", 0, 0, 0, 0],
]

# Jadval yaratish
table = doc.add_table(rows=1, cols=5)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Tablespace'
hdr_cells[1].text = 'Umumiy Joy (GB)'
hdr_cells[2].text = 'Band Joy (GB)'
hdr_cells[3].text = "Bo'sh Joy (GB)"
hdr_cells[4].text = 'Bandlik (%)'

for row in tablespace_data:
    cells = table.add_row().cells
    for i in range(5):
        cells[i].text = str(row[i])

# Xulosa
doc.add_heading("Xulosa", level=1)
doc.add_paragraph("Umumiy ma'lumotlar bazasi hajmi: 113.84 GB")
doc.add_paragraph("Umumiy band joy: 86.8 GB (76.3%)")
doc.add_paragraph("Umumiy bo'sh joy: 27.0 GB (23.7%)")
doc.add_paragraph(
    "Baza bandligi yuqori, bo'sh joyni nazorat qilish va kerak bo'lsa kengaytirish tavsiya etiladi."
)

# Faylni saqlash
file_path = "/mnt/data/Oracle_Baza_Tahlili.docx"
doc.save(file_path)
file_path
