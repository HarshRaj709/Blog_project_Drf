from django.shortcuts import render
from .serializers import BlogSerializer
from .models import Blog
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django.db.models import Q

#Create your views here.
class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all()  # Define the queryset to be used by the viewset
    serializer_class = BlogSerializer  # Define the serializer to be used by the viewset
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    # Optional: Override other methods if necessary, for example:
    def create(self, request):
        try:
            return super().create(request)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self,request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data':serializer.data,
                    'message':'blog created Successfully'
                },status=status.HTTP_201_CREATED)
            else:
                response_data={'data':serializer.errors}
                return Response(response_data,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data':str(e)},status = status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        try:
            # all = Blog.objects.all()
            blog = Blog.objects.filter(user = request.user.id)     #now get only data of requested user post
            if request.GET.get('search'):           #don't use request.GET['search'] as it may cause error. 
                search = request.GET.get('search')
                blog = Blog.objects.filter(Q(title__icontains = search)|
                                            Q(description__icontains = search))
            serializer = BlogSerializer(blog,many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request,pk):
        try:
            blog = Blog.objects.get(uuid=pk,user = request.user.id)     #to check that blog admin is the one who want to edit
            data = request.data
            serializer = BlogSerializer(data = data,instance =blog,partial=True )
            if serializer.is_valid():
                serializer.save()
                return Response({'message':"data updated successfully",'data':serializer.data},status = status.HTTP_200_OK)
            else:
                return Response({
                    'message':'Something went wrong'
                },status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,pk):
        try:
            blog = Blog.objects.get(uuid = pk,user = request.user.id)
            blog.delete()
            return Response({'message':'blog deleted successfully'})
        except Exception as e:
            print(e)
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    




def home(request):
    return render(request,'home.html')