# IoT Monitoring & Analytics Dashboard

<div align="center">
click to view dashboard :

[![View Interactive Dashboard](webpreview.png)](https://1drv.ms/x/c/1cb72b16f52dc456/IQTjHFDnwslAQ4_fmDIWelybAagU6xWA45i9Tw6dXyC6ep4?em=2&wdAllowInteractivity=True&ActiveCell='Dashboard'!A1&wdHideGridlines=True&wdHideHeaders=True&wdInConfigurator=True)

</div>

ESP8266 IoT monitoring project for collecting sensor readings and viewing them in an Excel analytics dashboard.

## Dashboard Features

- Temperature and humidity monitoring
- Ambient light (`LDR`) readings
- Light and fan status
- Timestamped data collection
- KPIs and sensor trend charts

## Files

<div align="center">

| File | Description |
|---|---|
| `ESPconnection.py` | Tests the ESP8266 connection |
| `esptoexcel.py` | Collects readings and updates the Excel workbook |
| `IoT_Analytics.xlsx` | Raw data, analytics, and dashboard |
| `webpreview.png` | Dashboard preview |

</div>

## Requirements

- Python 3.10+
- ESP8266 device
- `requests`
- `openpyxl`

```powershell
python -m pip install requests openpyxl
```

## Configuration

Set the ESP8266 endpoint in both Python scripts:

```python
ESP_URL = "http://192.168.0.228/data"
```

The endpoint should return:

```json
{
  "temperature": 32.8,
  "humidity": 45,
  "ldr": 8,
  "lightState": "ON",
  "fanState": "OFF"
}
```

## Usage

Test the connection:

```powershell
python ESPconnection.py
```

Start data collection:

```powershell
python esptoexcel.py
```

Stop collection with `Ctrl+C`. Close `IoT_Analytics.xlsx` before starting the collector to avoid an Excel file-lock error.

## License

[MIT License](LICENSE)
