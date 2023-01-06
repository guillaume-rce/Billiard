import matplotlib.pyplot as plt

#set axis limits of plot (x=0 to 20, y=0 to 20)
plt.axis([0, 20, 0, 20])
plt.axis("equal")

#define circles
c1=plt.Circle((5, 5), radius=1)
c2=plt.Circle((10, 10), radius=2)
c3=plt.Circle((15, 13), radius=3)

#add circles to plot
plt.gca().add_artist(c1)
plt.gca().add_artist(c2)
plt.gca().add_artist(c3)

plt.show()