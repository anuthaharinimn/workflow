
#from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from users.models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=False)
	confirm_password = serializers.CharField(write_only=True, required=False)

	class Meta:
		model = UserAccount
		fields = ('id', 'email', 'username', 'created', 'modified', 'first_name', 'last_name', 'tagline', 'password', 'confirm_password',)
		read_only_fields = ('created', 'modified',)

		def create(self, validated_data):
			return UserAccount.objects.create(**validated_data)

		def update(self, instance, validated_data):
			instance.username = validated_data.get('username', instance.username)
			instance.tagline = validated_data.get('tagline', instance.tagline)

			instance.save()

			password = validated_data.get('password', None)
			confirm_password = validated_data.get('confirm_password', None)

			if password and confirm_password and password == confirm_password:
				instance.set_password(password)
				instance.save()

			# this is required to update the seesion otherwise user has to loing again
			#update_session_auth_hash(self.context.get('request'), instance)
			return instance

