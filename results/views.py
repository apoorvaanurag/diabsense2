from django.shortcuts import render
# MatPlotLib
import matplotlib
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import upload.views as uv
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


# Bar Chart
def barchart(request):
    objects = ['Both','Infection','Ischaemia','None']
    y_pos = np.arange(len(objects))
    # multiply prob by 100 to adjust to %age
    # c = [0.10,0.20,0.25,0.45]

    try:
        c = uv.get_vals()
        qty = [i*100 for i in c]

        # round to 2 decimal places
        qty = [round(num, 2) for num in qty]

        plt.rcdefaults()
        fig, ax = plt.subplots()
        ax.barh(y_pos, qty, align='center', color='#4285F4')

        ax.set_yticks(y_pos, labels=objects)
        ax.invert_yaxis()  # labels read top-to-bottom
        for i, v in enumerate(qty):
            ax.text(v-v/2, i, str(v)+'%', color = 'white')
        ax.set_title('Final Prediction')
        plt.savefig('images/barchart.png')

        logging.info('Bar chart has been generated')

        return render(request,'bar_chart.html')

    except:
        return render(request, 'error.html')
