import subprocess
import cv2
import numpy as np
import os
import time
from pathlib import Path

from .mumu_screenshot import MumuScreenshot
from .start_icon_detector import IconDetector
from .mumu_click import Tapscreen
from .show_detector import Showdetector
from .slide import Slide


class Dailytasks:
    '''
    日常任务：

     [主页面角色互动]
            |  
            v
     [领取商店随机奖励]
            |  
            v
        [委托派遣]
            |  
            v
      [赠送一次礼物]
            |  
            v
        [秘纹升级]
            |  
            v
        [旅人升级]
            |  
            v
     [领取日常任务奖励]

    '''
    def __init__(self):
        self.screenshot_tool = MumuScreenshot()
        self.tapscreen_tool = Tapscreen()
        self.display_tool = Showdetector(output_dir="test")
        self.slide_tool = Slide()
        

    @staticmethod
    def screenshots_almost_same(img_a, img_b, pixel_threshold=3, change_ratio=0.001):
        """Return True if two screenshots are almost identical."""
        if img_a is None or img_b is None:
            return False
        if img_a.shape != img_b.shape:
            return False

        diff = cv2.absdiff(img_a, img_b)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, pixel_threshold, 255, cv2.THRESH_BINARY)
        changed_pixels = np.count_nonzero(mask)
        total_pixels = mask.size
        if total_pixels == 0:
            return False
        changed_ratio = changed_pixels / total_pixels
        return changed_ratio <= change_ratio

    
    def run(self):
        screenshot_tool = self.screenshot_tool
        tapscreen_tool = self.tapscreen_tool
        display_tool = self.display_tool
        slide_tool = self.slide_tool
        
        
        #商城图标检测，用于检测是否处于主页面
        maintitle_chake = os.path.join(os.path.dirname(__file__), "../templates/mainTitle_icon/Market.png")
        maintitle_detector = IconDetector(maintitle_chake)

        #采购图标检测
        market_template_path = os.path.join(os.path.dirname(__file__), "../templates/mainTitle_icon/Purchasing.png")
        market_detector = IconDetector(market_template_path)

        #采购界面检测
        marketpagecheak_template_path = os.path.join(os.path.dirname(__file__), "../templates/market/MarketPageCheak.png")
        marketpagecheak_detector = IconDetector(marketpagecheak_template_path)

        #检测委托是否有红点
        commission_template_path  = os.path.join(os.path.dirname(__file__), "../templates/mainTitle_icon/commission_red.png")
        commission_detector = IconDetector(commission_template_path)
        
        #委托页面检测
        commissionpagecheak_template_path  = os.path.join(os.path.dirname(__file__), "../templates/commission/CommissionPageCheak.png")
        commissionpagecheak_detector = IconDetector(commissionpagecheak_template_path)

        #派遣判定
        iscommission_template_path  = os.path.join(os.path.dirname(__file__), "../templates/commission/iscommission.png")
        iscommission_detector = IconDetector(iscommission_template_path)
        
        #再次派遣按钮检测
        commissionagain_template_path  = os.path.join(os.path.dirname(__file__), "../templates/commission/commission_again.png")
        commissionagain_detector = IconDetector(commissionagain_template_path)

        #礼物页面检测
        giftpagecheak_template_path  = os.path.join(os.path.dirname(__file__), "../templates/gift/giftpagecheak.png")
        giftpagecheak_detector = IconDetector(giftpagecheak_template_path)

        #秘纹界面检测
        cardpagecheak_template_path  = os.path.join(os.path.dirname(__file__), "../templates/card/cardpagecheak.png")
        cardpagecheak_detector = IconDetector(cardpagecheak_template_path)

        #旅人界面检测
        characterpagecheak_template_path  = os.path.join(os.path.dirname(__file__), "../templates/character/characterpagecheak.png")
        characterpagecheak_detector = IconDetector(characterpagecheak_template_path)

        #旅人升级检测
        characterupgradepagecheak_template_path  = os.path.join(os.path.dirname(__file__), "../templates/character/upgrade.png")
        characterupgradepagecheak_detector = IconDetector(characterupgradepagecheak_template_path)



        def Back2maintitle():
            tapscreen_tool.tap_screen(66, 37)
            time.sleep(1)
            screenshot1 = screenshot_tool.capture()
            (x3, y3), conf2 = maintitle_detector.find_icon(screenshot1)
            while x3 is None:
                tapscreen_tool.tap_screen(66, 37)
                screenshot1 = screenshot_tool.capture()
                (x3, y3), conf2 = maintitle_detector.find_icon(screenshot1)
        
            print("返回主界面完成")
            time.sleep(2)


        #主页面角色互动
        self.tapscreen_tool.tap_screen(646, 409)
        time.sleep(3)
        self.tapscreen_tool.tap_screen(646, 409)
        time.sleep(3)
        self.tapscreen_tool.tap_screen(646, 409)
        
        print("主页面角色互动完成")
        time.sleep(2)
        print("开始执行领取商店随机奖励")

        #领取商店随机奖励
        
        #点击采购图标
        screenshot1 = screenshot_tool.capture()
        (x1, y1), conf1 = market_detector.find_icon(screenshot1)
        self.display_tool.show_image_with_rectangle(screenshot1, (x1, y1), (x1+10, y1+10))
        tapscreen_tool.tap_screen(x1, y1)
        time.sleep(3)

        #检测是否已经处于采购界面
        screenshot1 = screenshot_tool.capture()
        (x2, y2), conf2 = marketpagecheak_detector.find_icon(screenshot1)
        while x2 is None:
            print("正在等待进入采购界面...")
            time.sleep(1)
            screenshot1 = screenshot_tool.capture()
            (x2, y2), conf2 = marketpagecheak_detector.find_icon(screenshot1)
        

        #点击领取随机奖励
        tapscreen_tool.tap_screen(73, 636)
        time.sleep(1)
        tapscreen_tool.tap_screen(73, 636)
        time.sleep(1)
        print("领取商店随机奖励完成")

        #返回主页面
        Back2maintitle()
        
        time.sleep(2)

        #委托派遣
        print("开始执行委托派遣")
        screenshot1 = screenshot_tool.capture()
        (x4, y4), conf2 = commission_detector.find_icon(screenshot1)
        tapscreen_tool.tap_screen(x4, y4)
        time.sleep(3)
        screenshot1 = screenshot_tool.capture()
        (x5, y5), conf2 = commissionpagecheak_detector.find_icon(screenshot1)

        while x5 is None:
            tapscreen_tool.tap_screen(x4, y4)
            time.sleep(1)
            screenshot1 = screenshot_tool.capture()
            (x5, y5), conf2 = commissionpagecheak_detector.find_icon(screenshot1)
        
        screenshot1 = screenshot_tool.capture()
        (xa, ya), conf2 = iscommission_detector.find_icon(screenshot1)

        if xa:
            print("已进入委托派遣界面")
            tapscreen_tool.tap_screen(1161, 632)
            time.sleep(4)
            tapscreen_tool.tap_screen(1161, 632)
            time.sleep(1)
            tapscreen_tool.tap_screen(68, 49)

            #一键再次派遣
            screenshot1 = screenshot_tool.capture()
            (x6, y6), conf2 = commissionagain_detector.find_icon(screenshot1)
            while x6 is None:
                tapscreen_tool.tap_screen(68, 49)
                time.sleep(1)
                screenshot1 = screenshot_tool.capture()
                (x6, y6), conf2 = commissionagain_detector.find_icon(screenshot1)
            
            tapscreen_tool.tap_screen(x6, y6)

            time.sleep(1)
            Back2maintitle()


        else:
            print("委托任务未完成或没有开始委托")
            Back2maintitle()


        time.sleep(2)
        #赠送礼物
        print("开始执行赠送礼物")
        tapscreen_tool.tap_screen(1044, 123)
        time.sleep(3)
        screenshot1 = screenshot_tool.capture()
        (x7, y7), conf2 = giftpagecheak_detector.find_icon(screenshot1)
        while x7 is None:
            tapscreen_tool.tap_screen(1044, 123)
            time.sleep(1)
            screenshot1 = screenshot_tool.capture()
            (x7, y7), conf2 = giftpagecheak_detector.find_icon(screenshot1)

        print("已进入赠送礼物界面")
        tapscreen_tool.tap_screen(398, 665)
        time.sleep(1)
        tapscreen_tool.tap_screen(398, 665)
        time.sleep(1)
        tapscreen_tool.tap_screen(398, 665)


        tapscreen_tool.tap_screen(690, 321)
        time.sleep(1)
        tapscreen_tool.tap_screen(898, 644)
        time.sleep(1)
        tapscreen_tool.tap_screen(898, 644)
        time.sleep(1)
        tapscreen_tool.tap_screen(898, 644)
        time.sleep(1)

        #返回主页面
        tapscreen_tool.tap_screen(1220, 49)
        time.sleep(2)
        screenshot1 = screenshot_tool.capture()
        (x8, y8), conf2 = maintitle_detector.find_icon(screenshot1)
        while x8 is None:
            tapscreen_tool.tap_screen(1220, 49)
            time.sleep(2)
            screenshot1 = screenshot_tool.capture()
            (x8, y8), conf2 = maintitle_detector.find_icon(screenshot1)
        
        print("返回主界面完成")



        #秘纹升级
        print("开始执行秘纹升级")
        tapscreen_tool.tap_screen(1125, 535)
        time.sleep(3)
        screenshot1 = screenshot_tool.capture()
        (x9, y9), conf2 = cardpagecheak_detector.find_icon(screenshot1)
        while x9 is None:
            tapscreen_tool.tap_screen(1125, 535)
            time.sleep(1)
            screenshot1 = screenshot_tool.capture()
            (x9, y9), conf2 = cardpagecheak_detector.find_icon(screenshot1)
        
        print("已进入秘纹升级界面")
        #滑动至页面底部
        screenshot_before_swipe = screenshot1
        slide_tool.swipe_up(1000)
        time.sleep(1)
        screenshot_after_swipe = screenshot_tool.capture()

        #判断否是已经滑动到页面底部
        while self.screenshots_almost_same(screenshot_before_swipe, screenshot_after_swipe) is False:
            print("继续滑动")
            screenshot_before_swipe = screenshot_after_swipe
            slide_tool.swipe_up(1000)
            time.sleep(1)
            screenshot_after_swipe = screenshot_tool.capture()
        print("已滑动至页面底部")
        time.sleep(1)

        #选取左下角秘闻进行升级
        tapscreen_tool.tap_screen(191, 562)
        time.sleep(1)
        tapscreen_tool.tap_screen(191, 562)
        time.sleep(1)
        tapscreen_tool.tap_screen(191, 562)
        time.sleep(1)
        tapscreen_tool.tap_screen(568, 661)
        time.sleep(1)
        tapscreen_tool.tap_screen(568, 661)
        time.sleep(1)
        tapscreen_tool.tap_screen(568, 661)
        time.sleep(1)
        tapscreen_tool.tap_screen(921, 469)
        time.sleep(1)
        tapscreen_tool.tap_screen(1008, 548)
        time.sleep(1)
        tapscreen_tool.tap_screen(1008, 548)
        time.sleep(1)
        tapscreen_tool.tap_screen(1008, 548)
        time.sleep(1)
        tapscreen_tool.tap_screen(1008, 548)
        time.sleep(1)
        print("秘纹升级完成")

        Back2maintitle()
        time.sleep(2)

        #开始执行旅人升级
        print("开始执行旅人升级")
        tapscreen_tool.tap_screen(1039, 561)   
        time.sleep(3)
        screenshot1 = screenshot_tool.capture()
        (x10, y10), conf2 = characterpagecheak_detector.find_icon(screenshot1)
        while x10 is None:
            tapscreen_tool.tap_screen(1039, 561)
            time.sleep(1)
            screenshot1 = screenshot_tool.capture()
            (x10, y10), conf2 = characterpagecheak_detector.find_icon(screenshot1)

        print("已进入旅人升级界面")


        #滑动至页面底部
        screenshot_before_swipe = screenshot1
        slide_tool.swipe_up(1000)
        time.sleep(1)
        screenshot_after_swipe = screenshot_tool.capture()

        #判断否是已经滑动到页面底部
        while self.screenshots_almost_same(screenshot_before_swipe, screenshot_after_swipe) is False:
            print("继续滑动")
            screenshot_before_swipe = screenshot_after_swipe
            slide_tool.swipe_up(1000)
            time.sleep(1)
            screenshot_after_swipe = screenshot_tool.capture()
        print("已滑动至页面底部")
        time.sleep(1)

        tapscreen_tool.tap_screen(173, 551)
        time.sleep(1)
        tapscreen_tool.tap_screen(173, 551)
        time.sleep(1)
        tapscreen_tool.tap_screen(173, 551)
        time.sleep(1)
        tapscreen_tool.tap_screen(1110, 522)
        time.sleep(1)
        screenshot1 = screenshot_tool.capture()
        (x11, y11), conf2 = characterupgradepagecheak_detector.find_icon(screenshot1)
        while x11 is None:
            print("旅人升级界面未加载完成，继续点击升级按钮")
            time.sleep(1)
            tapscreen_tool.tap_screen(1110, 522)
            time.sleep(1)
            screenshot1 = screenshot_tool.capture()
            (x11, y11), conf2 = characterupgradepagecheak_detector.find_icon(screenshot1)
        
        
        tapscreen_tool.tap_screen(x11, y11)
        time.sleep(1)
        tapscreen_tool.tap_screen(1028, 590)
        time.sleep(1)
        tapscreen_tool.tap_screen(1028, 590)
        time.sleep(1)
        tapscreen_tool.tap_screen(1028, 590)
        time.sleep(1)

        print("旅人升级完成")


        Back2maintitle()
        time.sleep(2)


        #领取奖励
        









        




        




        










        










    
        