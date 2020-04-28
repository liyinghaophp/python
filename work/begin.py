#
# 提供工作效率工具
# 自动化一键搞定
#

import tkinter as tk
import os
import json
import tkinter.messagebox

app_name = '李英豪'
app_size = '800x500'
# 文本域展示区域
textarea_index = None
pop_window = None
app_now = None


# ################### 数据库开始 ########################
class Db:
    # 数据文件路径
    dataPath = './data.json'

    # 新增数据
    def add(self, name, url):
        # 获取所有数据
        data = self.all()

        for item in data:
            if item['name'] == name:
                return '已存在name'

        # 添加数据
        # print(data)
        # return
        # data = []
        # if not data
        data.append({'name': name, 'url': url})
        # 数据存储
        res = self.__save(data)
        if res:
            return False
        return '保存失败'

    # 更新数据
    def update(self, key, data):
        # 获取所有数据
        data_list = self.all()
        unchanged = True
        for item in data_list:
            if item['name'] == str(key) and (item['url'] != data['url'] or item['name'] != data['name']):
                item['name'] = data['name']
                item['url'] = data['url']
                unchanged = False

        if unchanged:
            return '信息未发生变动'
        # 数据存储
        if self.__save(data_list):
            return False
        return '保存失败'

    # 更新数据
    def delete(self, name):
        # 获取所有数据
        data = self.all()
        # unchanged = True
        # for item in data:
        # aaaaa = range(len(data))
        for index in range(len(data)):
            if data[index]['name'] == name:
                del data[index]
                # unchanged = False
                if self.__save(data):
                    return False
                return '保存失败'

        return '信息未找到'

    # 获取数据
    # @staticmethod
    def all(self, name_key=0):
        try:
            file = open(self.dataPath, mode='r')
        # 没有找到文件则创建
        except FileNotFoundError:
            file = open(self.dataPath, mode='w+')
        file = open(self.dataPath, mode='r')
        # 读取
        json_data = file.read()
        file.close()

        if not json_data:
            return []

        # 转换
        data = json.loads(json_data)

        if name_key:
            for item in data:
                if item['name'] == str(name_key):
                    return item
        if name_key:
            return

        return data

    # 数据展示
    def show(self, name_key=0):
        # 读取
        data = self.all()
        print('######################### 开始运行 ###################\r\n')
        for item in data:
            if name_key:
                if item['name'] == name_key:
                    print(' name：' + item['name'].ljust(9, ' ') + ' ------ url：' + item['url'] + '\r\n')
            else:
                print(' name：' + item['name'].ljust(9, ' ') + ' ------ url：' + item['url'] + '\r\n')
        print('###################### 运行结束 ############################\r\n')
        return

    # 储存数据
    def __save(self, data):
        # 专用写入数据句柄
        file = open(self.dataPath, mode='w')
        # 数据格式转换
        jsn = json.dumps(data)
        # 写入
        result = file.write(jsn)
        # 保存
        file.close()

        # 结束
        if result:
            return True
        return False

    # 删除执行
    def __del__(self):
        pass


# ################### 数据库结束 ########################


# #################### 软件开始 #########################
class Work:
    # app路径列表
    # app_dir_list = [
    #     {'name':'QQ', 'url': r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\腾讯软件\QQ\腾讯QQ'},
    #     {'name':'weixin',"url":r'D:\微信\WeChat\WeChat.exe'},
    #     {'name':'sublime','url':r'D:\php\Phpstudy\Sublime Text 3\sublime_text.exe'},
    #     {'name':'360browser','url':r'D:\李英豪软件\360jisu\360Chrome\Chrome\Application\360chrome.exe'},
    #     {'name':'Xshell','url':r'D:\Xshell+Xftp\Xshell.exe'},
    #     {'name':'phpStudy','url':r'D:\php\Phpstudy\phpStudy.exe'},
    # ]

    # app_list = None
    add_app_name = None
    add_app_url = None
    primary_key = None

    # 开始运行软件
    def index(self):
        # 第1步，实例化object，建立窗口window
        window = tk.Tk()
        # 添加app使用的变量
        # 第2步，给窗口的可视化起名字
        window.title(app_name)
        # 第3步，设定窗口的大小(长 * 宽)
        window.geometry(app_size)  # 这里的乘是小x
        # 第4步，在图形界面上设定标签
        var = tk.StringVar()
        # 软件数据
        app_list = Db().all()
        msg = '点击开始，开始运行软件'
        l = tk.Label(window, text=msg, bg='green', fg='white', font=('Arial', 12), width=100, height=6)
        # 第5步，放置标签
        l.pack()  # Label内容content区域放置位置，自动调节尺寸
        # 第5步，在窗口界面设置放置Button按键
        b = tk.Button(window, text='开始运行', font=('Arial', 12), width=20, height=2, command=self.open_app)
        add = tk.Button(window, text='添加', font=('Arial', 12), width=5, height=1, command=self.add_app)
        edit = tk.Button(window, text='编辑', font=('Arial', 12), width=5, height=1, command=self.edit_app)
        add.place(x=20, y=130)
        edit.place(x=100, y=130)
        b.place(x=300, y=180)
        scroll = tkinter.Scrollbar()
        global textarea_index
        textarea_index = tk.Text(window, height=14, width=108)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        textarea_index.place(x=15, y=300)
        scroll.config(command=textarea_index.yview)
        textarea_index.config(yscrollcommand=scroll.set)
        if app_list:
            textarea_index.insert(tkinter.END,
                                  '######################################### 运行的软件 #######################################\r\n[')
            for item in Db().all():
                textarea_index.insert(tkinter.END, item['name'] + '、')
            textarea_index.insert(tkinter.END, ']')
        else:
            textarea_index.insert(tkinter.END,
                                  '######################################### 请添加需要执行的软件 #########################################')
        textarea_index.insert(tkinter.END, '\r\n')
        textarea_index.see(tkinter.END)
        textarea_index.update()
        # 第6步，主窗口循环显示
        window.mainloop()

    # 开始运行软件
    @staticmethod
    def open_app():
        global textarea_index
        app_list = Db().all()
        if app_list:
            textarea_index.insert(tkinter.END,
                                  '######################################### 开始运行 #########################################\r\n##\r\n')
            for item in app_list:
                os.startfile(item['url'])
                textarea_index.insert(tkinter.END,
                                      '##  打开：' + item['name'].ljust(10, ' ') + ' ------ 路径：' + item['url'] + '\r\n')
            textarea_index.insert(tkinter.END,
                                  '##\r\n######################################### 运行结束 #########################################\r\n')
        else:
            textarea_index.insert(tkinter.END,
                                  '######################################### 请添加需要执行的软件 #########################################\r\n')
        textarea_index.see(tkinter.END)
        textarea_index.update()

    # 编辑页面
    def edit(self):
        global pop_window, app_now
        site = app_now.curselection()
        if len(site) < 1:
            tkinter.messagebox.showerror(title='编辑提示', message='请选择需要编辑的应用！')
            return

        data = Db().all(app_now.get(site))
        if not data:
            return

        self.primary_key = data['name']
        pop_window = tk.Tk()
        pop_window.title('编辑')
        pop_window.wm_attributes('-topmost', 1)
        # 第3步，设定窗口的大小(长 * 宽)
        pop_window.geometry('500x300')  # 这里的乘是小x

        tk.Label(pop_window, text='软件名称： ').place(x=80, y=40)

        self.add_app_name = tk.Entry(pop_window, font=('Arial', 14))
        self.add_app_name.insert(0, data['name'])
        tk.Label(pop_window, text='软件路径： ').place(x=10, y=100)

        # addr = tk.StringVar(value='https://www.pynote.net')
        self.add_app_url = tk.Entry(pop_window, width=58)  # 显示成明文形式
        self.add_app_url.insert(0, data['url'])
        # 确认按钮
        b = tk.Button(pop_window, text='确定修改', font=('Arial', 12), width=30, height=2, command=self.edit_submit)
        b.place(x=150, y=170)

        self.add_app_name.place(x=150, y=40)
        self.add_app_url.place(x=80, y=100)

        # 第6步，主窗口循环显示
        pop_window.mainloop()

    # 編輯提交
    def edit_submit(self):
        url = self.add_app_url.get()
        name = self.add_app_name.get()

        if not name:
            tkinter.messagebox.showerror(title='编辑提示', message='名称不可以为空！')
            return

        if not url:
            tkinter.messagebox.showerror(title='编辑提示', message='路径不可以为空！')
            return

        if not self.primary_key:
            tkinter.messagebox.showerror(title='编辑提示', message='缺少关键参数，请重试打开尝试！')
            return

        try:
            os.startfile(url)
        except FileNotFoundError:
            tkinter.messagebox.showerror(title='添加软件提示', message='路径错误，没有可执行文件！')
            return

        result = Db().update(self.primary_key, {'name': name, 'url': url})
        # self.edit_app()
        if not result:
            global pop_window
            pop_window.destroy()
            app_now.delete(0, 'end')
            for item in Db().all():
                app_now.insert('end', item['name'])  # 从最后一个位置开始加入值
            return
        tkinter.messagebox.showerror(title='编辑提示', message=result)
        return

    # 编辑
    def edit_app(self):
        global pop_window, app_now
        pop_window = tk.Tk()
        pop_window.title('修改软件')
        # 第3步，设定窗口的大小(长 * 宽)
        pop_window.geometry('500x300')  # 这里的乘是小x
        pop_window.wm_attributes('-topmost', 1)

        tk.Label(pop_window, text='选择软件：').place(x=20, y=20)
        self.add_app_name = tk.Entry(pop_window, font=('Arial', 14))

        # 第5步，创建一个按钮并放置，点击按钮调用print_selection函数
        b1 = tk.Button(pop_window, text='删除', width=15, height=2, command=self.del_submit)
        b2 = tk.Button(pop_window, text='编辑', width=15, height=2, command=self.edit)
        # b3 = tk.Button(pop_window, text='修路径', width=15, height=2, command=self.del_submit)
        b1.place(x=320, y=30)
        b2.place(x=320, y=90)

        app_now = tk.Listbox(pop_window, width=25, height=13)
        # 创建一个list并将值循环添加到Listbox控件中
        for item in Db().all():
            app_now.insert('end', item['name'])  # 从最后一个位置开始加入值
        app_now.select_set(0)
        app_now.place(x=100, y=20)
        # 第6步，主窗口循环显示
        pop_window.mainloop()

        # print('1')

    # 刪除
    @staticmethod
    def del_submit():
        global app_now
        site = app_now.curselection()
        if len(site) < 1:
            tkinter.messagebox.showerror(title='删除提示', message='请选择需要编辑的应用！')
            return

        name_key = Db().all(app_now.get(site))
        name = name_key['name']

        if not name:
            tkinter.messagebox.showerror(title='删除提示', message='缺少关键参数，请重试打开尝试！')
            return
        result = Db().delete(name)
        if not result:
            app_now.delete(0, 'end')
            for item in Db().all():
                app_now.insert('end', item['name'])  # 从最后一个位置开始加入值
            return
        tkinter.messagebox.showerror(title='删除提示', message=result)
        return

    # 添加软件
    def add_app(self):
        global pop_window
        pop_window = tk.Tk()
        pop_window.title('添加软件')
        pop_window.wm_attributes('-topmost', 1)
        # 第3步，设定窗口的大小(长 * 宽)
        pop_window.geometry('500x300')  # 这里的乘是小x
        tk.Label(pop_window, text='软件名称： ').place(x=80, y=40)
        self.add_app_name = tk.Entry(pop_window, font=('Arial', 14))
        tk.Label(pop_window, text='软件路径： ').place(x=10, y=100)
        url_val = tk.StringVar()
        url_val.set("'D:\\code.exe'")
        self.add_app_url = tk.Entry(pop_window, textvariable=url_val, font=('Arial', 14), width=36)  # 显示成明文形式
        # 确认按钮
        b = tk.Button(pop_window, text='确定添加', font=('Arial', 12), width=30, height=2, command=self.add_submit)
        b.place(x=150, y=170)
        self.add_app_name.place(x=150, y=40)
        self.add_app_url.place(x=80, y=100)
        # 第6步，主窗口循环显示
        pop_window.mainloop()

    # 添加软件提交
    def add_submit(self):
        url = self.add_app_url.get()
        name = self.add_app_name.get()
        if name == '':
            tkinter.messagebox.showerror(title='添加软件提示', message='名称不可以为空！')
            return
        if url == '':
            tkinter.messagebox.showerror(title='添加软件提示', message='路径不可以为空！')
            return

        try:
            os.startfile(url)
        except FileNotFoundError:
            tkinter.messagebox.showerror(title='添加软件提示', message='路径错误，没有可执行文件！')
            return

        result = Db().add(name, url)
        if not result:
            global pop_window
            pop_window.destroy()
            return
        tkinter.messagebox.showerror(title='添加软件提示', message=result)
        return


# #################### 软件结束 #########################

# #################### 被引用 #########################
# code......

# #################### 打开软件 #########################
if __name__ == "__main__":
    Work().index()
