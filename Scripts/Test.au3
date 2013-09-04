#include<ImageSearch.au3>

;HotKeySet("p", "capture")
HotKeySet("f", "defineResearch")
HotKeySet("a", "algorithm")
HotKeySet("q", "quit")
Opt("MouseClickDownDelay", 100)
Dim $queueSize = 5
Dim $queue[$queueSize]= [""]
Dim $lastCheck
Dim $connection
Dim $myTurn
TCPStartup()


$c1 = 0
$v1 = 0
$c2 = 0
$v2 = 0
$count = 0

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
				;MsgBox(0, "Info", "error" & @error)
				reconnect()
			EndIf
		EndIf
	WEnd
EndFunc


Func capture()
	$pos = MouseGetPos()

	$count = $count +1
	If $count = 2 Then
		$c2 = $pos[0]
		$v2 = $pos[1]
		MsgBox(0, "Positions", "First: " & $c1 & "@" & $v1 & " Second: " & $c2 & "@" & $v2)
		$count = 0
	Else
		$c1 = $pos[0]
		$v1 = $pos[1]
	EndIf
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
		Send(@DesktopDir &"\Scripts")
		Sleep(500)
		Send("{ENTER}")
		Sleep(500)
		Send($name)
		Sleep(500)
		Send("{ENTER}")
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
			While Not searchForImage("FrSchieberUnten.png", $x, $y, 75) And $count <= 10
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
		executeResearch()
		Sleep(6000)
		schedule()
	WEnd
EndFunc


while 1
	Sleep(100)
WEnd