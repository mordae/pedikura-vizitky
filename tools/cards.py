#!/usr/bin/python3 -tt

from lxml import etree
import sys
import vobject
import re

parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

with open(sys.argv[1], 'r') as f:
    card = f.read()
    c = vobject.readOne(card)

with open(sys.argv[2], 'r') as f:
    svg = f.read().encode('utf-8')
    root = etree.fromstring(svg, parser=parser)

with open(sys.argv[3], 'r') as f:
    qrsrc = f.read().encode('utf-8')
    qr = etree.fromstring(qrsrc, parser=parser)


ns = {'n': "http://www.w3.org/2000/svg"}
name_e = root.xpath("//n:text[@id='name']/n:tspan", namespaces=ns)[0]
org_e = root.xpath("//n:text[@id='org']/n:tspan", namespaces=ns)[0]
phone_e = root.xpath("//n:text[@id='phone']/n:tspan", namespaces=ns)[0]
web_e = root.xpath("//n:text[@id='web']/n:tspan", namespaces=ns)[0]
email_e = root.xpath("//n:text[@id='email']/n:tspan", namespaces=ns)[0]

name_parts = [c.n.value.prefix, c.n.value.given, c.n.value.family]

name_e.text = ' '.join(filter(None,name_parts))
org_e.text = ' '.join(c.org.value)
phone_e.text = re.subn('([0-9]{3})', '\g<0> ', c.tel.value)[0].strip()
web_e.text = c.url.value
email_e.text = c.email.value

newQr = qr.xpath('//n:g[@id="Pattern"]', namespaces=ns)[0]
newViewBox = qr.attrib['viewBox']

symbol = root.xpath('//n:symbol[@id="qr"]', namespaces=ns)[0]
symbol.attrib['viewBox'] = newViewBox

oldQr = root.xpath('//n:symbol[@id="qr"]/n:g[@id="Pattern"]', namespaces=ns)[0]

for child in oldQr.getchildren():
    oldQr.remove(child)

for child in newQr.getchildren():
    oldQr.append(child)

with open(sys.argv[4], 'w') as f:
    f.write(etree.tostring(root, encoding='unicode'))


# vim:set sw=4 ts=4 et:
# -*- coding: utf-8 -*-

