#!/usr/bin/env python
'''
-------------------------------------------------------------------
| __FILE__:            gui.py                                     |
| __AUTHOR__:          Anthony Vidovic, 1130891                   |
|                      Tony Ngo, 1142414                          |
| __PROJECT__:         COVID-19 Data Analysis and Visualization   |
| __LAST UPDATED__:    Sunday, March 28th, 2021                   |
-------------------------------------------------------------------
| __SUMMARY__:         A graphical user interface that allows     |
|                      the user view plotted covid data.          |  
|                                                                 |
| __RUN WITH__:        python gui.py                              |
|                                                                 |
| __DATA__:            plot.PyFiles *.py (all files in directory) |
|                                                                 |
| __REFERENCES__:      below comments marked with 'Reference'     |
|                      have been used from an external source.    |
|                      Details will be provided in the comment.   |
-------------------------------------------------------------------
'''

# --------------------#
#      Libraries      #
# --------------------#
import subprocess
import datetime
import time
import tkinter as tk
from tkinter import ttk
from os import path
from PIL import Image, ImageTk

# --------------------#
#   Global Variables  #
# --------------------#
phu_names = [
        '', 'Algoma', 'Brant', 'Durham', 'Grey Bruce',
        'Haldimand-Norfolk', 'Haliburton, Kawartha', 'Halton',
        'Hamilton', 'Hastings and Prince Edward', 'Chatham-Kent',
        'Kingston, Frentenac and Lennox & Addington', 'Lambton', 'Leeds, Greenville',
        'Middlesex-London', 'Niagra Region', 'North Bay Parry Sound',
        'Northwestern', 'Ottawa', 'Peel', 'Peterborough', 'Porcupine',
        'Renfrew County', 'Eastern Ontario', 'Simcoe Muskoka', 'Sudbury',
        'Thundery Bay', 'Timiskaming', 'Waterloo', 'Wellington-Dufferin-Guelph', 'Windsor-Essex', 'York', 'Toronto', 'Southwestern', 'Huron Perth']

# --------------------#
#       Methods       #
# --------------------#
def run_file(filename, arg1, arg2):
    '''Runs the a given file

    param - filename: the file to run
    param - arg1: command line arg 1
    param - arg2: command line arg 2
    '''
    subprocess.Popen(["python", filename, arg1, arg2])

def swap_frame(open_frame,close_frame):
    '''Swaps two tkinter frames

    param - open_frame: the new frame to show
    param - close_frame: the old frame to close
    '''
    open_frame.tkraise()
    open_frame.grid()
    close_frame.grid_forget()

def gender_percentage_combobox_value(event):
    '''sets the current selected combo box value to phu_code_tk 

    param - event: the currently selected combo box value
    '''
    global phu_code_tk
    phu_code_tk = gender_percentage_dropdown.get()

def start_progress(frame, next_frame):
    '''sets the current selected combo box value to phu_code_tk 

    param - frame: current frame
    param - next_frame: next frame after progress
    '''
    
    progress_bar = ttk.Progressbar(frame, orient='horizontal', length=300,mode='determinate')
    progress_bar.place(x=367,y=510)
    progress_label = tk.Label(frame,font='monospace', bg='#FEFEFE')
    progress_label.config(text="")
    progress_label.place(x=497,y=465)
    progress_bar['value'] = 0

    rocket_image = tk.PhotoImage(file='GUIphotos/rocket_image.gif')
    rocket_label = tk.Label(frame, image=rocket_image, bd=0, bg='#466B91')
    

    #---Referenced code below---#
    '''
    _TITLE_:     create complete progress_bar with python tkinter
    _LINK_:      https://www.youtube.com/watch?v=isEQOipTbHM
    _SECTION_:   from 5:20, to 7:05 in video
    _AUTHORS_:   Delta electro Code
    _DATE_:      Jun 15, 2020
    '''
    for i in range(1,102,1):
        rocket_label.place(x=345+i*3-10, y=500)
        progress_bar['value'] = i
        window.update_idletasks()
        progress_label.config(text=str(i)+"%")
        time.sleep(0.05)
    #--End of referenced code--#
    rocket_label.destroy()
    progress_label.destroy()
    progress_bar.destroy()
    time.sleep(0.5)
    swap_frame(next_frame, frame)

def validate_age_entry(frame, next_frame, filename):
    '''Valdiates the age entered for question 2

    param - frame: the current frame
    param - next_frame: the next frame after validation
    param - filename: the file to run, passed into run_file()
    '''
    from_age = age_range_from_entry.get()
    to_age = age_range_to_entry.get()

    # If the age range given is valid
    if (from_age < to_age) and (from_age.isdigit() and to_age.isdigit()) and (int(from_age) in range(10,100,10) and int(to_age) in range(10,100,10)):
        run_file(filename, from_age, to_age)
        start_progress(frame, next_frame)                 
    else:
        invalid = tk.Label(frame, text="Invalid Entry", fg='red', bg='#FEFEFE',font=('monospace',9,'bold'))
        invalid.place(x=470,y=335)
        frame.after(3000, invalid.destroy)
 
def validate_date_entry(frame, next_frame, filename):
    '''Valdiates the date entered for question 3

    param - frame: the current frame
    param - next_frame: the next frame after validation
    param - filename: the file to run, passed into run_file()
    return: only returns if invalid input
    '''
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    from_date = caseTrendInRange_start_date.get()
    to_date = caseTrendInRange_end_date.get()

    try:  
        from_year = int(from_date.partition('-')[0])
        from_month  = int(from_date.partition('-')[2])
        to_year = int(to_date.partition('-')[0])
        to_month  = int(to_date.partition('-')[2])
    except:
        invalid = tk.Label(frame, text="Invalid Entry", fg='red', bg='#FEFEFE',font=('monospace',9,'bold'))
        invalid.place(x=470,y=335)
        frame.after(3000, invalid.destroy)
        return

    # 4 bools below used to shorten if condition
    size = len(from_date) == 7 and len(to_date) == 7
    in_range = ((from_year > 2019 and to_year > 2019) and (from_year and to_year <= current_year) and (from_month in range(1,13,1) and to_month in range(1,13,1)))
    order = (from_year < to_year) or (from_year == to_year and from_month < to_month)
    future_month = (to_year == current_year and to_month <= current_month) or to_year < current_year
    
    # If dates are valid show plot
    if size and in_range and order and future_month:
        run_file(filename, from_date, to_date)
        start_progress(frame, next_frame)
    else:
        invalid = tk.Label(frame, text="Invalid Entry", fg='red', bg='#FEFEFE',font=('monospace',9,'bold'))
        invalid.place(x=470,y=335)
        frame.after(3000, invalid.destroy)
    
def show_plot(frame, file, x, y):
    '''shows the plot for the corresponding question

    param - frame: the frame to plot on
    param - file: the plot file
    param - x: x-loc of where to place plot
    param - y: y-loc of where to place plot
    '''   
    # See if file exists
    if path.exists("/home/runner/PROJECTL01-CIS2250-3/plots/"+file): 
        load = Image.open("/home/runner/PROJECTL01-CIS2250-3/plots/"+file)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(frame, image=render, bd=2, bg="#FEFEFE")
        img.image = render
        img.place(x=x,y=y)  
    else:
        print("plot was not made, error error error...")
        
def find_ID (id_name):
    '''converts the chosen city to its PHU_ID

    param - id_name: the city name
    Return: the ID
    '''  
    phu_names = [
            ['2226','Algoma'], ['2227','Brant'], ['2230', 'Durham'], ['2233', 'Grey Bruce'],
            ['2234', 'Haldimand-Norfolk'], ['2235', 'Haliburton, Kawartha'], ['2236',   'Halton'], ['2237', 'Hamilton'], ['2238', 'Hastings and Prince Edward'], ['2240', 'Chatham-Kent'], ['2241', 'Kingston, Frentenac and Lennox & Addington'], ['2242', 'Lambton'], ['2243', 'Leeds, Greenville'], ['2244', 'Middlesex-London'], ['2246', 'Niagra Region'], ['2247', 'Northy Bay Parry Sound'], ['2249', 'Northwestern'], ['2251', 'Ottawa'], ['2253', 'Peel'], ['2255', 'Peterborough'], ['2256', 'Porcupine'], ['2257', 'Renfrew County'], ['2258', 'Eastern Ontario'], ['2260', 'Simcoe Muskoka'], ['2261', 'Sudbury'], ['2262', 'Thundery Bay'], ['2263', 'Timiskaming'], ['2265', 'Waterloo'], ['2266', 'Wellington-Dufferin-Guelph'], ['2268', 'Windsor-Essex'], ['2270', 'York'], ['3895', 'Toronto'], ['4913', 'Southwestern'], ['5183', 'Huron Perth']]

    for i in range(0, len(phu_names)-1):
        if (id_name.lower() == phu_names[i][1].lower()):
            return phu_names[i][0]

    

# --------------------#
#       Main Loop     #
# --------------------#
if __name__ == "__main__":

    # Setup window properties
    width = 1000
    height = 600
    window = tk.Tk()
    window.geometry('1000x600')
    window.maxsize(width, height)
    window.title("Buenos Aires")
    window.configure(bg="#FEFEFE")
    window.resizable(False,False)
    

    # Initialize frames
    home_frame = tk.Frame(window, width=width, height=height,bg="#FEFEFE")
    frame1 = tk.Frame(window, width=width, height=height,bg="#FEFEFE")
    gender_percentage_frame = tk.Frame(window, width=width, height=height,bg="#FEFEFE")
    age_range_frame = tk.Frame(window, width=width, height=height,bg="#FEFEFE")
    caseTrendInRange_frame = tk.Frame(window, width=width, height=height,bg="#FEFEFE")
    LTCHRatio_frame = tk.Frame(window, width=width, height=height,bg="#FEFEFE")
    gender_percentage_plot_frame = tk.Frame(window, width=width, height=height,bg="#FEFEFE")
    age_range_plot_frame = tk.Frame(window, width=width, height=height,bg="#FEFEFE")
    caseTrendInRange_plot_frame = tk.Frame(window, width=width, height=height,bg="#FEFEFE")
    LTCHRatio_plot_frame = tk.Frame(window, width=width, height=height,bg="#FEFEFE")

    # Create all Image variables    
    back_button_image = tk.PhotoImage(file="GUIphotos/backButton.gif")
    background_image = tk.PhotoImage(file='GUIphotos/homeBackground.gif')
    title_image = tk.PhotoImage(file="GUIphotos/frame1Title.gif")
    gender_percentage_buttom_image = tk.PhotoImage(file="GUIphotos/gender_percentage_button.png")
    age_range_buttom_image = tk.PhotoImage(file="GUIphotos/age_range_button.png")
    caseTrendInRange_buttom_image = tk.PhotoImage(file="GUIphotos/caseTrendInRange_button.png")
    LTCHRatio_buttom_image = tk.PhotoImage(file="GUIphotos/LTCHRatio_button.png")
    start_button_image = tk.PhotoImage(file="GUIphotos/startButton.gif")

    #======START OF DIFFERENT FRAMES======#

    #==home_frame==#
    home_frame.grid()
    image_label = tk.Label(home_frame, image=background_image, bd=0, highlightthickness=0).place(x=0,y=0)

    # start button on homepage
    home_button = tk.Button(home_frame, image=start_button_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE',padx=80, pady=40,command=lambda:swap_frame(frame1,home_frame), anchor='w', bd=0, highlightthickness = 0)
    home_button.place(x=180, y=330)
    #=====end=====#

    #==frame1==#
    # Title
    title_label = tk.Label(frame1, image=title_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', padx=0, pady=0, anchor='n', bd=0, highlightthickness = 0)
    title_label.place(x=width/4, y=10)

    # Back button
    back_button = tk.Button(frame1, image=back_button_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', padx=0, pady=0,command=lambda:swap_frame(home_frame,frame1), anchor='nw', bd=0,highlightthickness = 0)
    back_button.place(x=10, y=10)

    # Number texts
    num1_text = tk.Label(frame1, text="1", bd=0, bg='#FEFEFE', font=('Courier', 10, 'bold')).place(x=380,y=180)
    num2_text = tk.Label(frame1, text="2", bd=0, bg='#FEFEFE', font=('Courier', 10, 'bold')).place(x=600,y=180)
    num3_text = tk.Label(frame1, text="3", bd=0, bg='#FEFEFE', font=('Courier', 10, 'bold')).place(x=380,y=330)
    num4_text = tk.Label(frame1, text="4", bd=0, bg='#FEFEFE', font=('Courier', 10, 'bold')).place(x=600,y=330)

    # gender_percentage button
    gender_percentage_button = tk.Button(frame1, image=gender_percentage_buttom_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', command=lambda:swap_frame(gender_percentage_frame,frame1), anchor='w', bd=0,highlightthickness = 0)
    gender_percentage_button.place(x=310, y=200)

    # age_range button
    age_range_button = tk.Button(frame1, image=age_range_buttom_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', command=lambda:swap_frame(age_range_frame,frame1), anchor='w', bd=0,highlightthickness = 0)
    age_range_button.place(x=530, y=200)

    # caseTrendInRange button
    caseTrendInRange_button = tk.Button(frame1, image=caseTrendInRange_buttom_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', command=lambda:swap_frame(caseTrendInRange_frame,frame1), anchor='w', bd=0,highlightthickness = 0)
    caseTrendInRange_button.place(x=310, y=350)

    # LTCHRatio button
    LTCHRatio_button = tk.Button(frame1, image=LTCHRatio_buttom_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', command=lambda:swap_frame(LTCHRatio_frame,frame1), anchor='w', bd=0,highlightthickness = 0)
    LTCHRatio_button.place(x=530, y=350)
    #=====end=====#


    #==gender_percentage_frame with gender_percentage_plot_frame==#
    # Title
    gender_percentage_title = tk.Label(gender_percentage_frame, text="Fill in the required information to plot the data", bg='#FEFEFE', bd=0, font=('Courier', 13, 'bold')).place(x=250,y=100)

    # Back button
    gender_percentage_back_button = tk.Button(gender_percentage_frame, image=back_button_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', padx=0, pady=0,command=lambda:swap_frame(frame1,gender_percentage_frame), anchor='nw', bd=0,highlightthickness = 0)
    gender_percentage_back_button.place(x=10, y=10)

    # Dropdown combobox
    gender_percentage_text = tk.Label(gender_percentage_frame, text="Select a City: ", bg='#FEFEFE', bd=0, font=('Courier', 10)).place(x=320,y=240)
    gender_percentage_dropdown = ttk.Combobox(gender_percentage_frame, value=phu_names, state='readonly', width=29)
    gender_percentage_dropdown.current(0)
    gender_percentage_dropdown.place(x=450,y=240)
    gender_percentage_dropdown.bind("<<ComboboxSelected>>", gender_percentage_combobox_value)

    # Title for gender_percentage_plot_frame
    gender_percentage_plot_title = tk.Label(gender_percentage_plot_frame, text="Percentage of outbreak related cases per gender", bg="#FEFEFE", bd=0, font=('Courier', 15, 'bold')).place(x=240,y=15)

    # Back button for gender_percentage_plot_frame
    gender_percentage_plot_back_button = tk.Button(gender_percentage_plot_frame, image=back_button_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', padx=0, pady=0,command=lambda:swap_frame(gender_percentage_frame,gender_percentage_plot_frame), anchor='nw', bd=0,highlightthickness = 0)
    gender_percentage_plot_back_button.place(x=10, y=10)

    # Generate button
    generate_button_1 = tk.Button(gender_percentage_frame, text='Generate Plot', bg='#383838', fg='#FEFEFE', bd=0, font=('Courier', 10), highlightthickness = 0, padx=50, pady=20,command=lambda:[run_file('plot.PyFiles/genderPercentage.py', find_ID(phu_code_tk), phu_code_tk),start_progress(gender_percentage_frame, gender_percentage_plot_frame), show_plot(gender_percentage_plot_frame, 'genderPercentage_plot.png', 200,120)])
    generate_button_1.place(x=415, y=370)
    #=====End=====#


    #==age_range_frame with age_range_plot_frame==#
    # Title
    age_range_title = tk.Label(age_range_frame, text="Fill in the required information to plot the data", bg='#FEFEFE', bd=0, font=('Courier', 13, 'bold')).place(x=250,y=100)    

    # Back button
    age_range_back_button = tk.Button(age_range_frame, image=back_button_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', padx=0, pady=0,command=lambda:swap_frame(frame1,age_range_frame), anchor='nw', bd=0,highlightthickness = 0)
    age_range_back_button.place(x=10, y=10)

    age_range_text = tk.Label(age_range_frame, text="Entry Choices: 10, 20, 30, 40, 50, 60, 70, 80, 90", bg='#FEFEFE', bd=0, font=('Courier', 10, 'bold')).place(x=340,y=200)
    age_range_text1 = tk.Label(age_range_frame, text="Enter Start age: ", bg='#FEFEFE', bd=0, font=('Courier', 10)).place(x=350,y=250)
    age_range_text2 = tk.Label(age_range_frame, text="Enter End age: ", bg='#FEFEFE', bd=0, font=('Courier', 10)).place(x=360,y=290)

    # Entry boxes
    age_range_from_entry = tk.Entry(age_range_frame)
    age_range_from_entry.place(x=500,y=250)
    age_range_to_entry = tk.Entry(age_range_frame)
    age_range_to_entry.place(x=500,y=290)

    # Generate button
    generate_button_2 = tk.Button(age_range_frame, text='Generate Plot', bg='#383838', fg='#FEFEFE', bd=0, font=('Courier', 10), highlightthickness = 0, padx=50, pady=20,command=lambda:[validate_age_entry(age_range_frame,age_range_plot_frame, 'plot.PyFiles/ageRange.py'), show_plot(age_range_plot_frame, 'ageRange_plot.png', 80,-40)])
    generate_button_2.place(x=400, y=370)

    # Back button for age_range_plot_frame
    age_range_plot_back_button = tk.Button(age_range_plot_frame, image=back_button_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', padx=0, pady=0,command=lambda:swap_frame(age_range_frame,age_range_plot_frame), anchor='nw', bd=0,highlightthickness = 0)
    age_range_plot_back_button.place(x=10, y=10)
    #=====End=====#


    #==caseTrendInRange_frame with caseTrendInRange_plot_frame==#
    # Title
    caseTrendInRange_title = tk.Label(caseTrendInRange_frame, text="Fill in the required information to plot the data", bg='#FEFEFE', bd=0, font=('Courier', 13, 'bold')).place(x=250,y=100)

    # Back button
    caseTrendInRange_back_button = tk.Button(caseTrendInRange_frame, image=back_button_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', padx=0, pady=0,command=lambda:swap_frame(frame1,caseTrendInRange_frame), anchor='nw', bd=0,highlightthickness = 0)
    caseTrendInRange_back_button.place(x=10, y=10)
    
    caseTrendInRange_text = tk.Label(caseTrendInRange_frame, text="(YYYY-MM)", bg='#FEFEFE', bd=0, font=('Courier', 10, 'bold')).place(x=460,y=200)
    caseTrendInRange_text1 = tk.Label(caseTrendInRange_frame, text="Enter Start date: ", bg='#FEFEFE', bd=0, font=('Courier', 10)).place(x=350,y=250)
    caseTrendInRange_text2 = tk.Label(caseTrendInRange_frame, text="Enter To date: ", bg='#FEFEFE', bd=0, font=('Courier', 10)).place(x=360,y=290)

    # Entry boxes
    caseTrendInRange_start_date = tk.Entry(caseTrendInRange_frame)
    caseTrendInRange_start_date.place(x=500,y=250)
    caseTrendInRange_end_date = tk.Entry(caseTrendInRange_frame)
    caseTrendInRange_end_date.place(x=500,y=290)

    # Generate button
    generate_button_3 = tk.Button(caseTrendInRange_frame, text='Generate Plot', bg='#383838', fg='#FEFEFE', bd=0, font=('Courier', 10), highlightthickness = 0, padx=50, pady=20, command=lambda:[validate_date_entry(caseTrendInRange_frame, caseTrendInRange_plot_frame, 'plot.PyFiles/caseTrendInRange.py'),show_plot(caseTrendInRange_plot_frame, 'caseTrendInRange_plot.png', 60,0)])
    generate_button_3.place(x=415, y=370)

    # Back button for caseTrendInRange_plot_frame
    caseTrendInRange_plot_back_button = tk.Button(caseTrendInRange_plot_frame, image=back_button_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', padx=0, pady=0,command=lambda:swap_frame(caseTrendInRange_frame,caseTrendInRange_plot_frame), anchor='nw', bd=0,highlightthickness = 0)
    caseTrendInRange_plot_back_button.place(x=10, y=10)
    #=====End=====#


    #==LTCHRatio_frame with LTCHRatio_plot_frame==#
    # Title
    LTCHRatio_title = tk.Label(LTCHRatio_frame, text="Click the Generate button to plot the data", bg='#FEFEFE', bd=0, font=('Courier', 13, 'bold')).place(x=250,y=100)

    # Back button
    LTCHRatio_back_button = tk.Button(LTCHRatio_frame, image=back_button_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', padx=0, pady=0,command=lambda:swap_frame(frame1,LTCHRatio_frame), anchor='nw', bd=0,highlightthickness = 0)
    LTCHRatio_back_button.place(x=10, y=10)

    # Generate button
    generate_button_4 = tk.Button(LTCHRatio_frame, text='Generate Plot', bg='#383838', fg='#FEFEFE', bd=0, font=('Courier', 10), highlightthickness = 0, padx=100, pady=40,command=lambda:[start_progress(LTCHRatio_frame, LTCHRatio_plot_frame), show_plot(LTCHRatio_plot_frame, 'LTCHRatio_plot.png', 60, 0), run_file('plot.PyFiles/LTCHRatio.py','','')])
    generate_button_4.place(x=350, y=250)

    # Back button for LTCHRatioPlotFrame
    LTCHRatio_plot_back_button = tk.Button(LTCHRatio_plot_frame, image=back_button_image, bg='#FEFEFE', relief='flat', activebackground='#FEFEFE', padx=0, pady=0,command=lambda:swap_frame(LTCHRatio_frame,LTCHRatio_plot_frame), anchor='nw', bd=0,highlightthickness = 0)
    LTCHRatio_plot_back_button.place(x=10, y=10)
    #=====End=====#

    #======END OF DIFFERENT FRAMES======#

    window.mainloop()

# --------------------#
#    End of program   #
# --------------------#