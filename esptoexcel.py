import requests
import openpyxl
import os
import time
from datetime import datetime
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

# ---------------- CONFIGURATION ----------------

ESP_URL = "http://192.168.0.228/data"
EXCEL_FILE = "IoT_Analytics.xlsx"
SHEET_NAME = "Raw_Data"
TABLE_NAME = "IoT_Data"

COLLECTION_INTERVAL = 5  # Seconds

HEADERS = [
    "Timestamp",
    "Temperature",
    "Humidity",
    "LDR",
    "Light_Status",
    "Fan_Status"
]

# ---------------- CREATE EXCEL FILE ----------------

if not os.path.exists(EXCEL_FILE):

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = SHEET_NAME

    sheet.append(HEADERS)

    # Format header
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )
        cell.alignment = Alignment(horizontal="center")

    # Set column widths
    widths = [22, 16, 16, 12, 16, 16]

    for i, width in enumerate(widths, start=1):
        sheet.column_dimensions[
            get_column_letter(i)
        ].width = width

    # Create initial Excel Table
    table = Table(
        displayName=TABLE_NAME,
        ref="A1:F1"
    )

    style = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )

    table.tableStyleInfo = style
    sheet.add_table(table)

    workbook.save(EXCEL_FILE)
    workbook.close()

    print("Excel workbook created successfully!")

# ---------------- START COLLECTION ----------------

print("\n====================================")
print("  IOFT IOT EXCEL DATA COLLECTOR")
print("====================================")
print("Saving readings every 5 seconds...")
print("Automatically expanding IoT_Data table.")
print("Press CTRL+C to stop.\n")

while True:

    workbook = None

    try:

        # Get ESP8266 sensor data
        response = requests.get(ESP_URL, timeout=5)
        response.raise_for_status()

        data = response.json()

        # Open workbook
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook[SHEET_NAME]

        # Prepare new row
        timestamp = datetime.now()

        row = [
            timestamp,
            data.get("temperature"),
            data.get("humidity"),
            data.get("ldr"),
            data.get("lightState"),
            data.get("fanState")
        ]

        # Append new sensor readings
        sheet.append(row)

        # Identify the latest row
        last_row = sheet.max_row

        # Format timestamp
        timestamp_cell = sheet.cell(
            row=last_row,
            column=1
        )

        timestamp_cell.number_format = "yyyy-mm-dd hh:mm:ss"

        # ---------------- AUTO EXPAND EXCEL TABLE ----------------

        if TABLE_NAME in sheet.tables:

            table = sheet.tables[TABLE_NAME]

            # Expand table to include every new reading
            table.ref = f"A1:F{last_row}"

            # Update filter range if present
            if table.autoFilter:
                table.autoFilter.ref = table.ref

        else:
            raise ValueError(
                f"Excel Table '{TABLE_NAME}' not found in {SHEET_NAME}."
            )

        # Enable Excel formula recalculation on opening
        workbook.calculation.fullCalcOnLoad = True
        workbook.calculation.forceFullCalc = True
        workbook.calculation.calcMode = "auto"

        # Save workbook
        workbook.save(EXCEL_FILE)

        total_readings = last_row - 1
        current_table_range = table.ref

        print("------------------------------------")
        print("Data saved successfully!")
        print("Timestamp   :", timestamp)
        print("Temperature :", data.get("temperature"))
        print("Humidity    :", data.get("humidity"))
        print("LDR         :", data.get("ldr"))
        print("Light       :", data.get("lightState"))
        print("Fan         :", data.get("fanState"))
        print("Total rows  :", total_readings)
        print("Table range :", current_table_range)

    except requests.exceptions.RequestException as e:
        print("ESP8266 connection error:", e)

    except PermissionError:
        print("Excel file is locked. Close Excel and try again.")

    except Exception as e:
        print("Error:", e)

    finally:
        if workbook is not None:
            workbook.close()

    time.sleep(COLLECTION_INTERVAL)