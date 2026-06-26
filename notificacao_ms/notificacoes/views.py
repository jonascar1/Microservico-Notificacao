from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification, Target
from .serializers import NotificationSerializer, NotificationCreateSerializer
from .authentication import get_target_from_headers, get_empresa_from_headers


class NotificacoesNaoLidasCountView(APIView):
   
    def get(self, request):
        target = get_target_from_headers(request)
        count = Notification.objects.filter(target=target, is_read=False).count()
        return Response({'count': count})


class NotificacoesListView(APIView):
    

    def get(self, request):
        target = get_target_from_headers(request)
        notificacoes = Notification.objects.filter(target=target)

        # Filtro opcional por is_read
        is_read_param = request.query_params.get('is_read')
        if is_read_param is not None:
            is_read = is_read_param.lower() in ['true', '1', 'sim']
            notificacoes = notificacoes.filter(is_read=is_read)

        serializer = NotificationSerializer(notificacoes, many=True)
        return Response(serializer.data)


class NotificacaoMarcarLidaView(APIView):
   
    def patch(self, request, pk):
        target = get_target_from_headers(request)

        try:
            notificacao = Notification.objects.get(pk=pk, target=target)
        except Notification.DoesNotExist:
            return Response({'erro': 'Notificacao nao encontrada.'}, status=404)

        notificacao.is_read = True
        notificacao.save()

        serializer = NotificationSerializer(notificacao)
        return Response(serializer.data)


class NotificacaoCreateView(APIView):
  

    def post(self, request):
        empresa = get_empresa_from_headers(request)

        serializer = NotificationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Busca ou cria o target
        target, created = Target.objects.get_or_create(
            empresa=empresa,
            user_id=serializer.validated_data['user_id'],
        )

        # Cria a notificacao
        notificacao = Notification.objects.create(
    target=target,
    titulo=serializer.validated_data['titulo'],
    mensagem=serializer.validated_data['mensagem'],
)
        return Response(
            NotificationSerializer(notificacao).data,
            status=status.HTTP_201_CREATED,
        )

class NotificacoesMarcarTodasLidasView(APIView): # Para marcar as notificações como lida

    def patch(self, request):
        target = get_target_from_headers(request)

        Notification.objects.filter(
            target=target,
            is_read=False
        ).update(is_read=True)

        return Response({
            'mensagem': 'Todas as notificacoes foram marcadas como lidas.'
        })