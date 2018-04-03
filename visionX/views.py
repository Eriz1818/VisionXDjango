from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,render_to_response
from django.core.urlresolvers import reverse
import io
import os
from google.cloud import vision
from .forms import UploadFileForm
from .models import UploadFile
from .models import TagFreq
from .models import TempTable
from .tables import TagFreqTable
from .tables import TempTagFreqTable
from django_tables2 import RequestConfig
from django.template import loader
from django.db.models import F



def index(request):
    table = TagFreqTable(TagFreq.objects.all())
    RequestConfig(request).configure(table)
    tmp_table = TempTagFreqTable(TempTable.objects.all())
    RequestConfig(request).configure(tmp_table)
    # template = loader.get_template('visionX/index.html')
    if request.method == 'POST':
        # TempTable.objects.all().delete()
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file=request.FILES['file'])
            new_file.save()

            return render(request, 'visionX/index.html', { 'data' : table, 'tmp_data' : tmp_table })

    elif request.GET.get("result"):
        TempTable.objects.all().delete()
        print('working yay')
        ## vision code

        vision_client = vision.Client()

        # photo_categories = dict()
        for file in os.listdir('files/images/'):
            if not file.startswith('.'):
                print(file)
                with io.open('files/images/' + file, 'rb') as image_file:
                    image = vision_client.image(content=image_file.read())
                    labels = image.detect_labels()
                    for label in labels:
                        # if (int(label.score * 100) > 80):
                            # print(label.description, " score ", int(label.score * 100))
                            # for history table
                        if TagFreq.objects.filter(tag_Name=label.description):
                            print('old')
                            TagFreq.objects.filter(tag_Name=label.description).update(tag_freq=F('tag_freq')+1)
                        else:
                            print('new')
                            a = TagFreq(tag_Name=label.description,tag_freq=1)
                            a.save()

                            # for temp table
                        if TempTable.objects.filter(TempTagName=label.description):
                            print('old')
                            TempTable.objects.filter(TempTagName=label.description).update(TempTagFreq=F('TempTagFreq') + 1)
                        else:
                            print('new')
                            b = TempTable(TempTagName=label.description, TempTagFreq=1)
                            b.save()

        # print(photo_categories)
        filelist = [f for f in os.listdir('files/images/')]
        # print(filelist)
        for f in filelist:
            os.remove('files/images/' + f)
        table = TagFreqTable(TagFreq.objects.all())
        RequestConfig(request).configure(table)
        return render(request, 'visionX/index.html', { 'data' : table, 'tmp_data' : tmp_table })

    data = { 'data' : table, 'tmp_data' : tmp_table }
    return render(request, 'visionX/index.html', data)
