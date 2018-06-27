from rest_framework import serializers, viewsets, routers
from .models import Note, PersonalNote

#TODO: CRITICAL: Disable this or modify to only work for admin/superuser
class NoteSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Note
    fields = ('title', 'content')


class NoteViewSet(viewsets.ModelViewSet):
  serializer_class = NoteSerializer
  queryset = Note.objects.all()


class PersonalNoteSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = PersonalNote
    fields = ('title', 'content')
  
  def create(self, validated_data):
    # import pdb; pdb.set_trace()
    user = self.context['request'].user
    personal_note = PersonalNote.objects.create(user=user, **validated_data)
    return personal_note


class PersonalNoteViewSet(viewsets.ModelViewSet):
  serializer_class = PersonalNoteSerializer
  # queryset = PersonalNote.objects.all()
  queryset = PersonalNote.objects.none()

  def get_queryset(self):
    user = self.request.user

    if user.is_anonymous:
      return PersonalNote.objects.none()
    
    else:
      return PersonalNote.objects.filter(user=user)
