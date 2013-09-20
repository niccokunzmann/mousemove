#include<ImageSearch.au3>
#include <GUIConstantsEx.au3>
#include <WindowsConstants.au3>
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


;~ HotKeySet("^!q", "quit")
;~ Local $connection
;~ Local $myTurn
;~ TCPStartup()

;~ Func startServer()
;~ 	ShellExecute(@HomePath & "\Documents\GitHub\mousemove\schedule.py")
;~ 	If WinExists("C:\Windows\py.exe") Then
;~ 		Return True
;~ 	EndIf
;~ 	Return False
;~ EndFunc

;~ Func connect()
;~ 	Local $_connection
;~ 	If Not $connection Then
;~ 		For $i =0 To 2
;~ 			$_connection = TCPConnect("127.0.0.1", 5083)
;~ 			If @error Then
;~ 				startServer()
;~ 				Sleep(1000)
;~ 			Else
;~ 				$connection = $_connection
;~ 				If $connection Then
;~ 					MsgBox(0, "conn", "true")
;~ 				EndIf
;~ 				Return True
;~ 			EndIf
;~ 		Next
;~ 	EndIf
;~ 	Return False
;~ EndFunc

;~ Func reconnect()
;~ 	$connection = False
;~ 	connect()
;~ EndFunc

;~ Func schedule()
;~ 	connect()
;~ 	While 1
;~ 		Sleep(1000)
;~ 		If $myTurn Then
;~ 			$result = TCPSend($connection, "?")
;~ 			If Not $result Then
;~ 				$myTurn = False
;~ 				reconnect()
;~ 			Else
;~ 				$myTurn = False
;~ 			EndIf
;~ 		Else
;~ 			$result = TCPRecv($connection, 1)
;~ 			If @error = 0 Then
;~ 				$myTurn = True
;~ 				Return
;~ 			ElseIf @error = -1 Then
;~ 				ContinueLoop
;~ 			Else
;~ 				MsgBox(0, "Info", "error" & @error)
;~ 				reconnect()
;~ 			EndIf
;~ 		EndIf
;~ 	WEnd
;~ EndFunc

;~ Func quit()
;~ 	TCPShutdown()
;~ 	Exit
;~ EndFunc

;~ While 1
;~ 	MsgBox(0, "schedule", "schedule")
;~ 	schedule()
;~ 	Sleep(1000)
;~ WEnd


;~ HotKeySet("^!l", "levelUp")

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
#cs
;~ While 1
;~ 	Sleep(100)
;~ WEnd
#ce

;~ Dim $priorityRecruiting[5]

;~ Local $b1, $b2, $b3, $b4, $b5, $b6
;~ $width = 100
;~ GUICreate("Autorekrutierung", $width *6+20, 200)
;~ Opt("GUICoordMode", 2)

;~ $b1 = GUICtrlCreateButton("Bauernmiliz", 10, 150, $width)
;~ $b2 = GUICtrlCreateButton("Bogenschütze", 0, -1, $width)
;~ $b3 = GUICtrlCreateButton("Pikenier", 0, -1, $width)
;~ $b4 = GUICtrlCreateButton("Schwertkämpfer", 0, -1, $width)
;~ $b5 = GUICtrlCreateButton("Katapult", 0, -1, $width)
;~ $b6 = GUICtrlCreateButton("Fertig", 0, -1, $width)
;~ $currentIndex = 0
#cs
;~ GUISetState()
;~ While 1
;~ 	$msg = GUIGetMsg()
;~ 	Select
;~ 		Case $msg = $GUI_EVENT_CLOSE
;~ 			ExitLoop
;~ 		Case $msg = $b1
;~ 			MsgBox(0, 'Testing', 'Button 1 was pressed')
;~ 			GUICtrlDelete($b1)
;~ 			$priorityRecruiting[$currentIndex] = 1
;~ 			$currentIndex += 1
;~ 		Case $msg = $b2
;~ 			MsgBox(0, 'Testing', 'Button 2 was pressed')
;~ 			GUICtrlDelete($b2)
;~ 			$priorityRecruiting[$currentIndex] = 2
;~ 			$currentIndex += 1
;~ 		Case $msg = $b3
;~ 			MsgBox(0, 'Testing', 'Button 3 was pressed')
;~ 			GUICtrlDelete($b3)
;~ 			$priorityRecruiting[$currentIndex] = 3
;~ 			$currentIndex += 1
;~ 		Case $msg = $b4
;~ 			MsgBox(0, 'Testing', 'Button 4 was pressed')
;~ 			GUICtrlDelete($b4)
;~ 			$priorityRecruiting[$currentIndex] = 4
;~ 			$currentIndex += 1
;~ 		Case $msg = $b5
;~ 			MsgBox(0, 'Testing', 'Button 5 was pressed')
;~ 			GUICtrlDelete($b5)
;~ 			$priorityRecruiting[$currentIndex] = 5
;~ 			$currentIndex += 1
;~ 		Case $msg = $b6
;~ 			MsgBox(0, 'Testing', $priorityRecruiting[0] & "," & $priorityRecruiting[1]& "," & $priorityRecruiting[2]& "," & $priorityRecruiting[3]& "," & $priorityRecruiting[4])
;~ 			ExitLoop
;~ 	EndSelect
;~ WEnd
#ce

HotKeySet("^!r", "configureRecruiting")
HotKeySet("^!a", "algorithm")
HotKeySet("^!q", "quit")

Func searchForImageInArea($fileName, $x1, $y1, $right, $bottom, ByRef $x, ByRef $y, $tolerance)
	$result = _WaitForImageSearchArea($fileName, 1,1, $x1, $y1, $right, $bottom, $x, $y,$tolerance)
	If $result = 1 Then
		Return 1
	EndIf
	Return 0
EndFunc

Func searchForImage($fileName, ByRef $x, ByRef $y, $tolerance)
	$result = _WaitForImageSearch($fileName, 1, 1, $x, $y, $tolerance)
	If $result = 1 Then
		Return 1
	EndIf
	Return 0
EndFunc

Dim $priorityRecruiting[5] = [0,0,0,0,0]
Dim $NICHTS = 0, $MILIZ = 1, $BOGEN = 2, $PIKE = 3, $SCHWERT = 4, $KATAPULT = 5
Dim $MilizTopX=331, $BogenTopX=489, $PikeTopX=651, $SchwertTopX=813, $KatapultTopX=973
Dim $NUMBEROFVILLAGES = 2

Func configureRecruiting()
	Local $b1, $b2, $b3, $b4, $b5, $b6
	$width = 100
	GUICreate("Autorekrutierung", $width *6+20, 200)
	Opt("GUICoordMode", 2)

	$b1 = GUICtrlCreateButton("Bauernmiliz", 10, 150, $width)
	$b2 = GUICtrlCreateButton("Bogenschütze", 0, -1, $width)
	$b3 = GUICtrlCreateButton("Pikenier", 0, -1, $width)
	$b4 = GUICtrlCreateButton("Schwertkämpfer", 0, -1, $width)
	$b5 = GUICtrlCreateButton("Katapult", 0, -1, $width)
	$b6 = GUICtrlCreateButton("Fertig", 0, -1, $width)
	$currentIndex = 0

	GUISetState()
	While 1
		$msg = GUIGetMsg()
		Select
			Case $msg = $GUI_EVENT_CLOSE
				ExitLoop
			Case $msg = $b1
				GUICtrlDelete($b1)
				$priorityRecruiting[$currentIndex] = $MILIZ
				$currentIndex += 1
			Case $msg = $b2
				GUICtrlDelete($b2)
				$priorityRecruiting[$currentIndex] = $BOGEN
				$currentIndex += 1
			Case $msg = $b3
				GUICtrlDelete($b3)
				$priorityRecruiting[$currentIndex] = $PIKE
				$currentIndex += 1
			Case $msg = $b4
				GUICtrlDelete($b4)
				$priorityRecruiting[$currentIndex] = $SCHWERT
				$currentIndex += 1
			Case $msg = $b5
				GUICtrlDelete($b5)
				$priorityRecruiting[$currentIndex] = $KATAPULT
				$currentIndex += 1
			Case $msg = $b6
				MsgBox(0, 'Testing', $priorityRecruiting[0] & "," & $priorityRecruiting[1]& "," & $priorityRecruiting[2]& "," & $priorityRecruiting[3]& "," & $priorityRecruiting[4])
				ExitLoop
		EndSelect
	WEnd
	GUIDelete()
EndFunc

Func executeRecruiting()
	Local $x, $y
	If not $priorityRecruiting[0] Then Return
	For $i=1 To $NUMBEROFVILLAGES
		MouseClick("LEFT", 1167, 60)
		Sleep(200)
		MouseMove(0,0, 0)
		$result = searchForImage("MnDorf.png", $x, $y, 0)
		If $result Then
			MouseClick("LEFT", $x, $y)
		EndIf
		MouseMove(0,0, 0)
		$result = searchForImage("MnArmee.png", $x, $y, 0)
		If $result Then
			MouseClick("LEFT", $x, $y)
		EndIf
		startRecruiting()
	Next
EndFunc

Func startRecruiting()
	Local $x, $y
	For $type In $priorityRecruiting
		Select
			Case $type = $MILIZ
				While searchForImageInArea("RkEins.png", $MilizTopX, 481, $MilizTopX+46, 509, $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $BOGEN
				While searchForImageInArea("RkEins.png", $BogenTopX, 481, $BogenTopX+46, 509, $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $PIKE
				While searchForImageInArea("RkEins.png", $PikeTopX, 481, $PikeTopX+46, 509, $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $SCHWERT
				While searchForImageInArea("RkEins.png", $SchwertTopX, 481, $SchwertTopX+46, 509, $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $KATAPULT
				While searchForImageInArea("RkEins.png", $KatapultTopX, 481, $KatapultTopX+46, 509, $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $NICHTS
		EndSelect
	Next
EndFunc

Func algorithm()
	MsgBox(0, "trig", "gered", 1)
	While 1
		MsgBox(0, "Rec", "Recruiting", 1)
		executeRecruiting()
		MsgBox(0, "Rec", "Done", 1)
		Sleep(6000)
	WEnd
EndFunc

Func quit()
	Exit 0
EndFunc

While 1
	Sleep(100)
WEnd
