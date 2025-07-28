from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API" # Nombre que aparecera 
    # #Funcion para obtener todos los datos
    # def get(self, request): 
    #     return Response(data_list, status=status.HTTP_200_OK)

    def get(self, request):
      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)    

    # POST
    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)

class DemoRestApiItem(APIView):
    name = "Demo REST API - Item"

    # PUT: Reemplaza completamente los campos de un objeto (menos el id)
    def put(self, request, id):
        for item in data_list:
            if item['id'] == id:
                data = request.data
                if 'id' not in data or data['id'] != id:
                    return Response({'error': 'El ID no coincide o falta.'}, status=status.HTTP_400_BAD_REQUEST)
                if 'name' not in data or 'email' not in data:
                    return Response({'error': 'Faltan campos obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

                item['name'] = data['name']
                item['email'] = data['email']
                item['is_active'] = data.get('is_active', True)

                return Response({'message': 'Elemento reemplazado exitosamente.', 'data': item}, status=status.HTTP_200_OK)

        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    # PATCH: Actualiza parcialmente los campos del objeto
    def patch(self, request, id):
        for item in data_list:
            if item['id'] == id:
                data = request.data
                item.update({k: v for k, v in data.items() if k in ['name', 'email', 'is_active']})
                return Response({'message': 'Elemento actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)

        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    # DELETE: Eliminación lógica del objeto
    def delete(self, request, id):
        for item in data_list:
            if item['id'] == id:
                if not item.get('is_active', True):
                    return Response({'error': 'Elemento ya inactivo.'}, status=status.HTTP_400_BAD_REQUEST)
                item['is_active'] = False
                return Response({'message': 'Elemento eliminado lógicamente.'}, status=status.HTTP_200_OK)

        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
