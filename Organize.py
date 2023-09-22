import os
import shutil
from tkinter import *
from tkinter import messagebox, filedialog

# Dictionary of file extensions and their corresponding categories
Extensions = {
    'Documents': ('.pdf', '.doc', '.xls', 'txt', '.csv', '.zip',
                  '.xml', '.zip', '.docx', '.DOCX', '.odt'),
    'Pictures': ('.jpg', '.jpeg', '.png', '.JPG'),
    'Videos': ('.mp4', '.mkv', '.3gp', '.flv', '.mpeg'),
    'Music': ('.mp3', '.wav', '.m4a', '.webm'),
    'Programs': ('.py', '.cpp', '.c', '.sh', '.js'),
    'Apps': ('.exe', '.apk'),
}


class File_Organizer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x400")
        self.root.title('Junk File Organizer')
        self.root.resizable(width=False, height=False)
        self.root.configure(bg='white')

        # Create a big "File Organizer" label at the top
        big_label = Label(root, text="File Organizer",
                          font=("Arial", 36, 'bold'), bg='dodger blue', fg='white')
        big_label.pack(fill='x', padx=20, pady=(20, 10))

        self.Selected_Dir = ''
        self.Browsed = False

        # Frame for the rest of the content
        self.frame_2 = Frame(root, bg="white")
        self.frame_2.pack(fill='both', expand=True)

        self.Main_Page()

    def Main_Page(self):
        # Heading Label
        Heading_Label = Label(self.frame_2, text="Please Select the Folder", font=(
            "Arial", 20, 'bold'), bg='white')
        Heading_Label.place(x=140, y=10)

        # Button to select a folder
        Folder_Button = Button(self.frame_2, text="Select Folder", font=(
            "Arial", 12, 'bold'), bg="dodger blue", fg='white', width=20, height=2, command=self.Select_Directory)
        Folder_Button.place(x=40, y=80)

        # to display the selected folder path
        self.Folder_Entry = Entry(
            self.frame_2, font=("Helvetica", 12), width=32)
        self.Folder_Entry.place(x=256, y=85)

        # Status label
        Status = Label(self.frame_2, text="Status:",
                       font=("Arial", 16, 'bold'), bg='white')
        Status.place(x=180, y=140)

        # Status message
        self.Status_Label = Label(self.frame_2, text="Not Started Yet", font=(
            "Arial", 16), bg="white", fg="gray")
        self.Status_Label.place(x=256, y=140)

        # Start button
        Start_Button = Button(self.frame_2, text="Start", font=(
            "Arial", 16, 'bold'), bg="dodger blue", fg="white", width=10, height=2, command=self.Organizer)
        Start_Button.place(x=240, y=180)

    def Select_Directory(self):
        # To select a directory
        self.Selected_Dir = filedialog.askdirectory(title="Select a location")
        self.Folder_Entry.insert(0, self.Selected_Dir)
        self.Selected_Dir = str(self.Selected_Dir)
        if os.path.exists(self.Selected_Dir):
            self.Browsed = True

    def Organizer(self):
        # Check if a folder has been selected
        if not self.Browsed:
            messagebox.showwarning(
                'No folders are chosen', 'Please Select a Folder First')
            return

        try:
            self.Status_Label.config(text='Processing...')

            # Get the current selected path
            self.Current_Path = self.Selected_Dir

            # Check if the selected path exists
            if os.path.exists(self.Current_Path):
                self.Folder_List1 = []  # existing folders
                self.Folder_List2 = []  # created folders
                self.Flag = False  # To track if any files were moved

                for folder, extensions in Extensions.items():
                    self.folder_name = folder
                    self.folder_path = os.path.join(
                        self.Current_Path, self.folder_name)
                    os.chdir(self.Current_Path)

                    # To check if the folder already exists
                    if os.path.exists(self.folder_name):
                        self.Folder_List1.append(self.folder_name)
                    else:
                        self.Folder_List2.append(self.folder_name)
                        os.mkdir(self.folder_path)

                    # files with specific extensions and move them
                    for item in self.File_Finder(self.Current_Path, extensions):
                        self.Old_File_Path = os.path.join(
                            self.Current_Path, item)
                        self.New_File_Path = os.path.join(
                            self.folder_path, item)
                        shutil.move(self.Old_File_Path, self.New_File_Path)
                        self.Flag = True

            else:
                # Show an error message
                messagebox.showerror('Please Enter a Valid Path!')

            # Check if any files were moved and update the status label
            if self.Flag:
                self.Status_Label.config(text='Complete!')
                messagebox.showinfo('Done!', 'Complete!')
                self.Clear()
            if not self.Flag:
                self.Status_Label.config(text='Complete!')
                messagebox.showinfo(
                    'Done!', 'Folders have been created\nNo Files were there to move')
                self.Clear()
        except Exception as es:
            # Show an error message for exception
            messagebox.showerror("Error!", f"Error due to {str(es)}")

    def File_Finder(self, folder_path, file_extensions):
        # Function to find files with specific extensions in a folder
        self.files = []
        for file in os.listdir(folder_path):
            for extension in file_extensions:
                if file.endswith(extension):
                    self.files.append(file)
        return self.files

    def Clear(self):
        # Function to clear the selected folder path and status message
        self.Status_Label.config(text='Not Started Yet')
        self.Folder_Entry.delete(0, END)
        self.Selected_Dir = ''


if __name__ == "__main__":
    root = Tk()
    obj = File_Organizer(root)
    root.mainloop()
