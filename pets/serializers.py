from rest_framework import serializers

from groups.models import Group
from groups.serializers import GroupSerializer
from pets.models import Pet, Sex
from traits.models import Trait
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Sex.choices, default=Sex.DEFAULT)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def create(self, validated_data: dict):
        group_dict = validated_data.pop("group")
        traits_list = validated_data.pop("traits")

        group_obj, _ = Group.objects.get_or_create(**group_dict)
        pet_obj = Pet.objects.create(**validated_data, group=group_obj)

        for trait in traits_list:
            traits, _ = Trait.objects.get_or_create(**trait)
            pet_obj.traits.add(traits)

        return pet_obj

    def update(self, instance: Pet, validated_data: dict):
        group_dict: dict = validated_data.pop("group", None)
        traits_list: dict = validated_data.pop("traits", None)

        if group_dict:
            group_att, _ = Group.objects.get_or_create(**group_dict)
            instance.group = group_att

        if traits_list:
            traits_att_list = []
            for trait in traits_list:
                traits_att, _ = Trait.objects.get_or_create(**trait)
                traits_att_list.append(traits_att)

            instance.traits.set(traits_att_list)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
