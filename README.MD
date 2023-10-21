# Craftgate Python Client

Craftgate Python Client, Craftgate API'sinin Python uygulamasıdır.
Python'da yazılmış uygulamalardan Craftgate API'sine kolay erişim sağlar.

Craftgate API'sinin güvenlik kontrolleri bu istemci kütüphanesi tarafından gerçekleştirilir.

Craftgate API hakkında daha fazla bilgi için [dokümantasyon sayfasını](https://developer.craftgate.io) ziyaret edebilirsiniz.

## Kullanım

Güvenlik Önerilleri Craftgate önerileri için [burayı](https://developer.craftgate.io/security-recommendations) inceleyiniz.

Craftgate kendisine gönderilen ve size gönderdiği her isteğin bir imzalama algoritması ile doğrulamaktadır. Bu imza hesaplama
algoritması craftgateAdapter.py içinde tanımlı. İmza hesaplama için [burayı](https://developer.craftgate.io/api/#i%CC%87mza-hesaplama-) ziyaret edebilirsiniz.

Örnek olarak ödeme ve kart saklama servislerini kullanılmıştır.
craftgatePath.py içinde kullnacağınız Craftgate endpointleri tanımlayabilirsiniz. 

## Örnek Payload

3d Ödeme Başlatmak için örnek payload:
```
{
    "orderItem": [
        {
            "name": "Danışmanlık",
            "price": "35"
        }
    ],
    "price": "35",
    "externalId": "1919",
    "cardHolderName": "Salih Bilgin",
    "cardNumber": "5406670000000009",
    "expireYear": "2029",
    "expireMonth": "01",
    "cvc": "999",
    "saveToCard": false
}
```

## Test edilen Python sürümleri
<a href="https://www.python.org" rel="nofollow"><img src="https://camo.githubusercontent.com/1bc5ac25e9f8e6bcaabf1014bdfe7c1c654d04d3df3a48aada1118bd2b317fd2/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f666173746170692e7376673f636f6c6f723d253233333444303538" alt="Supported Python versions" data-canonical-src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" style="max-width: 100%;">
</a>

## Test edilen Python Framework'leri
<p> 
 <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/></a>
<a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/></a> 
<a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/></a> 
<a href="https://fastapi.tiangolo.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/github/explore/5deae0f0b95cec79f799c152535ca275e64595bb/topics/fastapi/fastapi.png" alt="fastapi" width="40" height="40"/></a>
</p>
