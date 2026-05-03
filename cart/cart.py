from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """Sepeti başlatıyoruz."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False, mode='perakende'):
        """Ürünü sepete ekliyoruz veya miktarını güncelliyoruz."""
        product_id = str(product.id)
        
        if product_id not in self.cart:
            # Yeni ürün eklenirken toptan modundaysa direkt 5'ten başlat
            initial_qty = 5 if mode == 'toptan' and quantity < 5 else quantity
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price_retail if mode == 'perakende' else product.price_wholesale),
                'mode': mode
            }
            self.cart[product_id]['quantity'] = initial_qty
        else:
            if override_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                # Mevcut miktarın üzerine gelen quantity'i ekle (eksi gelirse düşer)
                new_qty = self.cart[product_id]['quantity'] + quantity
                
                # KONTROL: Toptan modunda 5'in altına, perakende de 1'in altına düşmesin
                if mode == 'toptan' and new_qty < 5:
                    new_qty = 5
                elif mode == 'perakende' and new_qty < 1:
                    new_qty = 1
                    
                self.cart[product_id]['quantity'] = new_qty
        
        self.save()

    def save(self):
        """Oturumu güncelliyoruz."""
        self.session.modified = True

    def remove(self, product):
        """Ürünü sepetten siliyoruz."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Sepetteki ürünleri döngüye almamızı sağlayan metot.
        Hata buradaki bir eksiklikten kaynaklanıyor.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item  # Bu satır objeyi 'iterable' (döngüye sokulabilir) yapar

    def __len__(self):
        """Sepette toplam kaç adet ürün var?"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Toplam sepet tutarını hesaplıyoruz."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Sepeti boşaltıyoruz."""
        del self.session[settings.CART_SESSION_ID]
        self.save()