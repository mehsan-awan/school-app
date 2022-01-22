import csv
import tkinter
from tkinter import *
import os
from tkinter import ttk,Canvas,messagebox
from csv import writer
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.platypus.tables import Table
from reportlab.lib import colors
from PIL import ImageTk, Image
import pandas as pd


def append_list_as_row(file_name, list_of_elem):
	# Open file in append mode
	with open(file_name, 'a+', newline='') as write_obj:
		# Create a writer object from csv module
		csv_writer = writer(write_obj)
		# Add contents of list as last row in the csv file
		csv_writer.writerow(list_of_elem)


def register():
	new_student_adm_no_info = new_student_adm_no.get()
	new_student_name_info = new_student_name.get()
	new_student_father_name_info = new_student_father_name.get()
	new_student_class_info = new_student_class.get()
	new_student_section_info = new_student_section.get()
	new_student_category_info = new_student_category.get()
	row_contents = [new_student_adm_no_info,new_student_name_info,new_student_father_name_info,new_student_class_info, new_student_section_info,new_student_category_info, str(date.today()),0,0,0,"paid" ,0]

	# Append a list as new line to an old csv file
	append_list_as_row('data.csv', row_contents)
	messagebox.showinfo("New Admission","Registered successfully")
	new_admission()	
	
	
def withdraw():
	adm_no = wdw_adm_no.get()
	wdw_student_name_info = wdw_student_name.get()


	df = pd.read_csv('data.csv', index_col=0)
	name = df.at[int(adm_no), 'Name']
	if name == wdw_student_name_info:
		df.drop([int(adm_no)], inplace=True)
		df.to_csv('data.csv')
		messagebox.showinfo("Withdraw Student", "Student record deleted")
	else:
		messagebox.showerror("Withdraw Student", "Admission No and Name does not match with any student")
	wdw_adm_no_entry.delete(0,'end')
	wdw_name_entry.delete(0,'end')


def new_admission():
	print_one_inv_Frame.pack_forget()
	print_all_inv_Frame.pack_forget()
	new_adm_Frame.pack()
	wdw_Frame.pack_forget()
	print_inv_Frame.pack_forget()

	global new_student_adm_no,adm_no_entry
	Label(new_adm_Frame,text='Admission No:',bg=bottom_color,font=('bold',20)).place(x=50,y=50)
	new_student_adm_no=StringVar()
	adm_no_entry=Entry(new_adm_Frame,textvariable=new_student_adm_no,width=25,font=('bold',20))
	adm_no_entry.place(x=280,y=50)

	global new_student_name,name_entry
	Label(new_adm_Frame,text='Student Name:',bg=bottom_color,font=('bold',20)).place(x=50,y=130)
	new_student_name=StringVar()
	name_entry=Entry(new_adm_Frame,textvariable=new_student_name,width=25,font=('bold',20))
	name_entry.place(x=280,y=130)

	global new_student_father_name,father_name_entry
	Label(new_adm_Frame,text='Father Name:',bg=bottom_color,font=('bold',20)).place(x=50,y=210)
	new_student_father_name=StringVar()
	father_name_entry=Entry(new_adm_Frame,textvariable=new_student_father_name,width=25,font=('bold',20))
	father_name_entry.place(x=280,y=210)
	
	global new_student_class,w
	Label(new_adm_Frame,text='Class:',bg=bottom_color,font=('bold',20)).place(x=50,y=300)
	new_student_class = StringVar()
	new_student_class.set("Select Class") # default value
	w = OptionMenu(new_adm_Frame, new_student_class,"Select Class","KG","PG","PREP",1,2,3,4,5,6,7,8,9,10,11,12)
	w.place(x=280,y=300)

	global new_student_section,  new_student_section_entry
	Label(new_adm_Frame,text='Section:',bg=bottom_color,font=('bold',20)).place(x=50,y=380)
	new_student_section=StringVar()
	new_student_section_entry=Entry(new_adm_Frame,textvariable=new_student_section,width=25,font=('bold',20))
	new_student_section_entry.place(x=280,y=380)

	global new_student_category,c
	Label(new_adm_Frame,text='Category:',bg=bottom_color,font=('bold',20)).place(x=50,y=460)
	new_student_category=StringVar()
	new_student_category.set("Select Category") # default value
	c = OptionMenu(new_adm_Frame, new_student_category,"Select Category","Offr","Offr-retd","JCO/Sldr","JCO/Sldr-retd","Civil")
	c.place(x=280,y=460)


	Button(new_adm_Frame,text='REGISTER',command=register,bg='green',fg='white',width=20,height=2).place(x=300,y=520)


def withdraw_student():
	print_one_inv_Frame.pack_forget()
	print_all_inv_Frame.pack_forget()
	new_adm_Frame.pack_forget()
	wdw_Frame.pack()
	print_inv_Frame.pack_forget()
	global wdw_adm_no,wdw_adm_no_entry
	Label(wdw_Frame,text='Admission No:',bg=bottom_color,font=('bold',20)).place(x=50,y=50)
	wdw_adm_no=StringVar()
	wdw_adm_no_entry=Entry(wdw_Frame,textvariable=wdw_adm_no,width=25,font=('bold',20))
	wdw_adm_no_entry.place(x=280,y=50)

	global wdw_student_name,wdw_name_entry
	Label(wdw_Frame,text='Student Name:',bg=bottom_color,font=('bold',20)).place(x=50,y=130)
	wdw_student_name=StringVar()
	wdw_name_entry=Entry(wdw_Frame,textvariable=wdw_student_name,width=25,font=('bold',20))
	wdw_name_entry.place(x=280,y=130)
	
	Button(wdw_Frame,text='WITHDRAW',command=withdraw,bg='green',fg='white',width=20,height=2).place(x=300,y=200)

from reportlab.lib.pagesizes import letter, landscape, A4

def print_now(billing_month, adm_no, name, clas, sec, cat, date_of_issue, tution_fee, funds, fine, arrears):
	pdf = canvas.Canvas(name+".pdf", pagesize=landscape(A4))
	width, height = A4
	pdf.line(280,10,280,600)
	pdf.line(540,10,540,600)

	pdf.setTitle("Fee Slip")
	pdf.setFont('Times-Roman',16)
	pdf.drawString(100,570,'STUDENT COPY')
	pdf.drawString(360,570,'SCHOOL COPY')
	pdf.drawString(630,570,'BANK COPY')

	pdf.setFont("Times-Roman", 9)
	pdf.drawString(80,555,'ARMY PUBLIC SCHOOL & COLLEGE')
	pdf.drawString(110,540,'ORDANCE ROAD, RWP')
	pdf.drawString(340,555,'ARMY PUBLIC SCHOOL & COLLEGE')
	pdf.drawString(370,540,'ORDANCE ROAD, RWP')
	pdf.drawString(600,555,'ARMY PUBLIC SCHOOL COLLEGE')
	pdf.drawString(630,540,'ORDANCE ROAD, RWP')

	pdf.setFont('Times-Roman',11)
	pdf.drawString(30,525,'Bank:')
	pdf.drawString(30,510,'ASKARI BANK LTD.')
	pdf.drawString(30,495,'A/C No: 0164-165-05-0005-5')
	pdf.drawString(30,480,'Khadim Hussain Road Lalkurti RWP')

	pdf.setFont('Times-Bold',13)
	pdf.drawString(30,460,'Billing Month: '+billing_month)
	pdf.drawString(30,445,'Admission No: '+str(adm_no))
	pdf.drawString(30,430,'Name: '+name)
	pdf.drawString(30,415,'Class/Sec/Cat: '+str(clas)+'/'+sec+'/'+cat)
	pdf.setFont('Times-Bold',11)
	pdf.drawString(30,175,'Date of Issue: '+date_of_issue)
	pdf.drawString(30,160,'NOTE:')

	pdf.setFont('Times-Roman',11)
	pdf.drawString(30,145,'1. Last date to depositing fee is within 10 days from')
	pdf.drawString(30,130,'    date os issue. Fee deposit timings are 09.00 AM')
	pdf.drawString(30,115,'    to 03.00 PM.')
	pdf.drawString(30,100,'2. In case of late deposit, Rs.10/- per day will be')
	pdf.drawString(30,85,'    charged as late deposit charges till the time bill')
	pdf.drawString(30,70,'    is deposited.')
	pdf.drawString(30,55,'3. If fee bill is not deposited for two months, the')
	pdf.drawString(30,40,'    child will be stuck off from School Roll.')

	pdf.setFont('Times-Roman',14)
	pdf.drawString(100,20,'BANK STAMP')


	#School Copy
	pdf.setFont('Times-Roman',11)
	pdf.drawString(300,525,'Bank:')
	pdf.drawString(300,510,'ASKARI BANK LTD.')
	pdf.drawString(300,495,'A/C No: 0164-165-05-0005-5')
	pdf.drawString(300,480,'Khadim Hussain Road Lalkurti RWP')

	pdf.setFont('Times-Bold',13)
	pdf.drawString(300,460,'Billing Month: '+billing_month)
	pdf.drawString(300,445,'Admission No: '+str(adm_no))
	pdf.drawString(300,430,'Name: '+name)
	pdf.drawString(300,415,'Class/Sec/Cat: '+str(clas)+'/'+sec+'/'+cat)
	pdf.setFont('Times-Bold',11)
	pdf.drawString(300,175,'Date of Issue: '+date_of_issue)
	pdf.drawString(300,160,'NOTE:')

	pdf.setFont('Times-Roman',11)
	pdf.drawString(300,145,'1. Last date to depositing fee is within 10 days from')
	pdf.drawString(300,130,'    date os issue. Fee deposit timings are 09.00 AM')
	pdf.drawString(300,115,'    to 03.00 PM.')
	pdf.drawString(300,100,'2. In case of late deposit, Rs.10/- per day will be')
	pdf.drawString(300,85,'    charged as late deposit charges till the time bill')
	pdf.drawString(300,70,'    is deposited.')
	pdf.drawString(300,55,'3. If fee bill is not deposited for two months, the')
	pdf.drawString(300,40,'    child will be stuck off from School Roll.')

	pdf.setFont('Times-Roman',14)
	pdf.drawString(370,20,'BANK STAMP')

	#Bank Copy
	pdf.setFont('Times-Roman',11)
	pdf.drawString(560,525,'Bank:')
	pdf.drawString(560,510,'ASKARI BANK LTD.')
	pdf.drawString(560,495,'A/C No: 0164-165-05-0005-5')
	pdf.drawString(560,480,'Khadim Hussain Road Lalkurti RWP')

	pdf.setFont('Times-Bold',13)
	pdf.drawString(560,460,'Billing Month: '+billing_month)
	pdf.drawString(560,445,'Admission No: '+str(adm_no))
	pdf.drawString(560,430,'Name: '+name)
	pdf.drawString(560,415,'Class/Sec/Cat: '+str(clas)+'/'+sec+'/'+cat)
	pdf.setFont('Times-Bold',11)
	pdf.drawString(560,175,'Date of Issue: '+date_of_issue)
	pdf.drawString(560,160,'NOTE:')

	pdf.setFont('Times-Roman',11)
	pdf.drawString(560,145,'1. Last date to depositing fee is within 10 days from')
	pdf.drawString(560,130,'    date os issue. Fee deposit timings are 09.00 AM')
	pdf.drawString(560,115,'    to 03.00 PM.')
	pdf.drawString(560,100,'2. In case of late deposit, Rs.10/- per day will be')
	pdf.drawString(560,85,'    charged as late deposit charges till the time bill')
	pdf.drawString(560,70,'    is deposited.')
	pdf.drawString(560,55,'3. If fee bill is not deposited for two months, the')
	pdf.drawString(560,40,'    child will be stuck off from School Roll.')

	pdf.setFont('Times-Roman',14)
	pdf.drawString(630,20,'BANK STAMP')

	total=int(tution_fee)+int(funds)+int(fine)+int(arrears)
	data = [
		['Sr.#', 'PARTICULAR', 'AMOUNT'],
		['1.','Tution Fee',tution_fee],
		['2.','Funds',funds],
		['3.','Fine',fine],
		['4.','Arrears',arrears],
		['5.',' ',' '],
		['6.',' ',' '],
		['7.',' ',' '],
		['8.',' ',' '],
		['9.',' ',' '],
		['10.',' ',' '],
		[' ','Total',total]	
	]  

	table = Table(data)
	table.setStyle([("ALIGN", (0,0), (0,-1), "LEFT"),
			("ALIGN", (-1,0),(-1,-1),"RIGHT"),
			('BOX',(0,0),(-1,-1),1,colors.black),
		        ('INNERGRID', (0,0), (-1,-1), 1.25, colors.black)])

	table.wrapOn(pdf, width, height)
	table.drawOn(pdf, 50, 190)
	table.drawOn(pdf, 320, 190)
	table.drawOn(pdf, 580, 190)

	pdf.save()
	
def print_inv():
	billing_month=one_month.get()
	adm_no = one_adm_no.get()
	date_of_issue = str(date.today())
	tution_fee = one_tution.get()
	funds = one_funds.get()
	
	df= pd.read_csv('data.csv',index_col=0)
	name = df.at[int(adm_no),'Name']
	clas = df.at[int(adm_no),'Class']
	sec = df.at[int(adm_no),'Section']
	cat = df.at[int(adm_no),'Category']
	fine = df.at[int(adm_no),'Fine']
	paid = df.at[int(adm_no),'Payment']
	total = df.at[int(adm_no),'Total']

	if paid=='paid':
		arrears=0
	else:
		arrears= int(total)+200	

	print_now(billing_month,adm_no,name,clas,sec,cat,date_of_issue,tution_fee,funds,fine,arrears)
	df.at[int(adm_no),'Total']= int(tution_fee)+int(funds)+int(fine)+int(arrears)
	df.at[int(adm_no),'Arrears']=int(arrears)
	df.at[int(adm_no),'Payment']='not_paid'
	df.at[int(adm_no),'Billing Month']=billing_month
	df.at[int(adm_no), 'Fine'] = 0
	df.to_csv('data.csv')


	one_month_entry.delete(0,'end')
	one_adm_no_entry.delete(0,'end')
	one_tution_entry.delete(0,'end')
	one_funds_entry.delete(0,'end')
	
def print_all_invo():
	billing_month=all_month.get()
	date_of_issue = str(date.today())
	
	offr = all_offr.get()
	offr_retd = all_offr_retd.get()
	jco = all_jco.get()
	jco_retd = all_jco_retd.get()
	civil = all_civil.get()

	funds = all_funds.get()
	
	count=0
	with open('data.csv', mode='r') as infile:
		reader = csv.reader(infile)
		for row in reader:
			if count==0:
				pass
			else:
				adm_no=row[0]
				name=row[1]
				clas=row[3]
				sec=row[4]
				cat=row[5]
				fine=row[8]
				paid =row[10]
				total=row[9]
				if paid=='paid':
					arrears=0
				else:
					arrears= int(total)+200					
				
				if cat == 'Offr': tution_fee = offr
				elif cat == 'Offr-retd': tution_fee = offr_retd
				elif cat == 'JCO/Sldr': tution_fee = jco
				elif cat == 'JCO/Slde-retd': tution_fee = jco_retd
				elif cat == 'Civil': tution_fee = civil
				
				df= pd.read_csv('data.csv',index_col=0)
				df.at[int(adm_no),'Total']= int(tution_fee)+int(funds)+int(fine)+int(arrears)
				df.at[int(adm_no),'Arrears']=int(arrears)
				df.at[int(adm_no),'Payment']='not_paid'
				df.at[int(adm_no),'Billing Month']=billing_month
				df.at[int(adm_no), 'Fine'] = 0
				df.to_csv('data.csv')
				
				print_now(billing_month,adm_no,name,clas,sec,cat,date_of_issue,tution_fee,funds,int(fine),arrears)
			count+=1
	infile.close()
	all_month_entry.delete(0,'end')
	all_offr_entry.delete(0,'end')
	all_funds_entry.delete(0,'end')
	all_offr_retd_entry.delete(0,'end')
	all_jco_entry.delete(0,'end')
	all_jco_retd_entry.delete(0,'end')
	all_civil_entry.delete(0,'end')
def mark_paid():
	mark_adm_no_info = mark_adm_no.get()
	df= pd.read_csv('data.csv',index_col=0)
	df.at[int(mark_adm_no_info),'Payment']='paid'
	df.to_csv('data.csv')
	mark_adm_no_entry.delete(0,'end')

def fine_student():
	fine_adm_no_info = fine_adm_no.get()
	fine_amount_info = fine_amount.get()

	df= pd.read_csv('data.csv',index_col=0)
	prev_fine = df.at[int(fine_adm_no_info),'Fine']
	df.at[int(fine_adm_no_info),'Fine']= int(fine_amount_info)+int(prev_fine)
	df.to_csv('data.csv')


	fine_adm_no_entry.delete(0,'end')
	fine_amount_entry.delete(0,'end')

def print_one():
	print_all_inv_Frame.pack_forget()
	print_one_inv_Frame.pack()

	Label(print_one_inv_Frame,text='Print Tution Fee',bg='black',fg='white',font=('bold',20)).place(x=150,y=20)
	global one_adm_no,one_adm_no_entry
	Label(print_one_inv_Frame,text='Admission No:',bg=bottom_color,font=('bold',20)).place(x=50,y=80)
	one_adm_no=StringVar()
	one_adm_no_entry=Entry(print_one_inv_Frame,textvariable=one_adm_no,width=10,font=('bold',20))
	one_adm_no_entry.place(x=280,y=80)

	global one_tution,one_tution_entry
	Label(print_one_inv_Frame,text='Tution Fee:',bg=bottom_color,font=('bold',20)).place(x=50,y=140)
	one_tution=StringVar()
	one_tution_entry=Entry(print_one_inv_Frame,textvariable=one_tution,width=10,font=('bold',20))
	one_tution_entry.place(x=280,y=140)

	global one_funds,one_funds_entry
	Label(print_one_inv_Frame,text='Funds:',bg=bottom_color,font=('bold',20)).place(x=50,y=200)
	one_funds=StringVar()
	one_funds_entry=Entry(print_one_inv_Frame,textvariable=one_funds,width=10,font=('bold',20))
	one_funds_entry.place(x=280,y=200)

	global one_month,one_month_entry
	Label(print_one_inv_Frame,text='Billing Month:',bg=bottom_color,font=('bold',20)).place(x=50,y=260)
	one_month=StringVar()
	one_month_entry=Entry(print_one_inv_Frame,textvariable=one_month,width=10,font=('bold',20))
	one_month_entry.place(x=280,y=260)

	Button(print_one_inv_Frame,text='PRINT',command=print_inv,bg='green',fg='white',width=20,height=2).place(x=180,y=350)
	
	#Fine student
	Label(print_one_inv_Frame,text='FINE STUDENT',bg='black',fg='white',font=('bold',20)).place(x=920,y=20)
	global fine_adm_no,fine_adm_no_entry
	Label(print_one_inv_Frame,text='Admission No:',bg=bottom_color,font=('bold',20)).place(x=850,y=80)
	fine_adm_no=StringVar()
	fine_adm_no_entry=Entry(print_one_inv_Frame,textvariable=fine_adm_no,width=10,font=('bold',20))
	fine_adm_no_entry.place(x=1080,y=80)

	global fine_amount,fine_amount_entry
	Label(print_one_inv_Frame,text='Total Amount:',bg=bottom_color,font=('bold',20)).place(x=850,y=140)
	fine_amount=StringVar()
	fine_amount_entry=Entry(print_one_inv_Frame,textvariable=fine_amount,width=10,font=('bold',20))
	fine_amount_entry.place(x=1080,y=140)

	Button(print_one_inv_Frame,text='FINE',command=fine_student,bg='green',fg='white',width=20,height=2).place(x=1000,y=230)




def print_all():
	print_one_inv_Frame.pack_forget()
	print_all_inv_Frame.pack()

	global all_offr,all_offr_entry
	Label(print_all_inv_Frame,text='Print Tution Fee',bg='black',fg='white',font=('bold',20)).place(x=150,y=20)
	Label(print_all_inv_Frame,text='Offr:',bg=bottom_color,font=('bold',20)).place(x=50,y=80)
	all_offr=StringVar()
	all_offr_entry=Entry(print_all_inv_Frame,textvariable=all_offr,width=6,font=('bold',20))
	all_offr_entry.place(x=180,y=80)


	global all_offr_retd,all_offr_retd_entry
	Label(print_all_inv_Frame,text='Offr-Retd:',bg=bottom_color,font=('bold',20)).place(x=340,y=80)
	all_offr_retd=StringVar()
	all_offr_retd_entry=Entry(print_all_inv_Frame,textvariable=all_offr_retd,width=6,font=('bold',20))
	all_offr_retd_entry.place(x=540,y=80)

	global all_jco,all_jco_entry
	Label(print_all_inv_Frame,text='JCO/Sldr:',bg=bottom_color,font=('bold',20)).place(x=50,y=130)
	all_jco=StringVar()
	all_jco_entry=Entry(print_all_inv_Frame,textvariable=all_jco,width=6,font=('bold',20))
	all_jco_entry.place(x=180,y=130)

	global all_jco_retd,all_jco_retd_entry
	Label(print_all_inv_Frame,text='JCO/Sldr-Retd:',bg=bottom_color,font=('bold',20)).place(x=340,y=130)
	all_jco_retd=StringVar()
	all_jco_retd_entry=Entry(print_all_inv_Frame,textvariable=all_jco_retd,width=6,font=('bold',20))
	all_jco_retd_entry.place(x=540,y=130)

	global all_civil,all_civil_entry
	Label(print_all_inv_Frame,text='Civil:',bg=bottom_color,font=('bold',20)).place(x=50,y=180)
	all_civil=StringVar()
	all_civil_entry=Entry(print_all_inv_Frame,textvariable=all_civil,width=6,font=('bold',20))
	all_civil_entry.place(x=180,y=180)

	global all_funds,all_funds_entry
	Label(print_all_inv_Frame,text='Funds:',bg=bottom_color,font=('bold',20)).place(x=50,y=240)
	all_funds=StringVar()
	all_funds_entry=Entry(print_all_inv_Frame,textvariable=all_funds,width=6,font=('bold',20))
	all_funds_entry.place(x=180,y=240)

	global all_month,all_month_entry
	Label(print_all_inv_Frame,text='Billing Month:',bg=bottom_color,font=('bold',20)).place(x=50,y=300)
	all_month=StringVar()
	all_month_entry=Entry(print_all_inv_Frame,textvariable=all_month,width=15,font=('bold',20))
	all_month_entry.place(x=250,y=300)

	

	Button(print_all_inv_Frame,text='PRINT',command=print_all_invo,bg='green',fg='white',width=20,height=2).place(x=180,y=380)
	#Mark Payment
	Label(print_all_inv_Frame,text='Mark Paid',bg='black',fg='white',font=('bold',20)).place(x=950,y=20)

	global mark_adm_no,mark_adm_no_entry
	Label(print_all_inv_Frame,text='Admission No:',bg=bottom_color,font=('bold',20)).place(x=850,y=80)
	mark_adm_no=StringVar()
	mark_adm_no_entry=Entry(print_all_inv_Frame,textvariable=mark_adm_no,width=10,font=('bold',20))
	mark_adm_no_entry.place(x=1080,y=80)
	Button(print_all_inv_Frame,text='CONFIRM PAYMENT',command=mark_paid,bg='green',fg='white',width=20,height=2).place(x=1000,y=160)



def print_invoice():
	new_adm_Frame.pack_forget()
	wdw_Frame.pack_forget()
	print_inv_Frame.pack()
	print_all()
	
	Button(print_inv_Frame,text='PRINT INVOICES FOR ALL/MARK PAYMENT',command= print_all,bg='brown',width=95,height=2).place(x=0,y=0)
	Button(print_inv_Frame,text='PRINT INVOICES FOR ONE STUDENT/FINE ANY STUDENT',command= print_one, bg='brown',width=95,height=2).place(x=660,y=0)




global screen1
screen1 = tkinter.Tk()
screen1.geometry("1320x700")
screen1.title("ABC School")
screen1.resizable(width=False, height=False)


global bottom_color
bottom_color='white'
screen1.configure(bg='blue')


global topFrame
top_color= 'sandy brown'
topFrame = Frame(screen1, borderwidth=2, relief="solid",width=1320,height=120)
topFrame.pack(side="top",expand=True, fill="both")
topFrame.configure(bg=top_color)

Label(topFrame,text="STUDENT PORTAL",fg='black',bg=top_color,font=('bold',50)).pack()
photo = ImageTk.PhotoImage(Image.open("aps-logo.png"))
labelimage = Label(topFrame,image =photo,bg=top_color)
labelimage.place(x=20,y=0)


global middleFrame
middleFrame = Frame(topFrame, borderwidth=1, relief="solid",width=1320,height=40)
middleFrame.pack(side="bottom",expand=True, fill="both")
middleFrame.configure(bg=bottom_color)

global new_adm_Frame
new_adm_Frame = Frame(screen1, borderwidth=1, relief="solid",width=1320,height=570)
new_adm_Frame.pack(side="bottom",expand=True, fill="both")
new_adm_Frame.configure(bg=bottom_color)

global wdw_Frame
wdw_Frame = Frame(screen1, borderwidth=1, relief="solid",width=1320,height=570)
wdw_Frame.pack(side="bottom",expand=True, fill="both")
wdw_Frame.configure(bg=bottom_color)

global print_inv_Frame
print_inv_Frame = Frame(screen1, borderwidth=1, relief="solid",width=1320,height=40)
print_inv_Frame.pack(side="bottom",expand=True, fill="both")
print_inv_Frame.configure(bg=bottom_color)

global print_all_inv_Frame,print_one_inv_Frame
print_all_inv_Frame = Frame(screen1, borderwidth=1, relief="solid",width=1320,height=570)
print_all_inv_Frame.pack(side="bottom",expand=True, fill="both")
print_all_inv_Frame.configure(bg=bottom_color)

print_one_inv_Frame = Frame(screen1, borderwidth=1, relief="solid",width=1320,height=570)
print_one_inv_Frame.pack(side="bottom",expand=True, fill="both")
print_one_inv_Frame.configure(bg=bottom_color)






B1=Button(middleFrame, text='NEW ADMISSION',command=new_admission,bg="blue",width=65,height=2,fg="black")
B1.place(x=0,y=0)
B2=Button(middleFrame, text='WITHDRAW STUDENT',command=withdraw_student,bg="blue",width=65,height=2,fg="black")
B2.place(x=440,y=0)
B3=Button(middleFrame, text='FEE PORTAL',command=print_invoice,bg="blue",width=65,height=2,fg="black")
B3.place(x=880,y=0)


new_admission()

screen1.mainloop()
