class Payload:

    __pixKey = None
    __description = None
    __merchantName = None
    __merchantCity = None
    __txid = None
    __amount = None

    idPayloadFormatIndicator = '00'
    idMerchantAccountInformation = '26'
    idMerchantAccountInformationGui = '00'
    idMerchantAccountInformationKey = '01'
    idMerchantAccountInformationDescription = '02'
    idMerchantCategoryCode = '52'
    idTransactionCurrency = '53'
    idTransactionAmount = '54'
    idCountryCode = '58'
    idMerchantName = '59'
    idMerchantCity = '60'
    idAdditionalDataFieldTemplate = '62'
    idAdditionalDataFieldTemplateTxid = '05'
    idCRC16 = '63'


    def set_pix_key(self, __pixKey):
        self.__pixKey = __pixKey

        return self

    def set_description(self, __description):
        self.__description = __description

        return self

    def set_merchant_name(self, __merchantName):
        self.__merchantName = __merchantName

        return self

    def set_merchant_city(self, __merchantCity):
        self.__merchantCity = __merchantCity.upper()

        return self

    def set_txid(self, __txid):
        self.__txid = __txid.upper()

        return self

    def set_amount(self, __amount):
        self.__amount = str(__amount)

        return self

    def get_value(self,id, value):
        size = f'{len(value):02}'
        return id+size+value

    def __get_merchant_account_information(self):
        gui = self.get_value(self.idMerchantAccountInformationGui, 'br.gov.bcb.pix')
        key = self.get_value(self.idMerchantAccountInformationKey, self.__pixKey)
        description =  self.get_value(self.idMerchantAccountInformationDescription, self.__description)

        return self.get_value(self.idMerchantAccountInformation, gui+key+description)

    def __get_additional_data_field_template(self):
        txid = self.get_value(self.idAdditionalDataFieldTemplateTxid, self.__txid)
        return self.get_value(self.idAdditionalDataFieldTemplate, txid)

    def bit(self, resultado):
        resultado <<= 1 & 0x10000
        return resultado

    def __get_CRC16(self, payload):

        payload += self.idCRC16+'04'
        polinomio = 0x1021
        resultado = 0xFFFF

        if len(payload) > 0:
            for i in range(len(payload)):
                resultado ^= (ord(payload[i]) << 8)
                for bitwise in range(8):
                    if(self.bit(resultado)): resultado ^= polinomio
                    resultado &= 0xFFFF

        return self.idCRC16+'04'+hex(resultado).upper()

    def get_payload(self):
        payload = self.get_value(self.idPayloadFormatIndicator, '01') \
                  + self.__get_merchant_account_information() \
                  + self.get_value(self.idMerchantCategoryCode, '0000') \
                  + self.get_value(self.idTransactionCurrency, '986') \
                  + self.get_value(self.idTransactionAmount, self.__amount) \
                  + self.get_value(self.idCountryCode, 'BR') \
                  + self.get_value(self.idMerchantName, self.__merchantName) \
                  + self.get_value(self.idMerchantCity, self.__merchantCity) \
                  + self.__get_additional_data_field_template()

        return payload+self.__get_CRC16(payload)



