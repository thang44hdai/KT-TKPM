from rest_framework import serializers
from .models import Customer, Name, Address


class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Có thể hash mật khẩu nếu cần
        validated_data['password'] = validated_data['password']
        return super().create(validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=255)
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255)
    zip_code = serializers.CharField(max_length=20)
    is_active = serializers.BooleanField(
        default=True)  # Mặc định True nếu không truyền

    class Meta:
        model = Customer
        fields = ['username', 'password', 'firstname', 'lastname',
                  'street', 'city', 'state', 'zip_code', 'is_active']

    def create(self, validated_data):
        # Tạo mới Name object
        name = Name.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname']
        )

        # Tạo mới Address object
        address = Address.objects.create(
            street=validated_data['street'],
            city=validated_data['city'],
            state=validated_data['state'],
            zip_code=validated_data['zip_code']
        )

        # Tạo mới Customer object
        customer = Customer.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],  # Không hash mật khẩu
            name=name,
            address=address,
            is_active=validated_data.get('is_active', True)
        )

        return customer
