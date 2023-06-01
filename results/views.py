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
# import logging
# logging.basicConfig(
#     format='%(asctime)s %(levelname)-8s %(message)s',
#     level=logging.INFO,
#     datefmt='%Y-%m-%d %H:%M:%S')
from io import BytesIO
import base64

# Bar Chart
def barchart(request):
    # removed Both for production purposes as requested by client
    objects = ['Infection','Ischaemia','None']
    y_pos = np.arange(len(objects))

    try:
        # logging.info(uv.get_uploaded())
        if uv.get_uploaded() == False:
            # throw exception
            raise Exception
        c = uv.get_vals()
        c = c[1:] # remove first element

        # multiply prob by 100 to adjust to %age
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
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_url = base64.b64encode(img.getvalue()).decode()

        logging.info('Bar chart has been generated')
        uv.set_uploaded(False)

        return render(request,'bar_chart.html', {'img_url': img_url})

    except:
        return render(request, 'error.html')
