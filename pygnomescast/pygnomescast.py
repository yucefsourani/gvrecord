#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  pygnomescast.py
#  
#  Copyright 2018 youcef sourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import dbus
import time
import subprocess
import gi
import os
import pwd
import threading
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GLib



def gnome_shell_version():
    try:
        bus         = dbus.SessionBus()
        obj         = bus.get_object("org.gnome.Shell","/org/gnome/Shell")
        intf        = dbus.Interface(obj,"org.freedesktop.DBus.Properties")
        return intf.Get("org.gnome.Shell","ShellVersion")
    except :
        return False
        
        
        
def is_gnome_shell():
    if gnome_shell_version():
        return True
    return False



def get_audio_source():
    all_    = subprocess.Popen("""pactl list | grep -A2 'Source #' | grep 'Name: ' | cut -d" " -f2""",stdout=subprocess.PIPE,shell=True).communicate()[0].decode("utf-8").strip().split("\n")
    return all_



def get_audio_source_monitor():
    monitor =  subprocess.Popen("""pactl list | grep -A2 'Source #' | grep 'Name: .*\.monitor$' | cut -d" " -f2""",stdout=subprocess.PIPE,shell=True).communicate()[0].decode("utf-8").strip().split("\n")
    return monitor

def get_window_xid(): # On Xorg Only
    time.sleep(sl)
    d = Gdk.Display().get_default()
    dv=d.get_device_manager()
    p=dv.get_client_pointer()
    return p.get_window_at_position()[0].get_xid()



class MonitorInfo(object):
    def __init__(self,monitor):
        self.monitor   = monitor
        self.x         = self.monitor.get_geometry().x
        self.y         = self.monitor.get_geometry().y
        self.width     = self.monitor.get_geometry().width
        self.height    = self.monitor.get_geometry().height
        self.info      = {"monitor":self.monitor,"x":self.x,"y":self.y,"width":self.width,"height":self.height}
        
        
        
class ScreenInfo(object):
    def __init__(self,screen):
        self.screen    = screen
        self.width     = self.screen.get_width()
        self.height    = self.screen.get_height()
        self.info      = {"screen":self.screen,"width":self.width,"height":self.height}
        
        
        
class MonitorScreenInfo(object):
    display         = Gdk.Display().get_default()
    
    @staticmethod
    def get_default_display():
        return MonitorScreenInfo.display
    
    @staticmethod
    def get_screens_number():
        return MonitorScreenInfo.display.get_n_screens()
        
    @staticmethod
    def get_screens():
        display       = MonitorScreenInfo.display
        screen_number = display.get_n_screens()
        return [ScreenInfo(display.get_screen(screennumber)) for screennumber in range(screen_number) ]
        
    @staticmethod
    def get_monitors_number():
        return MonitorScreenInfo.display.get_n_monitors()
        
    @staticmethod
    def get_monitors():
        display        = MonitorScreenInfo.display
        monitor_number = display.get_n_monitors()
        return [MonitorInfo(display.get_monitor(monitornumber)) for monitornumber in range(monitor_number) ]
        


class Screencast(object):
    def __init__(self,file_template="Record-%d-%t",draw_cursor="true",\
                framerate="30",\
                pipeline="vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux"):
                    
        self.bus           = dbus.SessionBus()
        self.__obj         = self.bus.get_object("org.gnome.Shell.Screencast","/org/gnome/Shell/Screencast")
        self.__intf        = dbus.Interface(self.__obj,"org.gnome.Shell.Screencast")
        
        self.file_template = file_template
        self.draw_cursor   = draw_cursor
        self.framerate     = framerate
        self.pipeline      = pipeline
        
    def start(self):
        return self.__intf.Screencast(self.file_template,\
                                     {"draw-cursor":self.draw_cursor,"framerate":self.framerate,"pipeline":self.pipeline})
        
    def stop(self):
        return self.__intf.StopScreencast()
        
    

        
class ScreencastArea(object):
    def __init__(self,x,y,width,height,file_template="Record-%d-%t",\
                 draw_cursor="true",framerate="30",\
                 pipeline="vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux"):
        self.bus           = dbus.SessionBus()
        self.__obj         = self.bus.get_object("org.gnome.Shell.Screencast","/org/gnome/Shell/Screencast")
        self.__intf        = dbus.Interface(self.__obj,"org.gnome.Shell.Screencast")
        
        self.x             = x
        self.y             = y
        self.width         = width
        self.height        = height
        self.file_template = file_template
        self.draw_cursor   = draw_cursor
        self.framerate     = framerate
        self.pipeline      = pipeline
        
    def start(self):
        return self.__intf.ScreencastArea(self.x,self.y,self.width,self.height,\
                                      self.file_template,\
                                      {"draw-cursor":self.draw_cursor,"framerate":self.framerate,"pipeline":self.pipeline})
        
    def stop(self):
        return self.__intf.StopScreencast()

class SelecetAreaAndRecord(object):
    def __init__(self,file_template="Record-%d-%t",\
                 draw_cursor="true",framerate="30",\
                 pipeline="vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux"):
        self.bus           = dbus.SessionBus()
        self.__obj         = self.bus.get_object("org.gnome.Shell.Screencast","/org/gnome/Shell/Screencast")
        self.__intf        = dbus.Interface(self.__obj,"org.gnome.Shell.Screencast")
        self.file_template = file_template
        self.draw_cursor   = draw_cursor
        self.framerate     = framerate
        self.pipeline      = pipeline
        
    def start(self):
        x,y,width,height = self.select_area()
        return self.__intf.ScreencastArea(x,y,width,height,\
                                      self.file_template,\
                                      {"draw-cursor":self.draw_cursor,"framerate":self.framerate,"pipeline":self.pipeline})
        
    def stop(self):
        return self.__intf.StopScreencast()
        
    def select_area(self):
        obj         = self.bus.get_object("org.gnome.Shell.Screenshot","/org/gnome/Shell/Screenshot")
        intf        = dbus.Interface(obj,"org.gnome.Shell.Screenshot")
        return intf.SelectArea()



def get_exec(file_location):
    query = subprocess.Popen("xdg-mime query filetype {}".format(file_location).split(),stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()
    desktopentry = subprocess.Popen("xdg-mime  query default {}".format(query).split(),stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()
    home = pwd.getpwuid(os.geteuid()).pw_dir
    locations = [os.path.join(home,".local/share/applications"),
                 os.path.join(home,".local/share/flatpak/exports/share/applications"),
                 "/usr/share/applications",
                 "/usr/local/share/applications",
                 "/var/lib/flatpak/exports/share/"]
    desktopentry=[os.path.join(l,desktopentry) for l in locations if os.path.isfile(os.path.join(l,desktopentry))]
    if len(desktopentry)==0:
        return False
        
    try:
        with open(desktopentry[0]) as mf:
            for line in mf:
                line=line.strip()
                if line and line.startswith("Exec"):
                    try:
                        exec__ = line.split("=")[1]
                        return exec__.split()[0]
                    except:
                        return False
    except:
        return False
    return False
    




class PlayVideo(threading.Thread):
    def __init__(self,filelocation):
        threading.Thread.__init__(self)
        self.filelocation = filelocation

    def run(self):
        if  os.path.isfile(self.filelocation):
            exec__=get_exec(self.filelocation)
            if exec__:
                os.system(exec__+" "+self.filelocation+"&")
        else:
            return False
            

class ThreadScreenCastAreaRecord(threading.Thread):
    def __init__(self,x,y,width,height,filename,options):
        threading.Thread.__init__(self)
        self.filename = filename
        self.options  = options
        self.width = int(width)
        self.height = int(height)
        self.x = int(x)
        self.y = int(y)


        
    def run(self):
        time.sleep(self.options[3]+1)
        if self.options[4]:
            self.options[5].iconify()

        GLib.idle_add(self.options[6].set_sensitive,False)
        GLib.idle_add(self.options[7].set_sensitive,True)
        GLib.idle_add(self.options[9].set_sensitive,False)
        if self.options[8]:
            subprocess.call(self.options[8],shell=True)
        screencast = ScreencastArea(self.x,self.y,self.width,self.height,self.filename[7:],\
        framerate=self.options[0],draw_cursor=self.options[1],pipeline=self.options[2])
        return  screencast.start()
       
class ThreadAudioRecord(threading.Thread):
    def __init__(self,x,y,width,height,filename,options):
        threading.Thread.__init__(self)
        self.filename = filename
        self.options  = options
        self.width = int(width)
        self.height = int(height)
        self.x = int(x)
        self.y = int(y)
        self.hw = self.options[-1]
        self.q = self.options[-2]
        
    def run(self):
        time.sleep(self.options[3]+1)
        if self.options[4]:
            self.options[5].iconify()

        GLib.idle_add(self.options[6].set_sensitive,False)
        GLib.idle_add(self.options[7].set_sensitive,True)
        GLib.idle_add(self.options[9].set_sensitive,False)
        if self.options[8]:
            subprocess.call(self.options[8],shell=True)
        p = subprocess.Popen("ffmpeg -f alsa -i {} {} -y".format(self.hw,self.filename).split())
        self.q.put(p)


class ThreadStopRecord(threading.Thread):
    def __init__(self,recordbutton,stopbutton,command,isopenlocation,locations,playbutton,checkplay):
        threading.Thread.__init__(self)
        self.recordbutton = recordbutton
        self.stopbutton = stopbutton
        self.command = command
        self.isopenlocation = isopenlocation
        self.locations = locations
        self.playbutton = playbutton
        self.checkplay = checkplay

    def run(self):
        bus = dbus.SessionBus()
        object_ = bus.get_object("org.gnome.Shell.Screencast", "/org/gnome/Shell/Screencast")
        GLib.idle_add(self.stopbutton.set_sensitive,False)
        GLib.idle_add(self.recordbutton.set_sensitive,True)
        GLib.idle_add(self.playbutton.set_sensitive,True)
        if self.command:
            subprocess.call(self.command,shell=True)
        object_.get_dbus_method("StopScreencast",dbus_interface="org.gnome.Shell.Screencast")()
        if self.isopenlocation:
            location = os.path.dirname(self.locations)
            exec__=get_exec(location)
            if exec__:
                os.system(exec__+" "+location+"&")
            #subprocess.call("/usr/bin/xdg-open {}/".format(location).split())
        if self.checkplay:
            exec__=get_exec(self.locations)
            if exec__:
                os.system(exec__+" "+self.locations+"&")

