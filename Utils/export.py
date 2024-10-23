import csv
from fpdf import FPDF


def exportar_a_csv(ventas, fecha_inicio, fecha_fin):
    filename = f"ventas_report_{fecha_inicio}_a_{fecha_fin}.csv"
    try:
        with open(filename, mode="w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Venta ID", "Auto ID", "Marca",
                            "Modelo", "Fecha de Venta"])
            for venta, auto in ventas:
                writer.writerow([
                    venta.id,
                    venta.auto_id,
                    auto.marca,
                    auto.modelo,
                    venta.fecha_venta.strftime("%Y-%m-%d %H:%M:%S")
                ])
        print(f"Reporte CSV generado exitosamente: {filename}")
    except Exception as e:
        print(f"Error al exportar a CSV: {str(e)}")


def exportar_a_pdf(ventas, fecha_inicio, fecha_fin):
    filename = f"ventas_report_{fecha_inicio}_a_{fecha_fin}.pdf"
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Reporte de Ventas", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(
            200, 10, txt=f"Periodo: {fecha_inicio} a {fecha_fin}", ln=True, align='C')
        pdf.ln(10)  # Línea en blanco

        for venta, auto in ventas:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt=f"Venta ID: {venta.id}", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(
                0, 10, txt=f"Auto: {auto.codigo_vin} - {auto.marca} {auto.modelo}", ln=True)
            pdf.cell(
                0, 10, txt=f"Fecha de Venta: {venta.fecha_venta.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            pdf.ln(5)  # Espacio entre ventas

        pdf.output(filename)
        print(f"Reporte PDF generado exitosamente: {filename}")
    except Exception as e:
        print(f"Error al exportar a PDF: {str(e)}")
