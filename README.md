# MFND : MangaFreakNet Downloader

MFDN is a download assistant for the "mangafreak.net" website developed in python to allow automated and mass download of manga.

it allows the download but also the extraction of zip files, the organization of the files, the cutting of the double page in unique page and the regrouping of the page in only one pdf.

**ATTENTION: This program is a personal project made in a few minutes ! For all the amateurs of clean and optimized code pass your way. this program is not made to be a serious and well finished project.**

*Of course I remind you that downloading works that you don't own is obviously illegal in many countries ! and that I can't be held responsible for the use that you make of this program.*


## File architecture

> -downloads
>
> ​	-MangaName
>
> ​		-images
>
> ​		-pages
>
> ​		-zip
>
> ​		-MangaName.pdf
>
> [...]

*Be careful, the tree of folders presented is generated during the use (no need to create the folders yourself)*

At the root we find in addition to the program itself a folder downloads. This one contains folders, each one with the name of the manga in question. Each of these folders is composed of 3 folders and a PDF file (the file generated by the program containing all the downloaded chapters). These folders are: images which contains the image files (double page) grouped by chapters, the pages folder which contains the same thing but whose pages have been separated into single page and the zip folder which contains the files downloaded from the site in zip format.



## How to use it

launch the file downloader.py (python 3) in the console

```bash
py ./downloader.py
```



choose your manga : if you have already downloaded some chapters you could select it from the loading screen otherwise you could add it by entering its name (end of the download url)

![image-20220806170731481](./img/readme_screenshot.png)

then let yourself be guided by the instructions (normally the steps are to be done in the order of appearance in the menu)