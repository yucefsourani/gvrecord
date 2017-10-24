#!/usr/bin/python3
# -*- coding: utf-8 -*-
# TO DO
# icon
# audio
# config
import sys
import dbus
import json
import time
import subprocess
import os
import pwd
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, GdkPixbuf



bus = dbus.SessionBus()

MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""

css = b"""
#AreaChooser {
    background-color: rgba(255, 255, 255, 0);
    border: 1px solid red;
}
"""



#PipeLine From EasyScreenCast extention
gnome_wayland_pipeline = {   "mp41"   : [".mp4", "Mp4 x264 encoder (Quality L1)",  "x264enc psy-tune=\"none\" speed-preset=\"superfast\" subme=1 qp-min=28 qp-max=40 threads=%T  ! mp4mux name=mux",["/usr/lib64/gstreamer-1.0/libgstx264.so","/usr/lib/gstreamer-1.0/libgstx264.so"],["/usr/lib64/gstreamer-1.0/libgstisomp4.so","/usr/lib/gstreamer-1.0/libgstisomp4.so"]] ,
                             "mp42"   : [".mp4", "Mp4 x264 encoder (Quality L2)",  "x264enc psy-tune=\"animation\" speed-preset=\"fast\" subme=5 qp-min=18 qp-max=28 threads=%T  ! mp4mux name=mux" ,["/usr/lib64/gstreamer-1.0/libgstx264.so","/usr/lib/gstreamer-1.0/libgstx264.so"],["/usr/lib64/gstreamer-1.0/libgstisomp4.so","/usr/lib/gstreamer-1.0/libgstisomp4.so"]] ,
                             "mp43"   : [".mp4", "Mp4 x264 encoder (Quality L3)",  "x264enc psy-tune=\"animation\" speed-preset=\"medium\" subme=8 qp-min=10 qp-max=18 threads=%T  ! mp4mux name=mux",["/usr/lib64/gstreamer-1.0/libgstx264.so","/usr/lib/gstreamer-1.0/libgstx264.so"],["/usr/lib64/gstreamer-1.0/libgstisomp4.so","/usr/lib/gstreamer-1.0/libgstisomp4.so"]] ,
                             "mp44"   : [".mp4", "Mp4 x264 encoder (Quality L4)",  "x264enc psy-tune=\"film\" speed-preset=\"slower\" subme=10 qp-min=0 qp-max=10 threads=%T  ! mp4mux name=mux",["/usr/lib64/gstreamer-1.0/libgstx264.so","/usr/lib/gstreamer-1.0/libgstx264.so"],["/usr/lib64/gstreamer-1.0/libgstisomp4.so","/usr/lib/gstreamer-1.0/libgstisomp4.so"]],
                             "mkv1"   : [".mkv", "Mkv x264 encoder (Quality L1)",  "x264enc psy-tune=\"none\" speed-preset=\"superfast\" subme=1 qp-min=28 qp-max=40 threads=%T ! matroskamux name=mux",["/usr/lib64/gstreamer-1.0/libgstx264.so","/usr/lib/gstreamer-1.0/libgstx264.so"],["/usr/lib64/gstreamer-1.0/libgstmatroska.so","/usr/lib/gstreamer-1.0/libgstmatroska.so"]],
                             "mkv2"   : [".mkv", "Mkv x264 encoder (Quality L2)",  "x264enc psy-tune=\"animation\" speed-preset=\"fast\" subme=5 qp-min=18 qp-max=28 threads=%T ! matroskamux name=mux",["/usr/lib64/gstreamer-1.0/libgstx264.so","/usr/lib/gstreamer-1.0/libgstx264.so"],["/usr/lib64/gstreamer-1.0/libgstmatroska.so","/usr/lib/gstreamer-1.0/libgstmatroska.so"]],
                             "mkv3"   : [".mkv", "Mkv x264 encoder (Quality L3)",  "x264enc psy-tune=\"animation\" speed-preset=\"medium\" subme=8 qp-min=10 qp-max=18 threads=%T ! matroskamux name=mux",["/usr/lib64/gstreamer-1.0/libgstx264.so","/usr/lib/gstreamer-1.0/libgstx264.so"],["/usr/lib64/gstreamer-1.0/libgstmatroska.so","/usr/lib/gstreamer-1.0/libgstmatroska.so"]],
                             "mkv4"   : [".mkv", "Mkv x264 encoder (Quality L4)",  "x264enc psy-tune=\"film\" speed-preset=\"slower\" subme=10 qp-min=0 qp-max=10 threads=%T ! matroskamux name=mux",["/usr/lib64/gstreamer-1.0/libgstx264.so","/usr/lib/gstreamer-1.0/libgstx264.so"],["/usr/lib64/gstreamer-1.0/libgstmatroska.so","/usr/lib/gstreamer-1.0/libgstmatroska.so"]],
                             "webm81" : [".webm", "Webm VP8 encoder (Quality L1)", "vp8enc min_quantizer=13 max_quantizer=20 cpu-used=5 deadline=1000000 sharpness=2 target-bitrate=10000 threads=%T ! queue ! webmmux",["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"],["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"]],
                             "webm82" : [".webm", "Webm VP8 encoder (Quality L2)", "vp8enc min_quantizer=4 max_quantizer=13 cpu-used=2 deadline=500000 sharpness=0 target-bitrate=15000 threads=%T ! queue ! webmmux",["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"],["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"]],
                             "webm83" : [".webm", "Webm VP8 encoder (Quality L3)", "vp8enc min_quantizer=0 max_quantizer=7 cpu-used=1 deadline=500000 sharpness=0 target-bitrate=25000 threads=%T ! queue ! webmmux",["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"],["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"]],
                             "webm84" : [".webm", "Webm VP8 encoder (Quality L4)", "vp8enc min_quantizer=0 max_quantizer=0 cpu-used=0 deadline=100000 sharpness=0 target-bitrate=40000 threads=%T ! queue ! webmmux",["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"],["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"]],
                             "ogg1"   : [".ogg", "Ogg Theora Encoder (Quality L1)", "theoraenc speed-level=3 vp3-compatible=true quality=10 bitrate=10000  ! oggmux name=mux" ,["/usr/lib64/gstreamer-1.0/libgsttheora.so", "/usr/lib/gstreamer-1.0/libgsttheora.so"],["/usr/lib64/gstreamer-1.0/libgstogg.so", "/usr/lib/gstreamer-1.0/libgstogg.so"]] ,
                             "ogg2"   : [".ogg", "Ogg Theora Encoder (Quality L2)", "theoraenc speed-level=1 vp3-compatible=false quality=30 bitrate=25000  ! oggmux name=mux",["/usr/lib64/gstreamer-1.0/libgsttheora.so", "/usr/lib/gstreamer-1.0/libgsttheora.so"],["/usr/lib64/gstreamer-1.0/libgstogg.so", "/usr/lib/gstreamer-1.0/libgstogg.so"]] ,
                             "ogg3"   : [".ogg", "Ogg Theora Encoder (Quality L3)", "theoraenc speed-level=0 vp3-compatible=false quality=50 bitrate=50000  ! oggmux name=mux",["/usr/lib64/gstreamer-1.0/libgsttheora.so", "/usr/lib/gstreamer-1.0/libgsttheora.so"],["/usr/lib64/gstreamer-1.0/libgstogg.so", "/usr/lib/gstreamer-1.0/libgstogg.so"]] ,
                             "ogg4"   : [".ogg", "Ogg Theora Encoder (Quality L4)", "theoraenc speed-level=0 vp3-compatible=false quality=60 bitrate=100000  ! oggmux name=mux",["/usr/lib64/gstreamer-1.0/libgsttheora.so", "/usr/lib/gstreamer-1.0/libgsttheora.so"],["/usr/lib64/gstreamer-1.0/libgstogg.so", "/usr/lib/gstreamer-1.0/libgstogg.so"]] ,
                             "webm91" : [".webm", "Webm VP9 encoder (Quality L1)", "vp9enc min_quantizer=13 max_quantizer=20 cpu-used=5 deadline=1000000 sharpness=2 target-bitrate=10000 threads=%T ! queue ! webmmux",["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"],["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"]],
                             "webm92" : [".webm", "Webm VP9 encoder (Quality L2)", "vp9enc min_quantizer=4 max_quantizer=13 cpu-used=2 deadline=500000 sharpness=0 target-bitrate=15000 threads=%T ! queue ! webmmux",["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"],["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"]],
                             "webm93" : [".webm", "Webm VP9 encoder (Quality L3)", "vp9enc min_quantizer=0 max_quantizer=7 cpu-used=1 deadline=500000 sharpness=0 target-bitrate=25000 threads=%T ! queue ! webmmux",["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"],["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"]],
                             "webm94" : [".webm", "Webm VP9 encoder (Quality L4)", "vp9enc min_quantizer=0 max_quantizer=0 cpu-used=0 deadline=100000 sharpness=0 target-bitrate=40000 threads=%T ! queue ! webmmux",["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"],["/usr/lib64/gstreamer-1.0/libgstvpx.so","/usr/lib/gstreamer-1.0/libgstvpx.so"]]
                             }
                             

#xdg-open Fail
def get_exec(file_location):
    query = subprocess.Popen("xdg-mime query filetype {}".format(file_location).split(),stdout=subprocess.PIPE,encoding="utf-8").communicate()[0].strip()
    desktopentry = subprocess.Popen("xdg-mime  query default {}".format(query).split(),stdout=subprocess.PIPE,encoding="utf-8").communicate()[0].strip()
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
    
                             
def isgnomeversion():
    try:
        object_   = bus.get_object("org.gnome.Shell","/org/gnome/Shell")
        interface = dbus.Interface(object_,"org.freedesktop.DBus.Properties")
        version = interface.Get("org.gnome.Shell","ShellVersion")
    except:
        return False
    return version

def getaudiosource():
    all_    = subprocess.Popen("""pactl list | grep -A2 'Source #' | grep 'Name: ' | cut -d" " -f2""",stdout=subprocess.PIPE,encoding="utf-8",shell=True).communicate()[0].strip().split("\n")
    monitor =  subprocess.Popen("""pactl list | grep -A2 'Source #' | grep 'Name: .*\.monitor$' | cut -d" " -f2""",stdout=subprocess.PIPE,encoding="utf-8",shell=True).communicate()[0].strip().split("\n")
    return [all_,monitor]


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

class ScreenCastRecord(threading.Thread):
    def __init__(self,filename,options):
        threading.Thread.__init__(self)
        self.filename = filename
        self.options  = options
        
    def run(self):
        time.sleep(self.options[3]+1)
        if self.options[4]:
            self.options[5].iconify()
        object_ = bus.get_object("org.gnome.Shell.Screencast", "/org/gnome/Shell/Screencast")
        start = object_.get_dbus_method("Screencast",dbus_interface="org.gnome.Shell.Screencast")
        GLib.idle_add(self.options[6].set_sensitive,False)
        GLib.idle_add(self.options[7].set_sensitive,True)
        return start(self.filename[7:],{"framerate":self.options[0] ,"draw-cursor":self.options[1] ,"pipe":self.options[2]})
        
        
        
class ScreenCastAreaRecord(threading.Thread):
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
        object_ = bus.get_object("org.gnome.Shell.Screencast", "/org/gnome/Shell/Screencast")
        GLib.idle_add(self.options[6].set_sensitive,False)
        GLib.idle_add(self.options[7].set_sensitive,True)
        GLib.idle_add(self.options[9].set_sensitive,False)
        if self.options[8]:
            subprocess.call(self.options[8],shell=True)
        return object_.get_dbus_method("ScreencastArea",dbus_interface="org.gnome.Shell.Screencast")(self.x,self.y,self.width,self.height,self.filename[7:],{"framerate":self.options[0] ,"draw-cursor":self.options[1] ,"pipe":self.options[2]})
        
        
class StopRecord(threading.Thread):
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
            

class Yes_Or_No(Gtk.MessageDialog):
    def __init__(self,msg,parent):
        Gtk.MessageDialog.__init__(self,parent=parent,flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK_CANCEL,message_format=msg)
        
    def check(self):
        rrun = self.run()
        if rrun == Gtk.ResponseType.OK:
            self.destroy()
            return True
        else:
            self.destroy()
            return False


class NInfo(Gtk.MessageDialog):
    def __init__(self,message,parent=None):
        Gtk.MessageDialog.__init__(self,parent,1,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,message)
        self.parent=parent
        if self.parent != None:
            self.set_transient_for(self.parent)
            self.set_modal(True)
            self.parent.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)
        self.run() 
        if self.parent != None:
            self.parent.set_sensitive(True)
        self.destroy()



class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(700, 500)
        self.set_resizable(False)
        self.pipeline    = ""
        self.file_suffix = ""
        self.file_name   = "Record"+str(int(time.time()))
        self.folder = "file://"+GLib.get_user_special_dir(GLib.USER_DIRECTORY_VIDEOS)
        self.finaly_location = ""
        self.get_finaly_location()
        self.showmouse = True
        self.recordaudio = True
        self.openlocation = True
        self.frame_value = 30
        self.delay_value = 3
        self.real_delay  = 3
        self.minimize    = True
        self.paly_video  = False
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        
        self.display         = Gdk.Display().get_default()
        self.screen_number   = self.display.get_n_screens()
        self.screens         = [self.display.get_screen(screennumber) for screennumber in range(self.screen_number) ]
        self.monitor_number  = self.display.get_n_monitors()
        self.monitors        = [self.display.get_monitor(monitornumber) for monitornumber in range(self.monitor_number) ]
        self.screens_dict    = dict()
        self.monitors_dict   = dict()
        count =1
        for screen in self.screens:
            self.screens_dict.setdefault("screen{}".format(count),["Full Screen{}".format(count), screen.get_width(), screen.get_height(),0,0 ])
            count+=1
        count = 1
        for monitor in self.monitors:
            self.monitors_dict.setdefault("monitors{}".format(count),["Full Monitor{}".format(count), monitor.get_geometry().width, monitor.get_geometry().height,monitor.get_geometry().x,monitor.get_geometry().y ])
            count+=1

        self.screens_monitors_dict = self.screens_dict.copy()
        self.screens_monitors_dict.update(self.monitors_dict)
        self.screens_monitors_dict.update({"area":["Select Area"]})

        
        #vb
        vb = Gtk.VBox(spacing=10)
        #hb
        hb = Gtk.HBox(spacing=10)
        #vmainbox
        self.vmainbox = Gtk.VBox(spacing=15)
        hbox1 = Gtk.HBox(spacing=10)
        monitorscreenhbox = Gtk.HBox(spacing=10)
        widthheighthbox   = Gtk.HBox(spacing=10)
        xyhbox = Gtk.HBox(spacing=10)
        hbox2 = Gtk.HBox(spacing=10)
        hbox3 = Gtk.HBox(spacing=20)
        hbox4 = Gtk.HBox(spacing=20)
        hbox5 = Gtk.HBox(spacing=20)

        
        pipe_combo = Gtk.ComboBoxText()
        for id_,l in gnome_wayland_pipeline.items():
            if self.check_gst_plugins_exists(l[3]) and self.check_gst_plugins_exists(l[4]):
                pipe_combo.append(id_,l[1])
        pipe_combo.set_active(0)
        pipe_combo.connect("changed", self.on_pipe_combo_changed)
        pipe_combo.emit("changed")

        
        widthhbox  = Gtk.HBox(spacing=2)
        widthlabel = Gtk.Label("Width")
        widthadjustment = Gtk.Adjustment(value=self.screens[0].get_width(),lower=0,upper=self.screens[0].get_width()+1,page_size= 1,step_increment =1,page_increment=0)
        self.width_ = Gtk.SpinButton(adjustment=widthadjustment)
        self.widthhandler=self.width_.connect("changed", self.on_width___changed)
        widthhbox.pack_start(widthlabel,True,True,0)
        widthhbox.pack_start(self.width_,True,True,0)

        heighthbox  = Gtk.HBox(spacing=2)
        heightlabel  = Gtk.Label("Height")
        heightadjustment = Gtk.Adjustment(value=self.screens[0].get_height(),lower=0,upper=self.screens[0].get_height()+1,page_size= 1,step_increment =1,page_increment=0)
        self.height_ = Gtk.SpinButton(adjustment=heightadjustment)
        self.heighthandler=self.height_.connect("changed", self.on_height___changed)
        heighthbox.pack_start(heightlabel,True,True,0)
        heighthbox.pack_start(self.height_,True,True,0)
        
        xhbox  = Gtk.HBox(spacing=2)
        xlabel = Gtk.Label("X")
        xadjustment = Gtk.Adjustment(value=0,lower=0,upper=self.screens[0].get_width(),page_size= 1,step_increment =1,page_increment=0)
        self.x_ = Gtk.SpinButton(adjustment=xadjustment)
        self.xhandler=self.x_.connect("changed", self.on_x___changed)
        xhbox.pack_start(xlabel,True,True,0)
        xhbox.pack_start(self.x_,True,True,0)
        
        yhbox  = Gtk.HBox(spacing=2)
        ylabel = Gtk.Label("Y")
        yadjustment = Gtk.Adjustment(value=0,lower=0,upper=self.screens[0].get_height(),page_size= 1,step_increment =1,page_increment=0)
        self.y_ = Gtk.SpinButton(adjustment=yadjustment)
        self.yhandler=self.y_.connect("changed", self.on_y___changed)
        yhbox.pack_start(ylabel,True,True,0)
        yhbox.pack_start(self.y_,True,True,0)
        
        
        self.sm_combo = Gtk.ComboBoxText()
        for k,v in self.screens_monitors_dict.items():
            self.sm_combo.append(k,v[0])
        self.sm_combo.set_active(0)
        self.sm_combo.connect("changed", self.on_sm_combo_changed)
        self.sm_combo.emit("changed")
        
        self.filenameentry = Gtk.Entry()
        self.filenameentry.set_placeholder_text("Enter File Name...")
        self.filenameentry.set_max_length(20)
        self.filenameentry.connect("notify::text",self.on_filenameentry_active)

        
        self.choicefolder = Gtk.FileChooserButton(action="select-folder")
        self.choicefolder.set_uri(self.folder)
        self.choicefolder.connect("file-set",self.on_choicefolder_file_set)
        self.choicefolder.emit("file-set")
   
        
        vboxframe = Gtk.VBox(spacing = 2)
        vbox_mouse_audio = Gtk.VBox(spacing = 2)
        hboxmousecheckbutton = Gtk.HBox()
        hboxaudiocheckbutton = Gtk.HBox()
        hboxminimizecheckbutton = Gtk.HBox()
        hboxopencheckbutton = Gtk.HBox()
        hboxplaycheckbutton = Gtk.HBox()
        hboxframe = Gtk.HBox()
        hboxdelay = Gtk.HBox()
        vbox_frame_delay = Gtk.VBox(spacing = 10)

        frame_label = Gtk.Label("Framerate")
        adjustment = Gtk.Adjustment(value=self.frame_value,lower=10,upper=61,page_size=1,step_increment=1, page_increment=0)
        self.frame = Gtk.SpinButton(max_width_chars=2,value=self.frame_value,adjustment=adjustment)
        hboxframe.pack_start(frame_label,True,False,0)
        hboxframe.pack_start(self.frame,False,False,0)

        delay_label = Gtk.Label("Delay")
        adjustment1 = Gtk.Adjustment(value=self.delay_value,lower= 0,upper= 11,page_size= 1,step_increment =1, page_increment=0)
        self.delay = Gtk.SpinButton(max_width_chars=2,value=self.delay_value,adjustment=adjustment1)
        self.delay.connect("value-changed",self.on_delay_value_changed)
        self.delay.emit("value-changed")
        hboxdelay.pack_start(delay_label,True,False,0)
        hboxdelay.pack_start(self.delay,False,False,0)

        mouse_label = Gtk.Label("Show Mouse")
        self.mousecheckbutton = Gtk.CheckButton()
        self.mousecheckbutton.set_active(self.showmouse)
        hboxmousecheckbutton.pack_start(mouse_label,True,False,0)
        hboxmousecheckbutton.pack_start(self.mousecheckbutton,False,False,0)
       

        audio_label = Gtk.Label("Record Audio")
        self.audiocheckbutton = Gtk.CheckButton()
        self.audiocheckbutton.set_active(self.recordaudio)
        hboxaudiocheckbutton.pack_start(audio_label,True,False,0)
        hboxaudiocheckbutton.pack_start(self.audiocheckbutton,False,False,0)


        minimize_label = Gtk.Label("Minimize Before Record")
        self.minimizecheckbutton = Gtk.CheckButton()
        self.minimizecheckbutton.set_active(self.minimize)
        hboxminimizecheckbutton.pack_start(minimize_label,True,False,0)
        hboxminimizecheckbutton.pack_start(self.minimizecheckbutton,False,False,0)


        open_label = Gtk.Label("Open Location After Stop")
        self.opencheckbutton = Gtk.CheckButton()
        self.opencheckbutton.set_active(self.openlocation)
        hboxopencheckbutton.pack_start(open_label,True,False,0)
        hboxopencheckbutton.pack_start(self.opencheckbutton,False,False,0)

        play_label = Gtk.Label("Play Video After Stop")
        self.playcheckbutton = Gtk.CheckButton()
        self.playcheckbutton.set_active(self.paly_video)
        hboxplaycheckbutton.pack_start(play_label,True,False,0)
        hboxplaycheckbutton.pack_start(self.playcheckbutton,False,False,0)

        before_hbox = Gtk.HBox(spacing=2)
        before_label = Gtk.Label("Run Before")
        self.before_entry = Gtk.Entry()
        self.before_entry.set_placeholder_text("Enter Command...")
        before_hbox.pack_start(before_label,True,True,0)
        before_hbox.pack_start(self.before_entry,True,True,0)
        
        after_hbox = Gtk.HBox(spacing=2)
        after_label = Gtk.Label("Run After")
        self.after_entry = Gtk.Entry()
        self.after_entry.set_placeholder_text("Enter Command...")
        after_hbox.pack_start(after_label,True,True,0)
        after_hbox.pack_start(self.after_entry,True,True,0)


        self.playbutton = Gtk.Button("Play")
        self.playbutton.connect("clicked",self.play_)
        
        self.record_button = Gtk.Button("Record")
        self.record_button.connect("clicked",self.startcastrecord)
        self.stop_record_button = Gtk.Button("Stop")
        self.stop_record_button.connect("clicked",self.stopcastrecord)
        self.stop_record_button.set_sensitive(False)

        vbox_frame_delay.pack_start(hboxframe,True,True,0)
        vbox_frame_delay.pack_start(hboxdelay,True,True,0)
        
        vbox_mouse_audio.pack_start(hboxmousecheckbutton,True,True,0)
        vbox_mouse_audio.pack_start(hboxaudiocheckbutton,True,True,0)
        vbox_mouse_audio.pack_start(hboxminimizecheckbutton,True,True,0)
        vbox_mouse_audio.pack_start(hboxopencheckbutton,True,True,0)
        vbox_mouse_audio.pack_start(hboxplaycheckbutton,True,True,0)
        
        hbox1.pack_start(pipe_combo,True,True,0)
        monitorscreenhbox.pack_start(self.sm_combo,True,True,0)
        widthheighthbox.pack_start(widthhbox,True,True,0)
        widthheighthbox.pack_start(heighthbox,True,True,0)
        xyhbox.pack_start(xhbox,True,True,0)
        xyhbox.pack_start(yhbox,True,True,0)
        hbox2.pack_start(self.filenameentry,True,True,0)
        hbox2.pack_start(self.choicefolder,True,True,0)
        hbox3.pack_start(vbox_frame_delay,True,True,0)
        hbox3.pack_start(vbox_mouse_audio,True,True,0)
        hbox4.pack_start(before_hbox,True,True,0)
        hbox4.pack_start(after_hbox,True,True,0)
        
        self.delay_label = Gtk.Label("")
        self.delay_label.modify_fg(Gtk.StateType.NORMAL,Gdk.color_parse("red"))
        
        buttobvbox = Gtk.VBox(spacing=2)
        hbox5.pack_start(self.record_button,True,True,0)
        hbox5.pack_start(self.stop_record_button,True,True,0)
        buttobvbox.pack_start(self.delay_label,False,False,0)
        buttobvbox.pack_start(self.playbutton,False,False,0)
        buttobvbox.pack_start(hbox5,False,False,0)
        

        
        self.vmainbox.pack_start(hbox1,False,False,0)
        self.vmainbox.pack_start(monitorscreenhbox,False,False,0)
        self.vmainbox.pack_start(widthheighthbox,False,False,0)
        self.vmainbox.pack_start(xyhbox,False,False,0)
        self.vmainbox.pack_start(hbox2,False,False,0)
        self.vmainbox.pack_start(hbox3,False,False,0)
        self.vmainbox.pack_start(hbox4,False,False,0)
        self.vmainbox.pack_start(buttobvbox,False,False,0)
        hb.pack_start(self.vmainbox,True,True,0)
        vb.pack_start(hb,True,True,0)
        self.add(vb)
        self.show_all()


        
    def delay_(self):
        if self.real_delay<0:
            self.delay_label.set_text("")
            self.real_delay = self.delay.get_value_as_int()
            return False
        
        self.delay_label.set_text(str(self.real_delay))
        time.sleep(1)
        self.real_delay-=1
        return True

    def on_delay_value_changed(self,widget):
        self.real_delay = self.delay.get_value_as_int()

    def play_(self,button):
        t=PlayVideo(self.finaly_location[7:])
        t.start()

    def startcastrecord(self,button):
        if not self.filenameentry.get_text().strip():
            self.file_name   = "Record"+str(int(time.time()))
            self.get_finaly_location()
            
        if os.path.exists(self.finaly_location[7:]):
            if not os.path.isfile(self.finaly_location[7:]):
                msg = "Cant Replace  \"{}\"!\nAn older unknown location type with same name already exists".format(os.path.basename(self.finaly_location))
                NInfo(msg,self)
                return
            msg = "Replace file \"{}\"?\nAn older file with same name already exists".format(os.path.basename(self.finaly_location))
            yn = Yes_Or_No(msg,self)
            if not yn.check():
                return

        command = self.before_entry.get_text().replace("(((L)))",os.path.dirname(self.finaly_location)[7:]).replace("(((F)))",self.finaly_location[7:]).replace("(((BF)))",os.path.basename(self.finaly_location)).replace("(((S)))",os.path.basename(self.finaly_location).split(".")[-1]).strip()
        original_delay = self.delay.get_value_as_int()
        t1 = ScreenCastAreaRecord(self.x_.get_text(),self.y_.get_text(),self.width_.get_text(),self.height_.get_text(),self.finaly_location,[self.frame.get_value_as_int(),self.mousecheckbutton.get_active(),self.pipe,original_delay,self.minimizecheckbutton.get_active(),self,button,self.stop_record_button,command,self.playbutton])
        GLib.idle_add(self.delay_)
        t1.start()

    def stopcastrecord(self,button):
        command = self.after_entry.get_text().replace("(((L)))",os.path.dirname(self.finaly_location)[7:]).replace("(((F)))",self.finaly_location[7:]).replace("(((BF)))",os.path.basename(self.finaly_location)).replace("(((S)))",os.path.basename(self.finaly_location).split(".")[-1]).strip()
        t1 = StopRecord(self.record_button,self.stop_record_button,command,self.opencheckbutton.get_active(),self.finaly_location[7:],self.playbutton,self.playcheckbutton.get_active())
        t1.start()
        

        
    def get_finaly_location(self):
        self.finaly_location = os.path.join(self.folder,self.file_name+self.file_suffix)

    def on_filenameentry_active(self,widget,t):
        text = widget.get_text()
        if  text:
            self.file_name = text
        else:
            self.file_name = "Record"+str(int(time.time()))
        self.get_finaly_location()
        

        
        
    def on_choicefolder_file_set(self,widget):
        location = widget.get_uri()
        if location !=None:
            self.folder  = location
        self.get_finaly_location()



    def on_pipe_combo_changed(self,combo):
        iter_ = combo.get_active_iter()
        if iter_ != None:
            self.pipe = gnome_wayland_pipeline[combo.get_model()[iter_][1]][2]
            self.file_suffix = gnome_wayland_pipeline[combo.get_model()[iter_][1]][0]
        self.get_finaly_location()
    
    def on_sm_combo_changed(self,combo):
        self.width_.set_sensitive(False)
        self.height_.set_sensitive(False)
        self.x_.set_sensitive(False)
        self.y_.set_sensitive(False)
        iter_ = combo.get_active_iter()
        if iter_ != None:
            key = combo.get_model()[iter_][1]
            if key == "area":
                self.selectarea()
            
            elif key.startswith("screen"):
                self.width_.set_sensitive(True)
                self.height_.set_sensitive(True)
                self.x_.set_sensitive(True)
                self.y_.set_sensitive(True)
                self.width_.handler_block(self.widthhandler)
                self.height_.handler_block(self.heighthandler)
                self.x_.handler_block(self.xhandler)
                self.y_.handler_block(self.yhandler)
                
                ad = self.width_.get_adjustment()
                ad.set_lower(0)
                ad.set_upper(self.screens_monitors_dict[key][1]+1)
                self.width_.set_text(str(self.screens_monitors_dict[key][1]))
                
                
                ad = self.height_.get_adjustment()
                ad.set_lower(0)
                ad.set_upper(self.screens_monitors_dict[key][2]+1)
                self.height_.set_text(str(self.screens_monitors_dict[key][2]))
                
                
                ad = self.x_.get_adjustment()
                ad.set_lower(0)
                ad.set_upper(self.screens_monitors_dict[key][1])
                self.x_.set_text(str(self.screens_monitors_dict[key][3]))
                
                
                ad = self.y_.get_adjustment()
                ad.set_lower(0)
                ad.set_upper(self.screens_monitors_dict[key][2])
                self.y_.set_text(str(self.screens_monitors_dict[key][4]))

                self.width_.handler_unblock(self.widthhandler)
                self.height_.handler_unblock(self.heighthandler)
                self.x_.handler_unblock(self.xhandler)
                self.y_.handler_unblock(self.yhandler)
            else:
                self.width_.handler_block(self.widthhandler)
                self.height_.handler_block(self.heighthandler)
                self.x_.handler_block(self.xhandler)
                self.y_.handler_block(self.yhandler)
                
                ad = self.width_.get_adjustment()
                ad.set_lower(0)
                ad.set_upper(self.screens_monitors_dict[key][1]+1)
                self.width_.set_text(str(self.screens_monitors_dict[key][1]))
                
                
                ad = self.height_.get_adjustment()
                ad.set_lower(0)
                ad.set_upper(self.screens_monitors_dict[key][2]+1)
                self.height_.set_text(str(self.screens_monitors_dict[key][2]))
                
                
                ad = self.x_.get_adjustment()
                ad.set_lower(0)
                ad.set_upper(self.screens_monitors_dict[key][1])
                self.x_.set_text(str(self.screens_monitors_dict[key][3]))
                
                
                ad = self.y_.get_adjustment()
                ad.set_lower(0)
                ad.set_upper(self.screens_monitors_dict[key][2])
                self.y_.set_text(str(self.screens_monitors_dict[key][4]))

                self.width_.handler_unblock(self.widthhandler)
                self.height_.handler_unblock(self.heighthandler)
                self.x_.handler_unblock(self.xhandler)
                self.y_.handler_unblock(self.yhandler)
                


    def on_width___changed(self,e):
        text = e.get_text()
        iter_ = self.sm_combo.get_active_iter()
        key = self.sm_combo.get_model()[iter_][1]
        with self.x_.handler_block(self.xhandler):
            self.x_.set_text(str(int(self.screens_monitors_dict[key][1])-e.get_value_as_int()))

    def on_height___changed(self,e):
        iter_ = self.sm_combo.get_active_iter()
        key = self.sm_combo.get_model()[iter_][1]
        with self.y_.handler_block(self.yhandler):
            self.y_.set_text(str(int(self.screens_monitors_dict[key][2])-e.get_value_as_int()))

            
    def on_x___changed(self,e):
        text = e.get_text()
        iter_ = self.sm_combo.get_active_iter()
        key = self.sm_combo.get_model()[iter_][1]
        if key.startswith("monitor") and  key[8]!="1":
            with self.width_.handler_block(self.widthhandler):
                self.width_.set_text(str(self.screens_monitors_dict[key][1]+self.screens_monitors_dict[key][3]-e.get_value_as_int()))
        else:
            with self.width_.handler_block(self.widthhandler):   
                self.width_.set_text(str(int(self.screens_monitors_dict[key][1])-e.get_value_as_int()))
        
    def on_y___changed(self,e):
        iter_ = self.sm_combo.get_active_iter()
        key = self.sm_combo.get_model()[iter_][1]
        with self.height_.handler_block(self.heighthandler):
            self.height_.set_text(str(int(self.screens_monitors_dict[key][2])-e.get_value_as_int()))
        
    def check_gst_plugins_exists(self,locations):
        for location in  locations:
            if os.path.isfile(location):
                return True
        return False       


    def selectarea(self):
        self.hide()
        
        hb=Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "AreaChooser"
        
        window = Gtk.Window(title="AreaChooser",window_position=Gtk.WindowPosition.CENTER,gravity=Gdk.Gravity.SOUTH)
        window.set_titlebar(hb)
        window.set_name('AreaChooser')
        window.connect("delete-event", self.on_delete_areachooser)
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")
        
        button = Gtk.Button()
        button.connect("clicked",self.on_apply_areachooser,window)
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        
        box.add(button)
        hb.pack_start(box)

        window.show_all()

        

    def on_delete_areachooser(self,window,p):
        window.destroy()
        self.sm_combo.set_active(0)
        self.show()

    def on_apply_areachooser(self,button,window):
        width,height = window.get_size()
        x, y = window.get_position()
        x %= self.screens[0].get_width()
        y %= self.screens[0].get_height() 
        self.sm_combo.set_active(0)
        self.width_.handler_block(self.widthhandler)
        self.height_.handler_block(self.heighthandler)
        self.x_.handler_block(self.xhandler)
        self.y_.handler_block(self.yhandler)
        
        self.width_.set_text(str(width))
        self.height_.set_text(str(height))
        self.x_.set_text(str(x))
        self.y_.set_text(str(y))

        self.width_.handler_unblock(self.widthhandler)
        self.height_.handler_unblock(self.heighthandler)
        self.x_.handler_unblock(self.xhandler)
        self.y_.handler_unblock(self.yhandler)
        window.destroy()
        self.show()

        
        
class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.github.yucefsourani.GVrecord",
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         **kwargs)
        self.icon = "org.github.yucefsourani.gvrecord.png" if os.path.isfile("org.github.yucefsourani.gvrecord.png") else "/usr/share/pixmaps/org.github.yucefsourani.gvrecord.png"
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)
        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        if not self.window:
            if not isgnomeversion():
                NInfo("Gnome Shell Not Found")
                self.quit()
            self.window = AppWindow(application=self, title="GVrecord")

        self.window.present()

    def on_quit(self, action, param):
        self.quit()

    def on_about(self,a,p):
        authors = ["Youssef Sourani <youssef.m.sourani@gmail.com>"]
        about = Gtk.AboutDialog(parent=self.window,transient_for=self.window, modal=True)
        about.set_program_name("Gvrecord")
        about.set_version("0.1")
        about.set_copyright("Copyright © 2017 Youssef Sourani")
        about.set_comments("Simple Tool To Record Gnome Shell Screen")
        about.set_website("https://arfedora.blogspot.com")
        about.set_logo(GdkPixbuf.Pixbuf.new_from_file(self.icon))
        about.set_authors(authors)
        about.set_license_type(Gtk.License.GPL_3_0)
        translators = ("translator-credit")
        if translators != "translator-credits":
            about.set_translator_credits(translators)
        about.run()
        about.destroy()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
