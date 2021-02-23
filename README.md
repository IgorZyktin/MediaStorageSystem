# MediaStorageSystem

System for saving media content with tags.

Initial idea was to build a system in which you could 
throw media materials and, it will save them without duplicates.
So you could add one image many times, and it will be saved only once.

From practical side, idea of this repository can be described this way: 
"I want to gather any images related to the movie Blade runner. 
So I'll put inside every related image and await that there will 
be no duplicates at the end".

### Components of the system

- [Browser](browser/README.md)
    
    Allows you to browse what's inside the archive. 
    Built as a web app and planned to be deployable as a web server in the future.


- [Register](register/README.md)
    
    Allows you to upload new content to the archive. 
    Supposed to check for duplicates before inserting.
  
### Placement of components

All gathered media files are supposed to be packed into a 
single zip file and be shipped this way. No program components 
are supposed to be included into the package. All tools are to be 
placed near content manually.

After unpacking, folder structure must look like this:
```
your_media_folder
├── Description.md
├── Version file
├── root (folder for all the content)
│   ├── metainfo
│   │   ├── ...
│   │   ├── ...
│   ├── previews
│   │   ├── ...
│   │   ├── ...
│   ├── thumbnails
│   │   ├── ...
│   │   ├── ...
│   ├── images
│   │   ├── ...
│   │   ├── ...
│   ├── ...
├── mss_browser_vX.X (or folder with python code)
├── mss_register_vX.X.exe (or folder with python code)
├── other scripts or their compiled binaries
```

### Installation

You can download pre-built windows binary [here](https://github.com/IgorZyktin/MediaStorageSystem/blob/main/mss_browser_v1.1.zip):
