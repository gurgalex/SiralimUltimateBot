; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Siralim Access"
#define MyAppVersion "0.9.7"
#define MyAppPublisher "Alex Gurganus"
#define MyAppExeName "SiralimAccess.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{2EB082C4-54CD-49EC-B81D-14689BCA50B4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
OutputBaseFilename=SiralimAccess
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: dist\Siralim Access\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Siralim Access\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{tmp}\tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe"; DestDir: "{app}"; Flags: external skipifsourcedoesntexist

; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[code]
function IsTesseractInstalled(): Boolean;
begin;
    Result := RegKeyExists(HKA64, 'SOFTWARE\Tesseract-OCR');
 end;

[Run]
Filename: "{app}\tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe"; Parameters: ""; Flags: waituntilterminated; Check: not IsTesseractInstalled ; StatusMsg: "Tesseract OCR installation. Please wait..."

Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: postinstall 



[Code]
var
  DownloadPage: TDownloadWizardPage;

function OnDownloadProgress(const Url, FileName: String; const Progress, ProgressMax: Int64): Boolean;
begin
  if Progress = ProgressMax then
    Log(Format('Successfully downloaded file to {tmp}: %s', [FileName]));
  Result := True;
end;

procedure InitializeWizard;
begin
  DownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), SetupMessage(msgPreparingDesc), @OnDownloadProgress);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  if IsTesseractInstalled() then begin
  Result := True;
  DownloadPage.Hide;
  exit;
  end;

  if CurPageID = wpReady then begin
    DownloadPage.Clear;
    DownloadPage.Add('https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe', 'tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe', '');
    DownloadPage.Show;
    try
      try
        DownloadPage.Download;
        Result := True;
      except
        SuppressibleMsgBox(AddPeriod(GetExceptionMessage), mbCriticalError, MB_OK, IDOK);
        Result := False;
      end;
    finally
      DownloadPage.Hide;
    end;
  end else
    Result := True;
end;




//function InitializeSetup(): Boolean;

//begin;
//  Result := False
//    if IsTesseractInstalled() then
//       MsgBox('Tesseract is installed.', mbError, MB_OK)
//    else
//        MsgBox('Tesseract is not installed.', mbError, MB_OK);
//
//end;