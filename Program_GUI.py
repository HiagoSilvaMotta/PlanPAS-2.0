import sys
import tkinter as tk
import tkinter.ttk as ttk
import time

from Main_program import Mainloop
from Main_program import modbus
import threading
from queue import Queue

from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

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
        self.root = master

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
        tk2 = tk.Tk(master)

        self.default = []
        for x in range(18):
            self.default.append(tk.IntVar(tk2, 0))

        tk2.configure(height=720, width=1280)
        self.frame3 = ttk.Frame(tk2)
        self.frame3.configure(height=720, width=1280)
        message3 = tk.Message(self.frame3)
        message3.configure(text='Digite o IP do CLP', width=100)
        message3.pack(anchor="center", pady=20, side="top")
        self.entry = ttk.Entry(self.frame3)
        self.entry.pack(anchor="center", side="top")
        button1 = ttk.Button(self.frame3)
        button1.configure(text='Definir Endereço', command= self.conectar)
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
        self.spinbox2.configure(from_=0, to=99, textvariable=self.default[0],width=6)
        self.spinbox2.grid(column=1, row=1)
        self.spinbox3 = tk.Spinbox(labelframe2)
        self.spinbox3.configure(from_=0, to=99, textvariable=self.default[1],width=6)
        self.spinbox3.grid(column=1, row=2)
        self.spinbox4 = tk.Spinbox(labelframe2)
        self.spinbox4.configure(from_=0, to=99, textvariable=self.default[2],width=6)
        self.spinbox4.grid(column=1, row=3)
        self.spinbox5 = tk.Spinbox(labelframe2)
        self.spinbox5.configure(from_=0, to=99, textvariable=self.default[3],width=6)
        self.spinbox5.grid(column=1, row=4)
        self.spinbox6 = tk.Spinbox(labelframe2)
        self.spinbox6.configure(from_=0, to=99, textvariable=self.default[4],width=6)
        self.spinbox6.grid(column=1, row=5)
        self.spinbox7 = tk.Spinbox(labelframe2)
        self.spinbox7.configure(from_=0, to=99, textvariable=self.default[5],width=6)
        self.spinbox7.grid(column=1, row=6)
        label8 = tk.Label(labelframe2)
        label8.configure(text='Caixa de descarte 2')
        label8.grid(column=2, padx=17, row=0)
        self.spinbox8 = tk.Spinbox(labelframe2)
        self.spinbox8.configure(from_=0, to=99, textvariable=self.default[6],width=6)
        self.spinbox8.grid(column=2, row=1)
        self.spinbox9 = tk.Spinbox(labelframe2)
        self.spinbox9.configure(from_=0, to=99, textvariable=self.default[7],width=6)
        self.spinbox9.grid(column=2, row=2)
        self.spinbox10 = tk.Spinbox(labelframe2)
        self.spinbox10.configure(from_=0, to=99, textvariable=self.default[8],width=6)
        self.spinbox10.grid(column=2, row=3)
        self.spinbox11 = tk.Spinbox(labelframe2)
        self.spinbox11.configure(from_=0, to=99, textvariable=self.default[9],width=6)
        self.spinbox11.grid(column=2, row=4)
        self.spinbox12 = tk.Spinbox(labelframe2)
        self.spinbox12.configure(from_=0, to=99, textvariable=self.default[10],width=6)
        self.spinbox12.grid(column=2, row=5)
        self.spinbox13 = tk.Spinbox(labelframe2)
        self.spinbox13.configure(from_=0, to=99, textvariable=self.default[11],width=6)
        self.spinbox13.grid(column=2, row=6)
        label9 = tk.Label(labelframe2)
        label9.configure(text='Caixa de descarte 3')
        label9.grid(column=3, row=0)
        self.spinbox14 = tk.Spinbox(labelframe2)
        self.spinbox14.configure(from_=0, to=99, textvariable=self.default[12],width=6)
        self.spinbox14.grid(column=3, row=1)
        self.spinbox15 = tk.Spinbox(labelframe2)
        self.spinbox15.configure(from_=0, to=99, textvariable=self.default[13],width=6)
        self.spinbox15.grid(column=3, row=2)
        self.spinbox16 = tk.Spinbox(labelframe2)
        self.spinbox16.configure(from_=0, to=99, textvariable=self.default[14],width=6)
        self.spinbox16.grid(column=3, row=3)
        self.spinbox17 = tk.Spinbox(labelframe2)
        self.spinbox17.configure(from_=0, to=99, textvariable=self.default[15],width=6)
        self.spinbox17.grid(column=3, row=4)
        self.spinbox18 = tk.Spinbox(labelframe2)
        self.spinbox18.configure(from_=0, to=99, textvariable=self.default[16],width=6)
        self.spinbox18.grid(column=3, row=5)
        self.spinbox19 = tk.Spinbox(labelframe2)
        self.spinbox19.configure(from_=0, to=99, textvariable=self.default[17],width=6)
        self.spinbox19.grid(column=3, row=6)
        labelframe2.grid(column=0, row=0)
        labelframe4 = ttk.Labelframe(frame5)
        labelframe4.configure(height=200, text='Execução', width=200)
        self.button2 = ttk.Button(labelframe4)
        self.button2.configure(text='Iniciar', command=self.iniciar)
        tk2.bind('<Return>', self.iniciar)
        self.button2.pack(expand=True, side="top")
        self.button3 = ttk.Button(labelframe4)
        self.button3.configure(text='Reprogamar', command=self.reprogramar)
        self.button3.pack(expand=True, side="top")
        self.button5 = ttk.Button(labelframe4)
        self.button5.configure(text='Parar', command=self.parar)
        self.button5.pack(expand=True, side="top")
        button4 = ttk.Button(labelframe4)
        button4.configure(text='Voltar', command=self.desconectar)
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

        #Carrega as imagens GIF
        self.expiston = tk.PhotoImage(file='./assets/expiston.gif')
        self.piston = tk.PhotoImage(file='./assets/piston.gif')
        self.grdmet = tk.PhotoImage(file='./assets/grdmet.gif')
        self.medmet = tk.PhotoImage(file='./assets/medmet.gif')
        self.peqmet = tk.PhotoImage(file='./assets/peqmet.gif')
        self.grdnmet = tk.PhotoImage(file='./assets/grdnmet.gif')
        self.mednmet = tk.PhotoImage(file='./assets/mednmet.gif')
        self.peqnmet = tk.PhotoImage(file='./assets/peqnmet.gif')
        self.belt = tk.PhotoImage(file='./assets/belt.gif')
        self.belt_moving_frames = self.load_gif_frames('./assets/belt_moving.gif')

        #Criando imagens no canvas
        self.peqmet_moving_image = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.peqmet)
        self.peqnmet_moving_image = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.peqnmet)
        self.medmet_moving_image = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.medmet)
        self.mednmet_moving_image = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.mednmet)
        self.grdmet_moving_image = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.grdmet)
        self.grdnmet_moving_image = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.grdnmet)

        self.piston1_id = self.canvas1.create_image(345, 15, anchor=tk.NW, image=self.piston)
        self.piston2_id = self.canvas1.create_image(575, 15, anchor=tk.NW, image=self.piston)
        self.piston3_id = self.canvas1.create_image(785, 15, anchor=tk.NW, image=self.piston)
        self.expiston1_id = self.canvas1.create_image(345, 15, anchor=tk.NW, image=self.expiston)
        self.expiston2_id = self.canvas1.create_image(575, 15, anchor=tk.NW, image=self.expiston)
        self.expiston3_id = self.canvas1.create_image(785, 15, anchor=tk.NW, image=self.expiston)


        #Configurando imagens
        self.belt_id = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.belt)
        self.belt_moving_id = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.belt_moving_frames[0])
        self.frame_index = 0
        self.canvas1.tag_raise(self.piston1_id)
        self.canvas1.tag_raise(self.piston2_id)
        self.canvas1.tag_raise(self.piston3_id)
        self.canvas1.tag_raise(self.expiston1_id)
        self.canvas1.tag_raise(self.expiston2_id)
        self.canvas1.tag_raise(self.expiston3_id)
        self.canvas1.itemconfigure(self.expiston1_id, state=tk.HIDDEN)
        self.canvas1.itemconfigure(self.expiston2_id, state=tk.HIDDEN)
        self.canvas1.itemconfigure(self.expiston3_id, state=tk.HIDDEN)

        self.canvas1.itemconfigure(self.peqmet_moving_image, state=tk.HIDDEN)
        self.canvas1.tag_raise(self.peqmet_moving_image)

        self.canvas1.itemconfigure(self.peqnmet_moving_image, state=tk.HIDDEN)
        self.canvas1.tag_raise(self.peqnmet_moving_image)

        self.canvas1.itemconfigure(self.medmet_moving_image, state=tk.HIDDEN)
        self.canvas1.tag_raise(self.medmet_moving_image)

        self.canvas1.itemconfigure(self.mednmet_moving_image, state=tk.HIDDEN)
        self.canvas1.tag_raise(self.mednmet_moving_image)

        self.canvas1.itemconfigure(self.grdnmet_moving_image, state=tk.HIDDEN)
        self.canvas1.tag_raise(self.grdnmet_moving_image)

        self.canvas1.itemconfigure(self.grdmet_moving_image, state=tk.HIDDEN)
        self.canvas1.tag_raise(self.grdmet_moving_image)

        #definindo imagens de exibição da quantidade de peças em cada caixa
        self.cx1pm = self.canvas1.create_oval(320, 350, 355, 385, fill='black', state='hidden')
        self.cx1pm_t = self.canvas1.create_text(338, 368, text=str('P\n0'),fill="white", state='hidden')
        self.cx1mm = self.canvas1.create_oval(355, 350, 390, 385, fill='black', state='hidden')
        self.cx1mm_t = self.canvas1.create_text(373, 368, text=str('M\n0'), fill="white", state='hidden')
        self.cx1gm = self.canvas1.create_oval(390, 350, 425, 385, fill='black', state='hidden')
        self.cx1gm_t = self.canvas1.create_text(408, 368, text=str('G\n0'), fill="white", state='hidden')
        self.cx1p = self.canvas1.create_oval(320, 385, 355, 420, fill='white', state='hidden')
        self.cx1p_t = self.canvas1.create_text(338, 403, text=str('P\n0'), fill="black", state='hidden')
        self.cx1m = self.canvas1.create_oval(355, 385, 390, 420, fill='white', state='hidden')
        self.cx1m_t = self.canvas1.create_text(373, 403, text=str('M\n0'), fill="black", state='hidden')
        self.cx1g = self.canvas1.create_oval(390, 385, 425, 420, fill='white', state='hidden')
        self.cx1g_t = self.canvas1.create_text(408, 403, text=str('G\n0'), fill="black", state='hidden')

        self.cx2pm = self.canvas1.create_oval(550, 350, 585, 385, fill='black', state='hidden')
        self.cx2pm_t = self.canvas1.create_text(568, 368, text=str('P\n0'), fill="white", state='hidden')
        self.cx2mm = self.canvas1.create_oval(585, 350, 620, 385, fill='black', state='hidden')
        self.cx2mm_t = self.canvas1.create_text(603, 368, text=str('M\n0'), fill="white", state='hidden')
        self.cx2gm = self.canvas1.create_oval(620, 350, 655, 385, fill='black', state='hidden')
        self.cx2gm_t = self.canvas1.create_text(638, 368, text=str('G\n0'), fill="white", state='hidden')
        self.cx2p = self.canvas1.create_oval(550, 385, 585, 420, fill='white', state='hidden')
        self.cx2p_t = self.canvas1.create_text(568, 403, text=str('P\n0'), fill="black", state='hidden')
        self.cx2m = self.canvas1.create_oval(585, 385, 620, 420, fill='white', state='hidden')
        self.cx2m_t = self.canvas1.create_text(603, 403, text=str('M\n0'), fill="black", state='hidden')
        self.cx2g = self.canvas1.create_oval(620, 385, 655, 420, fill='white', state='hidden')
        self.cx2g_t = self.canvas1.create_text(638, 403, text=str('G\n0'), fill="black", state='hidden')

        self.cx3pm = self.canvas1.create_oval(760, 350, 795, 385, fill='black', state='hidden')
        self.cx3pm_t = self.canvas1.create_text(778, 368, text=str('P\n0'), fill="white", state='hidden')
        self.cx3mm = self.canvas1.create_oval(795, 350, 830, 385, fill='black', state='hidden')
        self.cx3mm_t = self.canvas1.create_text(813, 368, text=str('M\n0'), fill="white", state='hidden')
        self.cx3gm = self.canvas1.create_oval(830, 350, 865, 385, fill='black', state='hidden')
        self.cx3gm_t = self.canvas1.create_text(848, 368, text=str('G\n0'), fill="white", state='hidden')
        self.cx3p = self.canvas1.create_oval(760, 385, 795, 420, fill='white', state='hidden')
        self.cx3p_t = self.canvas1.create_text(778, 403, text=str('P\n0'), fill="black", state='hidden')
        self.cx3m = self.canvas1.create_oval(795, 385, 830, 420, fill='white', state='hidden')
        self.cx3m_t = self.canvas1.create_text(813, 403, text=str('M\n0'), fill="black", state='hidden')
        self.cx3g = self.canvas1.create_oval(830, 385, 865, 420, fill='white', state='hidden')
        self.cx3g_t = self.canvas1.create_text(848, 403, text=str('G\n0'), fill="black", state='hidden')

        self.cx4pm = self.canvas1.create_oval(1000, 175, 1035, 210, fill='black', state='hidden')
        self.cx4pm_t = self.canvas1.create_text(1018, 193, text=str('P\n0'), fill="white", state='hidden')
        self.cx4mm = self.canvas1.create_oval(1000, 210, 1035, 245, fill='black', state='hidden')
        self.cx4mm_t = self.canvas1.create_text(1018, 228, text=str('M\n0'), fill="white", state='hidden')
        self.cx4gm = self.canvas1.create_oval(1000, 245, 1035, 280, fill='black', state='hidden')
        self.cx4gm_t = self.canvas1.create_text(1018, 263, text=str('G\n0'), fill="white", state='hidden')
        self.cx4p = self.canvas1.create_oval(1035, 175, 1070, 210, fill='white', state='hidden')
        self.cx4p_t = self.canvas1.create_text(1053, 193, text=str('P\n0'), fill="black", state='hidden')
        self.cx4m = self.canvas1.create_oval(1035, 210, 1070, 245, fill='white', state='hidden')
        self.cx4m_t = self.canvas1.create_text(1053, 228, text=str('M\n0'), fill="black", state='hidden')
        self.cx4g = self.canvas1.create_oval(1035, 245, 1070, 280, fill='white', state='hidden')
        self.cx4g_t = self.canvas1.create_text(1053, 263, text=str('G\n0'), fill="black", state='hidden')

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

    def atualiza_descart(self):

        # --- CAIXA 1 ---
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte1['peca_grdmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa1_mg_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte1['peca_medmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa1_mm_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte1['peca_peqmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa1_mp_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte1['peca_grdnmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa1_nmg_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte1['peca_mednmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa1_nmm_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte1['peca_peqnmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa1_nmp_cont'], builder.to_registers())

        # --- CAIXA 2 ---
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte2['peca_grdmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa2_mg_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte2['peca_medmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa2_mm_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte2['peca_peqmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa2_mp_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte2['peca_grdnmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa2_nmg_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte2['peca_mednmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa2_nmm_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte2['peca_peqnmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa2_nmp_cont'], builder.to_registers())

        # --- CAIXA 3 ---
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte3['peca_grdmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa3_mg_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte3['peca_medmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa3_mm_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte3['peca_peqmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa3_mp_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte3['peca_grdnmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa3_nmg_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte3['peca_mednmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa3_nmm_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte3['peca_peqnmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa3_nmp_cont'], builder.to_registers())

        # --- CAIXA 4 ---
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte4['peca_grdmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa4_mg_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte4['peca_medmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa4_mm_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte4['peca_peqmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa4_mp_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte4['peca_grdnmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa4_nmg_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte4['peca_mednmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa4_nmm_cont'], builder.to_registers())

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(self.caixa_descarte4['peca_peqnmet'])
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa4_nmp_cont'], builder.to_registers())
        
        # --- TOTAL DE PEÇAS NA CAIXA 1 ---
        total_caixa1 = sum(self.caixa_descarte1.values())
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(total_caixa1)
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa1_total_cont'], builder.to_registers())

        # --- TOTAL DE PEÇAS NA CAIXA 2 ---
        total_caixa2 = sum(self.caixa_descarte2.values())
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(total_caixa2)
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa2_total_cont'], builder.to_registers())

        # --- TOTAL DE PEÇAS NA CAIXA 3 ---
        total_caixa3 = sum(self.caixa_descarte3.values())
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(total_caixa3)
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa3_total_cont'], builder.to_registers())

        # --- TOTAL DE PEÇAS NA CAIXA 4 ---
        total_caixa4 = sum(self.caixa_descarte4.values())
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(total_caixa4)
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['quantidade_caixa4_total_cont'], builder.to_registers())
        
        # caixas = {
        #     1: self.caixa_descarte1,
        #     2: self.caixa_descarte2,
        #     3: self.caixa_descarte3,
        #     4: self.caixa_descarte4,
        # }

        # map_peca_para_registro = {
        #     'peca_grdmet': 'mg_cont',
        #     'peca_medmet': 'mm_cont',
        #     'peca_peqmet': 'mp_cont',
        #     'peca_grdnmet': 'nmg_cont',
        #     'peca_mednmet': 'nmm_cont',
        #     'peca_peqnmet': 'nmp_cont',
        # }

        # for num_caixa, caixa in caixas.items():
        #     total = 0
        #     for peca, sufixo in map_peca_para_registro.items():
        #         valor = caixa.get(peca, 0)
        #         total += valor
        #         reg_nome = f'quantidade_caixa{num_caixa}_{sufixo}'
        #         endereco = self.client_instance.mem_words_addr.get(reg_nome)
        #         if endereco is not None:
        #             builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        #             builder.add_16bit_int(valor)
        #             self.client_instance.client.write_registers(endereco, builder.to_registers())

        #     # Envia o total da caixa
        #     reg_total = f'quantidade_caixa{num_caixa}_total_cont'
        #     endereco_total = self.client_instance.mem_words_addr.get(reg_total)
        #     if endereco_total is not None:
        #         builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        #         builder.add_16bit_int(total)
        #         self.client_instance.client.write_registers(endereco_total, builder.to_registers())


    #Atualiza a interface
    def update(self):

        if not self.end_que.empty():
            if self.end_que.get() == 2:
                self.text1.configure(state="normal")
                self.text1.insert(tk.END, "Plano finalizado com sucesso\n")
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                builder.add_16bit_int(4)
                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())


                self.text1.see(tk.END)
                self.text1.configure(state="disabled")
                self.iniciado = False

                #Zerando as demanddas
                self.default[0] = 0
                self.default[1] = 0
                self.default[2] = 0
                self.default[3] = 0
                self.default[4] = 0
                self.default[5] = 0
                self.default[6] = 0
                self.default[7] = 0
                self.default[8] = 0
                self.default[9] = 0
                self.default[10] = 0
                self.default[11] = 0
                self.default[12] = 0
                self.default[13] = 0
                self.default[14] = 0
                self.default[15] = 0
                self.default[16] = 0
                self.default[17] = 0

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
                            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                            builder.add_16bit_int(5)
                            self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())
                        case 'peca_peqmet':
                            self.text1.insert(tk.END, "Pequena Metálica\n")
                            self.proximapeca = "Pequena Metálica\n"
                            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                            builder.add_16bit_int(6)
                            self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

                        case 'peca_mednmet':
                            self.text1.insert(tk.END, "Média não Metálica\n")
                            self.proximapeca = "Média não Metálica\n"
                            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                            builder.add_16bit_int(7)
                            self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

                        case 'peca_medmet':
                            self.text1.insert(tk.END, "Média Metálica\n")
                            self.proximapeca = "Média Metálica\n"
                            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                            builder.add_16bit_int(8)
                            self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

                        case 'peca_grdnmet':
                            self.text1.insert(tk.END, "Grande não Metálica\n")
                            self.proximapeca = "Grande não Metálica\n"
                            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                            builder.add_16bit_int(9)
                            self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

                        case 'peca_grdmet':
                            self.text1.insert(tk.END, "Grande Metálica\n")
                            self.proximapeca = "Grande Metálica\n"
                            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                            builder.add_16bit_int(10)
                            self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

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
                                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                                builder.add_16bit_int(11)
                                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

                                
                                self.moving_piece_data['type'] = 'peca_peqnmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True

                            case 'peca_peqmet':
                                self.text1.insert(tk.END, "Peça detectada: Pequena Metálica\n")
                                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                                builder.add_16bit_int(12)
                                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

                                self.moving_piece_data['type'] = 'peca_peqmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True

                            case 'peca_mednmet':
                                self.text1.insert(tk.END, "Peça detectada: Média não Metálica\n")
                                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                                builder.add_16bit_int(13)
                                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

                                self.moving_piece_data['type'] = 'peca_mednmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True

                            case 'peca_medmet':
                                self.text1.insert(tk.END, "Peça detectada: Média Metálica\n")
                                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                                builder.add_16bit_int(14)
                                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

                                self.moving_piece_data['type'] = 'peca_medmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True

                            case 'peca_grdnmet':
                                self.text1.insert(tk.END, "Peça detectada: Grande não Metálica\n")
                                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                                builder.add_16bit_int(15)
                                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

                                self.moving_piece_data['type'] = 'peca_grdnmet'
                                self.moving_piece_data['moving'] = True
                                self.moving_piece_data['start'] = True

                            case 'peca_grdmet':
                                self.text1.insert(tk.END, "Peça detectada: Grande Metálica\n")
                                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                                builder.add_16bit_int(16)
                                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

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
                                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                                builder.add_16bit_int(17)
                                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())
                                self.caixa_descarte1[peca] = self.caixa_descarte1[peca] + 1
                                self.atualiza_descart()
                                #s =('peça '+ peca + 'chegou na caixa1\n')
                                #self.text1.insert(tk.END, s)
                                #s = ('quantidade de pecas do tipo ' + peca + ' na caixa 1:' + str(self.caixa_descarte1[peca])+'\n')
                                #self.text1.insert(tk.END, s)
                            case 'fc_2':
                                self.text1.insert(tk.END, "2\n")
                                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                                builder.add_16bit_int(18)
                                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())
                                self.caixa_descarte2[peca] = self.caixa_descarte2[peca] + 1
                                self.atualiza_descart()
                                #s =('peça ' + peca + 'chegou na caixa2')
                                #self.text1.insert(tk.END, s)
                                #s = ('quantidade de pecas do tipo ' + peca + ' na caixa 2:' + str(self.caixa_descarte2[peca])+'\n')
                                #self.text1.insert(tk.END, s)
                            case 'fc_3':
                                self.text1.insert(tk.END, "3\n")
                                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                                builder.add_16bit_int(19)
                                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())
                                self.caixa_descarte3[peca] = self.caixa_descarte3[peca] + 1
                                self.atualiza_descart()
                                #s = ('peça ' + peca + 'chegou na caixa3')
                                #self.text1.insert(tk.END, s)
                                #s = ('quantidade de pecas do tipo ' + peca + ' na caixa 3:' + str(self.caixa_descarte3[peca])+'\n')
                                #self.text1.insert(tk.END, s)
                            case 'fc_4':
                                self.text1.insert(tk.END, "4\n")
                                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                                builder.add_16bit_int(20)
                                self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

                                if self.proximapeca is not None:
                                    self.text1.insert(tk.END, 'Insira a proxima peça: ')
                                    self.text1.insert(tk.END, self.proximapeca)
                                
                                self.caixa_descarte4[peca] = self.caixa_descarte4[peca] + 1
                                self.atualiza_descart()
                                #s = ('peça ' + peca + 'chegou na caixa4')
                                #self.text1.insert(tk.END, s)
                                #s = ('quantidade de pecas do tipo ' + peca + ' na caixa 4:' + str(self.caixa_descarte4[peca])+'\n')
                                #self.text1.insert(tk.END, s)
                                #self.descartando_pecaincorreta = False
                        self.atualiza_descart()
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
                            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                            builder.add_16bit_int(21)
                            self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

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
        
        self.verificar_botoes()


    def verificar_botoes(self):
       
        if self.iniciado :
            modbus.write_coil_call(self.client_instance.client, self.client_instance.coil_addr['status_iniciado'], True)
        else:
            modbus.write_coil_call(self.client_instance.client, self.client_instance.coil_addr['status_iniciado'], False)

        if self.conectado and not self.iniciado:
            if modbus.read_coil_call(self.client_instance.client, self.client_instance.coil_addr['iniciar']):
                self.iniciar()
                print('Botão iniciar pressionado')

            elif modbus.read_coil_call(self.client_instance.client, self.client_instance.coil_addr['voltar']):
                self.desconectar()
                print('Botão voltar pressionado')

        elif self.conectado and self.iniciado:
            if modbus.read_coil_call(self.client_instance.client, self.client_instance.coil_addr['voltar']):
                self.desconectar()
                print('Botão voltar pressionado')

            elif modbus.read_coil_call(self.client_instance.client, self.client_instance.coil_addr['parar']):
                self.parar()
                print('Botão parar pressionado')

            elif modbus.read_coil_call(self.client_instance.client, self.client_instance.coil_addr['reprog']):
                self.reprogramar()
                print('Botão reprogramar pressionado')

        # Agende a próxima verificação em 200ms (ajuste conforme necessário)
        self.mainwindow.after(200, self.verificar_botoes)

        # while self.conectado == True and self.iniciado == False:
        #     #Verifica se o botao de iniciar foi pressionado
        #     if modbus.read_coil_call(self.client_instance.client, self.client_instance.coil_addr['iniciar']) == True:
        #         self.iniciar()
        #         print('Botão iniciar pressionado')
                    
        #         #Verifica se o botao de voltar foi pressionado
        #     if modbus.read_coil_call(self.client_instance.client, self.client_instance.coil_addr['voltar']) == True:
        #         self.desconectar()
        #         print('Botão voltar pressionado')

                

        # while self.conectado == True and self.iniciado == True:
        #     #Verifica se o botao de voltar foi pressionado
        #     if modbus.read_coil_call(self.client_instance.client, self.client_instance.coil_addr['voltar']) == True:
        #         print('Botão voltar pressionado')
        #         self.desconectar()
                

        #         #Verifica se o botao de parar foi pressionado
        #     if modbus.read_coil_call(self.client_instance.client, self.client_instance.coil_addr['parar']) == True:
        #         print('Botão parar pressionado')
        #         self.parar()
        #         # self.client_instance.running = False

        #     #Verifica se o botao de reprogramar foi pressionado
        #     if modbus.read_coil_call(self.client_instance.client, self.client_instance.coil_addr['reprog']) == True:
        #         print('Botão reprogramar pressionado')
        #         self.reprogramar()


    def spinboxIO(self):
    
        try:
            self.client_instance = Main_program_ThreadClient(self.ip)
        except Exception as err:
            print('Erro: Não foi possível conectar ao enderço do controlador.')
            self.new_window('Erro: Não foi possível conectar ao enderço do controlador.')
            raise err
        
        self.default[0] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa1_mp'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[1] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa1_mm'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[2] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa1_mg'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[3] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa1_nmp'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[4] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa1_nmm'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[5] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa1_nmg'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[6] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa2_mp'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[7] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa2_mm'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[8] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa2_mg'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[9] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa2_nmp'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[10] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa2_nmm'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[11] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa2_nmg'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[12] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa3_mp'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[13] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa3_mm'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[14] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa3_mg'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[15] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa3_nmp'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[16] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa3_nmm'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())
        self.default[17] = (BinaryPayloadDecoder.fromRegisters(self.client_instance.client.read_holding_registers(address=self.client_instance.mem_words_addr['quantidade_caixa3_nmg'], count=1).registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_16bit_int())

    def conectar(self):
        entered_value = self.entry.get()
        if entered_value != "":
            self.ip = entered_value
            self.frame6.tkraise()
            self.conectado = True
            self.handle_buttons()
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
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(1)
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

        self.text1.see(tk.END)
        self.text1.configure(state="disabled")
        self.thread_client = threading.Thread(target=lambda q, a: q.put(a.run()), args=(self.end_que, self.client_instance))
        self.thread_client.start()

    def reprogramar(self):
        self.client_instance.stop1()
        self.client_instance.reset()
        self.iniciado = False
        self.handle_buttons()
        #self.conectar()

        self.text1.configure(state="normal")
        self.text1.insert(tk.END, "Reprogramando\n")
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(2)
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

        self.text1.see(tk.END)
        self.text1.configure(state="disabled")
        while not self.pecas_que.empty():
            self.pecas_que.get()

    def parar(self):
        self.client_instance.stop1()
        self.client_instance.reset()
        self.iniciado = False
        self.handle_buttons()
        # Zerando as demanddas

        self.default[0] = 0
        self.default[1] = 0
        self.default[2] = 0
        self.default[3] = 0
        self.default[4] = 0
        self.default[5] = 0
        self.default[6] = 0
        self.default[7] = 0
        self.default[8] = 0
        self.default[9] = 0
        self.default[10] = 0
        self.default[11] = 0
        self.default[12] = 0
        self.default[13] = 0
        self.default[14] = 0
        self.default[15] = 0
        self.default[16] = 0
        self.default[17] = 0
        

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
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_16bit_int(3)
        self.client_instance.client.write_registers(self.client_instance.mem_words_addr['AVISOS'], builder.to_registers())

        self.text1.see(tk.END)
        self.text1.configure(state="disabled")
        while not self.pecas_que.empty():
            self.pecas_que.get()


    def desconectar(self):
        if self.client_instance is not None:
            self.client_instance.stop1()
            self.conectado = False
        self.frame3.tkraise()

    def generate_problem(self):
        # Armazena as informacoes sobre o problema desejado
        items = {
            'cx1_peq_metal': int(self.default[0]) - self.caixa_descarte1['peca_peqmet'],
            'cx1_med_metal': int(self.default[1]) - self.caixa_descarte1['peca_medmet'],
            'cx1_grd_metal': int(self.default[2]) - self.caixa_descarte1['peca_grdmet'],
            'cx1_peq': int(self.default[3]) - self.caixa_descarte1['peca_peqnmet'],
            'cx1_med': int(self.default[4]) - self.caixa_descarte1['peca_mednmet'],
            'cx1_grd': int(self.default[5]) - self.caixa_descarte1['peca_grdnmet'],

            'cx2_peq_metal': int(self.default[6]) - self.caixa_descarte2['peca_peqmet'],
            'cx2_med_metal': int(self.default[7]) - self.caixa_descarte2['peca_medmet'],
            'cx2_grd_metal': int(self.default[8]) - self.caixa_descarte2['peca_grdmet'],
            'cx2_peq': int(self.default[9]) - self.caixa_descarte2['peca_peqnmet'],
            'cx2_med': int(self.default[10]) - self.caixa_descarte2['peca_mednmet'],
            'cx2_grd': int(self.default[11]) - self.caixa_descarte2['peca_grdnmet'],

            'cx3_peq_metal': int(self.default[12]) - self.caixa_descarte3['peca_peqmet'],
            'cx3_med_metal': int(self.default[13]) - self.caixa_descarte3['peca_medmet'],
            'cx3_grd_metal': int(self.default[14]) - self.caixa_descarte3['peca_grdmet'],
            'cx3_peq': int(self.default[15]) - self.caixa_descarte3['peca_peqnmet'],
            'cx3_med': int(self.default[16]) - self.caixa_descarte3['peca_mednmet'],
            'cx3_grd': int(self.default[17]) - self.caixa_descarte3['peca_grdnmet']
        }
        print(items)
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