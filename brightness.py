import customtkinter as ctk
import screen_brightness_control as sbc

ctk.set_default_color_theme('blue') #Sets app theme
ctk.set_appearance_mode('system') #Set appearance mode -> 'system', 'dark' or 'light'

class Brightness(ctk.CTk):
    def __init__(self):
        super().__init__()

        #-------------------
        #App Initialization
        #-------------------
        self.title('Brightness Controller')
        self.geometry('500x200')
        self.resizable(False, False)

        #Get current screen brightness
        self.current = sbc.get_brightness()[0]
        self.widgets()

    def widgets(self):
        #----------
        #App Label
        #----------
        self.brightness_header = ctk.CTkLabel(self, 
                            text='Brightness Control', 
                            text_color=("#000000", "#fdfdfd"), 
                            font=('Times New Roman', 35, 'bold')
                            )
        self.brightness_header.pack(pady=20)

        #-----------------------------------------------------------------
        #creating first frame for displaying slider and brightness level
        #-----------------------------------------------------------------
        self.frame1 = ctk.CTkFrame(self, width=200, height=50)
        self.frame1.pack_propagate(False) #Propagated to attain the exact width and height values even if not used
        self.frame1.pack(padx=30, fill="x")

        #-----------------------------------------------
        #creating slider with current screen brightness
        #-----------------------------------------------
        self.brightness_slider= ctk.CTkSlider(self.frame1, from_ = 0, to = 100, 
                    border_color= '#4D4B4B',
                    progress_color=('#FFFFFF', '#000000'),
                    button_color=('#FFFFFF', '#000000'),
                    button_hover_color=('#000000', '#FFFFFF'),
                    state="normal",
                    command=self.set_brightness)
        self.brightness_slider.set(self.current)
        self.brightness_slider.pack(padx=15, expand=1, fill="x", side='right') #Expanded and filled to to contain the whole frame, set to the right in the frame
        
        #Brightness level label, to the left side in the frame
        self.brightness_label = ctk.CTkLabel(self.frame1, anchor='center', compound='center', 
                                            text=f'Level {self.current}%', 
                                            font=ctk.CTkFont(size=20, weight='bold'),
                                            text_color=("#000000", "#fdfdfd"))
        self.brightness_label.pack(padx=15, side='left')      

        #------------------------------------------------------------------------------
        #segmented buttons to control theme, directly on the app widow, not in a frame
        #------------------------------------------------------------------------------
        self.theme_button = ctk.CTkSegmentedButton(self, 
                                                   values=['Dark', 'Light'], 
                                                   fg_color=("#c0c0c0", "#1E1C1C"), 
                                                   bg_color='transparent', 
                                                   dynamic_resizing=True, 
                                                   font=ctk.CTkFont(size=15),
                                                   command=self.change_theme,
                                                   text_color=("#000000", "#fdfdfd"))
        self.theme_button.pack(side='left', padx=(32, 0))
        self.theme_button.set(ctk.get_appearance_mode())

        #---------------------------------------------------------------------------------------------------------
        #about the app button to show more info about the app, by the right side, also directly on the app window
        #---------------------------------------------------------------------------------------------------------
        self.about_button = ctk.CTkButton(
            self, 
            text="ℹ About", 
            width=70, 
            font=ctk.CTkFont(size=15), 
            text_color=("#000000", "#fdfdfd"), 
            command=self.about
        )
        self.about_button.pack(side='right', padx=(0, 32))
    
    def set_brightness(self, slider_value):
        #------------------------------------------------------
        #set screen brightness based on the sliders level value
        #-------------------------------------------------------
        brightness = int(slider_value)
        sbc.set_brightness(brightness)
        self.brightness_label.configure(text=f'Level {brightness}%')
    
    def change_theme(self, theme_name):
        #-------------------------------------------------------------------------------
        #function to change app theme based on clicked button from the segmented button
        #-------------------------------------------------------------------------------
        ctk.set_appearance_mode(theme_name.lower())

    def about(self):
        #--------------------------------
        #Pop-up dialog box initialization
        #--------------------------------
        self.dialog = ctk.CTkToplevel(self)
        self.dialog.title('About the Brightness Controller App')
        self.dialog.transient(self)
        self.dialog.overrideredirect(False)
        self.dialog.resizable(False, False)

        #----------------------
        #Dialog box main frame
        #----------------------
        self.dialog_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        self.dialog_frame.pack(expand=True)

        #-----------------------------------------------
        #text frame by the left in dialog box main frame
        #-----------------------------------------------
        self.text_frame = ctk.CTkFrame(self.dialog_frame, fg_color='transparent')
        self.text_frame.pack(side='left', fill='both', expand=True, pady=10)

        #------------------------------------------------
        #icon frame by the right in dialog box main frame
        #------------------------------------------------
        self.icon_frame = ctk.CTkFrame(self.dialog_frame, fg_color='transparent')
        self.icon_frame.pack(side='right', fill='both', expand=True)

        #--------------------------------------
        #Creating icon based on the icon frame
        #--------------------------------------
        self.icon = ctk.CTkLabel(self.icon_frame, text='💡', text_color='yellow', font=ctk.CTkFont(size=100))
        self.icon.pack()

        #------------------------------
        #Header text in the text frame
        #------------------------------
        self.header = ctk.CTkLabel(self.text_frame, text='Brightness Controller', font = ctk.CTkFont(size=20, weight='bold'))
        self.header.pack(anchor='w')

        #app version
        self.version = ctk.CTkLabel(self.text_frame, text='Version 1.0.1')
        self.version.pack(pady=5, anchor='w')

        #------------------------------------------------
        #More infomation about the app in the text frame
        #------------------------------------------------
        self.more_info = ctk.CTkLabel(self.text_frame, text=
        'A light weight desktop app\n'
        'for controlling screen brightness\n\n'
        'Built with Python, CustomTkinter\n'
        'and screen-brightness-control\n'
        , justify='left', wraplength=200).pack(anchor='w') #Left sided justification

        #--------------------------------------------
        #Developers name for cool looking experience
        #--------------------------------------------
        self.developer = ctk.CTkLabel(self.text_frame, text='Developer: Cyrus Akacha Cyprian', font=ctk.CTkFont(size=15, weight='bold'))
        self.developer.pack()

        #--------------------------------------------------
        #Mini-Buttons frame below in dialog box main frame
        #--------------------------------------------------
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 10)) #Frame stretches through entire dialog box frame

        ctk.CTkButton(button_frame, text="Close", width=100, command=self.dialog.destroy, 
                      fg_color='red', 
                      hover_color="#f56969").pack(side="right", padx=15)
        ctk.CTkButton(button_frame, text='Github', width=100, fg_color='black', hover_color="#5A5454").pack(side='left', padx=15)
        ctk.CTkButton(button_frame, text='Portfolio', width=100, fg_color='blue', hover_color="#1e8ddd").pack(side='left', padx=15)
if __name__ == '__main__':
    app = Brightness()
    app.mainloop()
