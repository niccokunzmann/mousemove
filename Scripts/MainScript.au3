#include<ImageSearch.au3>
#include <GUIConstantsEx.au3>
#include <WindowsConstants.au3>

HotKeySet("^!p", "pause")
HotKeySet("^!c", "capture")
HotKeySet("^!r", "configureRecruiting")
HotKeySet("^!f", "defineResearch")
HotKeySet("^!a", "algorithm")
HotKeySet("^!q", "quit")
Opt("MouseClickDownDelay", 100)
Dim $priorityRecruiting[6] = [0,0,0,0,0,0]
$queueSize=10
Dim $queue[$queueSize]= [""]
Dim $lastCheck
Dim $connection
Dim $myTurn = False
Dim $NICHTS = 0, $MILIZ = 1, $BOGEN = 2, $PIKE = 3, $SCHWERT = 4, $KATAPULT = 5, $KUNDSCHAFTER =6
Dim $MilizTopX=331, $BogenTopX=489, $PikeTopX=651, $SchwertTopX=813, $KatapultTopX=1019, $KundschafterTopX=995
Dim $NUMBEROFVILLAGES = 2
Dim $MyWinCenterY = 878/2
Dim $MyWinCenterX =1600/2
TCPStartup()

Func startServer()
	$result = ShellExecute(@WorkingDir & "\..\mousemove\schedule.py")
	If $result Then
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
			If $result And Not @error Then
				$myTurn = True
				Return
			Elseif @error Then
				MsgBox(0, "Info", "Something went wrong: error" & @error, 1)
				reconnect()
			Else
				ContinueLoop
			EndIf
		EndIf
	WEnd
EndFunc



$c2 = 0
$v2 = 0
Func capture()
	$pos = MouseGetPos()
	$c2 = $pos[0]
	$v2 = $pos[1]
	MsgBox(0, "Positions", "First: " & $c2 & "@" & $v2)
EndFunc


Func isResearching()
	$x1 = 0
	$x2 = 0
	Dim $x, $y
	$result = searchForImage("MnForschung.png", $x1, $x2, 0)
	If $result = 1 Then
		MouseClick("LEFT", $x1, $x2)
		sleep(500)
	EndIf

	$result = searchForImage("FrHintergrund.png", $x1, $x2, 0)
	If $result = 1 Then
		Return False
	Else
		Return True
	EndIf
EndFunc

Func configureRecruiting()
	Local $b1, $b2, $b3, $b4, $b5, $b6, $b7
	$width = 100
	GUICreate("Autorekrutierung", $width *6+20, 200)
	Opt("GUICoordMode", 2)

	$b1 = GUICtrlCreateButton("Bauernmiliz", 10, 150, $width)
	$b2 = GUICtrlCreateButton("Bogenschütze", 0, -1, $width)
	$b3 = GUICtrlCreateButton("Pikenier", 0, -1, $width)
	$b4 = GUICtrlCreateButton("Schwertkämpfer", 0, -1, $width)
	$b5 = GUICtrlCreateButton("Katapult", 0, -1, $width)
	$b7 = GUICtrlCreateButton("Kundschafter", 0, -1, $width)
	$b6 = GUICtrlCreateButton("Fertig",-1, 0, $width)
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
			Case $msg = $b7
				GUICtrlDelete($b7)
				$priorityRecruiting[$currentIndex] = $KUNDSCHAFTER
				$currentIndex += 1
			Case $msg = $b6
				ExitLoop
		EndSelect
	WEnd
	GUIDelete()
EndFunc

Func defineResearch()
	Dim $x1, $x2
	Run("C:\Windows\sysnative\SnippingTool.exe")
	WinWaitActive("Snipping Tool")
	while 1
		Sleep(300)
		$result = _ImageSearch("Pen.png", 1, $x1, $x2, 0)
		If $result = 1 Then ExitLoop

	WEnd
	WinClose("Snipping Tool")
	WinWaitActive("Snipping Tool", "Ja")
	Send("!j")
	WinWaitActive("Speichern unter")
	Local $name = ""
	For $i = 0 To $queueSize-1
		If $queue[$i] = "" Then
			$name = "r" & $i
			$queue[$i] = $name & ".png"
			ExitLoop
		EndIf
	Next
	If $name Then
		ClipPut(@WorkingDir&"\"&$name)
		Send("^v")
		Sleep(500)
		Send("{ENTER}")
		Sleep(500)
		WinWaitActive("Speichern unter bestätigen", "Ja", 3)
		If WinActive("Speichern unter bestätigen", "Ja") Then
			Send("!j")
		EndIf
	Else
		Send("{ESC}")
		Sleep(100)
		WinClose("Snipping Tool")
		WinWaitActive("Snipping Tool", "Ja")
		Send("!n")
		MsgBox(0, "Notice", "Queue for research full", 2)
		Return False
	EndIf
EndFunc

Func executeRecruiting()
	Local $x, $y
	If not $priorityRecruiting[0] Then Return
	For $i=1 To $NUMBEROFVILLAGES
		$result = searchForImage("MnPfeil.png", $x, $y, 0)
		If $result Then
			MouseClick("LEFT", $x, $y)
			Sleep(200)
		EndIf
		MouseMove(100,100, 0)
		$result = searchForImage("MnDorf.png", $x, $y, 0)
		If $result Then
			MouseClick("LEFT", $x, $y)
		EndIf
		MouseMove(100,100, 0)
		startRecruiting()
	Next
EndFunc

Func startRecruiting()
	Local $x, $y
	For $type In $priorityRecruiting
		$result = searchForImage("MnArmee.png", $x, $y, 0)
		If $result Then
			MouseClick("LEFT", $x, $y)
			Sleep(100)
		EndIf
		Select
			Case $type = $MILIZ
				While searchForImageInArea("RkEins.png", getCoordX($MilizTopX), getCoordY(481), getCoordX($MilizTopX)+46, getCoordY(509), $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $BOGEN
				While searchForImageInArea("RkEins.png", getCoordX($BogenTopX), getCoordY(481), getCoordX($BogenTopX)+46, getCoordY(509), $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $PIKE
				While searchForImageInArea("RkEins.png", getCoordX($PikeTopX), getCoordY(481), getCoordX($PikeTopX)+46, getCoordY(509), $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $SCHWERT
				While searchForImageInArea("RkEins.png", getCoordX($SchwertTopX), getCoordY(481), getCoordX($SchwertTopX)+46, getCoordY(509), $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $KATAPULT
				While searchForImageInArea("RkEins.png", getCoordX($KatapultTopX), getCoordY(481), getCoordX($KatapultTopX)+46, getCoordY(509), $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $KUNDSCHAFTER
				$result = searchForImage("MnReiter.png", $x, $y, 0)
				If $result Then
					MouseClick("LEFT", $x, $y)
					Sleep(300)
				EndIf
				While searchForImageInArea("RkEins.png", getCoordX($KundschafterTopX), getCoordY(481), getCoordX($KundschafterTopX)+46, getCoordY(509), $x, $y, 50)
					MouseClick("LEFT",$x, $y)
					Sleep(200)
				WEnd
			Case $type = $NICHTS
		EndSelect
	Next
EndFunc

Func executeResearch()
	If $queue[0] = "" Then Return
	If Not $lastCheck Then
		$lastCheck = TimerInit()
		openResearch()
		If Not isResearching() Then
			startResearch()
		EndIf
	ElseIf TimerDiff($lastCheck) >= 30000 Then ;900000ms are 15 minutes
		$lastCheck = TimerInit()
		openResearch()
		If Not isResearching() Then
			startResearch()
		EndIf
	EndIf
EndFunc

Func levelUp()
	Local $x, $y
	$result = searchForImage("ableForLevel.png", $x, $y, 100)
	If $result = 1 Then
		MouseClick("LEFT", $x, $y)
		Sleep(500)
		$result = searchForImage("levelUp.png", $x, $y, 100)
		If $result = 1 Then
			MouseClick("LEFT", $x, $y)
			Sleep(10000)
		EndIf
	EndIf
EndFunc

Func getCoordX( $x)
	$result = WinGetClientSize("Stronghold Kingdoms - Welt 3")
	$newX = $x -$MyWinCenterX + $result[0]/2
	Return $newX
EndFunc

Func getCoordY( $y)
	$result = WinGetClientSize("Stronghold Kingdoms - Welt 3")
	$newY = $y - $MyWinCenterY + $result[1]/2
	Return $newY
EndFunc

Func startResearch()
	Local $x, $y
	Dim $x1, $y1
	Dim $Fields[4] = ["FrGewerbe.png", "FrMilitär.png", "FrLandwirtschaft.png", "FrBildung.png"]
	For $field in $Fields
		$result = searchForImage($field, $x, $y, 0)
		If $result = 1 Then
			MouseClick("LEFT", $x, $y)
			Sleep(500)
		EndIf
		Local $x1, $y1
		$result = searchForImage("FrSchieber.png", $x1, $y1, 0)
		$count = 0
		If $result = 1 Then
			While $count <= 10
				If searchForImage("FrSchieberUnten.png", $x, $y, 75) Then
					$result = searchForImage($queue[0], $x, $y, 0)
					If $result = 1 Then
						MouseClick("LEFT", $x, $y)
						Sleep(500)
						updateQueue()
						Return
					EndIf
					ExitLoop
				EndIf
				$result = searchForImage($queue[0], $x, $y, 0)
				If $result = 1 Then
					MouseClick("LEFT", $x, $y)
					Sleep(500)
					updateQueue()
					Return
				Else
					MouseClickDrag("LEFT", $x1, $y1, $x1, $y1 +100)
					$y1 += 100
					$count += 1
					Sleep(500)
				EndIf
			WEnd
		EndIf
	Next
EndFunc



Func updateQueue()
	For $i = 1 To $queueSize-1
		$queue[$i-1] = $queue[$i]
	Next
	$queue[$queueSize-1] = ""
EndFunc

Func searchForImage($fileName, ByRef $x, ByRef $y, $tolerance)
	$result = _WaitForImageSearch($fileName, 1, 1, $x, $y, $tolerance)
	If $result = 1 Then
		Return 1
	EndIf
	Return 0
EndFunc

Func searchForImageInArea($fileName, $x1, $y1, $right, $bottom, ByRef $x, ByRef $y, $tolerance)
	$result = _WaitForImageSearchArea($fileName, 1,1, $x1, $y1, $right, $bottom, $x, $y,$tolerance)
	If $result = 1 Then
		Return 1
	EndIf
	Return 0
EndFunc

Func openResearch()
	Local $x, $y
	$result = searchForImage("MnForschung.png", $x, $y, 0)
	If $result = 1 Then
		MouseClick("LEFT", $x, $y)
		sleep(500)
	EndIf
	$result = searchForImage("FrListe.png", $x, $y, 0)
	If $result = 1 Then
		MouseClick("LEFT", $x, $y)
		sleep(500)
	EndIf
EndFunc

Func openGame()
	WinActivate("Stronghold Kingdoms - Welt 3")
	WinWaitActive("Stronghold Kingdoms - Welt 3")
EndFunc

Func gameActive()
	$active=WinActive("Stronghold Kingdoms - Welt 3")
	If $active = 0 Then
		Return False
	EndIf
	Return True
EndFunc

Func quit()
	Exit 0
EndFunc

Func algorithm()
	While 1
		schedule()
		MouseMove(100, 100, 0)
		Sleep(100)
		executeResearch()
		Sleep(500)
		levelUp()
		Sleep(500)
		executeRecruiting()
		Sleep(6000)
	WEnd
EndFunc

Func pause()
	While 1
		schedule()
		Sleep(100)
	WEnd
EndFunc


while 1
	Sleep(100)
WEnd