from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'titulo','mensagem','is_read', 'criado_em',]
        read_only_fields = ['id', 'criado_em']


class NotificationCreateSerializer(serializers.Serializer):
    titulo = serializers.CharField()
    user_id = serializers.IntegerField()
    mensagem = serializers.CharField()