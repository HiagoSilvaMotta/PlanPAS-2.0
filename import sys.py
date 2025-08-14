import sys
import tkinter as tk
import tkinter.ttk as ttk

from Main_program import Mainloop
from Main_program import modbus
import threading
from queue import Queue

#Extendendo a classe do programa principal
class Main_program_ThreadClient(Mainloop):
    def __init__(self,ip):
        super().__init__(ip)
        self.finalizado = False
        self.lock = threading.Lock()

    #Sobrescrevendo os metodos de escrita/leitura com metodos seguros para threads
    def get_table(self):
        with self.lock:
            return self.table

    def set_table(self, table):
        with self.lock:
            self.table = table

    def enable(self):
        with self.lock:
            self.running = True

    def stop1(self):
        with self.lock:
            self.stop = True

    def getstate(self):
        with self.lock:
            return self.running

    def setprecondition_dict(self, dicti):
        with self.lock:
            self.precondition_dict = dicti

    def getprecondition_dict(self):
        with self.lock:
            return self.precondition_dict

    def seteffect_dict(self, dicti):
        with self.lock:
            self.effect_dict = dicti

    def geteffect_dict(self):
        with self.lock:
            return self.effect_dict

    def run(self):
        self.finalizado = False
        try:
            Mainloop.run(self)
        except Exception as err:
            #self.stop1()
            raise err
            #sys.exit()
        else:
            if self.finalizado:
                return 2


#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk

class aUI:
    def __init__(self, master=None):
        self.ip = None
        self.thread_client = None
        self.client_instance = None
        self.end_que = Queue()
        self.pecas_que = Queue()
        self.descartando_pecaincorreta = False
        self.proximapeca = None
        self.conectado = False
        self.iniciado = False

        #Armazena informações sobre a existencia de uma peça em movimento
        self.moving_piece_data = {
            'type': None,
            'destination': None,
            'moving': False,
            'x_coord': 0,
            'y_coor': 0,
            'start': False
        }
        self.item_dx = 10
        self.item_dy = 10

        #Armazena a quantidade de peças em cada caixa
        self.caixa_descarte1 = {
            'peca_peqnmet': 0,
            'peca_peqmet': 0,
            'peca_mednmet': 0,
            'peca_medmet': 0,
            'peca_grdnmet': 0,
            'peca_grdmet': 0
        }
        self.caixa_descarte2 = {
            'peca_peqnmet': 0,
            'peca_peqmet': 0,
            'peca_mednmet': 0,
            'peca_medmet': 0,
            'peca_grdnmet': 0,
            'peca_grdmet': 0
        }
        self.caixa_descarte3 = {
            'peca_peqnmet': 0,
            'peca_peqmet': 0,
            'peca_mednmet': 0,
            'peca_medmet': 0,
            'peca_grdnmet': 0,
            'peca_grdmet': 0
        }
        self.caixa_descarte4 = {
            'peca_peqnmet': 0,
            'peca_peqmet': 0,
            'peca_mednmet': 0,
            'peca_medmet': 0,
            'peca_grdnmet': 0,
            'peca_grdmet': 0
        }

        self.precondition_dict = {}
        self.table = {
            'liga_esteira': False,
            'anvanca_ap1': False,
            'anvanca_ap2': False,
            'anvanca_ap3': False,
            'retrai_ap3': False,
            'fc_1': False,
            'fc_2': False,
            'fc_3': False,
            'fc_4': False,
            'peca_peqnmet': False,
            'peca_peqmet': False,
            'peca_mednmet': False,
            'peca_medmet': False,
            'peca_grandnmet': False,
            'peca_grandmet': False
        }

        # build ui
        tk2 = tk.Tk(master)  ##cria a janela principal, parece que não precisa desse master
        self.default = []
        for x in range(18):
            self.default.append(tk.IntVar(tk2, 0))

        tk2.configure(height=720, width=1280)
        self.frame3 = ttk.Frame(tk2)
        self.frame3.configure(height=720, width=1280)

        ##Isenrir IP
        message3 = tk.Message(self.frame3)
        message3.configure(text='Digite o IP do CLP', width=100)
        message3.pack(anchor="center", pady=20, side="top")
        self.entry = ttk.Entry(self.frame3)  ## entrada do ip
        self.entry.pack(anchor="center", side="top")
        button1 = ttk.Button(self.frame3)
        button1.configure(text='Definir Endereço', command= self.conectar) ##comando definit endereço
        button1.pack(anchor="center", pady=20, side="top")


        self.frame3.grid(column=0, row=0)
        self.frame3.pack_propagate(0)
        self.frame6 = ttk.Frame(tk2)
        self.frame6.configure(height=720, width=1280)
        self.canvas1 = tk.Canvas(self.frame6)
        self.canvas1.configure(height=450, state="normal", width=1152)
        self.canvas1.pack(padx=20, pady=20, side="top")
        frame5 = ttk.Frame(self.frame6)
        frame5.configure(height=200, width=200)
        labelframe2 = ttk.Labelframe(frame5)
        labelframe2.configure(height=200, text='Selecão de itens', width=200)
        label1 = tk.Label(labelframe2)
        label1.configure(text='Metalica Pequena')
        label1.grid(column=0, padx=20, pady=6, row=1)
        label2 = tk.Label(labelframe2)
        label2.configure(text='Metalica Media')
        label2.grid(column=0, row=2)
        label3 = tk.Label(labelframe2)
        label3.configure(text='Metalica Grande')
        label3.grid(column=0, pady=6, row=3)
        label4 = tk.Label(labelframe2)
        label4.configure(text='Nao metalica pequena')
        label4.grid(column=0, row=4)
        label5 = tk.Label(labelframe2)
        label5.configure(
            cursor="arrow",
            font="TkDefaultFont",
            text='Nao metalica media')
        label5.grid(column=0, pady=6, row=5)
        label6 = tk.Label(labelframe2)
        label6.configure(text='Nao metalica grande')
        label6.grid(column=0, row=6)
        label7 = tk.Label(labelframe2)
        label7.configure(text='Caixa de descarte 1')
        label7.grid(column=1, row=0)
        self.spinbox2 = tk.Spinbox(labelframe2)
        self.spinbox2.configure(from_=0, to=99, textvariable=self.default[0],width=6) ##CX1 MP
        self.spinbox2.grid(column=1, row=1)
        self.spinbox3 = tk.Spinbox(labelframe2)
        self.spinbox3.configure(from_=0, to=99, textvariable=self.default[1],width=6) ##CX1 MM
        self.spinbox3.grid(column=1, row=2)
        self.spinbox4 = tk.Spinbox(labelframe2)
        self.spinbox4.configure(from_=0, to=99, textvariable=self.default[2],width=6) ##CX1 MG
        self.spinbox4.grid(column=1, row=3)
        self.spinbox5 = tk.Spinbox(labelframe2)
        self.spinbox5.configure(from_=0, to=99, textvariable=self.default[3],width=6) ##CX1 NMP
        self.spinbox5.grid(column=1, row=4)
        self.spinbox6 = tk.Spinbox(labelframe2)
        self.spinbox6.configure(from_=0, to=99, textvariable=self.default[4],width=6) ##CX1 NMM
        self.spinbox6.grid(column=1, row=5)
        self.spinbox7 = tk.Spinbox(labelframe2)
        self.spinbox7.configure(from_=0, to=99, textvariable=self.default[5],width=6) ##CX1 NMG
        self.spinbox7.grid(column=1, row=6)
        label8 = tk.Label(labelframe2)
        label8.configure(text='Caixa de descarte 2')
        label8.grid(column=2, padx=17, row=0)
        self.spinbox8 = tk.Spinbox(labelframe2)
        self.spinbox8.configure(from_=0, to=99, textvariable=self.default[6],width=6) ##CX2 MP
        self.spinbox8.grid(column=2, row=1)
        self.spinbox9 = tk.Spinbox(labelframe2)
        self.spinbox9.configure(from_=0, to=99, textvariable=self.default[7],width=6) ##CX2 MM
        self.spinbox9.grid(column=2, row=2)
        self.spinbox10 = tk.Spinbox(labelframe2)
        self.spinbox10.configure(from_=0, to=99, textvariable=self.default[8],width=6) ##CX2 MG
        self.spinbox10.grid(column=2, row=3)
        self.spinbox11 = tk.Spinbox(labelframe2)
        self.spinbox11.configure(from_=0, to=99, textvariable=self.default[9],width=6) ##CX2 NMP
        self.spinbox11.grid(column=2, row=4)
        self.spinbox12 = tk.Spinbox(labelframe2)
        self.spinbox12.configure(from_=0, to=99, textvariable=self.default[10],width=6) ##CX2 NMM
        self.spinbox12.grid(column=2, row=5)
        self.spinbox13 = tk.Spinbox(labelframe2)
        self.spinbox13.configure(from_=0, to=99, textvariable=self.default[11],width=6) ##CX2 NMG
        self.spinbox13.grid(column=2, row=6)
        label9 = tk.Label(labelframe2)
        label9.configure(text='Caixa de descarte 3')
        label9.grid(column=3, row=0)
        self.spinbox14 = tk.Spinbox(labelframe2)
        self.spinbox14.configure(from_=0, to=99, textvariable=self.default[12],width=6) ##CX3 MP
        self.spinbox14.grid(column=3, row=1)
        self.spinbox15 = tk.Spinbox(labelframe2)
        self.spinbox15.configure(from_=0, to=99, textvariable=self.default[13],width=6) ##CX3 MM
        self.spinbox15.grid(column=3, row=2)
        self.spinbox16 = tk.Spinbox(labelframe2)
        self.spinbox16.configure(from_=0, to=99, textvariable=self.default[14],width=6) ##CX3 MG
        self.spinbox16.grid(column=3, row=3)
        self.spinbox17 = tk.Spinbox(labelframe2)
        self.spinbox17.configure(from_=0, to=99, textvariable=self.default[15],width=6) ##CX3 NMP
        self.spinbox17.grid(column=3, row=4)
        self.spinbox18 = tk.Spinbox(labelframe2)
        self.spinbox18.configure(from_=0, to=99, textvariable=self.default[16],width=6) ##CX3 NMM
        self.spinbox18.grid(column=3, row=5)
        self.spinbox19 = tk.Spinbox(labelframe2)
        self.spinbox19.configure(from_=0, to=99, textvariable=self.default[17],width=6) ##CX3 NMG
        self.spinbox19.grid(column=3, row=6)
        labelframe2.grid(column=0, row=0)
        labelframe4 = ttk.Labelframe(frame5)
        labelframe4.configure(height=200, text='Execução', width=200)
        self.button2 = ttk.Button(labelframe4)
        self.button2.configure(text='Iniciar', command=self.iniciar) ##INICIAR
        tk2.bind('<Return>', self.iniciar)
        self.button2.pack(expand=True, side="top")
        self.button3 = ttk.Button(labelframe4)
        self.button3.configure(text='Reprogamar', command=self.reprogramar) ##REPROG
        self.button3.pack(expand=True, side="top")
        self.button5 = ttk.Button(labelframe4)
        self.button5.configure(text='Parar', command=self.parar) ##PARAR
        self.button5.pack(expand=True, side="top")
        button4 = ttk.Button(labelframe4)
        button4.configure(text='Voltar', command=self.desconectar) ##VOLTAR
        button4.pack(expand=True, side="top")
        labelframe4.grid(column=2, padx=25, row=0)
        labelframe4.pack_propagate(0)
        labelframe3 = ttk.Labelframe(frame5)
        labelframe3.configure(
            height=200,
            text='Painel de mensagens',
            width=200)
        self.text1 = tk.Text(labelframe3)
        self.text1.configure(height=10, state="disabled", width=50)
        self.text1.pack(padx=0, pady=0, side="top")
        labelframe3.grid(column=3, row=0)
        frame5.pack(side="top")
        self.frame6.grid(column=0, row=0)
        self.frame6.pack_propagate(0)

        self.frame3.tkraise()

        # Main widget
        self.mainwindow = tk2

    def new_window(self, message):
        # Create a new window
        window = tk.Toplevel()
        window.title("Mensagem")

        # Set the size of the new window
        window.geometry("300x100")

        # Create a label to display the message
        label = tk.Label(window, text=message)
        label.pack(pady=15)

        # Create a button to close the new window
        close_button = tk.Button(window, text="Fechar", command=window.destroy)
        close_button.pack(pady=10)

    def load_gif_frames(self, file_path):
        frames = []
        image = tk.PhotoImage(file=file_path)
        try:
            i = 0
            while True:
                frames.append(image.subsample(1, 1).copy())
                i += 1
                image = tk.PhotoImage(file=file_path, format=f"gif -index {i}")
        except:
            pass
        return frames

    def run(self):
        self.update()
        self.mainwindow.mainloop()

    #Atualiza a interface
    def update(self):

        if not self.end_que.empty():
            if self.end_que.get() == 2:
                self.text1.configure(state="normal")
                self.text1.insert(tk.END, "Plano finalizado com sucesso\n")
                self.text1.see(tk.END)
                self.text1.configure(state="disabled")

                #Zerando as demanddas
                for value in range(18):
                    self.default[value].set(0)

                #Zerando os itens nas caixas:
                pecas = ['peca_peqnmet', 'peca_peqmet', 'peca_mednmet', 'peca_medmet', 'peca_grdnmet', 'peca_grdmet']
                for item in pecas:
                    self.caixa_descarte1[item] = 0
                    self.caixa_descarte2[item] = 0
                    self.caixa_descarte3[item] = 0
                    self.caixa_descarte4[item] = 0


        if self.thread_client is not None and self.thread_client.is_alive():
            self.spinbox2.configure(state=tk.DISABLED)
            self.spinbox3.configure(state=tk.DISABLED)
            self.spinbox4.configure(state=tk.DISABLED)
            self.spinbox5.configure(state=tk.DISABLED)
            self.spinbox6.configure(state=tk.DISABLED)
            self.spinbox7.configure(state=tk.DISABLED)
            self.spinbox8.configure(state=tk.DISABLED)
            self.spinbox9.configure(state=tk.DISABLED)
            self.spinbox10.configure(state=tk.DISABLED)
            self.spinbox11.configure(state=tk.DISABLED)
            self.spinbox12.configure(state=tk.DISABLED)
            self.spinbox13.configure(state=tk.DISABLED)
            self.spinbox14.configure(state=tk.DISABLED)
            self.spinbox15.configure(state=tk.DISABLED)
            self.spinbox16.configure(state=tk.DISABLED)
            self.spinbox17.configure(state=tk.DISABLED)
            self.spinbox18.configure(state=tk.DISABLED)
            self.spinbox19.configure(state=tk.DISABLED)
            self.button2.configure(state=tk.DISABLED)
            self.button3.configure(state=tk.NORMAL)
            self.button5.configure(state=tk.NORMAL)
        else:
            self.spinbox2.configure(state=tk.NORMAL)
            self.spinbox3.configure(state=tk.NORMAL)
            self.spinbox4.configure(state=tk.NORMAL)
            self.spinbox5.configure(state=tk.NORMAL)
            self.spinbox6.configure(state=tk.NORMAL)
            self.spinbox7.configure(state=tk.NORMAL)
            self.spinbox8.configure(state=tk.NORMAL)
            self.spinbox9.configure(state=tk.NORMAL)
            self.spinbox10.configure(state=tk.NORMAL)
            self.spinbox11.configure(state=tk.NORMAL)
            self.spinbox12.configure(state=tk.NORMAL)
            self.spinbox13.configure(state=tk.NORMAL)
            self.spinbox14.configure(state=tk.NORMAL)
            self.spinbox15.configure(state=tk.NORMAL)
            self.spinbox16.configure(state=tk.NORMAL)
            self.spinbox17.configure(state=tk.NORMAL)
            self.spinbox18.configure(state=tk.NORMAL)
            self.spinbox19.configure(state=tk.NORMAL)
            self.button2.configure(state=tk.NORMAL)
            self.button3.configure(state=tk.DISABLED)
            self.button5.configure(state=tk.DISABLED)

        # Informaçao sobre proxima peça a ser inserida e peça chegando
        if self.client_instance is not None:
            new_precondition_dict = self.client_instance.getprecondition_dict()
            new_table = self.client_instance.get_table()
            pecas = ['peca_peqnmet', 'peca_peqmet', 'peca_mednmet', 'peca_medmet', 'peca_grdnmet', 'peca_grdmet']
            for key in pecas:
                if key not in self.precondition_dict and key in new_precondition_dict:
                    self.text1.configure(state="normal")
                    self.text1.insert(tk.END, "Insira a próxima peça: ")
                    match key:
                        case 'peca_peqnmet':
                            self.text1.insert(tk.END, "Pequena não Metálica\n")
                            self.proximapeca = "Pequena não Metálica\n"
                        case 'peca_peqmet':
                            self.text1.insert(tk.END, "Pequena Metálica\n")
                            self.proximapeca = "Pequena Metálica\n"
                        case 'peca_mednmet':
                            self.text1.insert(tk.END, "Média não Metálica\n")
                            self.proximapeca = "Média não Metálica\n"
                        case 'peca_medmet':
                            self.text1.insert(tk.END, "Média Metálica\n")
                            self.proximapeca = "Média Metálica\n"
                        case 'peca_grdnmet':
                            self.text1.insert(tk.END, "Grande não Metálica\n")
                            self.proximapeca = "Grande não Metálica\n"
                        case 'peca_grdmet':
                            self.text1.insert(tk.END, "Grande Metálica\n")
                            self.proximapeca = "Grande Metálica\n"
                    self.text1.see(tk.END)
                    self.text1.configure(state="disabled")


                #Identifica nova peça detectada
                if key in self.table and key in new_table:
                    if self.table[key] is False and new_table[key] is True:
                        while not self.pecas_que.empty():
                            self.pecas_que.get()
                        self.pecas_que.put(key)
                        self.text1.configure(state="normal")

                        match key:
                            case 'peca_peqnmet':
                                self.text1.insert(tk.END, "Peça detectada: Pequena não Metálica\n")
                                self.moving_piece_data['type'] = 'peca_peqnmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True

                            case 'peca_peqmet':
                                self.text1.insert(tk.END, "Peça detectada: Pequena Metálica\n")
                                self.moving_piece_data['type'] = 'peca_peqmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True

                            case 'peca_mednmet':
                                self.text1.insert(tk.END, "Peça detectada: Média não Metálica\n")
                                self.moving_piece_data['type'] = 'peca_mednmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True

                            case 'peca_medmet':
                                self.text1.insert(tk.END, "Peça detectada: Média Metálica\n")
                                self.moving_piece_data['type'] = 'peca_medmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True

                            case 'peca_grdnmet':
                                self.text1.insert(tk.END, "Peça detectada: Grande não Metálica\n")
                                self.moving_piece_data['type'] = 'peca_grdnmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True

                            case 'peca_grdmet':
                                self.text1.insert(tk.END, "Peça detectada: Grande Metálica\n")
                                self.moving_piece_data['type'] = 'peca_grdmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True
                        self.text1.see(tk.END)
                        self.text1.configure(state="disabled")

            #Detecta peça chegando na caixa de descarte
            fc = ['fc_1', 'fc_2', 'fc_3', 'fc_4']
            for key in fc:
                if key in self.table and key in new_table:
                    if self.table[key] is False and new_table[key] is True and not self.pecas_que.empty():
                        self.text1.configure(state="normal")

                        # Informação sobre recebimento de peça
                        self.text1.insert(tk.END, "Peça recebida na caixa ")
                        peca = self.pecas_que.get()
                        match key:
                            case 'fc_1':
                                self.text1.insert(tk.END, "1\n")
                            case 'fc_2':
                                self.text1.insert(tk.END, "2\n")
                            case 'fc_3':
                                self.text1.insert(tk.END, "3\n")
                            case 'fc_4':
                                self.text1.insert(tk.END, "4\n")
                                if self.proximapeca is not None:
                                    self.text1.insert(tk.END, 'Insira a proxima peça: ')
                                    self.text1.insert(tk.END, self.proximapeca)
                        self.text1.see(tk.END)
                        self.text1.configure(state="disabled")

            # Detecta peça incorreta inserida
            pecas = ['peca_peqnmet', 'peca_peqmet', 'peca_mednmet', 'peca_medmet', 'peca_grdnmet', 'peca_grdmet']
            for key3 in pecas:
                if key3 in self.precondition_dict:
                    pecas_err = [item for item in pecas if item != key3]
                    for key4 in pecas_err:
                        if self.table[key4] is True and not self.descartando_pecaincorreta:
                            self.text1.configure(state="normal")
                            self.text1.insert(tk.END, "Peça incorreta, descartando.\n")
                            self.text1.see(tk.END)
                            self.text1.configure(state="disabled")
                            self.descartando_pecaincorreta = True

            self.table = new_table
            self.precondition_dict = new_precondition_dict

        self.UpdateCanvas()

        self.mainwindow.after(50, self.update)

    def handle_buttons(self):

        try:
            self.client_instance = Main_program_ThreadClient(self.ip)
        except Exception as err:
            print('Erro: Não foi possível conectar ao enderço do controlador.')
            self.new_window('Erro: Não foi possível conectar ao enderço do controlador.')
            raise err

        while self.conectado == True and self.iniciado == False:
            #Verifica se o botao de iniciar foi pressionado
            if modbus.read_coil_call(self.client, self.coil_addr['iniciar']) == True:
                self.iniciar()
                        #Verifica se o botao de voltar foi pressionado
            if modbus.read_coil_call(self.client, self.coil_addr['voltar']) == True:
                self.desconectar()

        while self.conectado == True and self.iniciado == True:
            #Verifica se o botao de voltar foi pressionado
            if modbus.read_coil_call(self.client, self.coil_addr['voltar']) == True:
                self.desconectar()

            #Verifica se o botao de parar foi pressionado
            if modbus.read_coil_call(self.client, self.coil_addr['parar']) == True:
                self.parar()
                self.client_instance.running = False

            #Verifica se o botao de reprogramar foi pressionado
            if modbus.read_coil_call(self.client, self.coil_addr['reprog']) == True:
                self.reprogramar()

    def spinboxIO (self):
        
        self.spinbox2.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa1_mp'])
        self.spinbox3.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa1_mm'])
        self.spinbox4.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa1_mg'])
        self.spinbox5.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa1_nmp'])
        self.spinbox6.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa1_nmm'])
        self.spinbox7.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa1_nmg'])
        self.spinbox8.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa2_mp'])
        self.spinbox9.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa2_mm'])
        self.spinbox10.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa2_mg'])
        self.spinbox11.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa2_nmp'])
        self.spinbox12.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa2_nmm'])
        self.spinbox13.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa2_nmg'])
        self.spinbox14.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa3_mp'])
        self.spinbox15.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa3_mm'])
        self.spinbox16.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa3_mg'])
        self.spinbox17.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa3_nmp'])
        self.spinbox18.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa3_nmm'])
        self.spinbox19.insert() = modbus.read_memory_word_call(self.client, self.mem_words_addr['quantidade_caixa3_nmg'])


    def conectar(self):
        entered_value = self.entry.get()
        if entered_value != "":
            self.ip = entered_value
            self.frame6.tkraise()
            self.conectado = True
        else:
            self.new_window('Endereço invalido')

    def iniciar(self):
        # try:
        #     self.client_instance = Main_program_ThreadClient(self.ip)
        # except Exception as err:
        #     print('Erro: Não foi possível conectar ao enderço do controlador.')
        #     self.new_window('Erro: Não foi possível conectar ao enderço do controlador.')
        #     raise err
        self.spinboxIO()
        self.iniciado = True
        self.generate_problem()
        self.client_instance.enable()
        self.text1.configure(state="normal")
        self.text1.insert(tk.END, "Iniciando\n")
        self.text1.see(tk.END)
        self.text1.configure(state="disabled")
        self.thread_client = threading.Thread(target=lambda q, a: q.put(a.run()), args=(self.end_que, self.client_instance))
        self.thread_client.start()

    def reprogramar(self):
        self.client_instance.stop1()
        self.text1.configure(state="normal")
        self.text1.insert(tk.END, "Reprogramando\n")
        self.text1.see(tk.END)
        self.text1.configure(state="disabled")
        while not self.pecas_que.empty():
            self.pecas_que.get()

    def parar(self):
        self.client_instance.stop1()
        # Zerando as demanddas
        for value in range(18):
            self.default[value].set(0)

        # Zerando os itens nas caixas:
        pecas = ['peca_peqnmet', 'peca_peqmet', 'peca_mednmet', 'peca_medmet', 'peca_grdnmet', 'peca_grdmet']
        for item in pecas:
            self.caixa_descarte1[item] = 0
            self.caixa_descarte2[item] = 0
            self.caixa_descarte3[item] = 0
            self.caixa_descarte4[item] = 0
        #self.conectar()
        self.text1.configure(state="normal")
        self.text1.insert(tk.END, "Parando\n")
        self.text1.see(tk.END)
        self.text1.configure(state="disabled")
        while not self.pecas_que.empty():
            self.pecas_que.get()


    def desconectar(self):
        if self.client_instance is not None:
            self.client_instance.stop1()
        self.frame3.tkraise()
        self.conectado = False

    def generate_problem(self):
        # Armazena as informacoes sobre o problema desejado
        items = {
            'cx1_peq_metal': int(self.spinbox2.get()) - self.caixa_descarte1['peca_peqmet'],
            'cx1_med_metal': int(self.spinbox3.get()) - self.caixa_descarte1['peca_medmet'],
            'cx1_grd_metal': int(self.spinbox4.get()) - self.caixa_descarte1['peca_grdmet'],
            'cx1_peq': int(self.spinbox5.get()) - self.caixa_descarte1['peca_peqnmet'],
            'cx1_med': int(self.spinbox6.get()) - self.caixa_descarte1['peca_mednmet'],
            'cx1_grd': int(self.spinbox7.get()) - self.caixa_descarte1['peca_grdnmet'],

            'cx2_peq_metal': int(self.spinbox8.get()) - self.caixa_descarte2['peca_peqmet'],
            'cx2_med_metal': int(self.spinbox9.get()) - self.caixa_descarte2['peca_medmet'],
            'cx2_grd_metal': int(self.spinbox10.get()) - self.caixa_descarte2['peca_grdmet'],
            'cx2_peq': int(self.spinbox11.get()) - self.caixa_descarte2['peca_peqnmet'],
            'cx2_med': int(self.spinbox12.get()) - self.caixa_descarte2['peca_mednmet'],
            'cx2_grd': int(self.spinbox13.get()) - self.caixa_descarte2['peca_grdnmet'],

            'cx3_peq_metal': int(self.spinbox14.get()) - self.caixa_descarte3['peca_peqmet'],
            'cx3_med_metal': int(self.spinbox15.get()) - self.caixa_descarte3['peca_medmet'],
            'cx3_grd_metal': int(self.spinbox16.get()) - self.caixa_descarte3['peca_grdmet'],
            'cx3_peq': int(self.spinbox17.get()) - self.caixa_descarte3['peca_peqnmet'],
            'cx3_med': int(self.spinbox18.get()) - self.caixa_descarte3['peca_mednmet'],
            'cx3_grd': int(self.spinbox19.get()) - self.caixa_descarte3['peca_grdnmet']
        }
        for key in items:
            if items[key] < 0:
                items[key] = 0

        # Gerando o problema a partir das informacoes inseridas
        lines = []

        n_box1 = items['cx1_peq_metal'] + items['cx1_med_metal'] + items['cx1_grd_metal'] + items['cx1_peq'] + items[
            'cx1_med'] + items['cx1_grd']
        n_box2 = items['cx2_peq_metal'] + items['cx2_med_metal'] + items['cx2_grd_metal'] + items['cx2_peq'] + items[
            'cx2_med'] + items['cx2_grd']
        n_box3 = items['cx3_peq_metal'] + items['cx3_med_metal'] + items['cx3_grd_metal'] + items['cx3_peq'] + items[
            'cx3_med'] + items['cx3_grd']

        n_peq_metal = items['cx1_peq_metal'] + items['cx2_peq_metal'] + items['cx3_peq_metal']
        n_med_metal = items['cx1_med_metal'] + items['cx2_med_metal'] + items['cx3_med_metal']
        n_grd_metal = items['cx1_grd_metal'] + items['cx2_grd_metal'] + items['cx3_grd_metal']

        n_peq = items['cx1_peq'] + items['cx2_peq'] + items['cx3_peq']
        n_med = items['cx1_med'] + items['cx2_med'] + items['cx3_med']
        n_grd = items['cx1_grd'] + items['cx2_grd'] + items['cx3_grd']

        n_items = sum(items.values())

        with open('problem-template.pddl', 'r') as f:
            for line in f:
                if line.startswith('	##definir_itens'):
                    line = '        '
                    num = 0
                    tipo_items = {}
                    for x in range(n_peq_metal):
                        line = line + 'item' + str(num) + ' - objeto\n        '
                        tipo_items['item' + str(num)] = 'peqmet'
                        num += 1

                    for x in range(n_med_metal):
                        line = line + 'item' + str(num) + ' - objeto\n        '
                        tipo_items['item' + str(num)] = 'medmet'
                        num += 1

                    for x in range(n_grd_metal):
                        line = line + 'item' + str(num) + ' - objeto\n        '
                        tipo_items['item' + str(num)] = 'grdmet'
                        num += 1

                    for x in range(n_peq):
                        line = line + 'item' + str(num) + ' - objeto\n        '
                        tipo_items['item' + str(num)] = 'peqnmet'
                        num += 1

                    for x in range(n_med):
                        line = line + 'item' + str(num) + ' - objeto\n        '
                        tipo_items['item' + str(num)] = 'mednmet'
                        num += 1

                    for x in range(n_grd):
                        line = line + 'item' + str(num) + ' - objeto\n        '
                        tipo_items['item' + str(num)] = 'grdnmet'
                        num += 1

                if line.startswith('	##definir_tipos'):
                    line = '        '
                    num = 0
                    tipo_items = {}
                    for x in range(n_peq_metal):
                        line = line + '(type item' + str(num) + ' ' + 'peqmet1)\n        '
                        tipo_items['item' + str(num)] = 'peqmet'
                        num += 1

                    for x in range(n_med_metal):
                        line = line + '(type item' + str(num) + ' ' + 'medmet1)\n        '
                        tipo_items['item' + str(num)] = 'medmet'
                        num += 1

                    for x in range(n_grd_metal):
                        line = line + '(type item' + str(num) + ' ' + 'grdmet1)\n        '
                        tipo_items['item' + str(num)] = 'grdmet'
                        num += 1

                    for x in range(n_peq):
                        line = line + '(type item' + str(num) + ' ' + 'peqnmet1)\n        '
                        tipo_items['item' + str(num)] = 'peqnmet'
                        num += 1

                    for x in range(n_med):
                        line = line + '(type item' + str(num) + ' ' + 'mednmet1)\n        '
                        tipo_items['item' + str(num)] = 'mednmet'
                        num += 1

                    for x in range(n_grd):
                        line = line + '(type item' + str(num) + ' ' + 'grdnmet1)\n        '
                        tipo_items['item' + str(num)] = 'grdnmet'
                        num += 1



                if line.startswith('	##definir_inicio'):
                    line = '        '
                    for x in range(n_items):
                        line = line + '(at item' + str(x) + ' inicio' + ')\n        '

                if line.startswith('        ##definir_destino'):
                    line = '        '

                    key_list = list(tipo_items.keys())

                    for keys in items:
                        match keys:
                            case 'cx1_peq_metal':
                                for x in range(items['cx1_peq_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx1_med_metal':
                                for x in range(items['cx1_med_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('medmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx1_grd_metal':
                                for x in range(items['cx1_grd_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx1_peq':
                                for x in range(items['cx1_peq']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqnmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx1_med':
                                for x in range(items['cx1_med']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('mednmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx1_grd':
                                for x in range(items['cx1_grd']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdnmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx2_peq_metal':
                                for x in range(items['cx2_peq_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx2_med_metal':
                                for x in range(items['cx2_med_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('medmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx2_grd_metal':
                                for x in range(items['cx2_grd_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx2_peq':
                                for x in range(items['cx2_peq']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqnmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx2_med':
                                for x in range(items['cx2_med']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('mednmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx2_grd':
                                for x in range(items['cx2_grd']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdnmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx3_peq_metal':
                                for x in range(items['cx3_peq_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqmet')
                                    tipo_items[key_list[position]] = 'box3'

                            case 'cx3_med_metal':
                                for x in range(items['cx3_med_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('medmet')
                                    tipo_items[key_list[position]] = 'box3'

                            case 'cx3_grd_metal':
                                for x in range(items['cx3_grd_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdmet')
                                    tipo_items[key_list[position]] = 'box3'

                            case 'cx3_peq':
                                for x in range(items['cx3_peq']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqnmet')
                                    tipo_items[key_list[position]] = 'box3'

                            case 'cx3_med':
                                for x in range(items['cx3_med']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('mednmet')
                                    tipo_items[key_list[position]] = 'box3'

                            case 'cx3_grd':
                                for x in range(items['cx3_grd']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdnmet')
                                    tipo_items[key_list[position]] = 'box3'

                    # for x in range(n_box1):
                    #   line += '(at box1 ' +
                    for key, value in tipo_items.items():
                        line += '(at ' + key + ' ' + value + ')' + '\n        '

                lines.append(line)

        # Escrevendo o problema no arquivo
        with open('problem.pddl', 'w') as f:
            f.writelines(lines)

    #adiciona um item ao contador da caixa de descarte
    def add_itemcounter(self,piece_type,destination):
        match destination:
            case 'fc_1':
                self.caixa_descarte1[piece_type] = self.caixa_descarte1[piece_type] + 1
            case 'fc_2':
                self.caixa_descarte2[piece_type] = self.caixa_descarte2[piece_type] + 1
            case 'fc_3':
                self.caixa_descarte3[piece_type] = self.caixa_descarte3[piece_type] + 1
            case 'fc_4':
                self.caixa_descarte4[piece_type] = self.caixa_descarte4[piece_type] + 1
                self.descartando_pecaincorreta = False



    def update_img_pos(self, piece_type):
        #destination = 'fc_1'
        # Atualiza o destino
        destination = None
        fc = ['fc_1', 'fc_2', 'fc_3']
        for key in fc:
            if key in self.client_instance.geteffect_dict():
                if self.client_instance.geteffect_dict()[key] is True:
                    destination = key

        if self.descartando_pecaincorreta:
            destination = 'fc_4'

        if destination is not None:

            match destination:
                case 'fc_1':
                    x_stopping = 340
                    y_stopping = 350
                case 'fc_2':
                    x_stopping = 570
                    y_stopping = 350
                case 'fc_3':
                    x_stopping = 800
                    y_stopping = 350
                case 'fc_4':
                    x_stopping = 900
                    y_stopping = 0

            match piece_type:
                case 'peca_peqnmet':
                    if self.canvas1.coords(self.peqnmet_moving_image)[0] < x_stopping:
                        self.canvas1.move(self.peqnmet_moving_image, self.item_dx, 0)

                    else:
                        if self.canvas1.coords(self.peqnmet_moving_image)[1] < y_stopping:
                            self.canvas1.move(self.peqnmet_moving_image, 0, self.item_dy)
                        else:
                            self.moving_piece_data['moving'] = False
                            self.canvas1.itemconfigure(self.peqnmet_moving_image, state=tk.HIDDEN)
                            self.add_itemcounter(piece_type, destination)

                case 'peca_peqmet':
                    if self.canvas1.coords(self.peqmet_moving_image)[0] < x_stopping:
                        self.canvas1.move(self.peqmet_moving_image, self.item_dx, 0)

                    else:
                        if self.canvas1.coords(self.peqmet_moving_image)[1] < y_stopping:
                            self.canvas1.move(self.peqmet_moving_image, 0, self.item_dy)
                        else:
                            self.moving_piece_data['moving'] = False
                            self.canvas1.itemconfigure(self.peqmet_moving_image, state=tk.HIDDEN)
                            self.add_itemcounter(piece_type, destination)

                case 'peca_mednmet':
                    if self.canvas1.coords(self.mednmet_moving_image)[0] < x_stopping:
                        self.canvas1.move(self.mednmet_moving_image, self.item_dx, 0)

                    else:
                        if self.canvas1.coords(self.mednmet_moving_image)[1] < y_stopping:
                            self.canvas1.move(self.mednmet_moving_image, 0, self.item_dy)
                        else:
                            self.moving_piece_data['moving'] = False
                            self.canvas1.itemconfigure(self.mednmet_moving_image, state=tk.HIDDEN)
                            self.add_itemcounter(piece_type, destination)

                case 'peca_medmet':
                    if self.canvas1.coords(self.medmet_moving_image)[0] < x_stopping:
                        self.canvas1.move(self.medmet_moving_image, self.item_dx, 0)

                    else:
                        if self.canvas1.coords(self.medmet_moving_image)[1] < y_stopping:
                            self.canvas1.move(self.medmet_moving_image, 0, self.item_dy)
                        else:
                            self.moving_piece_data['moving'] = False
                            self.canvas1.itemconfigure(self.medmet_moving_image, state=tk.HIDDEN)
                            self.add_itemcounter(piece_type, destination)

                case 'peca_grdmet':
                    if self.canvas1.coords(self.grdmet_moving_image)[0] < x_stopping:
                        self.canvas1.move(self.grdmet_moving_image, self.item_dx, 0)

                    else:
                        if self.canvas1.coords(self.grdmet_moving_image)[1] < y_stopping:
                            self.canvas1.move(self.grdmet_moving_image, 0, self.item_dy)
                        else:
                            self.moving_piece_data['moving'] = False
                            self.canvas1.itemconfigure(self.grdmet_moving_image, state=tk.HIDDEN)
                            self.add_itemcounter(piece_type, destination)

                case 'peca_grdnmet':
                    if self.canvas1.coords(self.grdnmet_moving_image)[0] < x_stopping:
                        self.canvas1.move(self.grdnmet_moving_image, self.item_dx, 0)

                    else:
                        if self.canvas1.coords(self.grdnmet_moving_image)[1] < y_stopping:
                            self.canvas1.move(self.grdnmet_moving_image, 0, self.item_dy)
                        else:
                            self.moving_piece_data['moving'] = False
                            self.canvas1.itemconfigure(self.grdnmet_moving_image, state=tk.HIDDEN)
                            self.add_itemcounter(piece_type, destination)

    def UpdateCanvas(self):

        #Atualizando o desenho da esteira e atuadores
        table = self.table
        if table['liga_esteira']:
            self.canvas1.itemconfigure(self.belt_id, state=tk.HIDDEN)
            self.canvas1.itemconfig(self.belt_moving_id, image=self.belt_moving_frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.belt_moving_frames)
            self.canvas1.itemconfigure(self.belt_moving_id, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.belt_moving_id, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.belt_id, state=tk.NORMAL)

        if table['anvanca_ap1']:
            self.canvas1.itemconfigure(self.expiston1_id, state=tk.NORMAL)
            self.canvas1.itemconfigure(self.piston1_id, state=tk.HIDDEN)
        else:
            self.canvas1.itemconfigure(self.expiston1_id, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.piston1_id, state=tk.NORMAL)

        if table['anvanca_ap2']:
            self.canvas1.itemconfigure(self.expiston2_id, state=tk.NORMAL)
            self.canvas1.itemconfigure(self.piston2_id, state=tk.HIDDEN)
        else:
            self.canvas1.itemconfigure(self.expiston2_id, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.piston2_id, state=tk.NORMAL)

        if table['anvanca_ap3']:
            self.canvas1.itemconfigure(self.expiston3_id, state=tk.NORMAL)
            self.canvas1.itemconfigure(self.piston3_id, state=tk.HIDDEN)
        else:
            self.canvas1.itemconfigure(self.expiston3_id, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.piston3_id, state=tk.NORMAL)



        #Atualizando posição da peça em movimento
        if self.moving_piece_data['moving']:

            if self.moving_piece_data['start'] is True:
                self.moving_piece_data['start'] = False

                Starting_piece_coord = [100, 200]
                match self.moving_piece_data['type']:
                    case 'peca_peqnmet':
                        self.canvas1.itemconfigure(self.peqnmet_moving_image, state=tk.NORMAL)
                        self.canvas1.coords(self.peqnmet_moving_image, *Starting_piece_coord)
                    case 'peca_peqmet':
                        self.canvas1.itemconfigure(self.peqmet_moving_image, state=tk.NORMAL)
                        self.canvas1.coords(self.peqmet_moving_image, *Starting_piece_coord)
                    case 'peca_medmet':
                        self.canvas1.itemconfigure(self.medmet_moving_image, state=tk.NORMAL)
                        self.canvas1.coords(self.medmet_moving_image, *Starting_piece_coord)
                    case 'peca_mednmet':
                        self.canvas1.itemconfigure(self.mednmet_moving_image, state=tk.NORMAL)
                        self.canvas1.coords(self.mednmet_moving_image, *Starting_piece_coord)
                    case 'peca_grdnmet':
                        self.canvas1.itemconfigure(self.grdnmet_moving_image, state=tk.NORMAL)
                        self.canvas1.coords(self.grdnmet_moving_image, *Starting_piece_coord)
                    case 'peca_grdmet':
                        self.canvas1.itemconfigure(self.grdmet_moving_image, state=tk.NORMAL)
                        self.canvas1.coords(self.grdmet_moving_image, *Starting_piece_coord)


            self.update_img_pos(self.moving_piece_data['type'])

        #Atualizando exibição das caixas
        self.updateboxes()

    def updateboxes(self):
        #Caixa de descarte 1
        if self.caixa_descarte1['peca_peqnmet'] > 0:
            self.canvas1.itemconfigure(self.cx1p_t, state=tk.NORMAL, text='P\n'+str(self.caixa_descarte1['peca_peqnmet']))
            self.canvas1.itemconfigure(self.cx1p, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx1p_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx1p, state=tk.HIDDEN)

        if self.caixa_descarte1['peca_mednmet'] > 0:
            self.canvas1.itemconfigure(self.cx1m_t, state=tk.NORMAL, text='M\n'+str(self.caixa_descarte1['peca_mednmet']))
            self.canvas1.itemconfigure(self.cx1m, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx1m_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx1m, state=tk.HIDDEN)

        if self.caixa_descarte1['peca_grdnmet'] > 0:
            self.canvas1.itemconfigure(self.cx1g_t, state=tk.NORMAL, text='G\n'+str(self.caixa_descarte1['peca_grdnmet']))
            self.canvas1.itemconfigure(self.cx1g, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx1g_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx1g, state=tk.HIDDEN)

        if self.caixa_descarte1['peca_peqmet'] > 0:
            self.canvas1.itemconfigure(self.cx1pm_t, state=tk.NORMAL,
                                       text='P\n' + str(self.caixa_descarte1['peca_peqmet']))
            self.canvas1.itemconfigure(self.cx1pm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx1pm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx1pm, state=tk.HIDDEN)

        if self.caixa_descarte1['peca_medmet'] > 0:
            self.canvas1.itemconfigure(self.cx1mm_t, state=tk.NORMAL,
                                       text='M\n' + str(self.caixa_descarte1['peca_medmet']))
            self.canvas1.itemconfigure(self.cx1mm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx1mm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx1mm, state=tk.HIDDEN)

        if self.caixa_descarte1['peca_grdmet'] > 0:
            self.canvas1.itemconfigure(self.cx1gm_t, state=tk.NORMAL,
                                       text='G\n' + str(self.caixa_descarte1['peca_grdmet']))
            self.canvas1.itemconfigure(self.cx1gm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx1gm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx1gm, state=tk.HIDDEN)

        #Caixa de descarte2
        if self.caixa_descarte2['peca_peqnmet'] > 0:
            self.canvas1.itemconfigure(self.cx2p_t, state=tk.NORMAL, text='P\n'+str(self.caixa_descarte2['peca_peqnmet']))
            self.canvas1.itemconfigure(self.cx2p, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx2p_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx2p, state=tk.HIDDEN)

        if self.caixa_descarte2['peca_mednmet'] > 0:
            self.canvas1.itemconfigure(self.cx2m_t, state=tk.NORMAL, text='M\n'+str(self.caixa_descarte2['peca_mednmet']))
            self.canvas1.itemconfigure(self.cx2m, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx2m_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx2m, state=tk.HIDDEN)

        if self.caixa_descarte2['peca_grdnmet'] > 0:
            self.canvas1.itemconfigure(self.cx2g_t, state=tk.NORMAL, text='G\n'+str(self.caixa_descarte2['peca_grdnmet']))
            self.canvas1.itemconfigure(self.cx2g, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx2g_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx2g, state=tk.HIDDEN)

        if self.caixa_descarte2['peca_peqmet'] > 0:
            self.canvas1.itemconfigure(self.cx2pm_t, state=tk.NORMAL,
                                       text='P\n' + str(self.caixa_descarte2['peca_peqmet']))
            self.canvas1.itemconfigure(self.cx2pm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx2pm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx2pm, state=tk.HIDDEN)

        if self.caixa_descarte2['peca_medmet'] > 0:
            self.canvas1.itemconfigure(self.cx2mm_t, state=tk.NORMAL,
                                       text='M\n' + str(self.caixa_descarte2['peca_medmet']))
            self.canvas1.itemconfigure(self.cx2mm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx2mm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx2mm, state=tk.HIDDEN)

        if self.caixa_descarte2['peca_grdmet'] > 0:
            self.canvas1.itemconfigure(self.cx2gm_t, state=tk.NORMAL,
                                       text='G\n' + str(self.caixa_descarte2['peca_grdmet']))
            self.canvas1.itemconfigure(self.cx2gm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx2gm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx2gm, state=tk.HIDDEN)

        # Caixa de descarte 3
        if self.caixa_descarte3['peca_peqnmet'] > 0:
            self.canvas1.itemconfigure(self.cx3p_t, state=tk.NORMAL,
                                       text='P\n' + str(self.caixa_descarte3['peca_peqnmet']))
            self.canvas1.itemconfigure(self.cx3p, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx3p_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx3p, state=tk.HIDDEN)

        if self.caixa_descarte3['peca_mednmet'] > 0:
            self.canvas1.itemconfigure(self.cx3m_t, state=tk.NORMAL,
                                       text='M\n' + str(self.caixa_descarte3['peca_mednmet']))
            self.canvas1.itemconfigure(self.cx3m, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx3m_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx3m, state=tk.HIDDEN)

        if self.caixa_descarte3['peca_grdnmet'] > 0:
            self.canvas1.itemconfigure(self.cx3g_t, state=tk.NORMAL,
                                       text='G\n' + str(self.caixa_descarte3['peca_grdnmet']))
            self.canvas1.itemconfigure(self.cx3g, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx3g_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx3g, state=tk.HIDDEN)

        if self.caixa_descarte3['peca_peqmet'] > 0:
            self.canvas1.itemconfigure(self.cx3pm_t, state=tk.NORMAL,
                                       text='P\n' + str(self.caixa_descarte3['peca_peqmet']))
            self.canvas1.itemconfigure(self.cx3pm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx3pm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx3pm, state=tk.HIDDEN)

        if self.caixa_descarte3['peca_medmet'] > 0:
            self.canvas1.itemconfigure(self.cx3mm_t, state=tk.NORMAL,
                                       text='M\n' + str(self.caixa_descarte3['peca_medmet']))
            self.canvas1.itemconfigure(self.cx3mm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx3mm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx3mm, state=tk.HIDDEN)

        if self.caixa_descarte3['peca_grdmet'] > 0:
            self.canvas1.itemconfigure(self.cx3gm_t, state=tk.NORMAL,
                                       text='G\n' + str(self.caixa_descarte3['peca_grdmet']))
            self.canvas1.itemconfigure(self.cx3gm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx3gm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx3gm, state=tk.HIDDEN)

        # Caixa de descarte 4
        if self.caixa_descarte4['peca_peqnmet'] > 0:
            self.canvas1.itemconfigure(self.cx4p_t, state=tk.NORMAL,
                                       text='P\n' + str(self.caixa_descarte4['peca_peqnmet']))
            self.canvas1.itemconfigure(self.cx4p, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx4p_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx4p, state=tk.HIDDEN)

        if self.caixa_descarte4['peca_mednmet'] > 0:
            self.canvas1.itemconfigure(self.cx4m_t, state=tk.NORMAL,
                                       text='M\n' + str(self.caixa_descarte4['peca_mednmet']))
            self.canvas1.itemconfigure(self.cx4m, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx4m_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx4m, state=tk.HIDDEN)

        if self.caixa_descarte4['peca_grdnmet'] > 0:
            self.canvas1.itemconfigure(self.cx4g_t, state=tk.NORMAL,
                                       text='G\n' + str(self.caixa_descarte4['peca_grdnmet']))
            self.canvas1.itemconfigure(self.cx4g, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx4g_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx4g, state=tk.HIDDEN)

        if self.caixa_descarte4['peca_peqmet'] > 0:
            self.canvas1.itemconfigure(self.cx4pm_t, state=tk.NORMAL,
                                       text='P\n' + str(self.caixa_descarte4['peca_peqmet']))
            self.canvas1.itemconfigure(self.cx4pm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx4pm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx4pm, state=tk.HIDDEN)

        if self.caixa_descarte4['peca_medmet'] > 0:
            self.canvas1.itemconfigure(self.cx4mm_t, state=tk.NORMAL,
                                       text='M\n' + str(self.caixa_descarte4['peca_medmet']))
            self.canvas1.itemconfigure(self.cx4mm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx4mm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx4mm, state=tk.HIDDEN)

        if self.caixa_descarte4['peca_grdmet'] > 0:
            self.canvas1.itemconfigure(self.cx4gm_t, state=tk.NORMAL,
                                       text='G\n' + str(self.caixa_descarte4['peca_grdmet']))
            self.canvas1.itemconfigure(self.cx4gm, state=tk.NORMAL)
        else:
            self.canvas1.itemconfigure(self.cx4gm_t, state=tk.HIDDEN)
            self.canvas1.itemconfigure(self.cx4gm, state=tk.HIDDEN)

if __name__ == "__main__":
    app = aUI()
    app.run()