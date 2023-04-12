#!/usr/bin/env python3
import sys
sys.path.append('/opt/managementagent/utils')
import os
from logs import log

def no_of_argv(args):
    return(len(args))


def main():
    if no_of_argv(sys.argv) < 5:
        log.error("The number of arguments are less than four")
        # validate required 4 arguments  : x and y co-ordinate where touch action fired with image height and width
        return 0
    endX = int(sys.argv[1])
    endY = int(sys.argv[2])
    imgHeight = int(sys.argv[3])
    imageWidth = int(sys.argv[4])
    IXNTOUCH_WIDTH = 9600
    IXNTOUCH_HEIGHT = 16384
    GDS_IXNTOUCH_WIDTH = 2250
    GDS_IXNTOUCH_HEIGHT = 4000
    CONCIERGE_IXNTOUCH = 32767

    try:
        if os.popen("find /dev/input/by-id -name usb-DISPLAX_SKIN_FIT*-event-if00").read():
            MANUFACTURER = "GDS"
            INPUT_DEVICE = os.popen(
                "find /dev/input/by-id -name usb-DISPLAX_SKIN_FIT*-event-if00").read()
        elif os.popen("find /dev/input/by-id -name usb-ILITEK_Multi-Touch-V*-event-if00").read():
            MANUFACTURER = "LG-MRI"
            INPUT_DEVICE = os.popen(
                "find /dev/input/by-id -name usb-ILITEK_Multi-Touch-V*-event-if00").read()
        elif os.popen("find /dev/input/by-id -name usb-SigmaSense_SigmaSense_Digitizer_*-event-if00").read():
            MANUFACTURER = "SigmaSense"
            INPUT_DEVICE = os.popen(
                "find /dev/input/by-id -name usb-SigmaSense_SigmaSense_Digitizer_*-event-if00").read()
        elif os.popen("find /dev/input/by-id -name usb-3M_3M_MicroTouch_USB_controller*-event-if00").read():
            MANUFACTURER = "3M_Microtouch"
            SCREEN_SIZE = os.popen(
                "xrandr -d :0 | awk / connected/{print sqrt( ($(NF-2))^2 + ($NF)^2 )/25.4}").read()
            #To get Display information to set 0 screen abstraction and counting field to detect screen size.
            INPUT_DEVICE = os.popen(
                "find /dev/input/by-id -name usb-3M_3M_MicroTouch_USB_controller*-event-if00").read()
        else:
            log.error("Unable to identify the touch device")
            return 1

        if MANUFACTURER == "GDS":
            IXNTOUCH_WIDTH = GDS_IXNTOUCH_WIDTH
            IXNTOUCH_HEIGHT = GDS_IXNTOUCH_HEIGHT

        if MANUFACTURER == "3M_Microtouch":
            IXNTOUCH_WIDTH = CONCIERGE_IXNTOUCH
            IXNTOUCH_HEIGHT = CONCIERGE_IXNTOUCH

        #to support hy indoor 55" (portrait). imgResolution: 868 * 1543.11 for GDS
        if MANUFACTURER == "GDS" and imgHeight > 1000:
            convertedX = endY*IXNTOUCH_HEIGHT/imgHeight
            GDSTOUCH = endX*IXNTOUCH_WIDTH/imageWidth
            convertedY = IXNTOUCH_WIDTH-GDSTOUCH

        #For GDS & Concierge large screens of HY
        elif MANUFACTURER == "3M_Microtouch" and imgHeight > 1000:
            convertedX = endY*IXNTOUCH_HEIGHT/imgHeight
            NECTOUCH = endX*IXNTOUCH_WIDTH/imageWidth
            convertedY = IXNTOUCH_WIDTH-NECTOUCH
        #For Concierge small screens of HY
        # to support hy outdoor 40" (landscape). imgResolution: 1920x1080
        elif MANUFACTURER == "3M_Microtouch" and imgHeight < 1001:
            convertedX = endX*IXNTOUCH_HEIGHT/imageWidth
            convertedY = endY*IXNTOUCH_WIDTH/imgHeight

        elif imgHeight > 1500 and not ("$MANUFACTURER" == 'GDS' or "$MANUFACTURER" == '3M_Microtouch'):
            ALLTOUCHDISPLAY = endY*IXNTOUCH_HEIGHT/imgHeight
            convertedX = IXNTOUCH_HEIGHT-ALLTOUCHDISPLAY
            convertedY = endX*IXNTOUCH_WIDTH/imageWidth

        #to support hy outdoor 32" (landscape). imgResolution: 868 * 488.25
        else:
            convertedX = endX*IXNTOUCH_HEIGHT/imageWidth
            convertedY = endY*IXNTOUCH_WIDTH/imgHeight

        if convertedX and convertedX > 0:
            if (convertedX < 0 or convertedX > 16384) and MANUFACTURER == "LG-MRI":
                log.error("Usage: x_position should be in a range of 0 to 16384")
                return 1
            elif (convertedX < 0 or convertedX > 4000) and MANUFACTURER == "GDS":
                log.error("Usage: x_position should be in range of 0 to 4000")
                return 1
            elif (convertedX < 0 or convertedX > 16510) and MANUFACTURER == "SigmaSense":
                log.error("Usage: x_position should be in range of 0 to 16510")
                return 1
            elif (convertedX < 0 or convertedX > 32767) and MANUFACTURER == "3M_Microtouch":
                log.error("Usage: x_position should be in range of 0 to 32767")
                return 1
            elif convertedX < 10:
                x_position = "000" + str(convertedX)
            elif convertedX < 100:
                x_position = "00" + str(convertedX)
            elif convertedX < 1000:
                x_position = "0" + str(convertedX)
            else:
                x_position = str(round(convertedX))
        else:
            log.error("Usage: x_position is not a positive decimal integer number")
            return 1
        if convertedY and convertedY > 0:
            if (convertedY < 0 or convertedY > 9600) and MANUFACTURER == "LG-MRI":
                log.error("Usage: {y_position} should be in a range of 0 to 9600")
                return 1
            elif (convertedY < 0 or convertedY > 2250) and MANUFACTURER == "GDS":
                log.error("Usage: {y_position} should be in a range of 0 to 2250")
                return 1
            elif (convertedY < 0 or convertedY > 9250) and MANUFACTURER == "SigmaSense":
                log.error("Usage: {y_position} should be in a range of 0 to 9250")

                return 1
            elif (convertedY < 0 or convertedY > 32767) and MANUFACTURER == "3M_Microtouch":
                log.error("Usage: {y_position} should be in a range of 0 to 32767")
                return 1
            elif convertedY < 10:
                y_position = "000" + str(convertedY)
            elif convertedY < 100:
                y_position = "00" + str(convertedY)
            elif convertedY < 1000:
                y_position = "0" + str(convertedY)
            else:
                y_position = str(round(convertedY)+1)
        else:
            return 1

        if MANUFACTURER == "GDS":
            touch_event_template_header = "/opt/managementagent/touchEvent/template/touch-event-template-header-gds"
            touch_event_template_body = "/opt/managementagent/touchEvent/template/touch-event-template-body-gds"
        elif MANUFACTURER == "LG-MRI":
            touch_event_template_header = "/opt/managementagent/touchEvent/template/touch-event-template-header-mri"
            touch_event_template_body = "/opt/managementagent/touchEvent/template/touch-event-template-body-mri"
        elif MANUFACTURER == "SigmaSense":
            touch_event_template_header = "/opt/managementagent/touchEvent/template/touch-event-template-header-sigma-sense"
            touch_event_template_body = "/opt/managementagent/touchEvent/template/touch-event-template-body-sigma-sense"
        elif MANUFACTURER == "3M_Microtouch" and SCREEN_SIZE < 55:
            touch_event_template_header = "/opt/managementagent/touchEvent/template/touch-event-template-header-concierge-small"
            touch_event_template_body = "/opt/managementagent/touchEvent/template/touch-event-template-body-concierge-small"
        elif MANUFACTURER == "3M_Microtouch":
            touch_event_template_header = "/opt/managementagent/touchEvent/template/touch-event-template-header-concierge-large"
            touch_event_template_body = "/opt/managementagent/touchEvent/template/touch-event-template-body-concierge-large"

        event_output = "better-touch-event-file"
        temporary_file = "temporary_file"

        if os.path.isfile("better-touch-event-file"):
            os.popen("rm better-touch-event-file")

        if os.path.isfile("temporary_file"):
            os.popen("rm temporary_file")

        codefiled = "E: 0.000000 0003 0039 0045      # EV_ABS / ABS_MT_TRACKING_ID  45\n\
E: 0.000000 0003 0035 " + x_position + "       # EV_ABS / ABS_MT_POSITION_X    $x_position\n\
E: 0.000000 0003 0036 " + y_position + "       # EV_ABS / ABS_MT_POSITION_Y    $y_position\n\
E: 0.000000 0001 014a 0001      # EV_KEY / BTN_TOUCH            1\n\
E: 0.000000 0003 0000 " + x_position + "       # EV_ABS / ABS_X                $x_position\n\
E: 0.000000 0003 0001 " + y_position + "      # EV_ABS / ABS_Y                $y_position"


        with open("temporary_file","a+") as f:
            f.write(codefiled)
        with open("/dev/null","a+") as f1:
            f1.write(codefiled)


        # create an completed event file
        os.popen("cat " + touch_event_template_header + " > " + event_output)
        os.popen("cat " + temporary_file + " >> " + event_output)
        os.popen("cat " + touch_event_template_body + " >> " + event_output)

        if os.path.isfile(not event_output):
            log.error("No touch event exists")
            return 1

        if os.path.isfile(not INPUT_DEVICE):
            log.error("Unable to find input device for: {} ".format(MANUFACTURER))
            return 1
        else:
            touchCommand ="evemu-play " + INPUT_DEVICE.strip('\n') + " < " + event_output
            os.popen(touchCommand)

        log.info("Success")

        os.popen("rm " + event_output)
        os.popen("rm " + temporary_file)
        print("sucess")

    except Exception as e:
        log.error("Unable to exicute Touch Event: {} ".format(e))


if __name__ == '__main__':
    main()
