from rest_framework import serializers

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=1000)

class AnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()