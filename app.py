from tkinter import *
import ftplib
import _thread


ANONYMOUS_USER = 'anonymous'
ANONYMOUS_PASSWORD = 'example@email.com'


class App:
    start_ip = ''
    end_ip = ''
    start_ip_int = [0, 0, 0, 0]
    end_ip_int = [255, 255, 255, 255]
    found_ct = 0

    # window: TK object
    def __init__(self, window):
        fm1 = Frame(window)
        label_description = Label(fm1,
                                  text="This FTP Knocker can find hosts that support anonymous FTP accessing on the Internet.\n"
                                       "Input the start & end ip address and run the searching.",
                                  justify='left')
        label_description.grid(sticky='w')
        fm1.grid(sticky='w', row=0, column=0)

        # 空白占位
        Label().grid(row=1, column=0)

        self.fm2 = Frame(window)
        label_start_ip = Label(self.fm2, text="Start IP", justify='left')
        label_start_ip.grid(sticky='w', row=0, column=0)
        start_ip_str = StringVar()
        self.entry_start_ip = Entry(self.fm2, textvariable=start_ip_str)
        self.entry_start_ip.grid(row=0, column=1, padx=50)
        label_end_ip = Label(self.fm2, text="End IP", justify='left')
        label_end_ip.grid(sticky='w', row=1, column=0)
        end_ip_str = StringVar()
        self.entry_end_ip = Entry(self.fm2, textvariable=end_ip_str)
        self.entry_end_ip.grid(row=1, column=1, padx=50)
        self.fm2.grid(sticky='w', row=2, column=0)

        # 空白占位
        Label().grid(row=3, column=0)

        fm3 = Frame(window)
        button_search = Button(fm3, text="Search", command=self.run_search, width=20)
        button_search.grid()
        fm3.grid(row=4, column=0)

        self.fm4 = Frame(window)
        label_trying = Label(self.fm4, text="Trying:                   ", fg='green')
        label_trying.grid(row=0, column=0, sticky='w')
        self.fm4.grid(row=5, column=0, sticky='w')

        # 空白占位
        Label().grid(row=6, column=0)

        fm5 = Frame(window)
        scrollbar = Scrollbar(fm5)
        scrollbar.grid(row=0, column=1)
        self.found_list = Listbox(fm5, yscrollcommand=scrollbar.set, width=80)
        self.found_list.grid(row=0, column=0, sticky='w', padx=10)
        scrollbar.config(command=self.found_list.yview)
        fm5.grid(row=7, column=0, sticky='w')

    def run_search(self):
        cover1 = Label(self.fm2, text='                 ')
        cover1.grid(row=0, column=2)
        cover2 = Label(self.fm2, text='                  ')
        cover2.grid(row=1, column=2)
        cover3 = Label(self.fm2, text='                                             ')
        cover3.grid(row=2, column=1, pady=10)
        self.start_ip = self.entry_start_ip.get()
        self.end_ip = self.entry_end_ip.get()
        start_ip_fields = self.start_ip.split('.')
        end_ip_fields = self.end_ip.split('.')
        start_ip_invalid_flag = 0
        end_ip_invalid_flag = 0
        if len(start_ip_fields) != 4:
            label_invalid_ip_alert = Label(self.fm2, text='Invalid IP', fg='red')
            label_invalid_ip_alert.grid(row=0, column=2)
            start_ip_invalid_flag = 1
        else:
            for i in [0, 1, 2, 3]:
                try:
                    cache = int(start_ip_fields[i])
                except:
                    label_invalid_ip_alert = Label(self.fm2, text='Invalid IP', fg='red')
                    label_invalid_ip_alert.grid(row=0, column=2)
                    start_ip_invalid_flag = 1
                    break
                else:
                    if cache < 0 or cache > 255:
                        label_invalid_ip_alert = Label(self.fm2, text='Invalid IP', fg='red')
                        label_invalid_ip_alert.grid(row=0, column=2)
                        start_ip_invalid_flag = 1
                        break
                    else:
                        self.start_ip_int[i] = cache
        if len(end_ip_fields) != 4:
            label_invalid_ip_alert = Label(self.fm2, text='Invalid IP', fg='red')
            label_invalid_ip_alert.grid(row=1, column=2)
            end_ip_invalid_flag = 1
        else:
            for i in [0, 1, 2, 3]:
                try:
                    cache = int(end_ip_fields[i])
                except:
                    label_invalid_ip_alert = Label(self.fm2, text='Invalid IP', fg='red')
                    label_invalid_ip_alert.grid(row=1, column=2)
                    end_ip_invalid_flag = 1
                    break
                else:
                    if cache < 0 or cache > 255:
                        label_invalid_ip_alert = Label(self.fm2, text='Invalid IP', fg='red')
                        label_invalid_ip_alert.grid(row=1, column=2)
                        end_ip_invalid_flag = 1
                        break
                    else:
                        self.end_ip_int[i] = cache
        if start_ip_invalid_flag == 0 and end_ip_invalid_flag == 0:
            start_lower = False
            if self.start_ip_int[0] < self.end_ip_int[0]:
                start_lower = True
            elif self.start_ip_int[0] > self.end_ip_int[0]:
                start_lower = False
            else:
                if self.start_ip_int[1] < self.end_ip_int[1]:
                    start_lower = True
                elif self.start_ip_int[1] > self.end_ip_int[1]:
                    start_lower = False
                else:
                    if self.start_ip_int[2] < self.end_ip_int[2]:
                        start_lower = True
                    elif self.start_ip_int[2] > self.end_ip_int[2]:
                        start_lower = False
                    else:
                        if self.start_ip_int[3] < self.end_ip_int[3]:
                            start_lower = True
                        elif self.start_ip_int[3] > self.end_ip_int[3]:
                            start_lower = False
                        else:
                            start_lower = True
            if start_lower is not True:
                label_invalid_ip_alert = Label(self.fm2, text='The start IP should be lower the the end IP!', fg='red')
                label_invalid_ip_alert.grid(row=2, column=1, pady=10)
            else:
                label_searching = Label(self.fm2, text='Searching... It may take a long time, please be patient.', fg='green')
                label_searching.grid(row=2, column=1, pady=10)
                _thread.start_new_thread(self.search, ())

    def search(self):
        for i in range(self.start_ip_int[0], self.end_ip_int[0]+1):
            for j in range(self.start_ip_int[1], self.end_ip_int[1]+1):
                for k in range(self.start_ip_int[2], self.end_ip_int[2]+1):
                    for l in range(self.start_ip_int[3], self.end_ip_int[3]+1):
                        ip = str(i) + '.' + str(j) + '.' + str(k) + '.' + str(l)
                        file = open('present_ip.txt', 'w')
                        file.write(ip)
                        file.close()
                        print("Trying: " + ip)
                        label_trying = Label(self.fm4, text="Trying: " + ip, fg='green')
                        label_trying.grid(row=0, column=0)
                        try:    # method from 
                            ftp = ftplib.FTP()
                            ftp.connect(ip, 21, 2.0)
                            if '230' in ftp.login(user=ANONYMOUS_USER, passwd=ANONYMOUS_PASSWORD):
                                print(ip)
                                self.found_list.insert(END, 'found: ' + ip)
                                self.found_list.grid(row=0, column=0, sticky='w', padx=10)
                                file = open('result.txt', 'a')
                                file.write(ip)
                                file.write('\n')
                                file.close()
                                ftp.quit()
                        except ftplib.all_errors:
                            pass
        self.found_list.insert(END, 'Finished!')
        self.found_list.grid(row=0, column=0, sticky='w', padx=10)


if __name__ == "__main__":
    root = Tk()

    # set the size and initial location of window
    root.geometry("600x450+400+180")

    # set the title
    root.title("Steve's FTP Knocker - Find anonymous FTP servers on the Internet!")

    # display the main window
    display = App(root)
    root.mainloop()
