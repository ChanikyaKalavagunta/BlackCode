from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

##


##SEARCH API 


##
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Category, Product

@csrf_exempt
def search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            # Search for products matching the query in their name or brand
            products = Product.objects.filter(Q(name__icontains=query) | Q(brand__icontains=query))
            # Search for categories matching the query in their name
            categories = Category.objects.filter(name__icontains=query)
            # Create a list of dictionaries representing the search results
            results = []
            for product in products:
                results.append({
                    'type': 'product',
                    'id': product.id,
                    'name': product.name,
                    'category': product.category.name,
                    'price': str(product.price),
                    'brand': product.brand,
                    'size': product.size
                })
            for category in categories:
                results.append({
                    'type': 'category',
                    'id': category.id,
                    'name': category.name,
                    'category': None,
                    'price': None,
                    'brand': None,
                    'size': None
                })
            return JsonResponse({'results': results})
    return JsonResponse({'error': 'Invalid request method'})


from rest_framework.views import APIView
from rest_framework.response import Response

class GetProductsByPrice(APIView):
    def post(self, request, format=None):
        min_price = request.data.get('min_price', None)
        max_price = request.data.get('max_price', None)

        if not min_price or not max_price:
            return Response({'error': 'Please provide both min_price and max_price.'}, status=400)

        products = Product.objects.filter(price__range=(min_price, max_price))

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# import ast
# import difflib
# from rest_framework.views import APIView
# from django.http import HttpResponse
# from rest_framework import serializers


# class AdsDataFilter(APIView) :
#     def post( self,request , format=None):
#         start =request.data.get("start")
#         end= request.data.get("end")
#         print("hi")
#         requestData=ast.literal_eval(request.data.get("requestData"))
#         print("hello")
#         extraField=requestData["extrafiled"] if type(requestData["extrafiled"]) is dict   else ast.literal_eval(requestData["extrafiled"])
#         del requestData['extrafiled']
#         print(requestData,extraField)
#         s=Product.objects.all()
#         print(s.count()) 
#         filters = {}
#         for key1 in requestData:
#             if not (key1=="minPrice" or key1=="maxPrice" or key1=="searchValue"):
#                 key1=key1
#                 filters[key1] = requestData[key1]
#         s1=Product.objects.filter(**filters)
#         print(Product.objects.filter(subCategoryValue="Refrigerators/Fridge").filter(category="Furniture"))
#         print(s1)
#         if 'minPrice' in requestData or 'maxPrice' in requestData:
#             s1=s1.filter(price_gte=int(requestData['minPrice']),price_lte=int(requestData['maxPrice']))
#         finalProduct=Product.objects.filter(category="e3322222")
#         print("latest",finalProduct)
#         if len(extraField) != 0:
#             for x1 in s1:
#                 count=len(extraField)
#                 countTemp=0
#                 if x1.extraField:
#                     if (not x1.extraField =="null"):
#                         x1.extraField=ast.literal_eval(x1.extraField)
#                         newTempObjProdctExtraFiled={}
#                         for x in x1.extraField:
#                             z1=x.encode("ascii", "ignore")
#                             z2=x1.extraField[x].encode("ascii", "ignore")
#                             z11=z1.decode()
#                             z44=z2.decode()
#                             newTempObjProdctExtraFiled[z11]=z44
#                         for singlekeyValue in extraField:
#                             if singlekeyValue in newTempObjProdctExtraFiled.keys():
#                                 m=difflib.SequenceMatcher(None,extraField[singlekeyValue],newTempObjProdctExtraFiled[singlekeyValue]).ratio()
#                                 if(m*100>80):
#                                     countTemp=countTemp+1
#                             # if extraField[singlekeyValue] is newTempObjProdctExtraFiled[singlekeyValue]:
#                             #     countTemp=countTemp+1
#                             #     print("checking")
#                 print(count,countTemp)
#                 print(type(count),type(countTemp))
#                 if(count==countTemp):
#                     t1=Product.objects.filter(pk=x1.pk).filter(is_active=True).filter(expiry=False).filter(deleted=False)
#                     if t1 :
#                         finalProduct=finalProduct.union(t1)
#         if "tital" in requestData:
#             print("tital is also calling",requestData["title"])
#             s1=s1.filter(title__icontains=requestData["title"])
#             finalProduct=finalProduct.filter(title__icontains=requestData["title"])
#         print("data in tital",s1.count())
#         finalProduct = serializers.serialize('json', finalProduct[int(start):int(end)] if len(extraField) != 0 else s1.filter(is_active=True).filter(expiry=False).filter(deleted=False)[int(start):int(end)]) 
#         return HttpResponse(finalProduct, content_type='application/json')










