from payload import Payload
import qrcode

if __name__ == '__main__':

    pix = Payload()
    pix.set_pix_key('19c0273f-0cad-483a-ad07-f7f86dac9837')\
        .set_description('PythonGit')\
        .set_merchant_name('Alexandre Augusto Simoes ')\
        .set_merchant_city('SAO PAULO')\
        .set_amount(10.00)\
        .set_txid('enginner')

    img = qrcode.make(pix.get_payload())
    img.save('localNoseuPc')

