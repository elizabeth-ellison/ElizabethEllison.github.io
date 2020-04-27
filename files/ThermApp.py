# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 17:41:26 2017

@author: dgoldber
"""


import matplotlib
import tkinter as tk
import numpy as np
import os
import glob
import time
#import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import scipy.linalg as LA2
import numpy.linalg as LA
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Therm(tk.Frame):
    
    albedo = .1
    Q_prime = 245                 # W/m^2
    l_star = 300                   # W / m^2
    T_air = 10.                     # deg C
    depth = 0.7                    # m
    max_time = 86400.            # seconds
    plot_frequency = 6.       # seconds
    k_deb = 1.                   # W / m-K
    Q_prime_var = 245.              # W / m^2
    l_star_var = 60.               # W / m^2
    T_air_var = 7.3                 # deg C
    meas_begin =0.           # seconds
    RH = .68                        # nondim
    RH_var = 0.27                    # nondim            
    u_wind = 2.5                   # m/s
    
##############################

    Q_prime_t = Q_prime            # W/m^2
    l_star_t = l_star              # W/m^2
    T_air_t = T_air                # deg C
    RH_t = RH
    
    delta_t = 600.                 # seconds
    emiss = 0.7                    # unitless
    rho_c = 1.67e6                 # J / m^3-K
    kappa_deb = k_deb/rho_c        # m^2 / s
    sigma_SB = 5.67e-8             # W / m^2 / K^4
    rho_0 = 1.29                   # kg / m^3
    P_0 = 101300.                   # Pa
    P_air = 80000.                 # Pa
    z_eddy = 2                   # m
    z0 = .01                       # m
    
    c_air = 1010                   # J / kg - K
    L_e = 2.49e6                # J / kg
    max_newton_iter = 1000
    newton_tol = 1.e-5
    rho_i = 900                   # kg/m^3
    Lf = 334.e3                   # J/kg

    n_levels = 20
    delta_z = 0.
    mu = 0.
    A_bl = (0.4 / np.log(z_eddy/z0))**2   
    str = tk.StringVar
    canvas = FigureCanvasTkAgg
    fig = Figure(figsize=(15,5))

    
    

#    A_bl = (0.4 / np.log(z_eddy/z0))**2    
#    delta_z = depth/n_levels
#    mu = kappa_deb * delta_t / delta_z**2
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.window = parent
        
        self.prompt1 = tk.Label(self, text="Enter the albedo:", anchor="w")
        self.prompt1.grid(row=0,column=0)
        self.entryAlbedo = tk.Entry(self)
        self.entryAlbedo.grid(row=0,column=1)
        self.entryAlbedo.delete(0,"end")
        self.entryAlbedo.insert(0,str(self.albedo))
        
        self.prompt2 = tk.Label(self, text="Enter Daily Avg SW Radiation:", anchor="w")
        self.prompt2.grid(row=1,column=0)
        self.entrySW = tk.Entry(self)
        self.entrySW.grid(row=1,column=1)
        self.entrySW.delete(0,"end")
        self.entrySW.insert(0,str(self.Q_prime))

        self.prompt3 = tk.Label(self, text="Enter Daily Avg LW Radiation:", anchor="w")
        self.prompt3.grid(row=2,column=0)
        self.entryLW = tk.Entry(self)
        self.entryLW.grid(row=2,column=1)
        self.entryLW.delete(0,"end")
        self.entryLW.insert(0,str(self.l_star))

        self.prompt2b = tk.Label(self, text="Enter Daily Variation SW Radiation:", anchor="w")
        self.prompt2b.grid(row=1,column=2)
        self.entrySW_var = tk.Entry(self)
        self.entrySW_var.grid(row=1,column=3)
        self.entrySW_var.delete(0,"end")
        self.entrySW_var.insert(0,str(self.Q_prime_var))

        self.prompt3b = tk.Label(self, text="Enter Daily Variation LW Radiation:", anchor="w")
        self.prompt3b.grid(row=2,column=2)
        self.entryLW_var = tk.Entry(self)
        self.entryLW_var.grid(row=2,column=3)
        self.entryLW_var.delete(0,"end")
        self.entryLW_var.insert(0,str(self.l_star_var))        

        self.prompt4 = tk.Label(self, text="Enter Avg 2m air temp:", anchor="w")
        self.prompt4.grid(row=3,column=0)
        self.entryAir = tk.Entry(self)
        self.entryAir.grid(row=3,column=1)
        self.entryAir.delete(0,"end")
        self.entryAir.insert(0,str(self.T_air))        

        self.prompt4b = tk.Label(self, text="Enter daily variation 2m air temp:", anchor="w")
        self.prompt4b.grid(row=3,column=2)
        self.entryAir_var = tk.Entry(self)
        self.entryAir_var.grid(row=3,column=3)
        self.entryAir_var.delete(0,"end")
        self.entryAir_var.insert(0,str(self.T_air_var))        
        
        self.prompt4c = tk.Label(self, text="Enter Avg 2m Rel Humidity:", anchor="w")
        self.prompt4c.grid(row=4,column=0)
        self.entryRH = tk.Entry(self)
        self.entryRH.grid(row=4,column=1)
        self.entryRH.delete(0,"end")
        self.entryRH.insert(0,str(self.RH))        

        self.prompt4d = tk.Label(self, text="Daily variation 2m Rel Humidity:", anchor="w")
        self.prompt4d.grid(row=4,column=2)
        self.entryRH_var = tk.Entry(self)
        self.entryRH_var.grid(row=4,column=3)
        self.entryRH_var.delete(0,"end")
        self.entryRH_var.insert(0,str(self.RH_var))   

        self.prompt5 = tk.Label(self, text="Enter Debris Thickness:", anchor="w")
        self.prompt5.grid(row=5,column=0)
        self.entryDebris = tk.Entry(self)
        self.entryDebris.grid(row=5,column=1)
        self.entryDebris.delete(0,"end")
        self.entryDebris.insert(0,str(self.depth))    
        
#        self.prompt10 = tk.Label(self, text="Overwrite .csv files?", anchor="w")
#        self.prompt10.grid(row=6,column=2)
        self.chekvar = tk.IntVar()
        self.entryover = tk.Checkbutton(self,text='Overwrite .csv files?',variable=self.chekvar)
        self.entryover.grid(row=6,column=3)

        
        self.prompt5 = tk.Label(self, text="Enter 2m Wind Speed:", anchor="w")
        self.prompt5.grid(row=6,column=0)
        self.entryWind = tk.Entry(self)
        self.entryWind.grid(row=6,column=1)
        self.entryWind.delete(0,"end")
        self.entryWind.insert(0,str(self.u_wind))  

        self.prompt6 = tk.Label(self, text="Enter Thermal Conductivity (W/m-K):", anchor="w")
        self.prompt6.grid(row=7,column=0)
        self.entryKdeb = tk.Entry(self)
        self.entryKdeb.grid(row=7,column=1)
        self.entryKdeb.delete(0,"end")
        self.entryKdeb.insert(0,str(self.k_deb))        

        self.prompt7 = tk.Label(self, text="Enter Total Time (Days):", anchor="w")
        self.prompt7.grid(row=8,column=0)
        self.entryTime = tk.Entry(self)
        self.entryTime.grid(row=8,column=1)
        self.entryTime.delete(0,"end")
        self.entryTime.insert(0,str(np.round(self.max_time)/86400.))        

        self.prompt8 = tk.Label(self, text="Enter Plot Frequency (hours):", anchor="w")
        self.prompt8.grid(row=8,column=2)
        self.entryFreq = tk.Entry(self)
        self.entryFreq.grid(row=8,column=3)       
        self.entryFreq.delete(0,"end")
        self.entryFreq.insert(0,str(self.plot_frequency))        
        
        self.prompt9 = tk.Label(self, text="Enter Begin Measurement (days):", anchor="w")
        self.prompt9.grid(row=9,column=0)
        self.entryPlotStart = tk.Entry(self)
        self.entryPlotStart.grid(row=9,column=1)       
        self.entryPlotStart.delete(0,"end")
        self.entryPlotStart.insert(0,str(np.round(self.meas_begin)/86400.))        


        self.str = tk.StringVar() 
        self.str.set("START")
        
        self.submit = tk.Button(self, text="Submit", command = self.calculate)
        self.submit.grid(row=9,column=2)
        
        self.output = tk.Label(self, textvariable=self.str)
        self.output.grid(row=9,column=3)       

        Therm.canvas = FigureCanvasTkAgg(Therm.fig, master=self.window)
        Therm.canvas.get_tk_widget().pack(side="bottom")
        


    def calculate(self):

        try:
            
            Therm.albedo = float(self.entryAlbedo.get())
            Therm.Q_prime = float(self.entrySW.get())
            Therm.Q_prime_var = float(self.entrySW_var.get())
            Therm.l_star = float(self.entryLW.get())
            Therm.l_star_var = float(self.entryLW_var.get())
            Therm.T_air = float(self.entryAir.get())
            Therm.T_air_var = float(self.entryAir_var.get())
            Therm.u_wind = float(self.entryWind.get())
            Therm.RH = float(self.entryRH.get())
            Therm.RH_var = float(self.entryRH_var.get())
            Therm.depth = float(self.entryDebris.get())
            Therm.k_deb = float(self.entryKdeb.get())
            Therm.max_time = 86400*float(self.entryTime.get())
            temp = float(self.entryFreq.get())
            Therm.plot_frequency = (Therm.delta_t/600.) * np.round(float(self.entryFreq.get())/(Therm.delta_t/600.))
            if (temp!=Therm.plot_frequency):
                print ('Plot frequency rounded to ' + str(Therm.plot_frequency) + ' hours')
            Therm.plot_frequency = Therm.plot_frequency * 3600.
                
            
            Therm.meas_begin = 86400*float(self.entryPlotStart.get())
            
            T = np.zeros(Therm.n_levels+1)
            time = np.arange(0,Therm.max_time+Therm.delta_t,Therm.delta_t)
            melt = np.zeros(np.shape(time))
            QS = np.zeros(np.shape(time))
            QLA = np.zeros(np.shape(time))
            QLS = np.zeros(np.shape(time))
            QH = np.zeros(np.shape(time))
            QC = np.zeros(np.shape(time))
            QE = np.zeros(np.shape(time))            
            n_plot = int(np.round(self.max_time/self.plot_frequency))
            T_plot = np.zeros([self.n_levels+2,n_plot+1])
            
            Therm.A_bl = (0.4 / np.log(Therm.z_eddy/Therm.z0))**2    
            Therm.delta_z = Therm.depth/Therm.n_levels
            Therm.mu = Therm.kappa_deb * Therm.delta_t / Therm.delta_z**2            

            Z = np.linspace(0,Therm.depth,Therm.n_levels+1)

            Therm.fig.clf()
            aa = Therm.fig.add_subplot(121)
            bb = Therm.fig.add_subplot(122)

            self.str.set("RUNNING")
            Therm.canvas.draw()
            for n in range(1,len(time)):
    
    
                Therm.Q_prime_t = Therm.Q_prime - np.cos(2*np.pi*time[n]/86400) * Therm.Q_prime_var
                Therm.l_star_t = Therm.l_star - np.cos(2*np.pi*time[n]/86400) * Therm.l_star_var
                Therm.T_air_t = Therm.T_air - np.cos(2*np.pi*time[n]/86400) * Therm.T_air_var
                Therm.RH_t = Therm.RH - np.cos(2*np.pi*time[n]/86400) * Therm.RH_var
    
                if (time[n] % 86400 == 0):
                    print(str(time[n])+' seconds')
    
                T_current = T[:-1]
                T_new = T[:-1]
    
    
                for k in range(Therm.max_newton_iter):
                    F, Qs, Ql_atm, Ql_snow, Qh, Qc, Qe = self.residual (T_new,T_current)        
                    
                    if ((LA.norm(F)/np.sqrt(Therm.n_levels))<Therm.newton_tol):
                        break

                    if (k==(Therm.max_newton_iter-1)):
                        print('did not converge: ' + str(LA.norm(F)))
                    
                    Jab = self.residual_gradient (T_new)
                    T_new = T_new - LA2.solve_banded((1,1),Jab,F)
        
                T[:-1] = T_new
                
                mr = self.k_deb * (T_new[-2]-T_new[-1])/self.delta_z / Therm.rho_i / Therm.Lf * 86400.
                melt[n] = max(mr,0)
                QS[n] = Qs
                QLA[n] = Ql_atm
                QLS[n] = Ql_snow
                QH[n] = Qh
                QC[n] = Qc
                QE[n] = Qe
                
                if((time[n]%self.plot_frequency)==0):
                    T_plot[1:,int(np.round(time[n]/self.plot_frequency))] = T
                    T_plot[0,int(np.round(time[n]/self.plot_frequency))] = time[n]
                    bb.clear()
                    bb.plot(time[0:n],melt[0:n])
                    if (time[n]>Therm.meas_begin):
                     aa.plot(T,np.flipud(Z))
                    Therm.canvas.draw()
#                    tk.Tk.update(self)
                    
                
            avg_melt = np.mean(melt[time>Therm.meas_begin])


#            for k in range(0,n_plot+1):
#                if (k*Therm.plot_frequency > Therm.meas_begin):
#                    aa.plot(T_plot[1:,k],np.flipud(Z))

            aa.set_xlabel('Temperature (C)')
            aa.set_ylabel('distance from ice (m)')
       
            bb.clear()
            bb.plot(time/86400,melt)
            bb.plot([Therm.meas_begin/86400,Therm.meas_begin/86400],[0,avg_melt*1.2],'r')               
            self.str.set(str(avg_melt)+' m/day')
            bb.set_xlabel('time(days)')
            bb.set_ylabel('melt rate (m/day)')
            
            Therm.canvas.draw()
            savevar = np.concatenate((time[1:,None],melt[1:,None],QS[1:,None],QLA[1:,None],QLS[1:,None],QH[1:,None],QE[1:,None],QC[1:,None]),1)
            
            str1 = 'Time (s)'
            for n in range(1,self.n_levels+1):
                str1 = str1 + ',' + str((n-1)*Therm.delta_z) + 'm depth'
                
            str1 = str1+',base\n'
            
            str2 = 'Time (s),Melt,Qs,QL_down,QL_up,Qh,Qe,Qc'
            
            str2 = str2+'\n'
            
            overw=self.chekvar.get()
            
            files = list(filter(os.path.isfile, glob.glob("TemperatureProfiles[0-9]*csv")))
            if ((len(files)>0) & (overw==0)):
              files.sort(key=lambda x: os.path.getmtime(x))
              filenum = int(files[-1].split('.')[0][19:])
              profiles_filename='TemperatureProfiles' + str(filenum+1) + '.csv'
            else:
              profiles_filename='TemperatureProfiles' + str(0) + '.csv'    

            files = list(filter(os.path.isfile, glob.glob("MeltHistory[0-9]*csv")))
            if ((len(files)>0) & (overw==0)):
              files.sort(key=lambda x: os.path.getmtime(x))
              filenum = int(files[-1].split('.')[0][11:])
              hist_filename='MeltHistory' + str(filenum+1) + '.csv'
            else:
              hist_filename='MeltHistory' + str(0) + '.csv'    
            
            
            with open(profiles_filename, 'w') as f:
              try:
                f.write('albedo,' + str(Therm.albedo) + '\n')
                f.write('Shortwave Average,' + str(self.Q_prime) + '\n') 
                f.write('Shortwave Variation,' + str(self.Q_prime_var) + '\n') 
                f.write('Atm. Longwave Average,' + str(self.l_star) + '\n') 
                f.write('Atm. Longwave Variation,' + str(self.l_star_var) + '\n') 
                f.write('Air temp average,' + str(self.T_air) + '\n') 
                f.write('Air temp variaion,' + str(self.T_air_var) + '\n') 
                f.write('Rel Humidity average,' + str(self.RH) + '\n') 
                f.write('Rel Humidity variaion,' + str(self.RH_var) + '\n') 
                f.write('Debris depth,' + str(self.depth) + '\n') 
                f.write('Wind speed,' + str(self.u_wind) + '\n') 
                f.write('Thermal Conductivity,' + str(self.k_deb) + '\n') 
                f.write('Plot Frequency,' + str(self.plot_frequency) + '\n') 
                f.write(str1)
                T_plot = np.transpose(T_plot)
                xxx = np.shape(T_plot)
                for i in range(0,xxx[0]):
                    str3 = str(T_plot[i,0])
                    for n in range(1,xxx[1]):
                        str3=str3+','+str(T_plot[i,n])
                    str3 = str3 + '\n'
                    f.write(str3)
                f.close()
              except:
                self.str.set('ERROR: CLOSE EXCEL FILES')
                print('GOT HERE')
                Therm.canvas.draw()


                    
            with open(hist_filename, 'w') as f:   
              try: 
                f.write('albedo,' + str(Therm.albedo) + '\n')
                f.write('Shortwave Average,' + str(self.Q_prime) + '\n') 
                f.write('Shortwave Variation,' + str(self.Q_prime_var) + '\n') 
                f.write('Atm. Longwave Average,' + str(self.l_star) + '\n') 
                f.write('Atm. Longwave Variation,' + str(self.l_star_var) + '\n') 
                f.write('Air temp average,' + str(self.T_air) + '\n') 
                f.write('Air temp variaion,' + str(self.T_air_var) + '\n') 
                f.write('Rel Humidity average,' + str(self.RH) + '\n') 
                f.write('Rel Humidity variaion,' + str(self.RH_var) + '\n') 
                f.write('Debris depth,' + str(self.depth) + '\n') 
                f.write('Wind speed,' + str(self.u_wind) + '\n') 
                f.write('Thermal Conductivity,' + str(self.k_deb) + '\n') 
                f.write('Plot Frequency,' + str(self.plot_frequency) + '\n')                 
                f.write(str2)
                xxx = np.shape(savevar)
                for i in range(0,xxx[0]):
                    str3 = str(savevar[i,0])
                    for n in range(1,xxx[1]):
                        str3=str3+','+str(savevar[i,n])
                    str3 = str3 + '\n'
                    f.write(str3)
                f.close()
              except:
                self.str.set('ERROR: CLOSE EXCEL FILES')
                print('GOT HERE')
                Therm.canvas.draw()
                
            
            Therm.fig.savefig('LatestPlot.png')
            
            print ('DONE')

        except ValueError:
            result = "Please enter numbers only, using . for decimal (e.g. 0.1 instead of 0,1)"
            self.str.set(result)
            print (result)

        
    def residual (self,T,T_old):
    
        N = T.size          # find the size of T
        F = np.zeros(N)     # make an array of zeros with the same size
        Ts = T[0]
    
        F[1:-1] = -1.*Therm.mu * T[0:-2] + \
              (1+2*Therm.mu) * T[1:-1] + \
              -1.*Therm.mu * T[2:]
        
        F[-1] = -1.*Therm.mu * T[-2] + \
              (1+2*Therm.mu) * T[-1]
              
        F[1:] = F[1:] - T_old[1:]

        # Tetens Equation        
        B = 0.
        C = 0.       
        if (Therm.T_air_t>0.):
            B = 17.27       
            C = 237.3
        else:
            B = 21.875      
            C = 265.5            
        vp_2m = .61078 * np.exp(B*Therm.T_air_t/(Therm.T_air_t+C))
        
        if (Ts>0.):
            B = 17.27       
            C = 237.3
        else:
            B = 21.875      
            C = 265.5
        vps = .61078 * np.exp(B*Ts/(Ts+C))

        
                
        Qs = Therm.Q_prime_t * (1-Therm.albedo)                   # incoming shortwave radiation        
        Ql_atm = Therm.emiss * (Therm.l_star_t)    # incoming longwae radiation    
        Ql_snow = Therm.emiss * (Therm.sigma_SB * (Ts+273.)**4)    # incoming longwae radiation    
        Qh = Therm.rho_0 * (Therm.P_air/Therm.P_0) * Therm.c_air * Therm.A_bl * Therm.u_wind * (Therm.T_air_t-Ts)   
        Qe = (0.622*Therm.rho_0/Therm.P_0) * Therm.L_e * Therm.A_bl * Therm.u_wind * (Therm.RH_t*vp_2m - vps)   
        Qc = Therm.k_deb / Therm.delta_z * (Ts-T[1])
           
        F[0] = -1.* (Qs + Ql_atm + Qh + Qe - Qc - Ql_snow)
        #print ('GOT HERE ' + str(Therm.Q_prime))
    
        return F, Qs, Ql_atm, Ql_snow, Qh, Qc, Qe
    
    def residual_gradient (self,T):
    
        N = T.size          # find the size of T
        J = np.zeros([3,N])     # make an array of zeros with the same size
        Ts = T[0]
        B = 0.
        C = 0.       
        if (Ts>0.):
            B = 17.27       
            C = 237.3
        else:
            B = 21.875      
            C = 265.5
    
        for i in range(1,N):

            if (i<N-1):
                J[0,i+1] = -1.*Therm.mu
                J[1,i] = 1 + 2*Therm.mu
            else:
                J[1,i] = 1 + 2.*Therm.mu
                J[2,i-1] = -1.*Therm.mu        
        
                    
        J[1,0] = J[1,0] - 4 * Therm.sigma_SB * (Ts+273.)**3
        J[1,0] = J[1,0] + Therm.rho_0 * (Therm.P_air/Therm.P_0) * Therm.c_air * Therm.A_bl * Therm.u_wind
        J[1,0] = J[1,0] + Therm.k_deb / Therm.delta_z
        J[1,0] = J[1,0] + (0.622*Therm.rho_0/Therm.P_0) * Therm.L_e * \
            Therm.A_bl * Therm.u_wind * B*C/(C+Ts)**2 * .61078 * np.exp(B*Therm.T_air_t/(Therm.T_air_t+C))
        J[0,1] = -Therm.k_deb / Therm.delta_z
    
        return J  

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    Therm(root).pack(fill="both", expand=True)
    root.mainloop()
