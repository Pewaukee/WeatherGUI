from tkinter import *
import requests
from bs4 import BeautifulSoup
from PIL import ImageTk, Image # for inserting an image as a label
from datetime import datetime # for comparing current time with local time of entered location

class MainApplication(object):
	def __init__(self, window) -> None:

		# set the window
		self.window = window

		# set the id for the session data, function cannot be accessed yet
		self.id = 0

		# create the canvas in order to insert images
		self.canvas = Canvas(self.window, width=400, height=400, bg='white')
		self.canvas.grid(row=1, column=1)

		# welcome label
		self.welcome_text = Label(self.window, text="Enter the city:\n(the more specific the better)", bg='white')
		self.welcome_text.place(x=20, y=20)
		# welcome label

		# Text box
		self.text = Text(self.window, width=17, height=1)
		font_tuple = ("Comic Sans", 12) # (font_name, font_size, font_type 'bold' etc;)
		self.text.configure(font=font_tuple, state=NORMAL) # state=NORMAL allows for deletion
		self.text.place(x=225,y=30)
		# Text box

		# weather display Label
		self.weather_label = Label(self.window, bg='white') # text is left blank to start
		self.weather_label.place(x=200, y=200, anchor=CENTER, width=250, height=60)
		# weather display Label

		# quit button
		self.quit_button = Button(self.window, text="Quit", command=self.quit)
		self.quit_button.place(x=175,y=350)
		# quit button

		# submit button
		self.submit_button = Button(window, text="Submit", command=self.submit)
		self.submit_button.place(x=175,y=75)
		# submit button

	def quit(self): # to exit the program
		print('quit button pressed')
		exit(1)

	def changeSkyImage(self, sky) -> None: # sky -> string
		conditions = {'mostly cloudy': 'mostlyCloudy.png', 'mostly sunny': 'mostlySunny.png', 
			'partly sunny': 'mostlyCloudy.png', 'partly cloudy': 'mostlySunny.png',
			'rain': 'rain.png', 'snow': 'snow.png', 'sunny': 'sunny.png', 'windy': 'windy.png', 
			'clear': 'clear.png', 'haze': 'haze.png', 'cloudy': 'cloudy.png', 'hail': 'hail.png'}
		for condition, pic in conditions.items(): # don't use conditions, need to access each dict item
			if (sky.__contains__(condition)):
				print(condition)
				path = f"weatherStates/{pic}"
				image = Image.open(path).resize((400,400))
				image = ImageTk.PhotoImage(image)
				self.canvas.create_image(200, 200, image=image)
				self.window.mainloop()


	def websiteReachError(self) -> None: # if an poor http response occurs, return back to white background
		path = f"weatherStates/white.png"
		image = Image.open(path).resize((400,400))
		image = ImageTk.PhotoImage(image)
		self.canvas.create_image(200, 200, image=image)
		self.window.mainloop()

	def get_soup(self, url) -> BeautifulSoup: # url -> string
		r = requests.get(url)
		if not r.status_code >= 200 and r.status_code < 300: # invalid http response, 300 goes into redirection
			self.weather_label.set('could not reach server')
			self.websiteReachError()
			return
		soup = BeautifulSoup(r.content, 'html.parser')
		return soup

	def add_to_file(self, filename, location, time, weather, sky) -> None: # filename, location, time, weather, sky -> string
		with open(filename, 'a') as f:
			cur_time = datetime.now().strftime("%H:%M:%S")
			string = f"Input time ~ {cur_time}\n--------------\n"
			string += f'Location: {location}\n'
			string += f'Local time (when submit was pressed): {time}\n'
			string += f'Weather: {weather}\n'
			string += f'Condition: {sky}\n\n'
			f.write(string)

	def submit(self) -> None:
		location = self.text.get('1.0', 'end-1c').strip() # get all the text from textbox
		print(location)
		self.text.delete('1.0', END) # delete the text from textbox in order to enter new location
			
		url = f"https://www.google.com/search?q=weather+{location}"
		soup = self.get_soup(url)

		#https://www.geeksforgeeks.org/how-to-extract-weather-data-from-google-in-python/
		try:
			# find gets first occurance
			weather = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
			# this contains time and sky description
			str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
		except AttributeError:
			self.weather_label['text'] = 'no information found'
			return # no information found about weather
 
		# format the data
		data = str.split('\n')
		time = data[0]
		sky = data[1]

		# change the weather_label text
		self.weather_label['text'] = (f"The weather in {location} is {weather}.\nCurrent condition is {sky} \nAll information for this session is available\n in session(#).txt")

		# add information to a text file
		self.add_to_file(f'session{self.id}.txt', location, time, weather, sky)

		#update the weather image to best match current weather
		self.changeSkyImage(sky.lower())

	def find_session_ID(self) -> None:
		"""
		every new session, want to get a new id to save the session's information
		to a new file named f'session{self.id}.txt'
		"""
		i = 0
		while True:
			try:
				with open(f'session{i}.txt', 'r') as f:
					i+=1
			except FileNotFoundError:
				self.id = i
				return

	def get_id(self) -> int:
		return self.id

def main():
	# create the window
	window = Tk()
	window.geometry("400x400") # window size
	# create a new MainApplication object in order to display stuff on screen
	obj = MainApplication(window) # window -> Tk
	obj.find_session_ID() # use a function call now to set the id for session(id).txt
	window.mainloop()

if __name__ == '__main__':
	main()



"""
additional notes:
may be better to use pack() or grid() instead of place()
don't use \ and enter when continuing strings, messes up proper label formatting
place(int x, int y) defines the coordinates where a tkinter object can go


also this is an attempt at trying to use weather.com, tried to use henderson as a 
default location and constructed a function only based off too specific a link, need
to have api work and click buttons through the program and be able to edit text fields 
on websites through code. May be possible with requests.post, but not sure


def find_henderson_weather(self): # not the way to do it
		# url for hourly henderson weather using weather.com
		url = f"https://weather.com/weather/hourbyhour/l/e54ab2e6e45e13b0ff72fe170814abbb05589fa91871f8f110df08f8cc9c27e0"
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')
		temp = soup.find_all('span', attrs={'data-testid':'TemperatureValue',
			'class':'DetailsSummary--tempValue--1K4ka'})
		temp = str(temp[0])
		print(temp[len(temp)-10:len(temp)-7])
"""