#include<ImageSearch.au3>

Func searchForImage($fileName, ByRef $x, ByRef $y, $tolerance)
	$result = _WaitForImageSearch($fileName, 1, 1, $x, $y, $tolerance)
	If $result = 1 Then
		Return 1
	EndIf
	Return 0
EndFunc


If $CmdLine[0] = 1 Then
	Local $x, $y
	$result = searchForImage($CmdLine[1], $x, $y, 125)
	If $result = 1 Then
		$result = ConsoleWrite("["&$x&","&$y&"]")
		If $result Then
			MsgBox(0, "Info", $result & "   " & @error)
		EndIf
	Else
		ConsoleWrite("1")
	EndIf
Else
	MsgBox(0, "Wrong Number of Arguments", "Wrong Number of Arguments. Pass the FileName as first Parameter")
EndIf

