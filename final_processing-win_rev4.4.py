from __future__ import print_function
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import os
import tkinter.messagebox as msgbox
import os.path
import time
import shutil

class frameInit:
    def __init__(self):
        self.root = Tk()
        self.root.title("최종 가공툴")
        self.root.geometry('410x275+500+150') 
        self.root.resizable(False, False) 
        
        self.current_path = os.getcwd()

        # select work folder frame
        sele_folder_frame = LabelFrame(self.root, text = '작업 폴더 선택')
        sele_folder_frame.pack(side = 'top', fill = 'both', pady = 8)

        # select work folder button frame
        sele_folder_top1 = Frame(sele_folder_frame)
        sele_folder_top1.pack(side = 'top', fill = 'both')

        sele_folder1 = Label(sele_folder_top1, text = '작업할 renamed 폴더들의 상위 폴더를 선택하세요.')
        sele_folder1.pack(side = 'left', fill = 'x', padx = 5)

        self.sele_folder2 = Button(sele_folder_top1, text = '열기', width = 8, command = self.open_dir)
        self.sele_folder2.pack(side = 'right', fill = 'x', padx = 5)
        
        # select work folder Entry frame
        sele_folder_top2 = Frame(sele_folder_frame)
        sele_folder_top2.pack(side = 'top', fill = 'both')

        self.sele_folder3 = Entry(sele_folder_top2, width = 57)
        self.sele_folder3.pack(side = 'left', fill = 'x', padx = 5, pady = 5)

        # select save folder frame
        save_folder_frame = LabelFrame(self.root, text = '저장 폴더 선택')
        save_folder_frame.pack(side = 'top', fill = 'both', pady = 8)
        
        # select save folder button frame
        save_folder_top1 = Frame(save_folder_frame)
        save_folder_top1.pack(side = 'top', fill = 'both')

        save_folder1 = Label(save_folder_top1, text = '저장할 폴더를 선택하세요.')
        save_folder1.pack(side = 'left', fill = 'x', padx = 5)

        self.save_folder2 = Button(save_folder_top1, text = '열기', width = 8, command = self.save_dir)
        self.save_folder2.pack(side = 'right', fill = 'x', padx = 5)

        # select save folder Entry frame
        save_folder_top2 = Frame(save_folder_frame)
        save_folder_top2.pack(side = 'top', fill = 'both')

        self.save_folder3 = Entry(save_folder_top2, width = 57)
        self.save_folder3.pack(side = 'left', fill = 'x', padx = 5, pady = 5)

        # final saving button frame
        save_folder_btn = Frame(self.root)
        save_folder_btn.pack(side = 'top', fill = 'both')

        self.save_btn = Button(save_folder_btn, text = '작업 시작', width = 15, command = self.save)
        self.save_btn.pack(side = 'right', fill = 'x', padx = 5)

        # save status frame
        save_status_frame = LabelFrame(self.root, text = '작업 현황')
        save_status_frame.pack(fill = 'both', pady = 8)

        # progressbar
        self.pro_var = DoubleVar()
        self.progressbar = ttk.Progressbar(save_status_frame, maximum =100, length = 250, variable = self.pro_var)
        self.progressbar.pack(side = 'left', padx =5, pady = 5)

        self.prog_rate = Label(save_status_frame, text = '')
        self.prog_rate.pack(side = 'right', padx = 5, pady = 5)

        self.root.mainloop()

    def open_dir(self):
        self.open_file = filedialog.askdirectory(title = '작업 폴더 열기.', initialdir = self.current_path)
        self.sele_folder3.configure(state = 'normal')
        self.sele_folder3.delete(0, END)
        self.sele_folder3.insert(0, self.open_file)
        self.sele_folder3.configure(state = 'readonly')
        self.save_btn.config(state = 'normal')
        self.pro_var.set(0)
        self.progressbar.update()
        self.prog_rate.configure(text = '')

        open_path = self.open_file
        open_worker_list = os.listdir(open_path)
        tot_file_qy = 0
        for x in open_worker_list:
            open_dated_list = os.listdir('{}\{}'.format(open_path, x))
            for y in open_dated_list:
                open_rename_list = os.listdir('{}\{}\{}'.format(open_path, x, y))
                tot_file_qy += len(open_rename_list)
                for z in open_rename_list:
                    if z.strip().split('.')[-1] != 'jpg':
                        os.remove('{}\{}\{}\{}'.format(open_path, x, y, z))
                        tot_file_qy -= 1
        self.prog_rate.configure(text = '선택 이미지 수 : {}'.format(tot_file_qy))

    def save_dir(self):
        self.save_file = filedialog.askdirectory(title = '저장 폴더 열기.', initialdir = self.current_path)
        self.save_folder3.configure(state = 'normal')
        self.save_folder3.delete(0, END)
        self.save_folder3.insert(0, self.save_file)
        self.save_folder3.configure(state = 'readonly')
        self.save_btn.configure(state = 'normal')

    def save(self):
        self.exit_ok = 0
        self.sele_folder2.configure(state = 'disabled')
        self.save_folder2.configure(state = 'disabled')
        self.save_btn.configure(state = 'disabled')
        if os.path.isdir('tmp'):
            shutil.rmtree('tmp')
        cur_time = time.localtime()
        cur_date = time.strftime('%Y%m%d', cur_time)
        self.make_tmp(cur_date)
        if self.exit_ok == 0:
            self.make_folder(cur_date)
        else:
            self.root.quit()
        if self.exit_ok == 0:
            self.make_ins_lst(cur_date)
        else:
            self.root.quit()
        if self.exit_ok == 0:
            shutil.rmtree('tmp')
            msgbox.showinfo('알림', '작업이 완료되었습니다.')
            self.sele_folder2.configure(state = 'normal')
            self.save_folder2.configure(state = 'normal')
        else:
            self.root.quit()

    def progress1(self, current_qy, total_qy):
        self.current_qy = current_qy + 1
        self.total_qy = total_qy
        i = (self.current_qy / self.total_qy) * 100

        self.pro_var.set(i)
        self.progressbar.update()

        state = 'tmp 저장 : {} / {}'.format(self.current_qy, self.total_qy)
        self.prog_rate.configure(text = state)

    def progress2(self, current_qy, total_qy):
        self.current_qy = current_qy + 1
        self.total_qy = total_qy
        i = (self.current_qy / self.total_qy) * 100

        self.pro_var.set(i)
        self.progressbar.update()

        state = '폴더 저장 : {} / {}'.format(self.current_qy, self.total_qy)
        self.prog_rate.configure(text = state)

    def make_tmp(self, cur_date):
        try:
            self.class_ins_old = {}
            with open('create/class_ins_hist.txt', 'r') as tmp_file:
                while True:
                    tmp_line = tmp_file.readline().strip()
                    if not tmp_line:
                        break
                    self.class_ins_old[tmp_line.split('|')[0]] = tmp_line.split('|')[1]
            open_path = self.open_file
            open_worker_list = sorted(os.listdir(open_path))
            tot_file_list = []
            tot_class_lists = []
            tot_ins_count = []
            self.tot_class_worker_ins_lists = []
            for x in open_worker_list:
                open_dated_list = sorted(os.listdir('{}\{}'.format(open_path, x)))
                for y in open_dated_list:
                    open_rename_list = sorted(os.listdir('{}\{}\{}'.format(open_path, x, y)))
                    tot_ins_lists = []
                    for z in open_rename_list:
                        class_name = z.strip().split('_')[0]
                        ins_id = z.strip().split('_')[2]
                        view_dir = z.strip().split('_')[3]
                        occl_name = z.strip().split('_')[4]
                        tot_class_lists.append(class_name)
                        tot_ins_lists.append('{}_{}'.format(class_name, ins_id))
                        tot_file_list.append([x, y, z, class_name, view_dir, occl_name])
                    tot_ins_list = sorted(set(tot_ins_lists), key = lambda x: tot_ins_lists.index(x))
                    for b in tot_ins_list:
                        ins_count = tot_ins_lists.count(b)
                        for c in range(ins_count):
                            tot_ins_count.append(ins_count)
            tot_class_list = sorted(set(tot_class_lists), key = lambda x: tot_class_lists.index(x))
            os.mkdir('tmp')
            if len(self.class_ins_old) == 0:
                self.ins_by_class = {}
                progress_count = 0
                for i in range(len(tot_class_list)) :
                    count = 1
                    repeat = 0
                    for j in range(len(tot_class_lists)):
                        str_count = str('{0:03d}'.format(count))
                        if tot_class_lists[j] == tot_class_list[i] and repeat < tot_ins_count[j]:
                            shutil.copyfile('{}\{}\{}\{}'.format(open_path, tot_file_list[j][0], tot_file_list[j][1], tot_file_list[j][2]), \
                                'tmp\{}_{}_{}_{}'.format(tot_file_list[j][3], str_count, tot_file_list[j][4], tot_file_list[j][5]))
                            self.save_pre_log(cur_date, '{}\{}\{}\{}'.format(open_path, tot_file_list[j][0], tot_file_list[j][1], tot_file_list[j][2]), \
                                '{}_{}_{}_{}'.format(tot_file_list[j][3], str_count, tot_file_list[j][4], tot_file_list[j][5]))
                            repeat += 1
                            progress_count +=1
                            self.progress1(progress_count, len(tot_class_lists))
                            self.tot_class_worker_ins_lists.append('{}_{}/{}'.format(tot_file_list[j][3], str_count, tot_file_list[j][0]))
                        if repeat == tot_ins_count[j]:
                            repeat = 0
                            count += 1
                    self.ins_by_class[tot_class_list[i]] = count - 1
            else:
                self.ins_by_class = self.class_ins_old.copy()
                progress_count = 0
                for i in range(len(tot_class_list)) :
                    if tot_class_list[i] not in self.class_ins_old:
                        count = 1
                    else:
                        count = int(self.class_ins_old[tot_class_list[i]]) + 1
                    repeat = 0
                    for j in range(len(tot_class_lists)):
                        str_count = str('{0:03d}'.format(count))
                        if tot_class_lists[j] == tot_class_list[i] and repeat < tot_ins_count[j]:
                            shutil.copyfile('{}\{}\{}\{}'.format(open_path, tot_file_list[j][0], tot_file_list[j][1], tot_file_list[j][2]), \
                                'tmp\{}_{}_{}_{}'.format(tot_file_list[j][3], str_count, tot_file_list[j][4], tot_file_list[j][5]))
                            self.save_pre_log(cur_date, '{}\{}\{}\{}'.format(open_path, tot_file_list[j][0], tot_file_list[j][1], tot_file_list[j][2]), \
                                '{}_{}_{}_{}'.format(tot_file_list[j][3], str_count, tot_file_list[j][4], tot_file_list[j][5]))
                            repeat += 1
                            progress_count +=1
                            self.progress1(progress_count, len(tot_class_lists))
                            self.tot_class_worker_ins_lists.append('{}_{}/{}'.format(tot_file_list[j][3], str_count, tot_file_list[j][0]))
                        if repeat == tot_ins_count[j]:
                            repeat = 0
                            count += 1
                    self.ins_by_class[tot_class_list[i]] = count - 1
        except:
            msgbox.showwarning('경고', '작업이 완료되지 않았습니다. 처음부터 다시 진행해 주세요.')
            if os.path.isdir('tmp'):
                shutil.rmtree('tmp')
            if os.path.isfile('create/save-{}.log'.format(cur_date)):
                os.remove('create/save-{}.log'.format(cur_date))
            self.exit_ok = 1

    def make_ins_lst(self, cur_date):
        class_ins_new = {}
        tot_class_worker_ins_dict = {}
        difficult_obj = ['ParkBench', 'Pole', 'FuseBox', 'DigitalDoorlock', 'Plunger', 'Mop', 'ManholeCover', 'Hourglass', 'Backpack', \
            'Bucket', 'Mitten', 'Toilet', 'Projector', 'Washbasin', 'SaltShaker', 'ShoppingCart', 'MotorScooter', 'DishDrainer', \
            'DiningTable', 'Dumbbell', 'EspressoMaker', 'AirFryer', 'Mailbox', 'CarSideMirror', 'Bicycle', 'Microwave', 'WaterPurifier', \
            'CarWheel', 'Printer', 'Pizza', 'SewerDrainage', 'Hotdog', 'Hamburger', 'Cucurbita', 'HwatuCard']
        for aa in self.tot_class_worker_ins_lists:
            if aa.strip().split('_')[0] in difficult_obj:
                tot_class_worker_ins_dict[aa.strip().split('/')[0]] = aa.strip().split('/')[1]
        shutil.copyfile('create/class_ins_hist.txt', 'create/class_ins_hist.bak')
        ins_by_class_lst = sorted(self.ins_by_class)
        with open('create/class_ins_hist.txt', 'w') as f:
            for key in ins_by_class_lst:
                tmp_line = f.writelines('{}|{}\n'.format(key, self.ins_by_class[key]))
                if key in self.class_ins_old.keys():
                    class_ins_new[key] = int(self.ins_by_class[key]) - int(self.class_ins_old[key])
                else:
                    class_ins_new[key] = int(self.ins_by_class[key])
        class_ins_new_lst = sorted(class_ins_new)
        total_ins_qy = sum(class_ins_new.values())
        total_spe_qy = len(tot_class_worker_ins_dict)
        special_worker = {}
        class_ins_by_worker = {}
        with open('create/class_ins_{}.txt'.format(cur_date), 'w') as f:
            for key in class_ins_new_lst:
                if class_ins_new[key] != 0:
                    line = '{}|{}'.format(key, class_ins_new[key])
                    worker = ''
                    for difkey, difvalue in tot_class_worker_ins_dict.items():
                        if difkey.strip().split('_')[0] == key:
                            if worker == '':
                                worker = difvalue
                                line = line + '|{} : {}, '.format(worker, difkey.strip().split('_')[1])
                                class_ins_by_worker['{}_{}'.format(worker, key)] = 1
                            elif worker == difvalue:
                                line += '{}, '.format(difkey.strip().split('_')[1])
                                class_ins_by_worker['{}_{}'.format(worker, key)] += 1
                            elif worker != difvalue:
                                # if worker in special_worker.keys():
                                #     special_worker[worker] += worker_ins_qy
                                # else:
                                #     special_worker[worker] = worker_ins_qy
                                worker = difvalue
                                # worker_ins_qy = 1
                                line = line + '|{} : {}, '.format(worker, difkey.strip().split('_')[1])
                                class_ins_by_worker['{}_{}'.format(worker, key)] = 1
                            if worker in special_worker.keys():
                                special_worker[worker] += 1
                            else:
                                special_worker[worker] = 1
                    tmp_line = f.writelines('{}\n'.format(line))
            special_workder_lst = sorted(special_worker)
            class_ins_by_worker_lst = sorted(class_ins_by_worker)
            f.writelines('총 인스턴스 수 : {}, 스페셜 총 인스턴스 수 : {}\n'.format(total_ins_qy, total_spe_qy))
            for key in special_workder_lst:
                class_ins_count = ''
                for x in class_ins_by_worker_lst:
                    if x.split('_')[0] == key:
                        class_ins_count += '{} > {}, '.format(x.split('_')[1], class_ins_by_worker[x])
                f.writelines('스페셜 워커 ID : {}, 총 인스턴스 수 : {}, 클래스별 인스턴스 수 : {}\n'.format(key, special_worker[key], class_ins_count))

    def make_folder(self, cur_date):
        try:
            open_path = self.open_file
            save_path = self.save_file
            tmp_list = os.listdir('tmp')
            cur_time = time.localtime()
            scur_date = time.strftime('%y%m%d', cur_time)
            target_list = []
            for x in tmp_list:
                class_name = x.strip().split('_')[0]
                if os.path.isdir('{}\image_data_{}'.format(save_path, cur_date)):
                    if os.path.isdir('{}\image_data_{}\{}'.format(save_path, cur_date, scur_date)):
                        if os.path.isdir('{}\image_data_{}\{}\{}'.format(save_path, cur_date, scur_date, class_name)):
                            shutil.copyfile('tmp\{}'.format(x), '{}\image_data_{}\{}\{}\{}'\
                                .format(save_path, cur_date, scur_date, class_name, x))
                        else:
                            os.mkdir('{}\image_data_{}\{}\{}'.format(save_path, cur_date, scur_date, class_name))
                            if os.path.isdir('{}\image_data_{}\{}\{}'.format(save_path, cur_date, scur_date, class_name)):
                                shutil.copyfile('tmp\{}'.format(x), '{}\image_data_{}\{}\{}\{}'\
                                        .format(save_path, cur_date, scur_date, class_name, x))
                        target_list.append(['{}'.format(x), '{}\image_data_{}\{}\{}\{}'\
                            .format(save_path, cur_date, scur_date, class_name, x)])
                    else:
                        os.mkdir('{}\image_data_{}\{}'.format(save_path, cur_date, scur_date))
                        os.mkdir('{}\image_data_{}\{}\{}'.format(save_path, cur_date, scur_date, class_name))
                        if os.path.isdir('{}\image_data_{}\{}\{}'.format(save_path, cur_date, scur_date, class_name)):
                            shutil.copyfile('tmp\{}'.format(x), '{}\image_data_{}\{}\{}\{}'\
                                .format(save_path, cur_date, scur_date, class_name, x))
                            target_list.append(['{}'.format(x), '{}\image_data_{}\{}\{}\{}'\
                                .format(save_path, cur_date, scur_date, class_name, x)])
                    if x.strip().split('_')[3] == 'None.jpg':
                        if os.path.isdir('{}\image_data_{}\{}_None'.format(save_path, cur_date, scur_date)):
                            if os.path.isdir('{}\image_data_{}\{}_None\{}'.format(save_path, cur_date, scur_date, class_name)):
                                shutil.copyfile('tmp\{}'.format(x), '{}\image_data_{}\{}_None\{}\{}'\
                                    .format(save_path, cur_date, scur_date, class_name, x))
                            else:
                                os.mkdir('{}\image_data_{}\{}_None\{}'.format(save_path, cur_date, scur_date, class_name))
                                if os.path.isdir('{}\image_data_{}\{}_None\{}'.format(save_path, cur_date, scur_date, class_name)):
                                    shutil.copyfile('tmp\{}'.format(x), '{}\image_data_{}\{}_None\{}\{}'\
                                        .format(save_path, cur_date, scur_date, class_name, x))
                            target_list.append(['{}'.format(x), '{}\image_data_{}\{}_None\{}\{}'\
                                .format(save_path, cur_date, scur_date, class_name, x)])
                        else:
                            os.mkdir('{}\image_data_{}\{}_None'.format(save_path, cur_date, scur_date))
                            os.mkdir('{}\image_data_{}\{}_None\{}'.format(save_path, cur_date, scur_date, class_name))
                            if os.path.isdir('{}\image_data_{}\{}_None\{}'.format(save_path, cur_date, scur_date, class_name)):
                                shutil.copyfile('tmp\{}'.format(x), '{}\image_data_{}\{}_None\{}\{}'\
                                    .format(save_path, cur_date, scur_date, class_name, x))
                                target_list.append(['{}'.format(x), '{}\image_data_{}\{}_None\{}\{}'\
                                    .format(save_path, cur_date, scur_date, class_name, x)])
                    self.progress2(tmp_list.index(x), len(tmp_list))
                else:
                    os.mkdir('{}\image_data_{}'.format(save_path, cur_date))
                    os.mkdir('{}\image_data_{}\{}'.format(save_path, cur_date, scur_date))
                    os.mkdir('{}\image_data_{}\{}\{}'.format(save_path, cur_date, scur_date, class_name))
                    if os.path.isdir('{}\image_data_{}\{}\{}'.format(save_path, cur_date, scur_date, class_name)):
                        shutil.copyfile('tmp\{}'.format(x), '{}\image_data_{}\{}\{}\{}'\
                            .format(save_path, cur_date, scur_date, class_name, x))
                        target_list.append(['{}'.format(x), '{}\image_data_{}\{}\{}\{}'\
                            .format(save_path, cur_date, scur_date, class_name, x)])
                    if x.strip().split('_')[3] == 'None.jpg':
                        os.mkdir('{}\image_data_{}\{}_None'.format(save_path, cur_date, scur_date))
                        os.mkdir('{}\image_data_{}\{}_None\{}'.format(save_path, cur_date, scur_date, class_name))
                        if os.path.isdir('{}\image_data_{}\{}_None\{}'.format(save_path, cur_date, scur_date, class_name)):
                            shutil.copyfile('tmp\{}'.format(x), '{}\image_data_{}\{}_None\{}\{}'\
                                .format(save_path, cur_date, scur_date, class_name, x))
                            target_list.append(['{}'.format(x), '{}\image_data_{}\{}_None\{}\{}'\
                                .format(save_path, cur_date, scur_date, class_name, x)])
                    self.progress2(tmp_list.index(x), len(tmp_list))
            self.save_log(cur_date, target_list)
        except:
            msgbox.showwarning('경고', '작업이 완료되지 않았습니다. 처음부터 다시 진행해 주세요.')
            if os.path.isdir('tmp'):
                shutil.rmtree('tmp')
            if os.path.isdir('{}\image_data_{}'.format(save_path, cur_date)):
                shutil.rmtree('{}\image_data_{}'.format(save_path, cur_date))
            if os.path.isfile('create/save-{}.log'.format(cur_date)):
                os.remove('create/save-{}.log'.format(cur_date))
            self.exit_ok = 1


    def save_pre_log(self, cur_date, origin, inter):
        if not os.path.isfile('create/save-{}.log'.format(cur_date)):
            with open('create/save-{}.log'.format(cur_date), 'w') as file:
                file.writelines('1|final processed|{}|{}\n'.format(origin, inter))
        else:
            with open('create/save-{}.log'.format(cur_date), 'r') as file:
                file_line = len(file.readlines()) + 1
            with open('create/save-{}.log'.format(cur_date), 'at') as file:
                file.writelines('{}|final processed|{}|{}\n'.format(file_line, origin, inter))

    def save_log(self, cur_date, target):
        line_list = []
        with open('create/save-{}.log'.format(cur_date), 'r') as file:
            while True:
                tmp_line1 = file.readline().strip()
                if not tmp_line1:
                    break
                tmp_line2 = tmp_line1.split('|')
                line_list.append(tmp_line2)
        with open('create/save-{}.log'.format(cur_date), 'w') as file:
            if len(line_list) == len(target):
                for i in range(len(line_list)):
                    for j in range(len(target)):
                        if line_list[i][3] == target[j][0]:
                            file.writelines('{}|{}|{}|{}\n'.format(line_list[i][0], line_list[i][1], line_list[i][2], target[j][1]))
            else:
                for i in range(len(line_list)):
                    diff = len(line_list) - len(target)
                    if int(line_list[i][0]) <= diff:
                        file.writelines('{}|{}|{}|{}\n'.format(line_list[i][0], line_list[i][1], line_list[i][2], line_list[i][3]))
                    else:
                        for j in range(len(target)):
                            if line_list[i][3] == target[j][0]:
                                file.writelines('{}|{}|{}|{}\n'.format(line_list[i][0], line_list[i][1], line_list[i][2], target[j][1]))

frameInit()