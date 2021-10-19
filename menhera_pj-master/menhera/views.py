from django.shortcuts import render

# Create your views here.
def index_template(request):
	return render(request, 'index.html')
def goods_template(request):
	return render(request, 'goods.html')
def blogs_template(request):
	return render(request, 'blogs.html')
def chat_template(request):
	return render(request, 'chat.html')
def future_template(request):
	return render(request, 'future.html')
def timeline_template(request):
	return render(request, 'timeline.html')
def test_template(request):
	return render(request, 'test.html')