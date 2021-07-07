# _*_ coding:UTF-8 _*_  

import pythoncom, PyHook3, ctypes, _thread
from threading import Thread
import time


class pyhk:
    """Hotkey class extending PyHook3"""

    def __init__(self):
        # initiate internal hotkey list
        self.KeyDownID = []
        self.KeyDown = []

        # initiate user hotkey list
        self.UserHKF = []
        self.UserHKFUp = []
        self.HKFIDDict = {}

        # create Lookup for event keys and ids
        # for keyboards
        self.ID2Key, self.Key2ID = self.createKeyLookup()
        
        
        # for mouse, artifical lookup first
        #self.mouseDown_MID2eventMessage, self.mouseDown_eventMessage2MID, self.mouseUp_MID2eventMessage, self.mouseUp_eventMessage2MID = self.createMouseLookup()

        # create list for singleEvent, ie there is only a key down, no key up
        #self.singleEventMouseMessage, self.singleEventMID = self.createSingleEventMouse()

        # creat list for merged keys like Ctrl <= Lcontrol, Rcontrol
        

        self.KeyID2MEID = self.createMergeKeys()

        # create a hook manager
        self.hm = PyHook3.HookManager()

        # watch for all keyboard events
        self.hm.KeyDown = self.OnKeyDown
        self.hm.KeyUp = self.OnKeyUp

        # watch for all mouse events
        self.hm.MouseAllButtonsDown = self.OnKeyDown
        self.hm.MouseAllButtonsUp = self.OnKeyUp

        self.hm.MouseMove = self.OnSingleEventMouse
        self.hm.MouseWheel = self.OnSingleEventMouse

        # set the hook
        self.hm.HookKeyboard()
        #self.hm.HookMouse()

        # set Ending hotkey
        self.EndHotkey = ['Ctrl', 'Shift', 'Q']
        self.setEndHotkey(self.EndHotkey)

    def start(self):
        """Start pyhk to check for hotkeys"""
        while True :
            pythoncom.PumpMessages()


    def end(self):
        """End pyhk to check for hotkeys"""
        ctypes.windll.user32.PostQuitMessage(0)

    # --------------------------------------------------------

    def isIDHotkey(self, hotkey):
        """Test if hotkey is coded in IDs"""
        for key in hotkey:
            if type(key) == str:
                return False
        return True

    def isHumanHotkey(self, hotkey):
        """Test if hotkey is coded human readable. Ex ALT F2"""
        try:
            [self.Key2ID[key] for key in hotkey]
        except:
            return False
        return True

    def hotkey2ID(self, hotkey):
        """Converts human readable hotkeys to IDs"""
        if self.isHumanHotkey(hotkey):
            return [self.Key2ID[key] for key in hotkey]
        else:
            raise Exception("Invalid Hotkey")

    def getHotkeyList(self, hotkey):
        """Create a IDlist of hotkeys if necessary to ensure functionality of merged hotkeys"""
        hotkeyVariationList = []
        hotkeyList = []

        # convert everyting into ID,MID,MEID
        if self.isIDHotkey(hotkey):
            IDHotkey = hotkey
        else:
            IDHotkey = self.hotkey2ID(hotkey)

        IDHotkeyTemp = IDHotkey[:]

        # check if there is a MEID and create accorind hotkeyVariationList
        for Key in self.KeyID2MEID:

            if self.KeyID2MEID[Key] in IDHotkeyTemp:
                # merged hotkey in hotkey
                # get MEID
                MEIDTemp = self.KeyID2MEID[Key]
                # get all KeyIDs
                KeyIDVariationTemp = [k for k in self.KeyID2MEID if self.KeyID2MEID[k] == MEIDTemp]

                # remove MEID from IDHotekey
                IDHotkeyTemp.remove(MEIDTemp)

                # store according MEID and KeyIDList
                hotkeyVariationList.append(KeyIDVariationTemp)

        if len(hotkeyVariationList) > 0:
            hotkeyVariationList.append(IDHotkeyTemp)
            # get all possible permutations
            hotkeyList = UniquePermutation(hotkeyVariationList)
        else:
            hotkeyList = [IDHotkey]

        return hotkeyList

    def addHotkey(self, hotkey, fhot, isThread=False, up=False):
        """Add hotkeys with according function"""
        hotkeyList = self.getHotkeyList(hotkey)

        newHKFID = self.getNewHKFID()
        self.HKFIDDict[newHKFID] = []

        if up:

            if len(hotkey) < 2:
                if isThread:
                    t = ExecFunThread(fhot)
                    for IDHotKeyItem in hotkeyList:
                        self.UserHKFUp.append([IDHotKeyItem, t.Start])
                        self.HKFIDDict[newHKFID].append([IDHotKeyItem, t.Start])

                else:
                    for IDHotKeyItem in hotkeyList:
                        self.UserHKFUp.append([IDHotKeyItem, fhot])
                        self.HKFIDDict[newHKFID].append([IDHotKeyItem, fhot])

        else:

            if isThread:
                t = ExecFunThread(fhot)
                for IDHotKeyItem in hotkeyList:
                    self.UserHKF.append([IDHotKeyItem, t.Start])
                    self.HKFIDDict[newHKFID].append([IDHotKeyItem, t.Start])

            else:
                for IDHotKeyItem in hotkeyList:
                    self.UserHKF.append([IDHotKeyItem, fhot])
                    self.HKFIDDict[newHKFID].append([IDHotKeyItem, fhot])

        return newHKFID

    def removeHotkey(self, hotkey=False, id=False):
        """Remove hotkeys and corresponding function"""
        HKFID = id
        try:
            if hotkey:
                hotkeyList = self.getHotkeyList(hotkey)
                try:
                    UserHKFTemp = [[hotk, fun] for hotk, fun in self.UserHKF if not (hotk in hotkeyList)]
                    self.UserHKF = UserHKFTemp[:]
                except:
                    pass
                try:
                    UserHKFTemp = [[hotk, fun] for hotk, fun in self.UserHKFUp if not (hotk in hotkeyList)]
                    self.UserHKFUp = UserHKFTemp[:]
                except:
                    pass
            elif HKFID:
                for item in self.HKFIDDict[HKFID]:
                    try:
                        self.UserHKF.remove(item)
                    except:
                        self.UserHKFUp.remove(item)
                self.HKFIDDict.pop(HKFID)
            else:
                self.UserHKF = []
                self.UserHKFUp = []
        except:
            pass

    def setEndHotkey(self, hotkey):
        """Add exit hotkeys"""
        self.removeHotkey(self.EndHotkey)
        self.EndHotkey = hotkey
        self.addHotkey(hotkey, self.end)

    # --------------------------------------------------------
    # ID functions for HKFID
    def getNewHKFID(self):
        try:
            return max(self.HKFIDDict.keys()) + 1
        except:
            return 1

    # --------------------------------------------------------

    def isHotkey(self, hotkey):
        """Check if hotkey is pressed down
            Hotkey is given as KeyID"""

        try:
            # make sure exact hotkey is pressed
            if not (len(hotkey) == len(self.KeyDownID)):
                return False
            for hotk in hotkey:
                if not (hotk in self.KeyDownID):
                    return False
        except:
            return False

        return True

    def OnKeyDown(self, event):

        if not "mouse" in event.MessageName:
            # check for merged keys first
            eventID = event.KeyID
        else:
            eventID = self.mouseDown_eventMessage2MID[event.Message]

        # make sure key only gets presse once
        if not (eventID in self.KeyDownID):

            self.KeyDownID.append(eventID)

            # Add user hotkeys and functions
            for hk, fun in self.UserHKF:
                if self.isHotkey(hk):
                    fun()

        return True

    def OnKeyUp(self, event):

        if not "mouse" in event.MessageName:
            eventID = event.KeyID
        else:
            eventID = self.mouseUp_eventMessage2MID[event.Message]

        # check for hotkey up keys
        for hk, fun in self.UserHKFUp:
            if hk[0] == eventID:
                fun()

        try:
            self.KeyDownID.remove(eventID)

        except:
            pass
        return True

    def OnSingleEventMouse(self, event):
        """Function to excetue single mouse events"""

        if event.Message in self.singleEventMouseMessage:
            # test for mouse wheel:
            if event.Message == 522:
                if event.Wheel == 1:
                    eventID = 1004
                else:
                    eventID = 1005
            # test mouse move
            elif event.Message == 512:
                eventID = 1000
            else:
                return False

            self.KeyDownID.append(eventID)

            # Add user hotkeys and functions
            for hk, fun in self.UserHKF:
                if self.isHotkey(hk):
                    fun()

            self.KeyDownID.remove(eventID)

        return True

    # --------------------------------------------------------

    def createKeyLookup(self):
        """Creates Key look up dictionaries, change names as you please"""
        ID2Key = {8: 'Back',
                  9: 'Tab',
                  13: 'Return',
                  20: 'Capital',
                  27: 'Escape',
                  32: 'Space',
                  33: 'Prior',
                  34: 'Next',
                  35: 'End',
                  36: 'Home',
                  37: 'Left',
                  38: 'Up',
                  39: 'Right',
                  40: 'Down',
                  44: 'Snapshot',
                  46: 'Delete',
                  48: '0',
                  49: '1',
                  50: '2',
                  51: '3',
                  52: '4',
                  53: '5',
                  54: '6',
                  55: '7',
                  56: '8',
                  57: '9',
                  65: 'A',
                  66: 'B',
                  67: 'C',
                  68: 'D',
                  69: 'E',
                  70: 'F',
                  71: 'G',
                  72: 'H',
                  73: 'I',
                  74: 'J',
                  75: 'K',
                  76: 'L',
                  77: 'M',
                  78: 'N',
                  79: 'O',
                  80: 'P',
                  81: 'Q',
                  82: 'R',
                  83: 'S',
                  84: 'T',
                  85: 'U',
                  86: 'V',
                  87: 'W',
                  88: 'X',
                  89: 'Y',
                  90: 'Z',
                  91: 'Lwin',
                  96: 'Numpad0',
                  97: 'Numpad1',
                  98: 'Numpad2',
                  99: 'Numpad3',
                  100: 'Numpad4',
                  101: 'Numpad5',
                  102: 'Numpad6',
                  103: 'Numpad7',
                  104: 'Numpad8',
                  105: 'Numpad9',
                  106: 'Multiply',
                  107: 'Add',
                  109: 'Subtract',
                  110: 'Decimal',
                  111: 'Divide',
                  112: 'F1',
                  113: 'F2',
                  114: 'F3',
                  115: 'F4',
                  116: 'F5',
                  117: 'F6',
                  118: 'F7',
                  119: 'F8',
                  120: 'F9',
                  121: 'F10',
                  122: 'F11',
                  123: 'F12',
                  144: 'Numlock',
                  160: 'Lshift',
                  161: 'Rshift',
                  162: 'Lcontrol',
                  163: 'Rcontrol',
                  164: 'Lmenu',
                  165: 'Rmenu',
                  186: 'Oem_1',
                  187: 'Oem_Plus',
                  188: 'Oem_Comma',
                  189: 'Oem_Minus',
                  190: 'Oem_Period',
                  191: 'Oem_2',
                  192: 'Oem_3',
                  219: 'Oem_4',
                  220: 'Oem_5',
                  221: 'Oem_6',
                  222: 'Oem_7',
                  1010: 'Ctrl',  # merged hotkeys
                  1011: 'Alt',
                  1012: 'Shift'}

        Key2ID = dict(map(lambda x, y: (x, y), ID2Key.values(), ID2Key.keys()))

        return ID2Key, Key2ID

    def createMouseLookup(self):
        """Takes a event.Message from mouse and converts it to artificial KeyID"""
        mouseDown_MID2eventMessage = {
            1001: 513,
            1002: 516,
            1003: 519}
        mouseDown_eventMessage2MID = dict(
            map(lambda x, y: (x, y), mouseDown_MID2eventMessage.values(), mouseDown_MID2eventMessage.keys()))

        mouseUp_MID2eventMessage = {
            1001: 514,
            1002: 517,
            1003: 520}
        mouseUp_eventMessage2MID = dict(
            map(lambda x, y: (x, y), mouseUp_MID2eventMessage.values(), mouseUp_MID2eventMessage.keys()))

        return mouseDown_MID2eventMessage, mouseDown_eventMessage2MID, mouseUp_MID2eventMessage, mouseUp_eventMessage2MID

    def createSingleEventMouse(self):
        """Store events that get executed on single event like wheel up
        MID   event.Message    pyhk hotkey      comments
        1000  512              mouse move
        1004  522              mouse wheel up   event.Wheel = 1
        1005  522              mouse wheel up   event.Wheel = 1"""

        singleEventMouseMessage = [512, 522]
        singleEventMID = [1000, 1004, 1005]

        return singleEventMouseMessage, singleEventMID

    def createMergeKeys(self):
        """Merge two keys into one
        KeyID   MEID    MergeHumanHotkey
        162     1010     Ctrl  (Lcontrol)
        163     1010     Ctrl  (Rcontrol
        164     1011     Alt   (Lmenu)
        165     1011     Alt   (Rmenu)
        160     1012     Shift (Lshift)
        161     1012     Shift (Rshift)"""

        KeyID2MEID = {162: 1010,
                      163: 1010,
                      164: 1011,
                      165: 1011,
                      160: 1012,
                      161: 1012}
        return KeyID2MEID

    def getHotkeyListNoSingleNoModifiers(self):
        """return a list of all hotkeys without single events and modifiers"""
        TempID2Key = self.ID2Key.copy()

        # get rid of single events and modifiers
        getRid = [160, 161, 162, 163, 164, 165, 1000, 1004, 1005, 1010, 1011, 1012]

        # get rid of Lwin and oems
        moreRid = [91, 186, 187, 188, 189, 190, 191, 192, 219, 220, 221, 222]

        for item in moreRid:
            getRid.append(item)

        for gR in getRid:
            TempID2Key.pop(gR)

        LTempID2Key = TempID2Key.values()

        return LTempID2Key


# permutation functions needed for merged hotkeys
def UniquePermutation2(l1, l2):
    """"Return UP of two lists"""
    ltemp = []
    for x1 in l1:
        for x2 in l2:
            ltemp.append([x1, x2])

    return ltemp


def UniquePermutation(li):
    """Return UP of a general list"""
    lcurrent = li[0]
    depth = 0
    for xl in li[1:]:
        lcurrenttemp = list()
        lcurrenttemp = UniquePermutation2(lcurrent, xl)

        if depth > 0:
            lcurrent = list()
            for item in lcurrenttemp:
                item0 = list(item[0])
                item0.append(item[1])
                lcurrent.append(item0)
        else:
            lcurrent = lcurrenttemp[:]
        depth += 1
    return lcurrent


# class for thread
class ExecFunThread:
    def __init__(self, fun):
        self.fun = fun

    def Start(self):
        self.running = True
        _thread.start_new_thread(self.Run, ())

    def IsRunning(self):
        return self.running

    def Run(self):
        self.fun()
        self.running = False


def test1():

    print("按下了F2")


def test2():

    print("按下了F3")
    #hot.removeHotkey(id=id3)

def test():

    hot = pyhk()
    id1 = hot.addHotkey(["F2"], test1)
    id3 = hot.addHotkey(["F3"], test2)
    hot.start()


if __name__ == '__main__':


    thread_hotKey = Thread(target=test)
    thread_hotKey.setDaemon(True)
    thread_hotKey.start()
    while True:
        print(time.time())
        time.sleep(2)