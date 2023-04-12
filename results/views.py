from django.shortcuts import render
# MatPlotLib
import matplotlib
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
# Bar Chart
def barchart(request):
    objects = ['Both','Infection','Ischaemia','None']
    y_pos = np.arange(len(objects))
    # multiply prob by 100 to adjust to %age
    c = [0.10,0.20,0.25,0.45]
    qty = [i*100 for i in c]

    plt.rcdefaults()
    fig, ax = plt.subplots()
    ax.barh(y_pos, qty, align='center', color='#4285F4')

    ax.set_yticks(y_pos, labels=objects)
    ax.invert_yaxis()  # labels read top-to-bottom
    for i, v in enumerate(qty):
        ax.text(v-v/2, i, str(v)+'%', color = 'white')
    ax.set_title('Final Prediction')
    plt.savefig('images/barchart.png')
    return render(request,'bar_chart.html')