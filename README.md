# MediaStorageSystem

System for saving media content with tags.

Initial idea was to build a system in which you could 
throw media materials in and it will save them without duplicates.

From practical side, idea of this repository can be described this way: 
"I want to gather any images related to the movie Blade runner. 
So I'll put inside every related image and await that there will 
be no duplicates at the end".

### Browser

Allows you to browse what's inside the archive. 
Built as a web application, deployable as a web server, but can also
run locally.
  
### Placement of components

Gathered media files are supposed to be packed into a single zip file 
and shipped this way. No program components (like browser) are supposed 
to be included into the package. All tools are to be placed near content 
manually. After download, contents must be unpacked..

Resulting folder structure must look like this:
```
your_media_folder
├── Description.md
├── <version file>
└── root
    ├── metainfo
    │   ├── ...
    │   └── ...
    ├── previews
    │   ├── ...
    │   └── ...
    ├── thumbnails
    │   ├── ...
    │   └── ...
    └── images
        ├── ...
        └── ...
```

### Installation

#### Browser

- [Version 1.2  <-- new](https://github.com/IgorZyktin/MediaStorageSystem/blob/main/mss_browser_v1.2.zip):
- [Version 1.1](https://github.com/IgorZyktin/MediaStorageSystem/blob/main/mss_browser_v1.1.zip):
- [Version 1.0](https://github.com/IgorZyktin/MediaStorageSystem/blob/main/mss_browser_v1.0.zip):
