import tkinter as tk
import tkinter.font as ft
import tkinter.ttk as ttk
import os
import time
import math

cwd = os.getcwd()

cards=['AC','2C','3C','4C','5C','6C','7C','8C','9C','10C','AD','2D','3D','4D','5D','6D','7D','8D','9D','10D',
'AS','2S','3S','4S','5S','6S','7S','8S','9S','10S','AH','2H','3H','4H','5H','6H','7H','8H','9H','10H']
cardsl=[0]*40
id4locl=[0]*40
shuf_count=3
past_st=[]
future_st=[]
game_state=''
to_newgame=True
to_shuffle=True
to_undo=True
to_redo=True

mainw=tk.Tk()  
mainw.geometry('1200x720')
mainw.title('Perpetual Motion')
mainw.configure(bg='green')

class card() :
   def __init__(self, i) :
       self.name=cards[i]
       self.im1=tk.PhotoImage(file=cwd + "/Images/Cards/" +self.name+".gif")
       self.button=tk.Button(mainw, image=self.im1, command=lambda x=i: swap(x))
       self.button.image=self.im1
       self.suit=i//10+1
       self.serialno=i%10+1
       self.locked=False
       self.loc_on_screen=39-i 
       self.eval_locked=False                  
        
for i in range(len(cards)) :
    cardsl[i]=card(i)    

def pack() :
    history=''
    for i in range(40) :
        history=history+str(cardsl[i].loc_on_screen+10)
    for i in range(1,40,10) :
        history=history+str(int(cardsl[i].locked))
    history=history+str(shuf_count)
    return(history)

def unpack(x) :
    global cardsl
    global shuf_count
    for i in range(40) :
        ab=int(x[i*2:i*2+2])-10
        cardsl[i].loc_on_screen=ab
    cardsl[1].locked=(int(x[80])==1)
    cardsl[11].locked=(int(x[81])==1)
    cardsl[21].locked=(int(x[82])==1)
    cardsl[31].locked=(int(x[83])==1)
    shuf_count=int(x[84])

def id4loc() :  #content=id, index=position, have position want to know the card
    for i in range(len(cardsl)) :
        id4locl[cardsl[i].loc_on_screen]=i
    return()   

def update_grid() :
    for i in range(40) :
        cardsl[i].button.grid(row=cardsl[i].loc_on_screen//10, column=cardsl[i].loc_on_screen%10, pady=3, padx=4)
    return()

def shuffle(x) :
    a=os.urandom(16)
    time.sleep(0.05)
    b=os.urandom(16)
    c=a+b
    d=int.from_bytes(c,'big')
    shuf=d%(math.factorial(len(x)))
    z=[0]*len(x) 
    for i in range(len(x),1,-1) :
        (shuf,card)=divmod(shuf,i)
        z[i-1]=x[card]
        x.remove(z[i-1])
    z[0]=x[0]
    return(z)

def acefb() :
    for i in range(0,40,10) :
        cardsl[i].im1=tk.PhotoImage(file=cwd +"/Images/Cards/Green_back.gif")
        cardsl[i].button.image=cardsl[i].im1
        cardsl[i].button.configure(image=cardsl[i].im1)
    return()

def aceff() :
    for i in range(0,40,10) :
        im=cardsl[i].name
        cardsl[i].im1=tk.PhotoImage(file=cwd +"/Images/Cards/" +im+".gif")
        cardsl[i].button.image=cardsl[i].im1
        cardsl[i].button.configure(image=cardsl[i].im1)

def check_lock() :
    for i in range(40) :
        cardsl[i].eval_locked=False
    for i in range(1,40,10) :
        if cardsl[i].loc_on_screen in (0,10,20,30) :
            j=i
            k=cardsl[j].loc_on_screen
            while j<i+9 :
                if k!=cardsl[j].loc_on_screen : break
                cardsl[j].eval_locked=True
                j=j+1
                k=k+1
    all_lock=True
    for i in range(40) :
        if i%10!=0 :
            all_lock=all_lock and cardsl[i].eval_locked
    return(all_lock)

def move_avail() :
    for i in range(0,40,10) :
        loc_a=cardsl[i].loc_on_screen
        if loc_a%10==0 : return(True)
        if id4locl[loc_a-1]%10 not in [0,9] : return(True)
    return(False) 
       
def lock() :
    check_lock()
    for i in range(40) : cardsl[i].locked=cardsl[i].eval_locked


def refresh() :
    global game_state, to_shuffle, to_undo, to_redo, to_newgame
    id4loc()
    game_state='Good Luck'
    to_newgame=True
    to_shuffle = shuf_count>0
    to_redo = not future_st==[]
    to_undo = not past_st==[]
    if check_lock() : 
        game_state='Game Won!'
        to_redo=False
        to_undo=False
        to_shuffle=False
        to_newgame=False
    elif not move_avail() :
        to_redo=False 
        if shuf_count==0 : 
            game_state='Game Over!'
        else : game_state='No Moves Available'
    else: pass
    butshuf.config(text='Shuffle: #'+ str(shuf_count))
    butredo.config(state=(tk.DISABLED,tk.NORMAL)[int(to_redo)])        
    butundo.config(state=(tk.DISABLED,tk.NORMAL)[int(to_undo)])
    butshuf.config(state=(tk.DISABLED,tk.NORMAL)[int(to_shuffle)])
    label1.configure(text=game_state)
    time.sleep(0.5)
    update_grid()
    


def calshuf() :
    global shuf_count
    global future_st
    global past_st
    past_st=[]
    future_st=[]
    shuf_count=shuf_count-1
    if shuf_count!=2 : lock() #saves arranging cards at start of new game
    aceff()
    unlocked_c=[]
    unlocked_p=[]
    for i in range(40) :
        if cardsl[i].locked==False :
            unlocked_c=unlocked_c+[i]
            unlocked_p=unlocked_p+[cardsl[i].loc_on_screen]
    unlocked_c=shuffle(unlocked_c)
    for i in range(len(unlocked_c)) :
        cardsl[unlocked_c[i]].loc_on_screen=unlocked_p[i]
    refresh()
    mainw.update()
    time.sleep(0.7)
    acefb()
    return()

def find_aloc() :
    goodaces=[]
    for i in range(0,40,10) :
        if cardsl[i].loc_on_screen in (0,10,20,30) :
            goodaces=goodaces+[i]
    return(goodaces)

def choose_ace(x) : #x=goodaces

    def quit_store(x) :
        if x=='No' : v1.set(-1)
        tlv1.destroy()

    tlv1 = tk.Toplevel(mainw)
    tlv1.title('')
    tlvl = tk.Label(tlv1,width=30)
    tlvl.configure(text='Choose Your Ace', font='Arial 16 bold')
    v1 = tk.IntVar(mainw)
    v1.set(-1)
    rb=[0]*len(x)
    tlvl.pack()
    for i in range(len(x)) :
        rb[i] = tk.Radiobutton(tlv1, text='Row: '+ str(cardsl[x[i]].loc_on_screen//10+1), variable=v1, value=i, indicatoron=True)
        rb[i].pack(padx=6)
        rb[i].configure(font='Arial 12 bold')
    tlvb1 = tk.Button(tlv1, text='Choose', command=lambda:quit_store('Yes'), font='Arial 16 bold')
    tlvb2 = tk.Button(tlv1, text='Cancel', command=lambda:quit_store('No'), font='Arial 16 bold')
    tlvb1.pack(side='left', pady=15, padx=40)
    tlvb2.pack(side='left', pady=15, padx=30)
    tlv1.deiconify()
    tlv1.wait_window()
    return(v1.get())

def swap(x) :  #xbeing the card id number
    global future_st
    global past_st
    history=pack()
    if cardsl[x].serialno==1 or cardsl[x].locked==True :
        unpack(history)
        refresh()
        return()
    if cardsl[x].serialno==2 :
        goodaces=find_aloc()
        if len(goodaces)==0 :
            unpack(history)
            refresh()
            return()
        if len(goodaces)==1 :
            (a,b)=(cardsl[x].loc_on_screen,cardsl[goodaces[0]].loc_on_screen)
            (cardsl[x].loc_on_screen,cardsl[goodaces[0]].loc_on_screen)=(b,a) 
            cardsl[x].locked=True
            past_st.append(history)
            future_st=[]
            refresh()
        if len(goodaces)>=2 :
            ace_id=choose_ace(goodaces)
            if ace_id<0 : return
            (a,b)=(cardsl[x].loc_on_screen,cardsl[goodaces[ace_id]].loc_on_screen)
            (cardsl[x].loc_on_screen,cardsl[goodaces[ace_id]].loc_on_screen)=(b,a) 
            cardsl[x].locked=True
            past_st.append(history)
            future_st=[]
            refresh()
    else:
        if cardsl[x-1].loc_on_screen%10==9 :
            unpack(history)
            refresh()
            return()
        if id4locl[cardsl[x-1].loc_on_screen+1] in (0,10,20,30) :
            y=id4locl[cardsl[x-1].loc_on_screen+1]
            (a,b)=(cardsl[x].loc_on_screen,cardsl[y].loc_on_screen)
            (cardsl[x].loc_on_screen,cardsl[y].loc_on_screen)=(b,a)
            past_st.append(history)
            future_st=[]
            refresh()
        else:
            unpack(history) 
            refresh()
    return()   

def do_shuffle() :

  def quit_store(x) :
    vq.set(x)
    tlv2.destroy()

  tlv2 = tk.Toplevel(mainw)
  tlv2.title('') # set title (otherwise inherited from main window which may be unsuitable)
  vq   = tk.StringVar()
  tlvl = tk.Label(tlv2, text='Are you sure?', pady=5, width=25, font='Arial 14 bold')
  tlvb1 = tk.Button(tlv2, text='Yes', command=lambda:quit_store('Yes'), font='Arial 16 bold')
  tlvb2 = tk.Button(tlv2, text='No', command=lambda:quit_store('No'), font='Arial 16 bold')
  tlvl.pack(fill="x")
  tlvb1.pack(side='left', pady=10, padx=50)
  tlvb2.pack(side='left', pady=10, padx=0)
  tlvb2.focus_set() # make default the No buttom
  tlv2.deiconify() # activate - i.e. bring to the front
  tlv2.wait_window() # wait for user to come back from this dialog window
  if vq.get() == 'Yes' : calshuf() 

def n_game() :
    global shuf_count
    shuf_count=3
    for i in range(40) :
        cardsl[i].locked=False
    calshuf()
    return()

def start_n_game() :

  def quit_store(x) :
    vq.set(x)
    tlv2.destroy()
  if to_newgame : 
      tlv2 = tk.Toplevel(mainw)
      tlv2.title('') # set title (otherwise inherited from main window which may be unsuitable)
      vq   = tk.StringVar()
      tlvl = tk.Label(tlv2, text='Are you sure?', pady=5, width=25, font='Arial 14 bold')
      tlvb1 = tk.Button(tlv2, text='Yes', command=lambda:quit_store('Yes'), font='Arial 16 bold')
      tlvb2 = tk.Button(tlv2, text='No', command=lambda:quit_store('No'), font='Arial 16 bold')
      tlvl.pack(fill="x")
      tlvb1.pack(side='left', pady=10, padx=50)
      tlvb2.pack(side='left', pady=10, padx=0)
      tlvb2.focus_set() # make default the No buttom
      tlv2.deiconify() # activate - i.e. bring to the front
      tlv2.wait_window() # wait for user to come back from this dialog window
      if vq.get() == 'Yes' : n_game()
  else: n_game()

def undo() :
    global past_st
    global future_st
    if past_st==[] : 
        refresh()
        return
    history=pack()
    future_st.append(history)
    now=past_st.pop()
    unpack(now)
    refresh()
    return()
        
def redo() :
    global past_st
    global future_st
    if future_st==[] : 
        refresh()
        return
    history=pack()
    past_st.append(history)
    now=future_st.pop()
    unpack(now)
    refresh()
    return()

frm1=tk.Frame(mainw, bg="green", width=600, height=700)
frm1.grid(row=6, column=0, columnspan=14, pady=100, sticky='swse')

imundo=tk.PhotoImage(file=cwd + "/Images/undo.gif")
butundo=tk.Button(frm1, text="Undo", image=imundo, compound="bottom", command=lambda : undo())
butundo.image=imundo
butundo.pack(anchor=tk.SW, side=tk.LEFT, padx=20)

imredo=tk.PhotoImage(file=cwd + "/Images/redo.gif")
butredo=tk.Button(frm1, text="Redo", image=imredo, compound="bottom", command=lambda : redo())
butredo.image=imredo
butredo.pack(anchor=tk.SW, side=tk.LEFT, padx=20)

imbutshuf=tk.PhotoImage(file=cwd + "/Images/shuffle.gif")
butshuf=tk.Button(frm1, text="Shuffle", image=imbutshuf, compound="bottom", command=lambda : do_shuffle())
butshuf.image=imbutshuf
butshuf.pack(anchor=tk.SW, side=tk.LEFT, padx=20)

imngame=tk.PhotoImage(file=cwd + "/Images/newgame.gif")
ngame=tk.Button(frm1, text="New Game", image=imngame, compound="bottom", command=lambda : start_n_game())
ngame.image=imngame
ngame.pack(anchor=tk.SW, side=tk.LEFT, padx=20)

label1=tk.Label(frm1,text='', font='Arial 16 bold')
label1.pack(anchor=tk.SW)

n_game()

mainw.mainloop()
