# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:21:04 2024

@author: barre
"""
import unittest
import coupon_stockpile as cs

class TestCouponStockpile(unittest.TestCase):
    def setUp(self):      
        self.coupon1 = cs.Coupon("soap", 2.0)
        self.coupon2 = cs.Coupon("applesauce", 3.1)
        
        self.coupons = [self.coupon1, self.coupon2]
        
        self.store = cs.Store("Walgreens", "https://www.walgreens.com/offers/offers.jsp", self.coupons)
        
        self.coupon3 = cs.Coupon("milk", 1.0, clipped=True)
        self.store2 = cs.Store("Walgreens", 
                               "https://www.walgreens.com/offers/offers.jsp", 
                               [self.coupon1, self.coupon2, self.coupon3])
        
    def test_coupon(self):
        self.assertEqual(self.coupon1.item_name, "soap")
        self.assertEqual(self.coupon2.amount, 3.1)
        
        self.assertEqual(self.coupons[0].amount, 2.0)
        self.assertEqual(self.coupons[1].item_name, "applesauce")
        
    def test_to_json(self):
        self.json_coupon2 = cs.to_json(self.coupon2)
        
        #Syntax of string very important. Do not change!
        self.assertEqual(self.json_coupon2, """{
"item_name": "applesauce",
"amount": 3.1,
"clipped": false,
"store": null,
"reward_point": null,
"purchase_amount": null,
"expiration_date": null,
"online_only": null,
"tags": null,
"exclusions": null
}""")
        
        with open("tests/sample_coupons_list2.json", 'r') as file:
            self.sample_coupon_list_contents = file.read()
        self.json_all_coupons = cs.to_json(self.coupons, indent=4)
        self.assertEqual(self.json_all_coupons, self.sample_coupon_list_contents)
            
    
    def test_json_import(self):
        #Single Coupon import
        self.coupon_data = cs.get_json_data("tests/sample_coupons.json")
        self.assertEqual(cs.Coupon(**self.coupon_data), cs.Coupon("soap", 2.0))
        
        #Multiple Coupon import           
        self.coupons_list_contents = cs.get_json_data("tests/sample_coupons_list.json")
        
        #JSON file is a list of Coupons, so parse through list, creating coupons through dict unpacking
        self.loaded_coupons = [cs.Coupon(**self.a_data) for self.a_data in self.coupons_list_contents]
        self.assertEqual(self.loaded_coupons, self.coupons)
        
    def test_json_export(self):
        #Syntax of string very important. Do not change!
        self.json_coupon1 = """{
    "item_name": "soap",
    "amount": 2.0,
    "clipped": false,
    "store": null,
    "reward_point": null,
    "purchase_amount": null,
    "expiration_date": null,
    "online_only": null,
    "tags": null,
    "exclusions": null
}"""

        cs.save_to_json(self.json_coupon1, "tests/sample_coupons_export.json")
        with open("tests/sample_coupons_export.json", "r") as file:
            self.sample_coupons_export_contents = file.read()
        with open("tests/sample_coupons2.json", 'r') as file:
            self.sample_coupons_contents = file.read()
        self.assertEqual(self.sample_coupons_export_contents, self.sample_coupons_contents)
        
    def test_coupon_store(self):
        self.assertEqual(self.store.coupons[1].item_name, "applesauce")
        
    def test_update_coupon_store_name(self):
        self.store.update_coupon_store_name()
        self.assertEqual(self.store.coupons[0].store, "Walgreens")
        
    def test_store_get_coupon_names(self):
        self.coupon_names = self.store.get_coupon_names()
        self.assertEqual(self.coupon_names[0], "soap")
        
    def test_get_clipped_coupons(self):
        self.clipped_coupons = self.store2.get_clipped_coupons()
        self.assertEqual(self.clipped_coupons[0].item_name, "milk")
        
if __name__ == '__main__':
    unittest.main()

    
    
    
