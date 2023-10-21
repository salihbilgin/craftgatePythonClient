from django.db import models


class Payments(models.Model):
    craftgatePaymentId = models.CharField(max_length=32)
    createdDate = models.DateTimeField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    paidPrice = models.FloatField(null=True, blank=True)
    walletPrice = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=3)
    conversationId = models.CharField(max_length=64)
    paymentSource = models.CharField(max_length=16)
    paymentType = models.CharField(max_length=16)
    paymentProvider = models.CharField(max_length=16)
    paymentGroup = models.CharField(max_length=32)
    paymentStatus = models.CharField(max_length=32)
    orderId = models.CharField(max_length=32)
    installment = models.FloatField(null=True, blank=True)
    isThreeDS = models.CharField(max_length=16)
    authCode = models.CharField(max_length=32)
    hostReference = models.CharField(max_length=64)
    transId = models.CharField(max_length=32)
    paymentPhase = models.CharField(max_length=32)
    merchantCommissionRate = models.FloatField(null=True, blank=True)
    merchantCommissionRateAmount = models.FloatField(null=True, blank=True)
    bankCommissionRate = models.FloatField(null=True, blank=True)
    bankCommissionRateAmount = models.FloatField(null=True, blank=True)
    paidWithStoredCard = models.CharField(max_length=32)
    binNumber = models.CharField(max_length=32)
    lastFourDigits = models.CharField(max_length=32)
    cardType = models.CharField(max_length=32)
    cardAssociation = models.CharField(max_length=32)
    cardBrand = models.CharField(max_length=32)
    cardHolderName = models.CharField(max_length=128)
    bankCardHolderName = models.CharField(max_length=128)
    pos = models.JSONField(null=True, blank=True)
    paymentTransactions = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'payments'
        verbose_name = 'payments'
        verbose_name_plural = 'payments'


class CardStore(models.Model):
    memberUserId = models.IntegerField(null=True, blank=True)  # Local User Id
    cardUserKey = models.CharField(max_length=64, null=True, blank=True)  # CraftGate User Id
    cardToken = models.CharField(max_length=64, null=True)
    cardAlias = models.CharField(max_length=64, null=True)
    cardType = models.CharField(max_length=64, null=True, blank=True)
    cardAssociation = models.CharField(max_length=64, null=True, blank=True)
    cardBrand = models.CharField(max_length=64, null=True, blank=True)
    cardBankName = models.CharField(max_length=64, null=True, blank=True)
    cardBankId = models.CharField(max_length=64, null=True, blank=True)
    binNumber = models.CharField(max_length=64, null=True, blank=True)
    lastFourDigits = models.CharField(max_length=64, null=True, blank=True)
    cardExpiryStatus = models.CharField(max_length=64, null=True, blank=True)
    isSendCraftGate = models.BooleanField(default=False)


    class Meta:
        db_table = 'cardstore'
        verbose_name = 'Card Store'
        verbose_name_plural = 'Card Store'

    def __str__(self):
        return str(self.id)
