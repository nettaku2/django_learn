def product_list(request):
    queryset = Product.objects.all()
    return render(request, 'template.html', {'result': list(queryset)})