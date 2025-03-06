[Setup]
AppName=Screenshot to PDF
AppVersion=1.0
DefaultDirName={pf}\ScreenshotToPDF
DefaultGroupName=ScreenshotToPDF
OutputDir=.
OutputBaseFilename=ScreenshotToPDFSetup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\screenshot_app.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Screenshot to PDF"; Filename: "{app}\screenshot_app.exe"
Name: "{commondesktop}\Screenshot to PDF"; Filename: "{app}\screenshot_app.exe"

[Run]
Filename: "{app}\screenshot_app.exe"; Description: "Launch Screenshot to PDF"; Flags: nowait postinstall skipifsilent
