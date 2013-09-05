#include<ImageSearch.au3>
;~ Dim $x, $y, $x1, $y1
;~ WinActivate("Stronghold Kingdoms - Welt 3")
;~ WinWaitActive("Stronghold Kingdoms - Welt 3")
;~ $result = searchForImage("FrSchieber.png", $x, $y, 0)
;~ If $result = 1 Then
;~ 	While Not searchForImage("FrSchieberUnten.png", $x1, $y1, 75)

;~ 		MouseClickDrag("LEFT", $x, $y, $x, $y +100)
;~ 		$y = $y +100
;~ 		Sleep(500)
;~ 	WEnd
;~ EndIf

;~ $result = searchForImage("FrSchieberUnten.png", $x, $y, 75)
;~ If $result = 1 Then
;~ 	MsgBox(0, "info", "did it")
;~ EndIf

;~ Func searchForImage($fileName, ByRef $x, ByRef $y, $tolerance)
;~ 	$result = _WaitForImageSearch($fileName, 1, 1, $x, $y, $tolerance)
;~ 	If $result = 1 Then
;~ 		Return 1
;~ 	EndIf
;~ 	Return 0
;~ EndFunc


HotKeySet("^!q", "quit")
Local $connection
Local $myTurn
TCPStartup()

Func startServer()
	ShellExecute(@HomePath & "\Documents\GitHub\mousemove\schedule.py")
	If WinExists("C:\Windows\py.exe") Then
		Return True
	EndIf
	Return False
EndFunc

Func connect()
	Local $_connection
	If Not $connection Then
		For $i =0 To 2
			$_connection = TCPConnect("127.0.0.1", 5083)
			If @error Then
				startServer()
				Sleep(1000)
			Else
				$connection = $_connection
				If $connection Then
					MsgBox(0, "conn", "true")
				EndIf
				Return True
			EndIf
		Next
	EndIf
	Return False
EndFunc

Func reconnect()
	$connection = False
	connect()
EndFunc

Func schedule()
	connect()
	While 1
		Sleep(1000)
		If $myTurn Then
			$result = TCPSend($connection, "?")
			If Not $result Then
				$myTurn = False
				reconnect()
			Else
				$myTurn = False
			EndIf
		Else
			$result = TCPRecv($connection, 1)
			If @error = 0 Then
				$myTurn = True
				Return
			ElseIf @error = -1 Then
				ContinueLoop
			Else
				MsgBox(0, "Info", "error" & @error)
				reconnect()
			EndIf
		EndIf
	WEnd
EndFunc

Func quit()
	TCPShutdown()
	Exit
EndFunc

While 1
	MsgBox(0, "schedule", "schedule")
	schedule()
	Sleep(1000)
WEnd
;~ HotKeySet("l", "levelUp")

;~ Func levelUp()
;~ 	Local $x, $y
;~ 	$result = searchForImage("ableForLevel.png", $x, $y, 0)
;~ 	If $result = 1 Then
;~ 		MouseClick("LEFT", $x, $y)
;~ 		Sleep(500)
;~ 		MsgBox(0, "found", "found")
;~ 		$result = searchForImage("levelUp.png", $x, $y, 0)
;~ 		If $result = 1 Then
;~ 			MouseClick("LEFT", $x, $y)
;~ 			Sleep(500)
;~ 		EndIf
;~ 	EndIf
;~ EndFunc

;~ While 1
;~ 	Sleep(100)
;~ WEnd
