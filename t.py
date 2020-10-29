import win32com.client as win32
import Window_Catia as wc
# def show_p(item,item1):
#     catapp = win32.Dispatch("CATIA.Application")
#     productDocument1 = catapp.ActiveDocument
#     product = productDocument1.Product
#     products1 = product.Products
#     product2 = products1.Item("%s" % item)
#     products2 = product2.Products
#     product3 = products2.Item("%s" % item1)
#     product3.ActivateDefaultShape()
# show_p("Product1.1", "following.1")

# def test_1(element1,element2,dist,relation):
#     catapp = win32.Dispatch("CATIA.Application")
#     productdoc = catapp.ActiveDocument
#     product = productdoc.Product
#     product = product.ReferenceProduct
#     constraints1 = product.Connections("CATIAConstraints")
#     ref1 = product.CreateReferenceFromName("Product1/%s.1/!PartBody/%s" % (element1,relation))
#     ref2 = product.CreateReferenceFromName("Product1/%s.1/!PartBody/%s" % (element2,relation))
#     constraint1 = constraints1.AddBiEltCst(2, ref1,ref2)
#     constraint1.Orientation = 0
#     product.Update()
#     return True

# def test_2(element1,element2,element4,element5,element3):
#     catapp = win32.Dispatch("CATIA.Application")
#     productdoc = catapp.ActiveDocument
#     product = productdoc.Product
#     product = product.ReferenceProduct
#     constraints1 = product.Connections("CATIAConstraints")
#     ref1 = product.CreateReferenceFromName("Product4/%s.1/%s.1/!PartBody/%s" % (element1,element2,element3))
#     ref2 = product.CreateReferenceFromName("Product4/%s.1/%s.1/!PartBody/%s" % (element4,element5,element3))
#     constraint1 = constraints1.AddBiEltCst(2, ref1,ref2)
#     constraint1.Orientation = 1
#     product.Update()
#
#     return True
# test_2('Product3','small2_left','Product2','small_left','Plane_Product_ZY')



# wc.show_p("Product1.1", "following.1")
# wc.show_p('Product1.1', 'left.1')
# wc.show_p('Product1.1', 'right.1')
# wc.show_p('Product1.1', 'top.1')
# wc.show_p('Product2.1', 'small_top.1')
# wc.show_p('Product2.1', 'small_left.1')
# wc.show_p('Product2.1', 'small_right.1')
# wc.show_p('Product2.1', 'small_following.1')
# wc.show_p('Product2.1', 'wheel_1.1')
# wc.show_p('Product2.1', 'wheel_2.1')
# wc.show_p('Product3.1', 'small2_top.1')
# wc.show_p('Product3.1', 'small2_left.1')
# wc.show_p('Product3.1', 'small2_right.1')
# wc.show_p('Product3.1', 'small2_following.1')
# wc.show_p('Product3.1', 'wheel_1.1')
# wc.show_p('Product3.1', 'wheel_2.1')