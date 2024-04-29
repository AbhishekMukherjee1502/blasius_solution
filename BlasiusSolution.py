#Libraries imported
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tkinter.filedialog import askdirectory

# System of ODEs
def Blasius(eta, f):
    return (f[1], f[2], f[0]*f[2])

# Boundary Conditions
f0 = [0, 1, -0.6276]

# Solving the system of ODEs
eta = np.linspace(0, 10, 10000)
f = solve_ivp(Blasius, [0, 10], f0, t_eval=eta)
x = f.t
f_0 = f.y[0]
f_1 = f.y[1]
f_2 = f.y[2]

# Export the values to an Excel file
blas = pd.DataFrame(data = {"η": x,
                   "f_0": f_0,
                   "f_1": f_1,
                   "f_2": f_2})
path = askdirectory(title='Select Folder to save solution figures')
blas.to_excel(path + "\Blasius Solution.xlsx")
print("Export Successful!")

# First instance of eta for f_1 ~ 0.99
for i in range(0, len(f_1)):
    if f_1[i] > 0.99:
        idx = i
        break
eta_edge = eta[idx]
print(f"The value of η for f_1 ~ 0.99 is {round(eta_edge, 3)}")

# Plotting the Solution
plt.plot(f_0, x, 'r--' ,  label = r"Stream Function $f({\eta})$")
plt.plot(f_1, x, 'g-.', label = r"Velocity Profile $f'({\eta})$")
plt.plot(f_2, x, 'b', label = r"Shear Stress Function $f''({\eta})$")
plt.legend()
#plt.xlim(0, 2)
plt.xlabel(r"$f'({\eta})$, $f'({\eta})$ and $f''({\eta})$")
plt.xticks(np.arange(0, 2.1, step = 0.2))
#plt.ylim(0, 10)
plt.ylabel(r"${\eta}$")
plt.grid(True)
ratio = 9/16
#plt.gca().set_aspect(abs((2-0)/(0-10))*ratio)
plt.savefig(path + "\solution.svg", dpi = 1200)
plt.show()


# Boundary Layer Profile Example

# Fluid Properties
U_infty = 100
rho = 1.225
mu = 1.789e-5
# Critical Values
Re_crit = 5e5
x_crit = Re_crit * mu / (U_infty * rho)
print(f"The value of x_crit is {round(x_crit, 4)} metres")

# Solving for delta
x = np.linspace(0, x_crit, 10000)
Re = rho * U_infty * x / mu
delta = eta_edge * x / (Re**0.5)
delta_max = delta[-1]
print(f"The value of delta_max is {round(delta_max, 4)} metres")

# Plotting the boundary layer profile
plt.plot(x, delta, 'r--')
plt.fill_between(x, delta, 0, color = "red", alpha = 0.2)
plt.title("Boundary Layer Profile")
#plt.xlim(0, x_crit)
plt.xlabel("Distance along the plate (in metres)")
#plt.ylim(0, delta_max*1.25)
plt.ylabel("Distance normal to plate (in metres)")
#plt.gca().set_aspect(abs((x_crit-0)/(0-delta_max*1.25))*ratio)
#plt.ticklabel_format(style='sci',scilimits=(-3, 0),axis='both')
plt.grid(True)
plt.savefig(path + "\BLprofile.svg", dpi = 1200)
plt.show()