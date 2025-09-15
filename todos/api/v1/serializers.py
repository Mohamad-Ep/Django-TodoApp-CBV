from rest_framework import serializers
from ...models import Todo
from rest_framework.reverse import reverse
from accounts.models import Profile
# ________________________________________________

class TodoSerializer(serializers.ModelSerializer):
    relative_url = serializers.SerializerMethodField(method_name='get_relative_url',read_only=True)
    
    class Meta:
        model = Todo
        fields = ['id','title','published_date','is_active','is_done','author','relative_url']
        read_only_fields = ['published_date','is_active','is_done','author']
        
    
    def get_relative_url(self,obj):
        request = self.context.get('request')
        return reverse('todos:api-v1:todo-details', kwargs={'pk': obj.pk}, request=request)
    
    def validate_title(self, value):
        if len(value) < 5 :
            raise serializers.ValidationError({"details":"تعداد کاراکتر عنوان نباید کمتر از 5 کاراکتر باشد"})
        return value
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        
        if request.parser_context.get("kwargs").get("pk"):
           rep.pop('relative_url')           
        return rep 
    
    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)
    
# ________________________________________________