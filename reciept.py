from docxtpl import DocxTemplate, InlineImage
from datetime import date

doc = DocxTemplate("stockinvoice.docx")

salesRows = [{"name":"Ps4 Pro Black", "quantity":2, "price":200_000, "total":200_000 * 2},
             {"name":"Ps5  White", "quantity":1, "price":500_000, "total":500_000}
              ]

# salesRows = [["Ps4 Pro Black", 2, 200_000, 400_000]]

context ={
    "invoice_id" : "434938382",
    "date" : date.today(),
    "recipent": "Olowoleru",
    "address": "address",
    "phone": "07033517584",
    "salesTbRows": salesRows,
    "subtotal": 200_000,
    "total": 200_000
}

doc.render(context)

doc.save("report.docx")