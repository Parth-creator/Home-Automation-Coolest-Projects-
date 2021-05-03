try:
	import pyfirmata as fir
	from rich import print
	from rich.console import Console
	import keyboard
except:
	import pip
	pip.main(['install', 'pyfirmata'])
	pip.main(['install', 'rich'])
	pip.main(['install', 'keyboard'])
	import pyfirmata as fir
import time

import pickle
import os
import getpass

os.system("cls")

console = Console()

try:
	board = fir.Arduino('COM8')
except:
	print("[red]COM8 is already taken or not plugged.\nTry re-plugging the Arduino[/red]")
	exit()

iterator = fir.util.Iterator(board)
iterator.start()


fanPin = board.get_pin('d:2:o')
buzzerPin = board.get_pin('d:4:o')
bluePin = board.get_pin('d:9:p')
greenPin = board.get_pin('d:10:p')
redPin = board.get_pin('d:11:p')

time.sleep(1)

timerCommand = "timer"
timerCommand.replace(" ", '')
timerCommand = timerCommand.lower()

fanCommand = "fan"
fanCommand.replace(" ", '')
fanCommand = fanCommand.lower()

rgbCommand = "rgb"
rgbCommand = rgbCommand.lower()

isTimerActive = False
secondsToWait = int

rgb_data = {
			"off" : [0, 0, 0],
			"red" : [10, 0, 0],
			"green": [0, 10, 0],
			"blue": [0, 0, 10],
			"magenta": [10, 0, 10],
			"orange": [10, 1, 0],
			"yellow": [10, 10, 0],
			"cyan": [0, 10, 10],
			"lightblue": [3, 3, 10],
			"deeppink": [10, 0, 1],
			"white": [10, 10, 10]
			}

timerDoc = """
			[magenta]
			This command is used to set timer using your command line.
			[cyan]Example:
				[magenta]>>timer 5[/magenta]
				[magenta]>>timer 5 * 60[/magenta][/cyan]
			NOTE: It should be in the format of "timer seconds"[/magenta]
"""

rgbDoc = """[magenta]
			This command is used to set the colour of RGB LED using your command line.
			[cyan]Example:
				[magenta]>>rgb 10 10 10[/magenta]
				[magenta]>>rgb white[/magenta]
			[/cyan]
			NOTE: It should be in the format of "rgb redValue greenValue blueValue"

			[cyan]Pre Loaded Colors:
				RED,
				GREEN,
				BLUE,
				MAGENTA,
				ORANGE,
				YELLOW,
				CYAN,
				LIGHTBLUE,
				DEEP PINK,
				WHITE
			[/cyan]

			[red]To turn off your LED type "rgb off".
			NOTE: RGB values should be from 0 to 10.[/red]
			[/magenta]
"""

fanDoc = """[magenta]
			This command is used to turn ON/OFF fan using your command line.
			[cyan]
			To turn ON the Fan "fan on".

			To turn OFF the Fan "fan off". [/cyan][/magenta]
"""

helpDoc = """[magenta]
			[cyan]FAN[/cyan]       Provides acces to DC-fan connected.
			[cyan]HELP[/cyan]      Provides Help information for the application.
			[cyan]QUIT[/cyan]      Closes the Application.
			[cyan]RGB[/cyan]       Provides acces to RGB LED.
			[cyan]TIMER[/cyan]     Provides a command-line timer.[/magenta]
"""
def string_to_rgb(argument):
	switcher = rgb_data
	return switcher.get(argument, "none")

def main():
	global user
	try:
		username = open('username', 'rb')
		password = open('password', "rb")
		user = pickle.load(username)
		passw = pickle.load(password)
		password.close()
		username.close()
	except Exception as e:
		username =  open("username", "ab")
		password = open('password', "ab")
		print("[cyan]Username: [/cyan]", end="")
		user = input()
		pickle.dump(user, username)
		username.close()
		print("[cyan]Password: [/cyan]", end="")
		passw = getpass.getpass(prompt="")
		pickle.dump(passw, password)
		password.close()
	while True:
		print(f"[green]root@{user.lower()}>>[/green]", end="")
		cmd = input("")
		cmd = cmd.lower()

		if cmd.replace(" ", "") == "quit" or cmd.lower() == "exit":
			break

		elif (cmd.replace(" ", "")) == rgbCommand:
			print(rgbDoc)

		elif (rgbCommand) in cmd:
			cmd = cmd.replace(rgbCommand, '')
			val = cmd.split()
			
			try:
				for i in range(0, len(val)):
					val[i] = int(val[i])
				if len(val) != 3 and len(val) != 0:
					print("[red]Syntax Error[/red]")
					continue	
				redPin.write(val[0]/10)
				greenPin.write(val[1]/10)
				bluePin.write(val[2]/10)
			except Exception as e:
				try:
					if (cmd.replace(" ", "")) != "":
						cmd = cmd.replace(" ", '')
						data = string_to_rgb(cmd)
						redPin.write(data[0]/10)
						greenPin.write(data[1]/10)
						bluePin.write(data[2]/10)
				except Exception as e:
					print("[red]Syntax Error[/red]")
					continue
		elif (cmd.replace(" ", "")) == timerCommand:
			print(timerDoc)

		elif (timerCommand) in cmd:
			cmd = cmd.replace(timerCommand, '')
			cmd = cmd.replace(" ", "")
			try:
				if cmd != "": 
					cmd = int(eval(cmd))
			except Exception as e:
				print("[red]Syntax Error[/red]")
				pass
			if cmd == "" or type(cmd) == str:
				pass
			else:
				print(f"Timer has been started for {str(cmd)} seconds")
				secondsToWait = cmd
				while secondsToWait != 0:
					if secondsToWait != 0:
						secondsToWait = secondsToWait - 1
						time.sleep(1)
					if secondsToWait == 0:
						buzzerPin.write(1)
						print("[cyan]Press Esc to stop...[/cyan]")
						keyboard.wait('esc')
						buzzerPin.write(0)

		elif cmd.replace(" ", "") == fanCommand:
			print(fanDoc)

		elif fanCommand in cmd:
			cmd = cmd.replace(" ", "")
			cmd = cmd.replace(fanCommand, "")
			
			if cmd == "on":
				fanPin.write(1)
			elif cmd == "off":
				fanPin.write(0)
			elif cmd == "":
				pass
			else:
				print("[red]Syntax Error[/red]")
		elif cmd == "help":
			print(helpDoc)
		elif cmd.replace(" ", "") == "cls":
			os.system("cls")
		elif cmd == "":
			pass
		else:
			print(f"[red]\"{cmd}\" is not recognized as an internal or external command[/red]")
				
main()
