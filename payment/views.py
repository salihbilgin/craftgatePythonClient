from django.shortcuts import render
from craftgatePath import *
from craftgateAdapter import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import JsonResponse


def CleanHtmlDecode(html_code):
    import re
    html_code = re.sub(r"\n", '', html_code)
    html_code = re.sub(r"\t", '', html_code)
    html_code = re.sub(r"\r", '', html_code)
    return html_code


class Payment3DInit(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        installment = request.data.get('installment', 1)
        externalId = request.data.get('externalId', '')
        # Kartın kaydedilmesi (saveToCard) için True gönderilmeli. Payment kısmında kart kayıt bilgileri dönüyor.
        saveToCard = request.data.get('saveToCard', '')
        itemsArray = data['orderItem']
        baseAdapter = BaseAdapterTest
        operationPath = "/payment/v1/card-payments/3ds-init"
        callbackUrl = CALLBACK_URL
        if saveToCard:
            payload = {"price": data['price'], "paidPrice": data['price'], "walletPrice": 0.0,
                       'installment': installment,
                       "currency": 'TRY', "paymentGroup": 'PRODUCT', "callbackUrl": callbackUrl,
                       "externalId": externalId,
                       "card": {"cardHolderName": data['cardHolderName'], "cardNumber": data['cardNumber'],
                                "expireMonth": data["expireMonth"], "expireYear": data['expireYear'],
                                "cvc": data['cvc'], storeCardAfterSuccessPayment: True}, "items": itemsArray}
        else:
            payload = {"price": data['price'], "paidPrice": data['price'], "walletPrice": 0.0,
                       'installment': installment,
                       "currency": 'TRY', "paymentGroup": 'PRODUCT', "callbackUrl": callbackUrl,
                       "externalId": externalId,
                       "card": {"cardHolderName": data['cardHolderName'], "cardNumber": data['cardNumber'],
                                "expireMonth": data["expireMonth"], "expireYear": data['expireYear'],
                                "cvc": data['cvc']}, "items": itemsArray}
        response = baseAdapter.httpPost(operationPath, payload)
        data = response.get("data")
        if data:
            import base64
            decodeHtml = base64.b64decode(data["htmlContent"]).decode("utf-8")
            cleanDecodeHtml = CleanHtmlDecode(decodeHtml)

            responseData = {'htmlCode': cleanDecodeHtml, 'paymentId': data["paymentId"], 'message': 'payment Created',
                            'success': True}
            return JsonResponse(responseData, status=status.HTTP_200_OK)
        else:
            responseData = {"errorCode": response["errors"]["errorCode"],
                            "error": response["errors"]["errorDescription"], }
            return JsonResponse(responseData, status=status.HTTP_400_BAD_REQUEST)


class Payment3DComplete(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payerCheck = request.data.get("status", "")
        if payerCheck == "SUCCESS":
            dataPost = request.data
            baseAdapter = BaseAdapterTest
            operationPath = PAYMENT_INIT_PATH_3D_PAY
            craftgateResponse = baseAdapter.httpPost(operationPath, {"paymentId": dataPost['paymentId']})
            data = craftgateResponse.get("data")
            if data:
                Payments.objects.create(craftgatePaymentId=data['id'], createdDate=data['createdDate'],
                                        price=data['price'], paidPrice=data['paidPrice'],
                                        walletPrice=data['walletPrice'], currency=data['currency'],
                                        conversationId=data['conversationId'], paymentSource=data['paymentSource'],
                                        paymentType=data['paymentType'], paymentProvider=data['paymentProvider'],
                                        paymentGroup=data['paymentGroup'], paymentStatus=data['paymentStatus'],
                                        installment=data['installment'], isThreeDS=True, authCode=data['authCode'],
                                        hostReference=data['hostReference'], paymentPhase=data['paymentPhase'],
                                        merchantCommissionRate=data['merchantCommissionRate'],
                                        merchantCommissionRateAmount=data['merchantCommissionRateAmount'],
                                        bankCommissionRate=data['bankCommissionRateAmount'],
                                        bankCommissionRateAmount=data['bankCommissionRateAmount'],
                                        paidWithStoredCard=data['paidWithStoredCard'], binNumber=data['binNumber'],
                                        lastFourDigits=data['lastFourDigits'], cardType=data['cardType'],
                                        cardAssociation=data['cardAssociation'], cardBrand=data['cardBrand'],
                                        cardHolderName=data['cardHolderName'],
                                        bankCardHolderName=data['bankCardHolderName'], pos=data['pos'],
                                        paymentTransactions=data['paymentTransactions'], )
                cardUserKey = request.data.get('cardUserKey', '')
                if cardUserKey:
                    CardStore.objects.create(memberUserId=data['externalId'],
                                             cardUserKey=data['cardUserKey'],
                                             cardToken=data['cardToken'],
                                             cardType=data['cardType'],
                                             cardAssociation=data['cardAssociation'],
                                             cardBrand=data['cardBrand'],
                                             cardBankName=data['bankCardHolderName'],
                                             cardBankId=dataCardStore.get('cardBankId', ''),
                                             binNumber=data['binNumber'],
                                             lastFourDigits=dataCardStore.data['lastFourDigits'],
                                             isSendCraftGate=True)
                return JsonResponse({'status': "ODEME BASARILI", 'success': True}, status=status.HTTP_201_CREATED)
        else:
            responseData = {"status": "ODEME BASARISIZ", 'success': False}
            return JsonResponse(responseData, status=status.HTTP_400_BAD_REQUEST)


class PaymentCardStoreList(APIView):
    craftGateOptions = CraftgateOptionsDiyetkolik()
    serializer_class = CardStoreSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = {'id': ['exact'], 'memberUserId': ['exact'], 'cardUserKey': ['exact'], }
    search_fields = ('id',)
    ordering = ['-isDefault', 'id']

    def get_queryset(self):
        return CardStore.objects.filter(is_deleted=False, is_active=True, memberUserId=self.request.user.id)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        ################################# CRAFTGATE POST #################################
        baseAdapter = BaseAdapterProd()
        operationPath = "/payment/v1/cards"
        payload = {"cardHolderName": request.data['cardHolderName'], "cardNumber": request.data['cardNumber'],
                   "expireYear": request.data['expireYear'], "expireMonth": request.data['expireMonth'], }
        headers = baseAdapter.prepareHeaders(headers=None, path=operationPath, request=payload)
        print(request.data['cardNumber'][-4:])
        print(request.data['cardNumber'][:8])
        ##İlk kayıtta isDefault True olacak. Sonrakilerde False , Daha sonra PUT işleminde değiştirebilir.
        print(self.request.user.id)
        userCardsCardStore = CardStore.objects.filter(is_deleted=False, memberUserId=int(self.request.user.id),
                                                      binNumber=request.data['cardNumber'][:8], isDiyetkolik=False,
                                                      lastFourDigits=request.data['cardNumber'][-4:]).exists()
        if not userCardsCardStore:
            isDefault = True
            response = requests.post(str(self.craftGateOptions.base_url) + str(operationPath), json=payload,
                                     headers=headers)
            if response.status_code == 201 or response.status_code == 200:
                data = response.json().get('data', {})
                cardStore = CardStore.objects.create(memberUserId=self.request.user.id,
                                                     cardUserKey=data.get('cardUserKey', ''),
                                                     cardToken=data.get('cardToken', ''),
                                                     cardAlias=data.get('cardAlias', ''),
                                                     cardType=data.get('cardType', ''),
                                                     cardAssociation=data.get('cardAssociation', ''),
                                                     cardBrand=data.get('cardBrand', ''),
                                                     cardBankName=data.get('cardBankName', ''),
                                                     cardBankId=data.get('cardBankId', ''),
                                                     binNumber=data.get('binNumber', ''),
                                                     lastFourDigits=data.get('lastFourDigits', ''),
                                                     cardExpiryStatus=data.get('cardExpiryStatus', ''),
                                                     isSendCraftGate=True, isDefault=isDefault)
                serializer = CardStoreSerializer(cardStore)
                responseData = {'status': status.HTTP_201_CREATED, 'message': 'CardStore Created',
                                'cardToken': cardStore.cardToken, 'data': serializer.data, 'success': True}
                return JsonResponse(responseData, status=status.HTTP_201_CREATED)
        else:
            responseData = {'errors': response.text, 'status': status.HTTP_422_UNPROCESSABLE_ENTITY,
                            'message': 'CardStore Not Created.', 'success': False}
            return JsonResponse(responseData,
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)  #################################CraftGate POST #################################
