import time
from django.shortcuts import render
from . import models, serializers, program_first, program_second, program_third
from threading import Thread, Event

def main(request):
    if request.method == 'GET':
        return render(request, 'prevention_theft/main.html')

    elif request.method == 'POST':
        evt.set()
        print("PROGRAM STOP")
        return render(request, 'prevention_theft/main.html')

def start(request):
    if request.method == 'GET':
        global evt; evt = Event()

        def BACKGROUND1(func):
            def background_func():
                Thread(target=func).start()
            return background_func
        @BACKGROUND1
        def background_func1():
            program_first.funct(evt)

        def BACKGROUND2(func):
            def background_func():
                Thread(target=func).start()
            return background_func
        @BACKGROUND2
        def background_func2():
            program_second.funct(evt)

        def BACKGROUND3(func):
            def background_func():
                Thread(target=func).start()
            return background_func
        @BACKGROUND3
        def background_func3():
            program_third.funct(evt)

        print("PROGRAM WAITING...")
        background_func1()
        time.sleep(10)
        background_func2()
        background_func3()
        print("PROGRAM RUNNING")
        return render(request, 'prevention_theft/start.html')
    
    elif request.method == 'POST':
        return render(request, 'prevention_theft/start.html')
    
def stealed_list(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            items = models.Item.objects.exclude(disappeared_count=0)
            serializer = serializers.ItemSerializer(items, many=True)
            return render(request,'prevention_theft/stealed_list.html', {'items':serializer.data})