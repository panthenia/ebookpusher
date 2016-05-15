print(__file__)
s = 'https://www.mlook.mobi/img/month_1203/831bf061c94392ec858dd583afdcd7555bc40f8b_66_88.jpg'
rs = s[::-1]
spl = rs.split('_', maxsplit=2)
qt = spl[0].split('.')[0]+'.'+spl[2]
print(qt)
result = qt[::-1]
print(result)
