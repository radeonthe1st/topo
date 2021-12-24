#!/usr/bin/env python
# coding: utf-8

## Importado de módulos y gente a organizar.

import random
import numpy as np
import os

default_flag = input("Run with default settings? (Year: 2022, Max people per day: 4) (Y/N) ")

if default_flag.lower() == 'y':
	chosen_year = 2022
	chosen_month = int(input('Please, choose month: '))
	max_people_per_day = 4
else:
	chosen_year = int(input('Please, choose year: '))
	chosen_month = int(input('Please, choose month: '))
	max_people_per_day = int(input("How many people are available at the same time? "))

from datetime import datetime,timedelta
def find_first_saturday(year, month):
    d = datetime(year, int(month), 7)
    offset = 5-d.weekday() #weekday = 0 means monday
    date = d + timedelta(offset)
    result = date.day
    if result>7:
        result -= 7
    return result

people = []
with open(f'{os.getcwd()}/people.txt') as file:
    for line in file:
        if line != '\n':
            people.append(line[:-1])


## Definición de los meses y sus días laborables.

thirty_day_months = [4,6,8,11]

def get_month_workdays(year,month):
    if month == 2:
        leap = input('Is there a leap day this year? (Y/N) ')
        if leap.lower() == 'y':
            last_month_day = 29
        else:
            last_month_day = 28
    elif month in thirty_day_months:
        last_month_day = 30
    else:
        last_month_day = 31
    month_saturdays = [x for x in range(find_first_saturday(year,month),32,7)]
    month_sundays = [x for x in range(find_first_saturday(year,month)+1,32,7)]
    weekends = month_saturdays+month_sundays
    
    holidays = []
    day = None
    while day != 'Stop':
        day = input('Please, enter holidays and write "Stop" when done: ')
        if day != "Stop" or day=='':
            holidays.append(int(day))
            
    workdays = [x for x in range(1,last_month_day+1) if x not in weekends and x not in holidays]
    return workdays


## Definición función para distribución de personal

month_names = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
               7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}

def distribucion_personal(year,month,max_people_per_day = 4):
    #mes_name =input_mes
    mes = get_month_workdays(year,month)
    print()
    mes_name = month_names[month]


    plazas_a_cubrir = len(mes)*max_people_per_day
    gente = people.copy()
    min_dias = plazas_a_cubrir//len(gente)
    personas_extra = plazas_a_cubrir%len(gente)
    print(f'{len(mes)} working days on {mes_name}: {mes}')
    print('------------------------------------------------------------')
    print(f'Each person must go {min_dias} days and {personas_extra} need to go one extra day')
    print('------------------------------------------------------------')
   

    mes_copy = mes.copy()
    done=False
    while done==False:
        random.shuffle(mes)
        gcopy=gente.copy()
        random.shuffle(gcopy)
        full_days=[]
        personas_dia = {dia : [] for dia in mes}
        dias_persona = {persona : [] for persona in gente}

        un_dia_mas = gente.copy()
        random.shuffle(un_dia_mas)
        un_dia_mas = un_dia_mas[:personas_extra]
        for persona in gcopy:
            its_persona=0
            if persona in un_dia_mas:
                while len(dias_persona[persona])<(min_dias+1) and its_persona<10000:
                    available_days = [x for x in mes if x not in full_days]
                    rand_day = random.choice(available_days)
                    if persona not in personas_dia[rand_day] and len(personas_dia[rand_day])<max_people_per_day:
                        personas_dia[rand_day].append(persona)
                        dias_persona[persona].append(rand_day)
                        if len(personas_dia[rand_day]) == max_people_per_day:
                            full_days.append(rand_day)
                    its_persona+=1
            elif persona not in un_dia_mas:
                while len(dias_persona[persona])<(min_dias) and its_persona<10000:
                    available_days = [x for x in mes if x not in full_days]
                    rand_day = random.choice(available_days)
                    if persona not in personas_dia[rand_day] and len(personas_dia[rand_day])<max_people_per_day:
                        personas_dia[rand_day].append(persona)
                        dias_persona[persona].append(rand_day)
                        if len(personas_dia[rand_day]) == max_people_per_day:
                            full_days.append(rand_day)
                    its_persona+=1
        if its_persona<1000:
            done=True
        else:
            done=False
    
    print(f'One extra day: {[persona for persona in gente if persona in un_dia_mas]}')
    print('-----------------------------------------------------------------------')

    a1 = 'Person'
    a2 = 'N. of days'
    a3 = 'Days assigned'
    
    print(f'{a1:<20}{a2 : ^20}{a3 : >30}')
    print('-----------------------------------------------------------------------')
    for persona in dias_persona:
        if persona in un_dia_mas:
            aux = f'{persona}'
            aux2 = f'{dias_persona[persona]}'
            print(f'{aux: <20} {len(dias_persona[persona]) : ^20} {aux2 : >30}')
        else:
            aux = f'{persona}'
            aux2 = f'{dias_persona[persona]}'
            print(f'{aux: <20} {len(dias_persona[persona]) : ^20} {aux2 : >30}')
    print('------------------------------------------------------------------------')
        
    
    dias=[]
    gentiña=[]
    n_dias=[]
    for dia in mes_copy:
        dias.append(dia)
        gentiña.append(len(personas_dia[dia]))
        print(f'{dia:<5} {personas_dia[dia]}')

    for pers in gente:
        n_dias.append(len(dias_persona[pers]))




## Sorteo OFICIAL de distribución de personal

distribucion_personal(chosen_year,chosen_month)
