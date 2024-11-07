from django.shortcuts import render

# Vista para manejar el error 404 (página no encontrada)
def error_404(request, exception):
    return render(request, 'error.html', {'mensaje': 'Página no encontrada'}, status=404)

# Vista para manejar el error 500 (error interno del servidor)
def error_500(request):
    return render(request, 'error.html', {'mensaje': 'Error interno del servidor'}, status=500)
