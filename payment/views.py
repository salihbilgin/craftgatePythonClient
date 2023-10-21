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
        orderPrice = data['price']
        installment = request.data.get('installment', 1)
        externalId = request.data.get('externalId', '')
        saveToCard = request.data.get('saveToCard', '')
        itemsArray = data['orderItem']
        baseAdapter = BaseAdapterTest
        operationPath = "/payment/v1/card-payments/3ds-init"
        callbackUrl = CALLBACK_URL
        if saveToCard:
            payload = {"price": orderPrice, "paidPrice": orderPrice, "walletPrice": 0.0, 'installment': installment,
                       "currency": 'TRY', "paymentGroup": 'PRODUCT', "callbackUrl": callbackUrl,
                       "externalId": externalId,
                       "card": {"cardHolderName": data['cardHolderName'], "cardNumber": data['cardNumber'],
                                "expireMonth": data["expireMonth"], "expireYear": data['expireYear'],
                                "cvc": data['cvc'], storeCardAfterSuccessPayment: True}, "items": itemsArray}
        else:
            payload = {"price": orderPrice, "paidPrice": orderPrice, "walletPrice": 0.0, 'installment': installment,
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
