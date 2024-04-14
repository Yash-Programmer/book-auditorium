from django.shortcuts import render

def error_404(request, exception):
    return render(request, "error.html", status=404, context={"message": "Page not found", "1": 4, "2": 0, "3": 4})


def error_500(request):
    return render(request, "error.html", status=500, context={"message": "Server", "1": 5, "2": 0, "3": 0})