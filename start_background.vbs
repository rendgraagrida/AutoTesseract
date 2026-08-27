Set WshShell = CreateObject("WScript.Shell")
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
pythonwPath = Chr(34) & scriptDir & "\.venv\Scripts\pythonw.exe" & Chr(34)
scriptPath = Chr(34) & scriptDir & "\ai_assistant.py" & Chr(34)
WshShell.Run pythonwPath & " " & scriptPath, 0, False
