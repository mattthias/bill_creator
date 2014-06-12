#!/usr/bin/python
# encoding: utf8

import csv
from fdfgen import forge_fdf
import subprocess
import datetime


class Order(object):
    def __init__(self, order_id, order_date, order_status, total, tax,
                 shipping_firstname, shipping_lastname, shipping_address1,
                 shipping_address2, shipping_postcode,
                 shipping_city, payment_method, box):
        self.order_id = order_id.decode('utf-8')
        # create a datetime object from incoming str date
        self.order_date = self._to_datetime(order_date.decode('utf-8'))
        self.order_status = order_status.decode('utf-8')

        # money related in €
        self.total = total.decode('utf-8')
        self.tax = tax.decode('utf-8')
        self.order_discount = None
        self.payment_method = payment_method.decode('utf-8')

        # Artikelbezeichnung
        self.box = box.decode('utf-8')

        # Coupons / Gutschein-Code / Voucher
        self.code = None

        self.shipping_firstname = shipping_firstname.decode('utf-8')
        self.shipping_lastname = shipping_lastname.decode('utf-8')
        self.shipping_address1 = shipping_address1.decode('utf-8')
        self.shipping_address2 = shipping_address2.decode('utf-8')
        self.shipping_postcode = shipping_postcode.decode('utf-8')
        self.shipping_city = shipping_city.decode('utf-8')

        self.billing_firstname = None
        self.billing_lastname = None
        self.billing_address1 = None
        self.billing_address2 = None
        self.billing_postcode = None
        self.billing_city = None

        self.age = None
        self.need_bill = self._need_bill()
        self.need_delivery_note = self._need_delivery_note()

    def __repr__(self):
        return "Bestellung: %s am %s bestellt, Kosten %s EUR (Mwst.: %s EUR)." % (self.box, self.order_date, self.total, self.tax)

    def _to_datetime(self, date_str):
        (year, month, day) = date_str.split(" ")[0].split("-")
        return datetime.datetime(int(year), int(month), int(day))

    def _need_bill(self):
        '''
            Es ist eine Rechnung wenn:
             - box gleich Monatsbücherbox
             - box gleich Schnupperdingsbums
             - Orderdate im Abrechungsmonat liegt

        '''

        if self.box in ["Monatsabo", "Probierbox"]:
            return True
        else:
            return False

    def _need_delivery_note(self):
        '''
        if shipping_address != billing_address
        '''
        return False


class PdfFormatter(object):
    def __init__(self, order, output_dir='./output/', template='billing_template.pdf'):
        self.order = order
        self.output_dir = output_dir
        self.template = template
        self.print_bill()

    def print_bill(self):
        fields = [
            ('shipping_name', self.order.shipping_firstname +
             ' ' + self.order.shipping_lastname),
            ('shipping_address1', self.order.shipping_address1),
            ('shipping_address2', self.order.shipping_address2),
            ('shipping_town', self.order.shipping_postcode +
             ' ' + self.order.shipping_city),
            ('order_date', self.order.order_date),
            ('payment_method', self.order.payment_method),
            ('total', self.order.total),
            ('tax', self.order.tax),
            ('box', self.order.box),
        ]

        fdf = forge_fdf("", fields, [], [], [])
        fdf_name = self.output_dir + '/' + self.order.order_id + '_' + self.order.shipping_lastname + '.fdf'
        with open(fdf_name, 'w') as fdf_file:
            fdf_file.write(fdf)

        pdf_name = self.output_dir + '/' + self.order.order_id + '_' + self.order.shipping_lastname + '.pdf'
        # pdftk vorlage.pdf fill_form data.fdf output ausgabe.pdf flatten
        subprocess.call(['pdftk',
                        self.template,
                        'fill_form',
                        fdf_name,
                        'output',
                        pdf_name,
                        'flatten'])


def main():
    stats = {}
    with open('export.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            # Erstelle ein Order-Objekt
            a = Order(order_id=row[0],
                      order_date=row[1],
                      order_status=row[2],
                      total=row[8],
                      tax=row[5],
                      shipping_firstname=row[22],
                      shipping_lastname=row[23],
                      shipping_address1=row[24],
                      shipping_address2=row[25],
                      shipping_postcode=row[26],
                      shipping_city=row[27],
                      payment_method=row[9],
                      box=row[33])

            print a.__repr__()
            if a.need_bill:
                PdfFormatter(a, template='rechnung.pdf')
            elif a.need_delivery_note:
                PdfFormatter(a, template='lieferschein.pdf')
            else:
                print "Something is wrong here: %s" % a.__repr__() 


if __name__ == '__main__':
    main()
