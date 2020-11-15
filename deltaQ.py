a1 = 0.19
a2 = 0.13
da1 = 0.01
da2 = 0.01

from math import sqrt, pi

fi = 4*pi*a1*a2**2*da1/((a1**2 + a2**2)**2)
se = 4*pi*a1**2*a2*da2/((a1**2 + a2**2)**2)

res = sqrt(fi**2 + se**2)

print(res)