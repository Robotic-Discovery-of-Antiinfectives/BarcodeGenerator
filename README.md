# BarcodeGenerator
![BarcodeGenerator Screenshot](assets/screenshot.png)

Intended to be used with AnalytikJena's barcode printer program.

Generates two CSV files containing 10 columns each.

1) `<ProjectNr><Screentype><RunNr>barcodes<date>.csv`

| Barcode     | ProjectNr | PlateNr | Phase          | PhaseID | RunNr | Date     | Info             |
|-------------|-----------|---------|----------------|---------|-------|----------|------------------|
| 007PrS02001 | 7         | 1       | Primary Screen | PrS     | 2     | 20260505 | Candida albicans |
| 007PrS02002 | 7         | 2       | Primary Screen | PrS     | 2     | 20260505 | Candida albicans |
| 007PrS02003 | 7         | 3       | Primary Screen | PrS     | 2     | 20260505 | Candida albicans |

2) `<ProjectNr><Screentype><RunNr>cybio_barcodes<date>.csv`

| Barcode     | value1 | value2 | value3         | value4 | value5 | value6           | value7 | value8 | value9 |
|-------------|--------|--------|----------------|--------|--------|------------------|--------|--------|--------|
| 007PrS02001 | 7      | 1      | Primary Screen | PrS    | 2      | Candida albicans | 260505 |        |        |
| 007PrS02002 | 7      | 2      | Primary Screen | PrS    | 2      | Candida albicans | 260505 |        |        |
| 007PrS02003 | 7      | 3      | Primary Screen | PrS    | 2      | Candida albicans | 260505 |        |        |

## Usage
Change directory to BarcodeGenerator and run in terminal:
```Sh
uv run --locked main.py
```

The above command starts the webapp. **Dont close the terminal!**

## Windows desktop launcher
The `run_barcode_generator.bat` script starts the app with the locked
dependencies.

1. Clone this repository on the Windows computer.
2. Copy `run_barcode_generator.bat` to the Desktop.
3. Double-click the script and enter the full path to the cloned project folder.
4. Keep the terminal open and open `http://127.0.0.1:8050` in a browser.

If the script stays in the project folder, it finds the project automatically
and does not ask for its path.

## Windows desktop shortcut
Use a Windows shortcut to launch the batch file from the cloned project.

1. Open the cloned project folder in File Explorer.
2. Right-click `run_barcode_generator.bat`.
3. Select **Show more options** if Windows displays the compact menu.
4. Select **Send to**, then **Desktop (create shortcut)**.
5. Double-click the new Desktop shortcut to start the app.

You can also right-click and drag `run_barcode_generator.bat` to the Desktop,
release the mouse button, and select **Create shortcuts here**.

This click-based method creates a Windows `.lnk` shortcut rather than an NTFS
symbolic link, and does not require administrator permissions.
