"""
    Anagram Shuffler generates a list of randomly selected letters based 
	roughly	on the normal frequency distribution of letters within English 
	and	generates anagrams from the list or a user-submitted phrase.
    
	Copyright (C) 2015  Jonathan Pharis <thejpharis@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

	The words found in the word list used in the anagrammer come from the 
	English Open Word List (EWOL) found at:
	http://dreamsteep.com/projects/the-english-open-word-list.html

	The EWOL makes use of the UK Advanced Cryptics Dictionary for which here is 
	licensing information:

		Copyright © J Ross Beresford 1993-1999. All Rights Reserved. 
		The following restriction is placed on the use of this publication: 
		if the UK Advanced Cryptics Dictionary is used in a software package 
		or redistributed in any form, the copyright notice must be prominently 
		displayed and the text of this document must be included verbatim.
	
	"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random

from word_list import *

letter_distribution = ['a','a','a','a','a','a','a','a',
                       'b','b',
					   'c','c','c',
					   'd','d','d','d',
					   'e','e','e','e','e','e','e','e','e','e','e','e','e',
					   'f','f',
					   'g','g',
					   'h','h','h','h','h','h',
					   'i','i','i','i','i','i','i',
					   'j',
					   'k',
					   'l','l','l','l',
					   'm','m','m',
					   'n','n','n','n','n','n','n',
					   'o','o','o','o','o','o','o','o',
					   'p','p',
					   'q',
					   'r','r','r','r','r','r',
					   's','s','s','s','s','s',
					   't','t','t','t','t','t','t','t','t',
					   'u','u','u',
					   'v',
					   'w','w','w',
					   'x',
					   'y','y',
					   'z']

vowels = ['a','e','i','o','u']

anagrams_list = []
   
class Anagram_Shuffler_App:

	def __init__(self, master):
		
		master.columnconfigure(0, weight=1)		
		master.rowconfigure(0, weight=1)
		
		content = ttk.Frame(master, padding=(3,3,12,12))
		content.grid(column=0, row=0, sticky=(N,S,E,W))
		content.columnconfigure(0, weight=1)
		content.rowconfigure(0, weight=1)
		frame = ttk.Frame(content)
		frame.grid(column=0, row=0, sticky=(N,S,E,W))
		frame.columnconfigure(0, weight=1)
		frame.columnconfigure(1, weight=1)
		frame.rowconfigure(0, weight=1)
		
		self.mygreen = "#7fb5a7"
		self.mybggreen = "#478978"
		
		self.style = ttk.Style()
		
		self.n = ttk.Notebook(frame)
		self.f1 = ttk.Frame(self.n)
		self.f2 = ttk.Frame(self.n)
		self.f3 = ttk.Frame(self.n)
		self.n.add(self.f1, text='Options')
		self.n.add(self.f2, text='Shuffled Letters')
		self.n.add(self.f3, text='Anagrams')
		self.n.grid(column=0, row=0, columnspan=2, pady=5, padx=5, sticky=(NSEW))
		self.f1.columnconfigure(0, weight=0)
		self.f1.columnconfigure(1, weight=0)
		self.f1.columnconfigure(2, weight=1)
		self.f1.columnconfigure(3, weight=1)
		self.f1.rowconfigure(0, weight=1)
		self.f1.rowconfigure(1, weight=0)
		self.f2.columnconfigure(0, weight=1)
		self.f2.rowconfigure(0, weight=1)
		self.f3.columnconfigure(0, weight=1)
		self.f3.rowconfigure(0, weight=1)
		
		self.shuffler = Button(
			frame, text='Shuffle!', bg='green', fg='white', 
			command=self.shuffle_letters
			)
		self.shuffler.grid(column=0, row=1, pady=5, padx=5, sticky=(W,E))
		self.shuffler.columnconfigure(0, weight=1)
		self.shuffler.rowconfigure(0, weight=1)
		
		self.quit = Button(
			frame, text='QUIT', fg='red', command=frame.quit
			)
		self.quit.grid(column=1, row=1, pady=5, padx=5, sticky=(W,E))
		self.quit.columnconfigure(0, weight=1)
		self.quit.rowconfigure(0, weight=1)
		
		self.count_label = ttk.Label(self.f1, justify=CENTER, text='Shuffle between 0-20 letters!\n(If 0, a random amount of\nletters will be shuffled.)')
		self.count_label.grid(column=0, row=0, pady=5, padx=5, sticky=(S))
		
		self.count = IntVar()
		self.c = ttk.Entry(self.f1, width=2, justify=CENTER, textvariable=self.count)
		self.c.grid(column=0, row=1, pady=5, padx=5, sticky=(N))
		
		self.count.set(0)
		
		options_frame = ttk.Labelframe(self.f1, text='Shuffling Options:')
		options_frame.grid(column=1, row=0, rowspan=3, sticky=(S))
		
		self.check_caps = BooleanVar()
		self.caps_checkbox = ttk.Checkbutton(
			options_frame, text='ALL CAPS', variable=self.check_caps
			)
		self.caps_checkbox.grid(column=0, row=0, pady=5, padx=5, sticky=(W))
		self.check_caps.set(TRUE)
		
		self.check_alphabetize = BooleanVar()
		self.alphabetize_checkbox = ttk.Checkbutton(
			options_frame, text='Alphabetize', variable=self.check_alphabetize
			)
		self.alphabetize_checkbox.grid(column=0, row=1, pady=5, padx=5, sticky=(W))
		
		self.check_no_vowels = BooleanVar()
		self.no_vowels_checkbox = ttk.Checkbutton(
			options_frame, text='No Vowels', variable=self.check_no_vowels
			)
		self.no_vowels_checkbox.grid(column=0, row=2, pady=5, padx=5, sticky=(W))
		
		self.check_perfect_anagram = BooleanVar()
		self.perfect_anagram_checkbox = ttk.Checkbutton(
			options_frame, text='True Anagrams Only', variable=self.check_perfect_anagram
			)
		self.perfect_anagram_checkbox.grid(column=0, row=3, pady=5, padx=5, sticky=(W))
		
		self.output_text = Text(self.f2, height=2, width=18, relief='sunken')
		self.output_text.config(state=NORMAL, font='Helvetica 22')
		self.output_text.tag_config('output', font='Helvetica 22', justify=CENTER, wrap=CHAR)
		self.output_text.grid(column=0, row=0, pady=5, padx=15, sticky=(NSEW))
		
		self.anagrammer_button = Button(
			self.f2, text='Anagram it!', bg=self.mybggreen, fg='white', command=self.anagrammer)
		self.anagrammer_button.grid(column=0, row=1, padx=5, pady=5, sticky=(S,E))
		
		self.anagrams = StringVar(anagrams_list)
		self.anagrams_box = Text(self.f3, height=6, width=15, relief='sunken')
		self.anagrams_box.grid(column=0, row=0, pady=5, padx=15, sticky=(NSEW))
		self.anagrams_box.config(state=DISABLED)
		self.anagrams_box.tag_config('anagrams_output', font='Helvetica 14', justify=LEFT, wrap=WORD)
		self.anagram_scroll = ttk.Scrollbar(self.f3, orient=VERTICAL, command=self.anagrams_box.yview)
		self.anagram_scroll.grid(column=1, row=0, sticky=(NS))
		self.anagrams_box['yscrollcommand'] = self.anagram_scroll.set
		
		ttk.Sizegrip().grid(column=0, row=0, sticky=(S,E))
		
	def shuffle_letters(self):
	
		self.n.select(self.f2)
		
		shuffle_count = self.count.get()
		caps_check = self.check_caps.get()
		alphabetize_check = self.check_alphabetize.get()
		no_vowels_check = self.check_no_vowels.get()
	
		shuffled_letters_blank = []
		shuffled_letters = shuffled_letters_blank
		
		if shuffle_count == 0:
			shuffle_count = random.randint(1,20)
			
		while shuffle_count > 0:
			letter = random.choice(letter_distribution)
			if no_vowels_check == TRUE:
				if letter not in vowels:
					shuffled_letters.append(letter)
					shuffle_count -= 1
			else:
				shuffled_letters.append(letter)
				shuffle_count -= 1
		
		if alphabetize_check == TRUE:
			shuffled_letters = sorted(shuffled_letters)
		
		shuffled_letters = ' '.join(shuffled_letters)
		
		if caps_check == TRUE:
			shuffled_letters = shuffled_letters.upper()
			
		self.output_text.config(state=NORMAL)
		self.output_text.delete(1.0, END)
		self.output_text.insert(END, shuffled_letters, 'output')
			
	def anagrammer(self):
		
		anagrams_list = []
		
		self.n.select(self.f3)
		
		perfect_anagram_check = self.check_perfect_anagram.get()
		
		shuffled_letters = list(self.output_text.get(1.0, END).lower())
		del(shuffled_letters[-1])
		shuffled_letters = list(filter((' ').__ne__, shuffled_letters))
			
		for letter in shuffled_letters:
			for word in eval('%s_words' % letter.upper()):
				if sorted(word) == sorted(shuffled_letters):
					if word not in anagrams_list:
						anagrams_list.append(word)
		
		if perfect_anagram_check == FALSE:
			for letter in shuffled_letters:
				for word in eval('%s_words' % letter.upper()):
					
					sorted_word = sorted(word)
					temp_shuffled_letters = shuffled_letters.copy()
					count = 0
					
					if word not in anagrams_list:
						for letter in sorted_word:
							if letter in temp_shuffled_letters:
								temp_shuffled_letters.remove(letter)
								count += 1
								if count == len(sorted_word):
									anagrams_list.append(word)
									count = 0
							else:
								count = 0
								break
									
		anagrams_list = sorted(anagrams_list)
		
		self.anagrams_box.config(state=NORMAL)
		self.anagrams_box.delete(1.0, END)
		
		for word in anagrams_list:
			self.anagrams_box.insert(END, word + '\n', 'anagrams_output')
		
		self.anagrams_box.config(state=DISABLED)
		
		
root = Tk()

root.title('Anagram Shuffler')

root.option_add('*tearOff', FALSE)

def Help():
	
	help_window = Toplevel(root)
	help_window.title('Help')
	
	help_window.columnconfigure(0, weight=1)
	help_window.rowconfigure(0, weight=1)
	
	help_text = Text(help_window, height=30, width=60, relief='sunken')
	help_text.grid(column=0, row=0, padx=5, pady=5, sticky=(NSEW))
	help_text.tag_config('help', font='Helvetica 11', justify=LEFT, wrap=WORD)
		
	help_text_scroll = ttk.Scrollbar(help_window, orient=VERTICAL, command=help_text.yview)
	help_text_scroll.grid(column=1, row=0, sticky=(NS))
	help_text['yscrollcommand'] = help_text_scroll.set
	
	help_text.config(state=NORMAL, wrap=WORD)
	help_text.insert(1.0, '''
Anagram Shuffler is meant as a tool for teachers to allow students to practice \
recalling vocabulary given a list of randomly selected letters.
	
Anagram Shuffler serves two functions:

(1) it generates a list of randomly selected letters based \
roughly	on the normal frequency distribution of letters within English and
(2) generates anagrams from the list or a user-submitted phrase.

	
1. Options Tab

To generate a list of randomly selected letters, enter a number between \
1 and 20 into the entry box on the options tab and click the "Shuffle!" button. \
If 0 is entered into the entrybox, a random number of letters (between 1 and 20) \
will be generated.
(NOTE: This button may be pressed from any other tab to generate a new set of \
letters with the same settings.)
	
ALL CAPS: 
This option displays the random letters in all capitals. \
It is selected by default.
	
Alphabetize: 
This option orders the random letters alphabetically. \
This can be helpful when working with longer lists of letters as it \
can be easier to see exactly how many of each letter there are if \
they are alphabetized.

No Vowels:
This option will force only consonants to be generated randomly. Select this \
option if you plan to allow students to use any and all vowels freely.

True Anagrams Only:
By default, the anagrammer will provide a list of words made of any combination \
of letters in the Shuffled Letters tab. Select this option to have to anagrammer \
return only words that use all the letters in the Shuffled Letters tab.


2. Shuffled Letters Tab

The list of randomly generated letters appears here.

To generate anagrams from the letters, click the "Anagram it!" button on this tab. \
Longer lists of letters can take a few seconds to generate the list of anagrams.

Any number of letters can be manually entered into this tab in order to generate 
anagrams from any word or phrase. Try your name!


3. Anagrams Tab

The list of anagrams generated appears here.

The list is ordered alphabetically, one word per line.

There are about 128,985 words contained in the word lists. Longer sequences of letters \
in the Shuffled Letters tab can generate very long lists of anagrams which can take \
considerable processing power and time, therefore please take caution when choosing \
to anagram very long phrases or letter combinations.

The word lists used by the anagrammer only contain words up to 10 letters in length, \
therefore the anagrammer will not produce words longer than 10 letters. All proper \
nouns, as well as words requiring diacritical symbols, hyphens, and apostrophes have \
been removed from the lists.

Please note: As the word lists were originally created for cryptanalysis, then \
modified for use in word games like Scrabble™, they contain some rare and strange \
words, some of which are never used in English conversation. When checking student's \
answers, it may be necessary to have them prove they understand the word by giving \
a definition or using it in a sentence.


Happy anagramming!
	''', 'help'
	)
	help_text.config(state=DISABLED)

def About():
		
	messagebox.showinfo(
		message= '''Copyright (C) 2015  Jonathan Pharis <thejpharis@gmail.com> 
		
This program is free software: you can redistribute it and/or modify it under \
the terms of the GNU General Public License as published by the Free Software \
Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT \
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS \
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with \
this program.  If not, see http://www.gnu.org/licenses/

Source code can be found at https://github.com/TheZahir/Anagram-Shuffler/
____________________________________________________________________

The anagrammer uses a word list derived from the English Open Word List (EWOL) \
found at: http://dreamsteep.com/projects/the-english-open-word-list.html

The EWOL makes use of the UK Advanced Cryptics Dictionary for which here is the \
required licensing information:

Copyright © J Ross Beresford 1993-1999. All Rights Reserved. 
The following restriction is placed on the use of this publication: \
if the UK Advanced Cryptics Dictionary is used in a software package \
or redistributed in any form, the copyright notice must be prominently \
displayed and the text of this document must be included verbatim.
		''', title='About'
		)
		
menubar = Menu(root)
menu_help = Menu(menubar)
menu_help.add_command(label='Help Contents', command=Help)
menu_help.add_command(label='About', command=About)
menubar.add_cascade(label='?', menu=menu_help)

root.config(menu=menubar)

app = Anagram_Shuffler_App(root)

root.mainloop()
root.destroy()