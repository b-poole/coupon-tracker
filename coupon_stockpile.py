# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:16:49 2024

@author: barre
"""

import log
import json
import datetime
from dataclasses import dataclass, asdict
from typing import Optional

#Initilize logger
logger = log.setup_logging(__name__)

@dataclass       
class Coupon:
    item_name: str
    amount: float
    clipped: bool = False
    store: Optional[str] = None
    reward_point: Optional[bool] = None
    purchase_amount: Optional[int] = None
    expiration_date: Optional[datetime.date] = None
    online_only: Optional[bool] = None
    tags: Optional[list[str]] = None
    exclusions: Optional[list[str]] = None
    
    def __post__init__(self):
        raise NotImplementedError
        
    def clip_coupon(self):
        self.clipped = True

@dataclass
class Store:
    name: str
    url: str 
    coupons: Optional[list[Coupon]]
    
    def __post__init__(self):
        raise NotImplementedError
        
    def update_coupon_list(self) -> None:
        self.coupons = self.scrape_coupons()
    
    def scrape_coupons(self) -> list[Coupon]:
        raise NotImplementedError
    
    def update_coupon_store_name(self) -> None:
        for coupon in self.coupons:
            coupon.store = self.name
            
    def get_coupon_names(self) -> list[str]:
        return [coupon.item_name for coupon in self.coupons]
    
    def get_clipped_coupons(self) -> list[Coupon]:
        clipped_coupons = []
        for coupon in self.coupons:
            if coupon.clipped:
                clipped_coupons.append(coupon)
        return clipped_coupons
    

#Tested as of 6:00pm est 6/9/2024
def get_json_data(filepath: str):
    with open(filepath, 'r') as file:
        return json.load(file)

#Tested as of 6:00pm est 6/9/2024
def to_json(obj, indent=0) -> str:
    if isinstance(obj, list):
        obj_list = [asdict(o) for o in obj]
        return json.dumps(obj_list, indent=indent)
    return json.dumps(asdict(obj), indent=indent)

#Tested as of 6:00pm est 6/9/2024               
def save_to_json(json_str: str, filepath: str) -> None:
    with open(filepath, 'w') as file:
        file.write(json_str)

        
if __name__ == '__main__':
    logger.info("Initilizing")
    coupon1 = Coupon("soap", 2.0)
    coupon2 = Coupon("applesauce", 3.1)
    coupon3 = Coupon("milk", 1.0, clipped=True)
    coupons = [coupon1, coupon2, coupon3]
    
    store = Store("Walgreens", "https://www.walgreens.com/offers/offers.jsp", coupons)
    
    
    save_to_json(to_json(store, indent=4), "stores.json")
    
    