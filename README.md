# gvrecord v0.4(For Gnome Shell Only)
Simple Tool To Record  Screen

https://arfedora.blogspot.com

ملاحظة مهمة إذا سجلت فيديو مع صوت وبعد التسجيل مباشرتا شغلت الفيديو ولم تجد الصوت إنتظر قليلا يكون البرنامج مازال يدمج الفيديو والصوت سويا ,على حسب طول الفيديو قد يأخذ بعض الثواني .


بعد عملية الدمج يتم إستبدال الفيديو  الذي لا يحتوي الصوت بالفيديو الذي يحتوي الصوت ربما أغير هذا السلوك في المستقبل عندها سيتاخر ظهور الفيديو حتى إنتهاء عملية الدمج كان بإمكاني عمل شيء مثل 

loading

أو شيء لاكني فضلت تشغيل عملية الدمج ب 

process 

أخرى يعني حتى لو اغلقنا البرنامج بالخطا أثناء التسجيل لن تخسر ما سجلته وسيتم الدمج ب 

process

اخرى وملفات الصوت وعميلة الدمج تتم في مجلد

/tmp/gvrecord

ربما إحتجت إسترجاع شيء من هناك في حال حصل أي مشكلة مع العلم كل شيء في مجلد 

tmp

سيتخلص منه النظام لاحقا. 

لمزيد من المعلومات

https://arfedora.blogspot.com/2018/04/gvrecord.html


Important note: if you recorded a video with sound, and you played the video immediately but you didn't hear anything, just give it few moments the program is still embedding Audio Track into video.
After embedding the audio the old video get replaced by the new one containing both Audio and Video Tracks, i might change this behavior in the future, but the end result will need sometime before you can see it or play it.
i could have done something like loading...
but i preferred the embedding operation done by process, meaning even if you close the program by mistake you'll not lose your recordings and the embedding will be carried on by the process.

the sound track and the embedding operation files can be found in /tmp/gvrecord
you can recover your files from that directory in case something happened, but keep in mind that everything is in tmp directory will be erased by the system later.



# To DO

support kde xfce ...

support Gif.




# Screenshot

![Alt text](https://raw.githubusercontent.com/yucefsourani/gvrecord/master/0.jpg "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/gvrecord/master/2.jpg "Screenshot")



* Requires

  * ``` python3 ```
  
  * ``` python3-dbus ```
  
  * ``` pygobject3 ```
 
  * ``` python3-gobject ```
  
  * ``` gstreamer1-plugins-good ```
    
  * ``` gstreamer1-plugins-base ```

  * ``` sox #For Remove Noise ```

  * ``` libsox-fmt-mp3 #For ubuntu ```

  * ``` ffmpeg #For Audio Record ```

  * ``` alsa-utils ```


* To Use
 
  * ``` cd && git clone https://github.com/yucefsourani/gvrecord ```

  * ``` chmod 755 ~/gvrecord/gvrecord.py ```
  
  * ``` ~/gvrecord/gvrecord.py ```



* Install For Fedora

  * ``` sudo  dnf copr enable youssefmsourani/gvrecord  -y ```
  
  * ``` sudo  dnf install gvrecord  -y ```
