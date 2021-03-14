# MediaStorageSystem

System for saving media content with tags.

Initial idea was to build a system in which you could 
throw media materials in and it will save them without duplicates.

From practical side, idea of this repository can be described this way: 
"I want to gather any images related to the movie Blade runner. 
So I'll put inside every related image and await that there will 
be no duplicates at the end". 

**Currently adding is not yet implemented, so archive is read only.**

**Currently system works only with images.**

### Browser

Allows you to browse what is inside the archive. 
Built as a web application, deployable as a web server, but can also
run locally. Regular python flask based application.
  
### Placement of components

Gathered media files are supposed to be packed into a single zip file 
and shipped this way. No program components (like browser) are supposed 
to be included into the package. All tools are to be placed near content 
manually. After download, contents must be unpacked.

Resulting folder structure must look like this:
```
my_archive
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

### Search engine

You can use logical keywords to perform search, such as: AND, OR and NOT.
Exactly uppercase. Search is not working for spelling mistakes.
Your request must match tag exactly. Anything, except keywords, 
is converted to lowercase during processing.

Meanings are:

* AND - record is included only if text is present in at least one tag.
* OR - record is included if text is present, but other keywords might change it.
* NOT - record is excluded if text is found in any tag.

Query will be split into series of pairs keyword+text.
If your request does not start from keyword, system will automatically
add AND at the start. So "cats AND dogs NOT frogs" will be turned
into "AND cats AND dogs NOT frogs". As a result, human readable form
of this request is: "show me all records, that specifically have
tag 'dogs' and optionally have tag 'cats', but definitely do not have tag 'frogs'".

Do not think of the query as of logical rule. Each keyword is treated
separately. You cannot use queries like "cats AND NOT dogs".

### Special keywords

For images:

* TINY - only tiny images.
* SMALL - only small images.
* MEAN - only regular size images.
* BIG - only big images.
* HUGE - only huge images.

For video/audion or animated images:

* MOMENT - only super short duration.
* SHORT - only short duration.
* MEDIUM - only medium length duration.
* LONG - only long duration.

For specific media type:

* IMAGE - only static images.
* GIF - only animated images.
* VIDEO - only video files.
* AUDIO - only audio files.

Other:
      
* DESC - show found records in reverse order.

For example: dragons AND SHORT AND DESC.
Logical keywords do not matter here, AND will be always used.

### Synonyms

Since you have to match tags literally, soon it becomes tedious to write 
search requests. Synonyms are here to help you! In file called 'synonyms.json' 
you can write down replacements you'd like to use. Everything in given list of 
words will be treated equally. JSON key is comment and value is an array of tags.

Example of synonyms.json:
```json
{
	"If user wants to find cats": ["cat", "kitty", "kitten"],
	"If user wants to find dogs": ["dog", "puppy", "doggie"] 
}
```

### Tags on demand (not yet implemented)

Sometimes you don't want something to be shown during regular search. 
Like things not really appropriate, or something you specifically do not like. 
You can describe such things in a file called "tags_on_demand.json".

Tags in this list will be shown only if they were specifically included in 
search request. Synonyms are not applied to this tags. Syntax is similar to synonyms.

Example of tags_on_demand.json:
```json
{
	"Some users do not like spiders": ["spider", "arachnids", "arachnid"]
}
```

### Code injection

You can add text file called "injection.html" to the browser folder. 
Everything from this file will be added at the bottom of every rendered page, 
without escaping, before the end of the "body" tag. This feature is added so 
you could include external metrics/features, that require adding some 
HTML/JS code to your page.


