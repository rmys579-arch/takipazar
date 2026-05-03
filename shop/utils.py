import iyzipay
from django.utils import translation

current_language = translation.get_language() # 'tr' veya 'en' döner
iyzico_locale = 'tr' if current_language == 'tr' else 'en'
def start_3ds_payment(order, card_details, cart):
    # API Anahtarları ve Bağlantı Ayarları
    options = {
        'api_key': 'sandbox-wPnVZ7Hlw5Uk8XRSX4VUVCpSFR3oYiyJ',
        'secret_key': 'VCtmsSRLi7oBzNb7bhF1Jsllhzepcajt',
        'base_url': 'https://api.iyzipay.com' # Protokolsüz en güvenli hal
    }

    # Callback URL (Banka onayından sonra döneceği adres)
    callback_url = "http://127.0.0.1:8000/shop/payment/callback/"

    # İstek Sözlüğü
    request = {
        'locale': iyzico_locale,
        'conversationId': str(order.id),
        'price': str(order.total_paid).replace(',', '.'),
        'paidPrice': str(order.total_paid).replace(',', '.'),
        'currency': 'TRY',
        'basketId': str(order.id),
        'paymentChannel': 'WEB',
        'paymentGroup': 'PRODUCT',
        'callbackUrl': callback_url,
        'paymentCard': {
            'cardHolderName': str(card_details['card_name']),
            'cardNumber': str(card_details['card_number']),
            'expireMonth': str(card_details['expire_month']),
            'expireYear': str(card_details['expire_year']),
            'cvc': str(card_details['cvc']),
            'registerCard': '0'
        },
        'buyer': {
            'id': str(order.id),
            'name': str(order.first_name),
            'surname': str(order.last_name),
            'gsmNumber': f"+90{order.phone}" if not str(order.phone).startswith('+') else str(order.phone),
            'email': str(order.email),
            'identityNumber': '11111111111', # Sandbox için sabit kalabilir
            'registrationAddress': str(order.address),
            'ip': '85.34.78.112',
            'city': str(order.city),
            'country': str(order.country),
        },
        'shippingAddress': {
            'contactName': f"{order.first_name} {order.last_name}",
            'city': str(order.city),
            'country': str(order.country),
            'address': str(order.address),
        },
        'billingAddress': {
            'contactName': f"{order.first_name} {order.last_name}",
            'city': str(order.city),
            'country': str(order.country),
            'address': str(order.address),
        },
        'basketItems': [
            {
                'id': str(item['product'].id),
                'name': str(item['product'].name)[:100],
                'category1': 'Taki',
                'itemType': 'PHYSICAL',
                'price': str(item['total_price']).replace(',', '.')
            } for item in cart
        ]
    }

    # 3D Secure Başlatma İşlemi
    threeds_initialize = iyzipay.ThreedsInitialize().create(request, options)
    
    try:
        if hasattr(threeds_initialize, 'to_json_result'):
            res_data = threeds_initialize.to_json_result()
        else:
            res_data = threeds_initialize.read().decode('utf-8')
        
        # Geliştirme aşamasında terminalden izlemek için:
        print("--- IYZICO DEBUG ---")
        print(res_data)
        
        return res_data
        
    except Exception as e:
        print(f"IYZICO OKUMA HATASI: {e}")
        return None
