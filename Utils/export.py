import csv
from fpdf import FPDF
from datetime import datetime

def get_filename(tipo_reporte, extension, **kwargs):
    """
    Genera un nombre de archivo estandarizado para los reportes
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if 'fecha_inicio' in kwargs and 'fecha_fin' in kwargs:
        return f"{tipo_reporte}_{kwargs['fecha_inicio']}_a_{kwargs['fecha_fin']}.{extension}"
    
    marca_str = ""
    if 'marca_filtro' in kwargs and kwargs['marca_filtro'] and kwargs['marca_filtro'] != "Todas":
        marca_str = f"_{kwargs['marca_filtro']}"
        
    return f"{tipo_reporte}{marca_str}_{timestamp}.{extension}"

def exportar_a_csv(datos, tipo_reporte="ventas", **kwargs):
    """
    Exporta datos a CSV según el tipo de reporte
    """
    try:
        filename = get_filename(tipo_reporte, "csv", **kwargs)
        
        with open(filename, mode="w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if tipo_reporte == "ventas":
                writer.writerow(["Venta ID", "Auto ID", "Marca", "Modelo", "Fecha de Venta"])
                for venta, auto in datos:
                    writer.writerow([
                        venta.id,
                        venta.auto_id,
                        auto.marca,
                        auto.modelo,
                        venta.fecha_venta.strftime("%Y-%m-%d %H:%M:%S")
                    ])
                    
            elif tipo_reporte == "autos_mas_vendidos":
                writer.writerow(["Marca", "Cantidad Vendidos"])
                for marca, cantidad in datos:
                    writer.writerow([marca.capitalize(), cantidad])
                    
            elif tipo_reporte == "ingresos_totales":
                writer.writerow(["Concepto", "Valor"])
                for concepto, valor in datos:
                    writer.writerow([concepto, valor])
            
            # Agregar más tipos de reportes aquí siguiendo el mismo patrón
                    
        print(f"Reporte CSV generado exitosamente: {filename}")
        return True
        
    except Exception as e:
        print(f"Error al exportar a CSV: {str(e)}")
        raise

def exportar_a_pdf(datos, tipo_reporte="ventas", **kwargs):
    """
    Exporta datos a PDF según el tipo de reporte
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        filename = get_filename(tipo_reporte, "pdf", **kwargs)
        
        if tipo_reporte == "ventas":
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Reporte de Ventas", ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Periodo: {kwargs['fecha_inicio']} a {kwargs['fecha_fin']}", 
                    ln=True, align='C')
            pdf.ln(10)

            for venta, auto in datos:
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, txt=f"Venta ID: {venta.id}", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.cell(0, 10, txt=f"Auto: {auto.codigo_vin} - {auto.marca} {auto.modelo}", 
                        ln=True)
                pdf.cell(0, 10, txt=f"Fecha de Venta: {venta.fecha_venta.strftime('%Y-%m-%d %H:%M:%S')}", 
                        ln=True)
                pdf.ln(5)
        
        elif tipo_reporte == "autos_mas_vendidos":
            # Título
            pdf.set_font("Arial", 'B', 16)
            titulo = "Reporte de Autos más Vendidos por Marca"
            if kwargs.get('marca_filtro') and kwargs['marca_filtro'] != "Todas":
                titulo += f" - {kwargs['marca_filtro']}"
            pdf.cell(0, 10, txt=titulo, ln=True, align='C')
            pdf.ln(10)
            
            # Contenido
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(95, 10, txt="Marca", border=1, ln=0, align='C')
            pdf.cell(95, 10, txt="Cantidad Vendidos", border=1, ln=1, align='C')
            
            pdf.set_font("Arial", size=12)
            for marca, cantidad in datos:
                pdf.cell(95, 10, txt=marca.capitalize(), border=1, ln=0)
                pdf.cell(95, 10, txt=str(cantidad), border=1, ln=1, align='C')
                
        elif tipo_reporte == "ingresos_totales":
            # Título
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, txt="Reporte de Ingresos Totales", ln=True, align='C')
            pdf.ln(10)
            
            # Periodo
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt=f"Período: {kwargs['fecha_inicio']} al {kwargs['fecha_fin']}", 
                    ln=True, align='C')
            pdf.ln(10)
            
            # Contenido
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(100, 10, txt="Concepto", border=1, ln=0, align='C')
            pdf.cell(90, 10, txt="Valor", border=1, ln=1, align='C')
            
            pdf.set_font("Arial", size=12)
            for concepto, valor in datos:
                pdf.cell(100, 10, txt=concepto, border=1, ln=0)
                pdf.cell(90, 10, txt=valor, border=1, ln=1, align='C')

        # Agregar más tipos de reportes aquí siguiendo el mismo patrón

        pdf.output(filename)
        print(f"Reporte PDF generado exitosamente: {filename}")
        return True
        
    except Exception as e:
        print(f"Error al exportar a PDF: {str(e)}")
        raise